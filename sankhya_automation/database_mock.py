# Mock da classe OracleDatabase para teste sem Oracle
import logging

logger = logging.getLogger(__name__)

class OracleDatabase:
    """
    Mock da classe OracleDatabase para teste sem conexão Oracle
    """
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        logger.info("Mock OracleDatabase inicializado")

    def connect(self) -> bool:
        """Mock da conexão"""
        logger.info("Mock: Conectando ao banco Oracle...")
        self.connection = "mock_connection"
        return True

    def disconnect(self):
        """Mock da desconexão"""
        logger.info("Mock: Desconectando do banco Oracle...")
        self.connection = None

    def testar_conexao(self) -> bool:
        """Mock do teste de conexão"""
        logger.info("Mock: Testando conexão com banco Oracle...")
        return self.connection is not None

    def contar_planejamentos_pendentes(self, data_planejamento: str, braco: int, rodada_inicial: int, rodada_final: int) -> int:
        """Mock da contagem de planejamentos"""
        logger.info(f"Mock: Contando planejamentos para {data_planejamento}, braço {braco}, rodadas {rodada_inicial}-{rodada_final}")
        # Simular alguns planejamentos pendentes
        return (rodada_final - rodada_inicial + 1) * 3

    def buscar_planejamentos(self, data_planejamento: str, braco: int, rodada_inicial: int, rodada_final: int):
        """Mock da busca de planejamentos"""
        logger.info(f"Mock: Buscando planejamentos para {data_planejamento}, braço {braco}, rodadas {rodada_inicial}-{rodada_final}")
        
        # Simular dados de planejamento
        planejamentos = []
        for rodada in range(rodada_inicial, rodada_final + 1):
            for i in range(3):  # 3 planejamentos por rodada
                planejamentos.append({
                    'NUPLAN': f'PLAN{rodada}{i+1:02d}',
                    'CODPROD': f'PROD{rodada}{i+1:03d}',
                    'QTDPLAN': 100 + (i * 50),
                    'RODADA': rodada
                })
        
        return planejamentos

    def atualizar_idiproc(self, nuplan: str, idiproc: int) -> bool:
        """Mock da atualização do IDIPROC"""
        logger.info(f"Mock: Atualizando NUPLAN {nuplan} com IDIPROC {idiproc}")
        return True

    def gerar_lote_para_ops(self, idiprocs: list, braco: int) -> bool:
        """Mock da geração de lote"""
        logger.info(f"Mock: Gerando lote para OPs {idiprocs} no braço {braco}")
        return True

