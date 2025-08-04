"""
Aplicação principal para automação de Ordens de Produção no sistema Sankhya.
...
"""

import logging
import sys
from typing import Dict, Any
from database import OracleDatabase
from sankhya_api import SankhyaAPI
from interface import InterfaceUsuario

# ... (configuração do logging continua igual) ...

logger = logging.getLogger(__name__)

class AutomacaoOrdemProducao:
    """
    Classe principal para automação de criação de Ordens de Produção.
    """
    
    def __init__(self):
        self.db = OracleDatabase()
        self.api = SankhyaAPI()
        self.interface = InterfaceUsuario()
        
        self.total_ops_criadas = 0
        self.total_falhas = 0
        self.ops_criadas_sucesso = []
        self.detalhes_falhas = []

    def verificar_conexoes(self) -> bool:
        self.interface.exibir_progresso("Verificando conexões...", "info")
        if not self.db.connect() or not self.db.testar_conexao():
            self.interface.exibir_progresso("Falha na conexão com o banco Oracle.", "erro")
            return False
        self.interface.exibir_progresso("Conexão com banco Oracle estabelecida.", "sucesso")
        
        # A autenticação inicial agora é feita dentro do loop,
        # mas mantemos um teste de conexão aqui como um pré-requisito.
        if not self.api.testar_conexao():
            self.interface.exibir_progresso("Falha no teste inicial de conexão com a API Sankhya.", "erro")
            self.db.disconnect()
            return False
        self.interface.exibir_progresso("Conexão com API Sankhya estabelecida.", "sucesso")
        return True

    def processar_uma_rodada(self, data_planejamento: str, braco: int, rodada_atual: int):
        """
        Processa todos os planejamentos de UMA ÚNICA rodada.
        """
        self.interface.exibir_progresso(f"--- Iniciando processamento da Rodada: {rodada_atual} ---", "info")
        
        registros = self.db.buscar_planejamentos(data_planejamento, braco, rodada_atual, rodada_atual)
        
        if not registros:
            self.interface.exibir_progresso(f"Nenhum planejamento pendente para a Rodada {rodada_atual}.", "aviso")
            return

        self.interface.exibir_progresso(f"Processando {len(registros)} planejamentos para a Rodada {rodada_atual}...", "info")
        
        idiprocs_desta_rodada = []
        for i, registro in enumerate(registros, 1):
            self.interface.exibir_progresso(f"  [{i}/{len(registros)}-{rodada_atual}] Processando NUPLAN: {registro['NUPLAN']}...", "info")
            
            try:
                dados_produto_api = {"CODPRODPA": registro['CODPROD'], "IDPROC": 51, "CODPLP": 1, "TAMLOTE": registro['QTDPLAN']}
                sucesso, idiproc, mensagem = self.api.criar_ordem_producao(dados_produto_api)

                if sucesso and idiproc:
                    if self.db.atualizar_idiproc(registro['NUPLAN'], idiproc):
                        self.interface.exibir_progresso(f"    ✅ OP {idiproc} criada e NUPLAN {registro['NUPLAN']} atualizado.", "sucesso")
                        self.total_ops_criadas += 1
                        self.ops_criadas_sucesso.append({"nuplan": registro['NUPLAN'], "idiproc": idiproc})
                        idiprocs_desta_rodada.append(idiproc)
                    else:
                        erro_msg = f"OP {idiproc} criada, mas FALHA ao atualizar banco."
                        self.interface.exibir_progresso(f"    ❌ {erro_msg}", "erro")
                        self.detalhes_falhas.append({"nuplan": registro['NUPLAN'], "erro": erro_msg})
                        self.total_falhas += 1
                else:
                    erro_msg = f"Erro ao criar OP: {mensagem}"
                    self.interface.exibir_progresso(f"    ❌ {erro_msg}", "erro")
                    self.detalhes_falhas.append({"nuplan": registro['NUPLAN'], "erro": erro_msg})
                    self.total_falhas += 1
            except Exception as e:
                erro_msg = f"Erro inesperado ao processar NUPLAN {registro['NUPLAN']}: {e}"
                logger.error(erro_msg, exc_info=True)
                self.interface.exibir_progresso(f"    ❌ {erro_msg}", "erro")
                self.detalhes_falhas.append({"nuplan": registro['NUPLAN'], "erro": erro_msg})
                self.total_falhas += 1
            
            import time
            time.sleep(0.5)

        self.interface.exibir_progresso(f"Finalizando a Rodada {rodada_atual}...", "info")
        if idiprocs_desta_rodada:
            if self.db.gerar_lote_para_ops(idiprocs_desta_rodada, braco):
                self.interface.exibir_progresso(f"Lote unificado e braço registrados para a Rodada {rodada_atual}.", "sucesso")
            else:
                self.interface.exibir_progresso(f"FALHA ao registrar lote/braço para a Rodada {rodada_atual}.", "erro")
        else:
            self.interface.exibir_progresso("Nenhuma OP criada com sucesso nesta rodada, geração de lote ignorada.", "aviso")

    def finalizar_conexoes(self):
        try:
            self.interface.exibir_progresso("Finalizando conexões...", "info")
            if self.api: self.api.logout()
            if self.db: self.db.disconnect()
            self.interface.exibir_progresso("Conexões finalizadas.", "sucesso")
        except Exception as e:
            logger.error(f"Erro ao finalizar conexões: {e}")

    # --- MÉTODO EXECUTAR ATUALIZADO COM A LÓGICA DE RE-AUTENTICAÇÃO ---
    def executar(self):
        """
        Método principal que orquestra toda a aplicação.
        """
        try:
            parametros = self.interface.coletar_parametros()
            if not parametros:
                self.interface.exibir_progresso("Operação cancelada na coleta de parâmetros.", "aviso")
                return
            
            data_planejamento, braco, rodada_inicial, rodada_final = parametros
            print()

            # A verificação de conexão com o banco é feita uma vez.
            if not self.db.connect() or not self.db.testar_conexao():
                self.interface.exibir_progresso("Falha na conexão com o banco Oracle. Abortando.", "erro")
                return
            
            print()

            total_a_processar = self.db.contar_planejamentos_pendentes(data_planejamento, braco, rodada_inicial, rodada_final)

            if total_a_processar == 0:
                self.interface.exibir_progresso("Nenhum planejamento pendente encontrado para o range de rodadas informado.", "aviso")
            else:
                if self.interface.confirmar_continuacao(f"Encontrados {total_a_processar} planejamentos no total. Deseja processar todos?"):
                    # Loop principal que itera sobre cada rodada
                    for rodada in range(rodada_inicial, rodada_final + 1):
                        # --- MELHORIA ADICIONADA AQUI ---
                        # Inicia uma nova sessão da API para cada rodada
                        self.interface.exibir_progresso(f"Iniciando nova sessão na API para a Rodada {rodada}...", "info")
                        if not self.api.autenticar():
                            self.interface.exibir_progresso(f"Falha ao re-autenticar para a Rodada {rodada}. Abortando processo.", "erro")
                            break # Interrompe o loop principal se a autenticação falhar

                        # Chama o método que processa a rodada com a sessão nova
                        self.processar_uma_rodada(data_planejamento, braco, rodada)
                        print() # Adiciona espaço entre o processamento de cada rodada
                else:
                    self.interface.exibir_progresso("Processamento cancelado pelo usuário.", "aviso")

            self.interface.exibir_progresso("--- Todas as rodadas do range foram processadas. ---", "sucesso")

        except KeyboardInterrupt:
            self.interface.exibir_progresso("Operação interrompida pelo usuário.", "aviso")
        except Exception as e:
            erro_msg = f"Erro inesperado na aplicação: {e}"
            logger.error(erro_msg, exc_info=True)
            self.interface.exibir_progresso(erro_msg, "erro")
        finally:
            self.finalizar_conexoes()
            self.interface.exibir_resumo_final(
                self.total_ops_criadas, 
                self.total_falhas,
                self.ops_criadas_sucesso,
                self.detalhes_falhas
            )

# ... (função main() continua igual) ...
def main():
    """
    Função principal da aplicação.
    """
    try:
        app = AutomacaoOrdemProducao()
        app.executar()
    except Exception as e:
        print(f"❌ Erro crítico na aplicação: {e}")
        logger.critical(f"Erro crítico na aplicação: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()