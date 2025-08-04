# Aplicação para Automação de Ordens de Produção (Sankhya API)

## Visão Geral

Esta aplicação Python automatiza a criação de Ordens de Produção (OPs) no sistema ERP Sankhya. A aplicação lê dados de planejamento de produção de um banco de dados Oracle e, para cada item do planejamento, faz uma chamada de API para o Sankhya, criando a respectiva Ordem de Produção e atualizando o item original no banco com o número da OP criada.

## Funcionalidades

- **Interface de Console Intuitiva**: Coleta parâmetros do usuário de forma interativa
- **Conexão com Oracle**: Consulta dados da tabela AD_PLAN com filtros dinâmicos
- **Integração com API Sankhya**: Autenticação e criação de OPs via API REST
- **Atualização Automática**: Atualiza o banco Oracle com os IDs das OPs criadas
- **Tratamento de Erros**: Gerenciamento robusto de falhas e exceções
- **Logging Completo**: Registro detalhado de todas as operações
- **Feedback em Tempo Real**: Progresso e status das operações

## Requisitos do Sistema

### Software
- Python 3.11 ou superior
- Acesso ao banco de dados Oracle
- Conectividade com a API Sankhya

### Dependências Python
- `requests` >= 2.32.0
- `sqlalchemy` >= 2.0.0
- `oracledb` >= 3.2.0
- `python-dotenv` >= 1.1.0

## Instalação

### 1. Clone ou baixe os arquivos do projeto

```bash
mkdir sankhya_op_automation
cd sankhya_op_automation
# Copie todos os arquivos Python para este diretório
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as credenciais

Copie o arquivo `.env.example` para `.env` e ajuste as configurações:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
# Configurações do Banco de Dados Oracle
ORACLE_HOST=seu_host_oracle
ORACLE_PORT=1521
ORACLE_SERVICE=seu_service_name
ORACLE_USER=seu_usuario
ORACLE_PASSWORD=sua_senha

# Configurações da API Sankhya
SANKHYA_BASE_URL=http://seu_servidor_sankhya:8180/mge
SANKHYA_LOGIN_URL=https://api.sankhya.com.br/login
SANKHYA_GATEWAY_URL=https://api.sankhya.com.br/gateway/v1/mge/service.sbr
SANKHYA_APP_KEY=sua_app_key
SANKHYA_USERNAME=seu_usuario_sankhya
SANKHYA_PASSWORD=sua_senha_sankhya
```

## Uso

### Teste das Conexões

Antes de executar a aplicação principal, teste as conexões:

```bash
python test_connections.py
```

Este comando verificará:
- Conectividade com o banco Oracle
- Autenticação com a API Sankhya
- Acesso à tabela AD_PLAN

### Execução da Aplicação Principal

```bash
python main.py
```

A aplicação solicitará os seguintes parâmetros:

1. **Data do Planejamento**: Data específica no formato DD/MM/YYYY (ex: 21/07/2025)
2. **Braço de Produção**: Número do braço que será programado (ex: 1)
3. **Range de Rodadas**: Rodada inicial e final (ex: 1 a 5)

### Exemplo de Execução

```
======================================================================
    APLICAÇÃO PARA AUTOMAÇÃO DE ORDENS DE PRODUÇÃO
                    Sistema Sankhya
======================================================================

📅 Data do Planejamento:
   Digite a data específica para a qual a produção será programada.
   Formato: DD/MM/YYYY (ex: 21/07/2025)

   Data: 21/07/2025

🏭 Braço de Produção:
   Digite o número do braço que será programado.
   Exemplo: 1, 2, 3, etc.

   Braço: 1

🔄 Range de Rodadas:
   Digite a rodada inicial e final a serem processadas.
   Exemplo: rodada inicial = 1, rodada final = 5

   Rodada inicial: 1
   Rodada final: 5

📋 Resumo dos Parâmetros:
   Data do Planejamento: 21/07/2025
   Braço de Produção: 1
   Range de Rodadas: 1 a 5

   Confirma os parâmetros? (s/n): s
```

## Estrutura do Projeto

```
sankhya_op_automation/
├── main.py                 # Aplicação principal
├── config.py              # Configurações e credenciais
├── database.py            # Módulo de conexão com Oracle
├── sankhya_api.py         # Módulo de integração com API Sankhya
├── interface.py           # Interface de usuário (console)
├── test_connections.py    # Script de teste das conexões
├── requirements.txt       # Dependências Python
├── .env.example          # Exemplo de arquivo de configuração
├── .env                  # Arquivo de configuração (criar)
└── README.md             # Esta documentação
```

