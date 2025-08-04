# Guia de Instalação - Aplicação Sankhya OP Automation

## Pré-requisitos

### Sistema Operacional
- Windows 10/11, macOS 10.15+, ou Linux (Ubuntu 18.04+)
- Conexão com internet para instalação de dependências

### Software Necessário
- **Python 3.11 ou superior**
  - Download: https://www.python.org/downloads/
  - Durante a instalação no Windows, marque "Add Python to PATH"

### Acesso aos Sistemas
- **Banco de Dados Oracle**: Credenciais e conectividade
- **API Sankhya**: AppKey, Token e credenciais de usuário

## Instalação Passo a Passo

### 1. Preparação do Ambiente

#### Windows
```cmd
# Abra o Prompt de Comando como Administrador
# Verifique se o Python está instalado
python --version

# Se necessário, instale o pip
python -m ensurepip --upgrade
```

#### Linux/macOS
```bash
# Verifique se o Python está instalado
python3 --version

# Instale pip se necessário (Ubuntu/Debian)
sudo apt update
sudo apt install python3-pip

# macOS com Homebrew
brew install python3
```

### 2. Download da Aplicação

Crie um diretório para a aplicação e copie todos os arquivos:

```bash
# Crie o diretório
mkdir sankhya_op_automation
cd sankhya_op_automation

# Copie os seguintes arquivos para este diretório:
# - main.py
# - config.py
# - database.py
# - sankhya_api.py
# - interface.py
# - test_connections.py
# - requirements.txt
# - .env.example
# - README.md
```

### 3. Instalação das Dependências

```bash
# Instale as dependências Python
pip install -r requirements.txt

# Ou instale individualmente:
pip install requests sqlalchemy oracledb python-dotenv
```

### 4. Configuração das Credenciais

#### 4.1 Crie o arquivo de configuração
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# No Windows:
copy .env.example .env
```

#### 4.2 Edite o arquivo .env

Abra o arquivo `.env` em um editor de texto e configure suas credenciais:

```env
# Configurações do Banco de Dados Oracle
ORACLE_HOST=201.48.122.72
ORACLE_PORT=12821
ORACLE_SERVICE=Orcl
ORACLE_USER=SANKHYA
ORACLE_PASSWORD=vasap128

# Configurações da API Sankhya
SANKHYA_BASE_URL=http://ecoplax.rcs.inf.br:8180/mge
SANKHYA_LOGIN_URL=https://api.sankhya.com.br/login
SANKHYA_GATEWAY_URL=https://api.sankhya.com.br/gateway/v1/mge/service.sbr
SANKHYA_APP_KEY=d828b56b-c64d-4607-98a4-71cbc07008c9
SANKHYA_USERNAME=FELIPE
SANKHYA_PASSWORD=1357997531

# Configurações da aplicação
DEBUG=False
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
```

**⚠️ IMPORTANTE**: Substitua os valores de exemplo pelas suas credenciais reais.

### 5. Teste da Instalação

Execute o script de teste para verificar se tudo está funcionando:

```bash
python test_connections.py

# No Windows, se necessário:
python.exe test_connections.py
```

**Resultado esperado**:
```
============================================================
    TESTE DE CONEXÕES - SANKHYA OP AUTOMATION
============================================================

🔍 Testando conexão com banco Oracle...
✅ Conexão com banco Oracle OK.
✅ Consulta na tabela AD_PLAN executada. Registros encontrados: X

🔍 Testando conexão com API Sankhya...
✅ Autenticação com API Sankhya OK.
✅ Logout da API Sankhya OK.

============================================================
                RESULTADO DOS TESTES
