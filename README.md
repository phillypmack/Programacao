# Sankhya Automation - Automação de Ordens de Produção

Esta aplicação automatiza a criação de Ordens de Produção (OPs) no sistema ERP Sankhya, centralizando o processo de planejamento e execução de produção a partir de dados extraídos de um banco de dados Oracle. Com interface web intuitiva, integração robusta com APIs e monitoramento detalhado, o sistema visa agilidade, rastreabilidade e confiabilidade para operações industriais.

---

## 🚀 Principais Funcionalidades

- **Interface Web Intuitiva:** Coleta parâmetros do usuário e exibe progresso em tempo real.
- **Conexão e Consulta Oracle:** Busca planejamentos pendentes na tabela `AD_PLAN` com filtros dinâmicos.
- **Integração com API Sankhya:** Autenticação, criação e atualização de OPs via API REST.
- **Processamento em Lote:** Processa múltiplas rodadas de produção de maneira sequencial e segura.
- **Monitoramento & Relatórios:** Exibe logs, progresso detalhado e resumo final com sucessos e falhas.
- **Mock para Testes:** Suporte a ambientes de teste sem dependências externas reais.

---

## 🏗️ Estrutura do Projeto

```
programacao/
├── main.py                     # Aplicação Flask principal
├── requirements.txt            # Dependências Python
├── static/                     # Frontend (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── sankhya_script.js
├── sankhya_automation/         # Módulos de backend
│   ├── database.py             # Conexão com Oracle
│   ├── sankhya_api.py          # API do Sankhya
│   ├── config.py               # Carregamento de configurações
│   ├── database_mock.py        # Mock para testes sem Oracle
│   └── sankhya_api_mock.py     # Mock para testes sem API
├── .env.example                # Exemplo de arquivo de configuração
└── README.md
```

---

## ⚙️ Instalação

1. **Clone o repositório e acesse a pasta:**
   ```bash
   git clone https://github.com/phillypmack/programacao.git
   cd programacao
   ```

2. **Instale as dependências Python:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as credenciais corretas para o banco Oracle e API Sankhya

   ```bash
   cp .env.example .env
   # edite o arquivo .env conforme seu ambiente
   ```

---

## ▶️ Execução

Para iniciar o servidor web da aplicação:
```bash
python main.py
```

Acesse `http://localhost:5000` no navegador para utilizar a interface web.

---

## 🔌 APIs Disponíveis

- `POST /api/sankhya/verificar_conexoes` – Verifica conectividade com Oracle e API Sankhya.
- `POST /api/sankhya/buscar_planejamentos` – Conta planejamentos pendentes de acordo com filtros.
- `POST /api/sankhya/processar_rodada` – Processa uma rodada de produção.
- `POST /api/sankhya/finalizar_conexoes` – Logout da sessão API.
- `GET /api/sankhya/resumo` – Retorna resumo da última execução.

---

## 💡 Fluxo de Funcionamento

1. **Coleta de parâmetros:** Usuário informa data, braço e rodada.
2. **Verificação de conexões:** Teste de conectividade Oracle e Sankhya.
3. **Consulta:** Busca registros pendentes na tabela AD_PLAN.
4. **Processamento:** Para cada item:
    - Autentica na API Sankhya
    - Cria Ordem de Produção
    - Atualiza banco Oracle com ID da OP criada
5. **Relatório:** Mostra resumo de OPs criadas, falhas e logs detalhados.

---

## 🛠️ Requisitos

- Python 3.11+
- Banco de dados Oracle acessível
- API Sankhya disponível e credenciais válidas

### Dependências principais:
- `requests`
- `sqlalchemy`
- `oracledb`
- `python-dotenv`
- `flask`

---

## 📝 Exemplo de Uso

1. Acesse a interface web, informe parâmetros requisitados (data, braço, rodada).
2. Clique em "Processar" e acompanhe o progresso em tempo real.
3. Ao final, consulte o resumo das OPs processadas e eventuais erros.

---

## 🔒 Segurança

- Nunca armazene credenciais diretamente no código.
- Use o arquivo `.env` (não versionado) para configurações sensíveis.
- Garanta permissões adequadas no usuário Sankhya e Oracle.

---

## 🧰 Solução de Problemas

- **Erro de conexão com Oracle:** Verifique host, porta, service name e rede.
- **Erro de autenticação Sankhya:** Revise credenciais e permissões no `.env`.
- **Nenhum planejamento encontrado:** Confirme filtros e se há registros pendentes.

Consulte os logs detalhados (`sankhya_op_automation.log`) para diagnóstico.

---

## 🤝 Suporte

- Execute `python test_connections.py` para diagnosticar conectividade.
- Consulte a documentação oficial da API Sankhya.
- Entre em contato com o administrador do sistema ERP, se necessário.

---

## 🏷️ Licença

Aplicação para uso interno e automação de processos empresariais.

---

**Desenvolvido por:** phillypmack  
**Inteligrncia artifical da estruruta** Manus AI
**Insteligencia artificial de refinamento** Gemini AI
**Data:** 23/07/2025  
**Versão:** 1.0.0