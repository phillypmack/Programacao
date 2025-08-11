# =========================================================================
# Estágio 1: Instalação do Oracle Instant Client
# Usamos uma imagem base do Debian para instalar as dependências do Oracle.
# =========================================================================
FROM debian:bullseye-slim as oracle-client

# Define variáveis de ambiente para a instalação
ENV ORACLE_VERSION=21.13.0.0.0
ENV ORACLE_HOME=/opt/oracle/instantclient

# Instala dependências necessárias para baixar e descompactar o client
RUN apt-get update && apt-get install -y wget unzip libaio1 && rm -rf /var/lib/apt/lists/*

# Baixa e instala o Oracle Instant Client
WORKDIR /tmp
RUN wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basic-linux.x64-${ORACLE_VERSION}dbru.zip && \
    unzip instantclient-basic-linux.x64-${ORACLE_VERSION}dbru.zip && \
    mkdir -p ${ORACLE_HOME} && \
    mv instantclient_21_13/* ${ORACLE_HOME}/ && \
    rm -rf /tmp/*

# =========================================================================
# Estágio 2: Construção da Aplicação Python
# Usamos uma imagem oficial do Python e copiamos o client do estágio anterior.
# =========================================================================
FROM python:3.11-slim-bullseye

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o Oracle Instant Client instalado no estágio anterior
COPY --from=oracle-client /opt/oracle/instantclient /opt/oracle/instantclient

# Configura as variáveis de ambiente para que o Python encontre as bibliotecas do Oracle
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient
# Atualiza o cache do linker para reconhecer as novas bibliotecas
RUN ldconfig

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todos os arquivos da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta 5000, que é a porta interna do Flask
EXPOSE 5001

# Define o comando padrão que será executado quando o container iniciar
CMD ["python", "main.py"]