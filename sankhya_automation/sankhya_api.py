"""
Módulo para integração com a API Sankhya.
...
"""
import logging
import requests
import json
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime
from config import SANKHYA_CONFIG, APP_CONFIG

# ... (código anterior da classe SankhyaAPI) ...
logger = logging.getLogger(__name__)

RESOURCE_ID = "br.com.sankhya.prod.OrdensProducaoHTML"

class SankhyaAPI:
    def __init__(self):
        # Carrega as configurações essenciais no construtor
        self.bearer_token: Optional[str] = None
        self.client_token: Optional[str] = SANKHYA_CONFIG.get('client_token')
        self.mge_session: Optional[str] = SANKHYA_CONFIG.get('mge_session')
        self.session = requests.Session()
        self.session.timeout = APP_CONFIG.get('timeout', 60)
        logger.info("Instância da SankhyaAPI criada.")

    def autenticar(self) -> bool:
        """Etapa 1: Realiza autenticação para obter o bearerToken."""
        logger.info("Iniciando nova autenticação na API Sankhya...")
        
        # Valida as configurações carregadas no construtor
        if not all([self.client_token, self.mge_session]):
            logger.error("Erro Crítico: SANKHYA_CLIENT_TOKEN ou SANKHYA_MGE_SESSION não estão definidos na configuração.")
            return False

        headers = {
            'token': self.client_token,
            'appkey': SANKHYA_CONFIG['app_key'],
            'username': SANKHYA_CONFIG['username'],
            'password': SANKHYA_CONFIG['password']
        }
        try:
            response = self.session.post(SANKHYA_CONFIG['login_url'], headers=headers)
            response.raise_for_status()
            data = response.json()
            
            self.bearer_token = data.get("bearerToken")
            
            if self.bearer_token:
                logger.info("Autenticação realizada com sucesso (bearerToken obtido e armazenado).")
                return True
            else:
                error_msg = data.get('statusMessage', 'bearerToken não encontrado na resposta de login.')
                logger.error(f"Falha na autenticação: {error_msg}")
                return False
        except requests.RequestException as e:
            logger.error(f"Erro na requisição de autenticação: {e}", exc_info=True)
            return False
        except json.JSONDecodeError:
            logger.error(f"Falha ao decodificar a resposta JSON da autenticação. Resposta recebida: {response.text}")
            return False

    # ... (métodos _get_new_nulop, _inserir_produto, _validar_lote, _lancar_op, criar_ordem_producao continuam iguais) ...
    def _get_new_nulop(self) -> Optional[int]:
        """Etapa 2: Cria um rascunho (NULOP) para a Ordem de Produção."""
        logger.info("Criando rascunho (NULOP)...")
        service_name = "LancamentoOrdemProducaoSP.getNovoLancamentoOP"
        params = {"serviceName": service_name, "outputType": "json", "mgeSession": self.mge_session, "resourceID": RESOURCE_ID}
        payload = {"serviceName": service_name, "requestBody": {"params": {"descricao": f"Novo lançamento via API - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", "reutilizar": "N"}}}
        headers = {'Authorization': f'Bearer {self.bearer_token}', 'Content-Type': 'application/json'}
        try:
            response = self.session.post(SANKHYA_CONFIG['gateway_url'], headers=headers, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "1":
                nulop = data.get("responseBody", {}).get("lancamento", {}).get("nulop")
                logger.info(f"Rascunho NULOP {nulop} criado com sucesso.")
                return int(nulop)
            else:
                logger.error(f"Erro ao obter NULOP: {data.get('statusMessage')}")
                return None
        except (requests.RequestException, ValueError) as e:
            logger.error(f"Erro na requisição get_new_nulop: {e}", exc_info=True)
            return None

    def _inserir_produto(self, nulop: int, dados_produto: Dict[str, Any]) -> bool:
        """Etapa 3: Insere o produto no rascunho da Ordem de Produção."""
        logger.info(f"Inserindo produto no NULOP {nulop}...")
        service_name = "LancamentoOrdemProducaoSP.inserirProdutoHTML5"
        params = {"serviceName": service_name, "outputType": "json", "mgeSession": self.mge_session, "resourceID": RESOURCE_ID}
        payload = {"serviceName": service_name, "requestBody": {"params": {
            "nulop": str(nulop),
            "codprod": str(dados_produto.get("CODPRODPA")),
            "idproc": str(dados_produto.get("IDPROC")),
            "codplp": str(dados_produto.get("CODPLP")),
            "tamlote": str(dados_produto.get("TAMLOTE")),
            "agruparEmUnicaOP": False, "controle": {}, "minLote": "0.0", "multiIdeal": "0.0", "oldTamLote": "1.0", "opDesmonte": "N", "opReparo": "N"
        }}}
        headers = {'Authorization': f'Bearer {self.bearer_token}', 'Content-Type': 'application/json'}
        try:
            response = self.session.post(SANKHYA_CONFIG['gateway_url'], headers=headers, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "1":
                logger.info("Produto inserido com sucesso.")
                return True
            else:
                logger.error(f"Erro ao inserir produto: {data.get('statusMessage')}")
                return False
        except requests.RequestException as e:
            logger.error(f"Erro na requisição de inserção do produto: {e}", exc_info=True)
            return False

    def _validar_lote(self, dados_produto: Dict[str, Any]) -> bool:
        """Etapa 3.5: Valida o tamanho do lote."""
        logger.info("Validando tamanho do lote...")
        service_name = "LancamentoOrdemProducaoSP.validarTamanhoLote"
        params = {"serviceName": service_name, "outputType": "json", "mgeSession": self.mge_session, "resourceID": RESOURCE_ID}
        payload = {"serviceName": service_name, "requestBody": {"params": {"tamLote": str(dados_produto.get("TAMLOTE")), "multiploIdeal": "0", "minLote": "0"}}}
        headers = {'Authorization': f'Bearer {self.bearer_token}', 'Content-Type': 'application/json'}
        try:
            response = self.session.post(SANKHYA_CONFIG['gateway_url'], headers=headers, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "1":
                logger.info("Validação de lote OK.")
                return True
            else:
                logger.warning(f"Aviso na validação do lote: {data.get('statusMessage')}")
                return True # Continua mesmo com avisos
        except requests.RequestException as e:
            logger.error(f"Erro na requisição de validação de lote: {e}", exc_info=True)
            return False

    def _lancar_op(self, nulop: int) -> Optional[int]:
        """Etapa 4: Finaliza e lança a Ordem de Produção."""
        logger.info(f"Finalizando e lançando a OP para o NULOP {nulop}...")
        service_name = "LancamentoOrdemProducaoSP.lancarOrdensDeProducao"
        params = {"serviceName": service_name, "outputType": "json", "mgeSession": self.mge_session, "resourceID": RESOURCE_ID}
        payload = {"serviceName": service_name, "requestBody": {"params": {"nulop": str(nulop), "ignorarWarnings": "N"}}}
        headers = {'Authorization': f'Bearer {self.bearer_token}', 'Content-Type': 'application/json'}
        try:
            response = self.session.post(SANKHYA_CONFIG['gateway_url'], headers=headers, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "1" and int(data.get("responseBody", {}).get("ordensIniciadas", {}).get("quantidade", {}).get("$", 0)) > 0:
                ordens = data.get("responseBody", {}).get("ordens", {}).get("ordem", [])
                if isinstance(ordens, dict):
                    ordens = [ordens]
                id_op = ordens[0].get("$")
                logger.info(f"Ordem de Produção {id_op} lançada com sucesso!")
                return int(id_op)
            else:
                logger.error(f"Erro ao lançar OP: {data.get('statusMessage')}")
                return None
        except (requests.RequestException, KeyError, IndexError, ValueError) as e:
            logger.error(f"Erro na requisição de lançamento da OP: {e}", exc_info=True)
            return None

    def criar_ordem_producao(self, dados_produto: Dict[str, Any]) -> Tuple[bool, Optional[int], str]:
        """Orquestra o fluxo completo de criação de uma Ordem de Produção."""
        nulop = self._get_new_nulop()
        if not nulop:
            return False, None, "Falha ao criar o rascunho (NULOP)."

        if not self._inserir_produto(nulop, dados_produto):
            return False, None, "Falha ao inserir o produto no rascunho."

        if not self._validar_lote(dados_produto):
            logger.warning("Continuando processo mesmo após aviso na validação do lote.")

        id_op_final = self._lancar_op(nulop)
        if id_op_final:
            return True, id_op_final, f"OP {id_op_final} criada com sucesso."
        else:
            return False, None, "Falha ao finalizar e lançar a Ordem de Produção."

    # --- NOVO MÉTODO ADICIONADO ---
    def gerar_rodada_vasap(self, idiprocs: List[int]) -> Optional[str]:
        """
        Aciona o botão "Gerar Rodada Vasap" para um conjunto de Ordens de Produção.
        
        Args:
            idiprocs (List[int]): Lista de IDs das Ordens de Produção (IDIPROC).
            
        Returns:
            Optional[str]: O número da rodada gerado, ou None em caso de falha.
        """
        logger.info(f"Acionando 'Gerar Rodada Vasap' para {len(idiprocs)} OPs...")
        
        # Monta o payload conforme a imagem fornecida
        service_name = "ActionButtonsSP.executeSTP"
        
        # Converte a lista de inteiros para o formato que a API espera
        rows_payload = [{"IDIPROC": str(pid)} for pid in idiprocs]
        
        payload = {
            "serviceName": service_name,
            "requestBody": {
                "clientEventList": {},
                "stpCall": {
                    "actionID": "136",
                    "procName": "STP_GERAR_RODADA_VASAP",
                    "rootEntity": "CabecalhoInstanciaProcesso",
                    "rows": rows_payload
                }
            }
        }
        
        headers = {'Authorization': f'Bearer {self.bearer_token}', 'Content-Type': 'application/json'}
        params = {"serviceName": service_name, "outputType": "json", "mgeSession": self.mge_session}

        try:
            response = self.session.post(SANKHYA_CONFIG['gateway_url'], headers=headers, params=params, json=payload)
            response.raise_for_status()
            data = response.json()
            
            logger.debug(f"Resposta completa de gerar_rodada_vasap: {json.dumps(data, indent=2)}")

            if data.get("status") == "1":
                # A resposta de um botão de ação geralmente vem em 'pendingArgs' ou 'pk'
                # Esta parte pode precisar de ajuste fino com base na resposta real da API
                response_body = data.get("responseBody", {})
                
                # Tentativa 1: Procurar em 'callID' ou similar
                numero_rodada = response_body.get("callID") # Exemplo, pode ser outro nome
                
                # Tentativa 2: Procurar em mensagens de retorno
                if not numero_rodada and "message" in response_body:
                    # Tenta extrair um número da mensagem de sucesso
                    import re
                    match = re.search(r'Rodada (\d+) gerada', response_body["message"])
                    if match:
                        numero_rodada = match.group(1)

                if numero_rodada:
                    logger.info(f"Rodada Vasap número '{numero_rodada}' gerada com sucesso.")
                    return str(numero_rodada)
                else:
                    logger.warning("Ação 'Gerar Rodada' executada, mas não foi possível extrair o número da rodada da resposta.")
                    # Retorna um valor padrão ou None, dependendo da regra de negócio
                    return None
            else:
                logger.error(f"Erro ao acionar 'Gerar Rodada': {data.get('statusMessage')}")
                return None
        except requests.RequestException as e:
            logger.error(f"Erro na requisição para 'Gerar Rodada': {e}", exc_info=True)
            return None

    def logout(self):
        """Etapa Final: Realiza o logout da sessão na API Sankhya."""
        if not self.bearer_token:
            logger.info("Nenhuma sessão ativa para fazer logout.")
            return

        logger.info("Realizando logout da API Sankhya...")
        # CORREÇÃO: Usando um serviço de logout mais comum. 'MobileLoginSP.logout' é uma alternativa frequente.
        service_name = "MobileLoginSP.logout" 
        params = {"serviceName": service_name, "outputType": "json", "mgeSession": self.mge_session}
        headers = {'Authorization': f'Bearer {self.bearer_token}'}
        
        try:
            response = self.session.post(SANKHYA_CONFIG['gateway_url'], headers=headers, params=params, json={}, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "1":
                logger.info("Logout da API Sankhya realizado com sucesso.")
            else:
                logger.warning(f"Resposta de logout não foi status 1. Mensagem: {data.get('statusMessage')}")

        except requests.RequestException as e:
            logger.error(f"Erro na requisição de logout: {e}.")
        finally:
            # CORREÇÃO: Apenas o bearer_token deve ser limpo. As outras configurações são fixas.
            self.bearer_token = None
            logger.info("Token de sessão local limpo.")

    def testar_conexao(self) -> bool:
        """Testa a conexão realizando uma autenticação e um logout em sequência."""
        if self.autenticar():
            self.logout()
            return True
        return False