"""
Arquivo de configuração para a aplicação de automação de Ordens de Produção Sankhya.
Este arquivo contém as configurações de conexão com o banco Oracle e API Sankhya.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env se existir
load_dotenv()

# Configurações do Banco de Dados Oracle
ORACLE_CONFIG = {
    'host': os.getenv('ORACLE_HOST', '201.48.122.72'),
    'port': os.getenv('ORACLE_PORT', '12821'),
    'service_name': os.getenv('ORACLE_SERVICE', 'Orcl'),
    'username': os.getenv('ORACLE_USER', 'SANKHYA'),
    'password': os.getenv('ORACLE_PASSWORD', 'vasap128')
}

# String de conexão Oracle
ORACLE_DATABASE_URI = f"oracle+oracledb://{ORACLE_CONFIG['username']}:{ORACLE_CONFIG['password']}@{ORACLE_CONFIG['host']}:{ORACLE_CONFIG['port']}/{ORACLE_CONFIG['service_name']}"

# Configurações da API Sankhya
SANKHYA_CONFIG = {
    'base_url': os.getenv('SANKHYA_BASE_URL', 'http://ecoplax.rcs.inf.br:8180/mge'),
    'login_url': os.getenv('SANKHYA_LOGIN_URL', 'https://api.sankhya.com.br/login'),
    'gateway_url': os.getenv('SANKHYA_GATEWAY_URL', 'https://api.sankhya.com.br/gateway/v1/mgeprod/service.sbr'),
    'app_key': os.getenv('SANKHYA_APP_KEY', '61787b87-e480-4918-8d03-9830cab7c200'),
    'client_token': os.getenv('SANKHYA_CLIENT_TOKEN'),
    'username': os.getenv('SANKHYA_USERNAME', 'felipe.santos@vasap.com.br'),
    'password': os.getenv('SANKHYA_PASSWORD', 'Shark@777'),
    # --- CORREÇÃO ADICIONADA AQUI ---
    # A mgeSession é estática e carregada da configuração, conforme seu script original.
    'mge_session': os.getenv('SANKHYA_MGE_SESSION', 'W5cGv0PR4OajnG1F56Met0aIibhkI1XJH9gpDjcl')
}

# Configurações da aplicação
APP_CONFIG = {
    'debug': os.getenv('DEBUG', 'False').lower() == 'true',
    'log_level': os.getenv('LOG_LEVEL', 'INFO'),
    'timeout': int(os.getenv('REQUEST_TIMEOUT', '60'))
}