# Sankhya Automation - Automação de Ordens de Produção

Esta aplicação Python automatiza a criação de Ordens de Produção (OPs) no sistema ERP Sankhya. A aplicação lê dados de planejamento de um banco de dados Oracle e, para cada item, cria a respectiva Ordem de Produção via API, atualizando o banco com o número da OP criada.

## Funcionalidades

- **Interface Web Intuitiva**: Coleta parâmetros e exibe o progresso em tempo real.
- **Conexão com Oracle**: Consulta planejamentos pendentes na tabela `AD_PLAN`.
- **Integração com API Sankhya**: Autenticação e criação de OPs via API REST.
- **Processamento em Lote**: Processa múltiplas "rodadas" de produção de forma sequencial.
- **Monitoramento e Relatórios**: Exibe logs, progresso e um resumo final com sucessos e falhas.

## Instalação

1.  **Instalar dependências Python:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configurar Variáveis de Ambiente:**
    - Copie o arquivo `.env.example` para `.env`.
    - Preencha o arquivo `.env` com as credenciais corretas para o banco de dados Oracle e a API Sankhya.

## Execução

Para iniciar o servidor web da aplicação, execute:

```bash
python main.py

sankhya_automation_app/
├── main.py                 # Aplicação Flask principal
├── requirements.txt        # Dependências Python
├── static/                 # Frontend (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── sankhya_script.js
└── sankhya_automation/     # Módulos de backend
    ├── database.py         # Conexão com Oracle
    ├── sankhya_api.py      # API do Sankhya
    ├── config.py           # Carregamento de configurações
    ├── database_mock.py    # Mock para testes sem Oracle
    └── sankhya_api_mock.py # Mock para testes sem API}

    APIs Disponíveis
POST /api/sankhya/verificar_conexoes: Verifica a conectividade com o Oracle e a API Sankhya.
POST /api/sankhya/buscar_planejamentos: Conta quantos planejamentos estão pendentes para os parâmetros informados.
POST /api/sankhya/processar_rodada: Processa uma única rodada de produção.
POST /api/sankhya/finalizar_conexoes: Realiza o logout da sessão da API.
GET /api/sankhya/resumo: Retorna o resumo da última execução.

### Conclusão