============================================================
✅ Todos os testes passaram! A aplicação está pronta para uso.
```

## Solução de Problemas na Instalação

### Erro: "python não é reconhecido como comando"

**Windows**:
1. Reinstale o Python marcando "Add Python to PATH"
2. Ou adicione manualmente ao PATH:
   - Painel de Controle → Sistema → Configurações Avançadas
   - Variáveis de Ambiente → PATH → Adicionar caminho do Python

**Linux/macOS**:
```bash
# Use python3 em vez de python
python3 --version
python3 -m pip install -r requirements.txt
```

### Erro: "pip não encontrado"

```bash
# Windows
python -m ensurepip --upgrade

# Linux
sudo apt install python3-pip

# macOS
python3 -m ensurepip --upgrade
```

### Erro na instalação do oracledb

**Linux**:
```bash
# Instale dependências do sistema
sudo apt install libaio1 libaio-dev

# Para CentOS/RHEL:
sudo yum install libaio libaio-devel
```

**Windows**:
- Instale o Microsoft Visual C++ Redistributable
- Download: https://aka.ms/vs/17/release/vc_redist.x64.exe

### Erro de conexão com Oracle

1. **Verifique conectividade de rede**:
   ```bash
   # Teste se o servidor está acessível
   telnet 201.48.122.72 12821
   ```

2. **Verifique as credenciais**:
   - Host, porta e service name corretos
   - Usuário e senha válidos
   - Permissões adequadas na tabela AD_PLAN

3. **Firewall**:
   - Libere a porta 12821 no firewall
   - Verifique se não há proxy bloqueando

### Erro de autenticação Sankhya

1. **Verifique as credenciais**:
   - AppKey válida e ativa
   - Token de consentimento correto
   - Usuário e senha do SankhyaID

2. **Permissões**:
   - Usuário deve ter permissão de "Incluir" em Ordens de Produção
   - Verificar se o usuário não está bloqueado

3. **Conectividade**:
   ```bash
   # Teste conectividade com a API
   curl -I https://api.sankhya.com.br/login
   ```

## Configuração de Ambiente de Desenvolvimento

### Ambiente Virtual (Recomendado)

```bash
# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### IDE Recomendadas

- **Visual Studio Code**: Com extensões Python
- **PyCharm**: Community ou Professional
- **Sublime Text**: Com pacote Python

## Configuração para Produção

### 1. Variáveis de Ambiente do Sistema

Em vez de usar arquivo `.env`, configure as variáveis no sistema:

**Windows**:
```cmd
setx ORACLE_HOST "seu_host"
setx ORACLE_USER "seu_usuario"
# ... outras variáveis
```

**Linux/macOS**:
```bash
export ORACLE_HOST="seu_host"
export ORACLE_USER="seu_usuario"
# Adicione ao ~/.bashrc ou ~/.profile para persistir
```

### 2. Agendamento de Execução

**Windows (Task Scheduler)**:
1. Abra o Agendador de Tarefas
2. Criar Tarefa Básica
3. Configure para executar: `python C:\caminho\para\main.py`

**Linux (Cron)**:
```bash
# Edite o crontab
crontab -e

# Exemplo: executar diariamente às 8h
0 8 * * * cd /caminho/para/aplicacao && python3 main.py
```

### 3. Monitoramento

Configure monitoramento dos logs:
- Arquivo: `sankhya_op_automation.log`
- Rotação de logs para evitar arquivos muito grandes
- Alertas em caso de falhas críticas

## Backup e Recuperação

### Backup dos Dados
- Arquivo `.env` com credenciais
- Logs de execução
- Configurações customizadas

### Recuperação
1. Reinstale as dependências: `pip install -r requirements.txt`
2. Restaure o arquivo `.env`
3. Execute teste: `python test_connections.py`

## Atualizações

Para atualizar a aplicação:
1. Faça backup do arquivo `.env`
2. Substitua os arquivos Python pelos novos
3. Verifique se há novas dependências em `requirements.txt`
4. Execute os testes novamente

---

**Suporte**: Em caso de problemas, consulte os logs em `sankhya_op_automation.log` e execute o script de teste para diagnóstico.

