import os
import sys
from flask import Flask, send_from_directory, request, jsonify
import logging
import json
from typing import Dict, Any


# Importações do sankhya_op_automation (usando mocks para teste)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'sankhya_automation'))
try:
    from database import OracleDatabase
    from sankhya_api import SankhyaAPI
except ImportError:
    # Usar mocks se as dependências não estiverem disponíveis
    from database_mock import OracleDatabase
    from sankhya_api_mock import SankhyaAPI

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'


# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('unified_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SankhyaAutomationAPI:
    """
    Classe para integrar a funcionalidade do sankhya_op_automation via API
    """
    
    def __init__(self):
        self.db: Optional[OracleDatabase] = None
        self.api: Optional[SankhyaAPI] = None
        self.total_ops_criadas = 0
        self.total_falhas = 0
        self.ops_criadas_sucesso = []
        self.detalhes_falhas = []

    def verificar_conexoes(self) -> Dict[str, Any]:
        """Verifica conexões com banco e API"""
        try:
            # Só cria novas instâncias se não existirem
            if not self.db:
                self.db = OracleDatabase()
            if not self.api:
                self.api = SankhyaAPI()
            
            if not self.db.connect() or not self.db.testar_conexao():
                return {"sucesso": False, "erro": "Falha na conexão com o banco Oracle"}
            
            # O teste de conexão da API agora autentica e faz logout,
            # garantindo que não deixa sessões abertas.
            if not self.api.testar_conexao():
                self.db.disconnect()
                return {"sucesso": False, "erro": "Falha na conexão com a API Sankhya"}
            
            return {"sucesso": True, "mensagem": "Conexões estabelecidas com sucesso"}
        except Exception as e:
            logger.error(f"Erro ao verificar conexões: {e}")
            return {"sucesso": False, "erro": str(e)}

    def buscar_planejamentos(self, data_planejamento: str, braco: int, rodada_inicial: int, rodada_final: int) -> Dict[str, Any]:
        """Busca planejamentos pendentes"""
        try:
            if not self.db:
                return {"sucesso": False, "erro": "Conexão com banco não estabelecida"}
            
            total = self.db.contar_planejamentos_pendentes(data_planejamento, braco, rodada_inicial, rodada_final)
            return {"sucesso": True, "total": total}
        except Exception as e:
            logger.error(f"Erro ao buscar planejamentos: {e}")
            return {"sucesso": False, "erro": str(e)}

    def processar_rodada(self, data_planejamento: str, braco: int, rodada: int) -> Dict[str, Any]:
        """Processa uma rodada específica"""
        try:
            if not self.db or not self.api:
                return {"sucesso": False, "erro": "Conexões não estabelecidas"}
            
            # Re-autenticar para cada rodada
            if not self.api.autenticar():
                return {"sucesso": False, "erro": f"Falha ao autenticar para a rodada {rodada}"}
            
            registros = self.db.buscar_planejamentos(data_planejamento, braco, rodada, rodada)
            
            if not registros:
                return {"sucesso": True, "mensagem": f"Nenhum planejamento pendente para a rodada {rodada}", "processados": 0}

            idiprocs_desta_rodada = []
            processados = 0
            
            for registro in registros:
                try:
                    dados_produto_api = {
                        "CODPRODPA": registro['CODPROD'], 
                        "IDPROC": 51, 
                        "CODPLP": 1, 
                        "TAMLOTE": registro['QTDPLAN']
                    }
                    
                    sucesso, idiproc, mensagem = self.api.criar_ordem_producao(dados_produto_api)

                    if sucesso and idiproc:
                        if self.db.atualizar_idiproc(registro['NUPLAN'], idiproc):
                            self.total_ops_criadas += 1
                            self.ops_criadas_sucesso.append({"nuplan": registro['NUPLAN'], "idiproc": idiproc})
                            idiprocs_desta_rodada.append(idiproc)
                            processados += 1
                        else:
                            erro_msg = f"OP {idiproc} criada, mas falha ao atualizar banco"
                            self.detalhes_falhas.append({"nuplan": registro['NUPLAN'], "erro": erro_msg})
                            self.total_falhas += 1
                    else:
                        erro_msg = f"Erro ao criar OP: {mensagem}"
                        self.detalhes_falhas.append({"nuplan": registro['NUPLAN'], "erro": erro_msg})
                        self.total_falhas += 1
                        
                except Exception as e:
                    erro_msg = f"Erro inesperado ao processar NUPLAN {registro['NUPLAN']}: {e}"
                    logger.error(erro_msg, exc_info=True)
                    self.detalhes_falhas.append({"nuplan": registro['NUPLAN'], "erro": erro_msg})
                    self.total_falhas += 1
                
                import time
                time.sleep(0.5)

            # Gerar lote para OPs criadas
            if idiprocs_desta_rodada:
                if self.db.gerar_lote_para_ops(idiprocs_desta_rodada, braco):
                    return {"sucesso": True, "processados": processados, "ops_criadas": len(idiprocs_desta_rodada)}
                else:
                    return {"sucesso": False, "erro": f"Falha ao registrar lote/braço para a rodada {rodada}"}
            else:
                return {"sucesso": True, "processados": processados, "ops_criadas": 0, "mensagem": "Nenhuma OP criada com sucesso"}
                
        except Exception as e:
            logger.error(f"Erro ao processar rodada {rodada}: {e}")
            return {"sucesso": False, "erro": str(e)}

    def finalizar_conexoes(self):
        """Finaliza conexões"""
        try:
            if self.api:
                # Chama o método de logout corrigido
                self.api.logout()
            if self.db and self.db.connection:
                self.db.disconnect()
        except Exception as e:
            logger.error(f"Erro ao finalizar conexões: {e}")

    def obter_resumo(self) -> Dict[str, Any]:
        """Retorna resumo do processamento"""
        return {
            "total_ops_criadas": self.total_ops_criadas,
            "total_falhas": self.total_falhas,
            "ops_criadas_sucesso": self.ops_criadas_sucesso,
            "detalhes_falhas": self.detalhes_falhas
        }

# Instância global do automation
sankhya_automation = SankhyaAutomationAPI()

# Rotas para o Sankhya Automation
@app.route('/api/sankhya/verificar_conexoes', methods=['POST'])
def verificar_conexoes():
    # Reutiliza a instância global para verificar as conexões
    resultado = sankhya_automation.verificar_conexoes()
    return jsonify(resultado)

@app.route('/api/sankhya/buscar_planejamentos', methods=['POST'])
def buscar_planejamentos():
    data = request.json
    resultado = sankhya_automation.buscar_planejamentos(
        data['data_planejamento'],
        data['braco'],
        data['rodada_inicial'],
        data['rodada_final']
    )
    return jsonify(resultado)

@app.route('/api/sankhya/processar_rodada', methods=['POST'])
def processar_rodada():
    data = request.json
    resultado = sankhya_automation.processar_rodada(
        data['data_planejamento'],
        data['braco'],
        data['rodada']
    )
    return jsonify(resultado)

@app.route('/api/sankhya/finalizar_conexoes', methods=['POST'])
def finalizar_conexoes():
    # Chama o método de finalização na instância global
    sankhya_automation.finalizar_conexoes()
    return jsonify({"sucesso": True, "mensagem": "Conexões finalizadas"})

@app.route('/api/sankhya/resumo', methods=['GET'])
def obter_resumo():
    resumo = sankhya_automation.obter_resumo()
    return jsonify(resumo)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "Aplicação Unificada - Auto Prog Master & Sankhya Automation", 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5001, debug=True)

