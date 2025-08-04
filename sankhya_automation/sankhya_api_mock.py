# Mock da classe SankhyaAPI para teste sem conexão real
import logging
import random
import time

logger = logging.getLogger(__name__)

class SankhyaAPI:
    """
    Mock da classe SankhyaAPI para teste sem conexão real
    """
    
    def __init__(self):
        self.authenticated = False
        self.session_id = None
        logger.info("Mock SankhyaAPI inicializado")

    def testar_conexao(self) -> bool:
        """Mock do teste de conexão"""
        logger.info("Mock: Testando conexão com API Sankhya...")
        return True

    def autenticar(self) -> bool:
        """Mock da autenticação"""
        logger.info("Mock: Autenticando na API Sankhya...")
        self.authenticated = True
        self.session_id = f"mock_session_{int(time.time())}"
        return True

    def logout(self):
        """Mock do logout"""
        logger.info("Mock: Fazendo logout da API Sankhya...")
        self.authenticated = False
        self.session_id = None

    def criar_ordem_producao(self, dados_produto: dict) -> tuple:
        """Mock da criação de ordem de produção"""
        codprod = dados_produto.get('CODPRODPA', 'UNKNOWN')
        tamlote = dados_produto.get('TAMLOTE', 0)
        
        logger.info(f"Mock: Criando OP para produto {codprod}, lote {tamlote}")
        
        # Simular sucesso na maioria dos casos (90%)
        if random.random() < 0.9:
            # Gerar um IDIPROC mock
            idiproc = random.randint(100000, 999999)
            return True, idiproc, f"OP {idiproc} criada com sucesso"
        else:
            # Simular falha ocasional
            return False, None, "Erro simulado na criação da OP"