## Fluxo de Funcionamento

1. **Coleta de Parâmetros**: A aplicação solicita ao usuário os parâmetros de entrada
2. **Verificação de Conexões**: Testa conectividade com banco Oracle e API Sankhya
3. **Consulta de Dados**: Executa consulta SQL na tabela AD_PLAN com os filtros fornecidos
4. **Processamento em Loop**: Para cada registro encontrado:
   - Autentica na API do Sankhya
   - Monta e envia requisição para criar a Ordem de Produção
   - Extrai o ID da nova OP da resposta da API
   - Atualiza o banco Oracle com o IDIPROC
5. **Relatório Final**: Exibe resumo com total de OPs criadas e falhas

## Consulta SQL Utilizada

A aplicação executa a seguinte consulta na tabela AD_PLAN:

```sql
SELECT NUPLAN, CODPROD, QTDPLAN
FROM AD_PLAN
WHERE
    TRUNC(DTINC) = TO_DATE(:data_planejamento, 'DD/MM/YYYY')
    AND BRACO = :braco
    AND RODADA BETWEEN :rodada_inicial AND :rodada_final
    AND IDIPROC IS NULL
ORDER BY NUPLAN
```

## Estrutura do Payload da API

Para cada NUPLAN encontrado, a aplicação monta o seguinte payload:

```json
{
    "serviceName": "CRUDServiceProvider.saveRecord",
    "requestBody": {
        "dataSet": {
            "rootEntity": "OrdemProducao",
            "dataRow": {
                "localFields": {
                    "CODPLAN": { "$": "1" },
                    "CODPROD": { "$": "codigo_do_produto" },
                    "CODPROC": { "$": "1" },
                    "QTDPROD": { "$": "quantidade_planejada" }
                }
            }
        }
    }
}
```

## Tratamento de Erros

A aplicação possui tratamento robusto de erros para:

- **Erros de Conexão**: Falhas na conectividade com banco ou API
- **Erros de Autenticação**: Credenciais inválidas ou expiradas
- **Erros de Validação**: Dados inválidos ou malformados
- **Erros de Regras de Negócio**: Violações de regras configuradas no ERP
- **Erros Inesperados**: Exceções não previstas

Todos os erros são registrados no arquivo `sankhya_op_automation.log` e exibidos na tela.

## Logging

A aplicação gera logs detalhados em dois locais:
- **Console**: Mensagens de progresso e status
- **Arquivo**: `sankhya_op_automation.log` com histórico completo

Níveis de log:
- `INFO`: Operações normais e progresso
- `WARNING`: Situações que merecem atenção
- `ERROR`: Erros que impedem operações específicas
- `CRITICAL`: Erros que impedem a execução da aplicação

## Segurança

### Credenciais
- Nunca inclua credenciais diretamente no código
- Use o arquivo `.env` para configurações sensíveis
- Adicione `.env` ao `.gitignore` se usar controle de versão

### Permissões
- O usuário Sankhya deve ter permissão de "Incluir" no módulo de Ordens de Produção
- O usuário Oracle deve ter acesso de leitura/escrita na tabela AD_PLAN

## Solução de Problemas

### Erro de Conexão com Oracle
```
DPY-6005: cannot connect to database
```
**Soluções**:
- Verifique se o servidor Oracle está acessível
- Confirme host, porta e service name
- Teste conectividade de rede

### Erro de Autenticação Sankhya
```
400 Bad Request
```
**Soluções**:
- Verifique as credenciais no arquivo `.env`
- Confirme se a AppKey está correta
- Verifique se o usuário tem permissões adequadas

### Nenhum Planejamento Encontrado
**Soluções**:
- Verifique se existem registros na tabela AD_PLAN para os parâmetros fornecidos
- Confirme se os registros não possuem IDIPROC já preenchido
- Verifique a data e formato (DD/MM/YYYY)

## Suporte

Para suporte técnico ou dúvidas sobre a aplicação:

1. Verifique os logs em `sankhya_op_automation.log`
2. Execute `python test_connections.py` para diagnosticar problemas de conectividade
3. Consulte a documentação oficial da API Sankhya
4. Entre em contato com o administrador do sistema ERP

## Licença

Esta aplicação foi desenvolvida para uso interno e automação de processos empresariais.

---

**Desenvolvido por**: Manus AI  
**Data**: 23/07/2025  
**Versão**: 1.0.0

