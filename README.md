# 📊 Teste Técnico - API de Atos da RFB

API backend para coleta automatizada (web scraping), persistência e disponibilização de atos normativos da Receita Federal, com autenticação JWT e arquitetura orientada a serviços.

---

## 🚀 Tecnologias Utilizadas

- Python 3.12+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Requests-HTML / BeautifulSoup (Web Scraping)
- JWT (Autenticação)
- Docker + Docker Compose
- Pytest (Testes automatizados)

---

## 📌 Funcionalidades

### 🔎 Web Scraping
- Extração de atos normativos diretamente do site da Receita Federal
- Tratamento e normalização dos dados

### 🗄️ Banco de Dados
- Persistência em PostgreSQL (produção via Docker)
- Estrutura relacional com SQLAlchemy

### 🔐 Autenticação
- Registro de usuário
- Login com geração de token JWT
- Proteção de endpoints sensíveis

### 🔁 CRUD de Atos
- Criar ato
- Listar atos com filtros
- Buscar ato por ID
- Atualizar ato
- Excluir ato (soft delete)

### 📊 Dashboard
- Total de registros
- Agrupamento por tipo de ato
- Agrupamento por órgão

### ⚙️ RPA (Automação)
- Endpoint para disparar scraping manualmente
- Inserção em massa no banco

### 🧪 Testes Automatizados
- Testes com Pytest
- Banco isolado com SQLite para testes

---

## 🗂️ Estrutura do Projeto

```bash
.
├── api/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── templates/
│   ├── v1/
│   │   └── endpoints/
│   ├── main.py
│   ├── security.py
│   └── services.py
│
├── infra/
│   └── config.py
│
├── rpa/
│   ├── utils/
│   │   ├── fetch.py
│   │   ├── parse.py
│   │   └── get_dates.py
│   └── web/
│       └── scraper.py
│
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🐳 Como Executar com Docker

### Pré-requisitos:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Passos:
1. Clone o repositório:
```bash
git clone https://github.com/Cesar-hash/Teste_Tecnico-Desenvolvedor_Backend.git
cd Teste_Tecnico-Desenvolvedor_Backend
```

2. Suba os containers:
```bash
docker-compose up -d --build
```

3. Acessar a API
👉 Swagger: http://localhost:8000/docs
👉 Login page: http://localhost:8000/api/v1/web/login

---

## 📄 Uso da API
- Documentação Interativa (Swagger): Após iniciar a aplicação, acesse `http://localhost:8000/docs` para ver todos os endpoints disponíveis, seus parâmetros e testá-los em tempo real.

### 🔐 Autenticação (Passo a passo)
- A API utiliza autenticação baseada em JWT para proteger endpoints sensíveis.

1. Criar usuário
    * POST /api/v1/auth/register
    ```json
            {
            "username": "admin",
            "password": "1234"
            }
    ```

2. Fazer login
    * POST /api/v1/auth/login
    Retorno:
    ```json
            {
            "access_token": "...",
            "token_type": "bearer"
            }
    ```

3. Autorizar no Swagger
    * Clique em Authorize
    * Cole:
        Bearer SEU_TOKEN

### 📡 Principais Endpoints
- Web
    * GET /api/v1/web/login
    * GET /api/v1/web/atos
    * GET /api/v1/web/dashboard

- Atos
    * POST /api/v1/atos/
    * GET /api/v1/atos/
    * GET /api/v1/atos/{id}
    * PUT /api/v1/atos/{id}
    * DELETE /api/v1/atos/{id}

- Dashboard
    * GET /api/v1/dashboard/    

- RPA (Executa o scraping e persiste os dados no banco)
    * POST /api/v1/rpa/trigger-extraction

### 🔎 Filtros disponíveis
* GET /api/v1/atos/?search=RFB&data_publicacao=2026-04-22

---

## 🧪 Executando os Testes
```bash
pytest -q
```
Resultado esperado:
```bash
4 passed
```

---

## 🌟 Diferenciais

- Arquitetura em camadas (API, serviços, RPA)
- Autenticação JWT com proteção de endpoints
- Web scraping integrado à API
- Testes automatizados com banco isolado (SQLite)
- Containerização completa com Docker
- Logs estruturados para rastreabilidade
