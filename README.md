# Research Navigator - LLM App de Pesquisa Científica

Aplicação para buscar, organizar e resumir literatura científica integrando múltiplas APIs acadêmicas.

## 🎯 Funcionalidades

- **Busca Paralela** em 8 APIs acadêmicas (OpenAlex, Semantic Scholar, CORE, PubMed, Europe PMC, Crossref, arXiv, BASE)
- **Deduplicação Inteligente** de resultados por DOI e assinatura (título + autores + ano)
- **Rankeamento Híbrido** (relevância, recência, citações)
- **Resumos com LLM** (OpenAI GPT-4) com extração de objetivos, metodologia, resultados, limitações
- **Síntese Multi-artigos** para revisões de literatura
- **Coleções Personalizadas** para organizar artigos
- **Exportação** em BibTeX, APA, ABNT
- **API REST** completa com FastAPI

## 🛠️ Stack Tecnológico

- **Backend**: FastAPI (Python 3.11)
- **Banco de dados**: PostgreSQL 15 + pgvector (embeddings)
- **Cache**: Redis 7
- **Processamento**: Celery + Redis Queue
- **LLM**: OpenAI GPT-4 (configurável)
- **Auth**: OAuth2 (integrado com portal do aluno)

## 📚 APIs Integradas

| API | Cobertura | Rate Limits (grátis) |
|-----|-----------|---------------------|
| OpenAlex | >450M works | $1/dia (~10k reqs) |
| Semantic Scholar | >250M papers | 1 req/s (com key) |
| CORE | >300M full-texts | Limites razoáveis |
| PubMed | >35M biomédico | Alto limite |
| Europe PMC | >40M biomédico | Limites generosos |
| Crossref | >170M DOIs | Milhares/dia |
| arXiv | >2M preprints | Muito generoso |
| BASE | >300M docs | OAI-PMH |

## 🚀 Quick Start

### Com Docker (Recomendado)

```bash
# Clone o repositório
git clone https://github.com/oguidomingos/research-navigator.git
cd research-navigator

# Configure as variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves de API

# Inicie os serviços
docker-compose up -d

# Acesse a API
open http://localhost:8000/docs
```

Atalho:

```bash
./scripts/dev-up.sh
```

### Sem Docker

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure o banco PostgreSQL e Redis
# Edite .env com suas configurações

# Execute as migrations
alembic upgrade head

# Inicie o servidor
uvicorn main:app --reload
```

## 📖 Documentação da API

Acesse `/docs` para Swagger UI ou `/redoc` para ReDoc.

### Endpoints Principais

- `POST /api/v1/search/articles` - Buscar artigos
- `GET /api/v1/articles/{id}` - Obter artigo por ID
- `POST /api/v1/articles/{id}/cite` - Gerar citação
- `GET /api/v1/collections` - Listar coleções
- `POST /api/v1/collections` - Criar coleção
- `POST /api/v1/collections/{id}/articles` - Adicionar artigos à coleção
- `POST /api/v1/summary/article` - Gerar resumo de artigo
- `POST /api/v1/summary/collection` - Gerar síntese de coleção
- `POST /api/v1/export` - Exportar citações

## 📁 Estrutura do Projeto

```
research-navigator/
├── backend/
│   ├── app/
│   │   ├── api_clients/      # Clientes para APIs externas
│   │   ├── api/              # Endpoints FastAPI
│   │   ├── core/             # Configuração e database
│   │   ├── models/           # Modelos SQLAlchemy
│   │   ├── schemas/          # Schemas Pydantic
│   │   └── services/         # Lógica de negócio
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                 # Next.js (em desenvolvimento)
├── docker-compose.yml
└── README.md
```

## 🔧 Configuração

### Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `DATABASE_URL` | URL do PostgreSQL (async) | Sim |
| `REDIS_URL` | URL do Redis | Sim |
| `OPENAI_API_KEY` | Chave da OpenAI | Sim |
| `OPENALEX_API_KEY` | Chave do OpenAlex | Não |
| `SEMANTIC_SCHOLAR_API_KEY` | Chave do Semantic Scholar | Não |
| `CORE_API_KEY` | Chave do CORE | Não |
| `SECRET_KEY` | Chave secreta para JWT | Sim |

## 🧪 Testes

```bash
cd backend
pytest
```

## 📝 Licença

Proprietário - Instituto IIBPR
