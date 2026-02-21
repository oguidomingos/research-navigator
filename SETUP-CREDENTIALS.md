# 🔑 Credenciais Necessárias - Research Navigator

Este arquivo lista todas as credenciais que você precisa fornecer para o setup completo.

## 📋 Checklist de Credenciais

### 1. Clerk (Autenticação)

Criar conta em [clerk.com](https://clerk.com) e obter:

#### Development (Local)
- ✅ **VITE_CLERK_PUBLISHABLE_KEY** (frontend)
  - Formato: `pk_test_...`
  - Onde: Clerk Dashboard → API Keys → Publishable Key (Test)
  - Arquivo: `frontend/.env.local`

- ✅ **CLERK_SECRET_KEY** (backend)
  - Formato: `sk_test_...`
  - Onde: Clerk Dashboard → API Keys → Secret Key (Test)
  - Arquivo: `.env` (raiz do projeto)

- ✅ **CLERK_FRONTEND_API_URL**
  - Formato: `https://your-app.clerk.accounts.dev`
  - Onde: Clerk Dashboard → JWT Templates → Convex → Issuer
  - Arquivo: `.env` (raiz do projeto)

- ✅ **CLERK_JWKS_URL**
  - Formato: `https://your-app.clerk.accounts.dev/.well-known/jwks.json`
  - Construído a partir do CLERK_FRONTEND_API_URL
  - Arquivo: `.env` (raiz do projeto)

#### Production (Vercel)
- ✅ **VITE_CLERK_PUBLISHABLE_KEY** (produção)
  - Formato: `pk_live_...`
  - Onde: Clerk Dashboard → API Keys → Publishable Key (Live)
  - Onde configurar: Vercel → Project Settings → Environment Variables

- ✅ **CLERK_SECRET_KEY** (produção - se houver backend)
  - Formato: `sk_live_...`
  - Onde: Clerk Dashboard → API Keys → Secret Key (Live)

---

### 2. Convex (Backend Realtime)

Inicializar com `npx convex dev`:

#### Development (Local)
- ✅ **VITE_CONVEX_URL**
  - Formato: `https://amazing-cat-123.convex.cloud`
  - Gerado automaticamente após `npx convex dev`
  - Arquivo: `frontend/.env.local`

#### Production (Vercel)
- ✅ **VITE_CONVEX_URL** (produção)
  - Formato: `https://amazing-cat-456.convex.cloud`
  - Gerado após `npx convex deploy`
  - Onde configurar: Vercel → Project Settings → Environment Variables

- ✅ **CONVEX_DEPLOY_KEY** (opcional - CI/CD)
  - Para deploy automático via GitHub Actions
  - Onde: Convex Dashboard → Settings → Deploy Keys

---

### 3. FastAPI Backend (Opcional)

#### LLM (OpenAI ou OpenRouter)
- ✅ **OPENAI_API_KEY**
  - Formato: `sk-...`
  - Onde: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
  - Arquivo: `.env` (raiz do projeto)

**OU**

- ✅ **OPENROUTER_API_KEY**
  - Formato: `sk-or-v1-...`
  - Onde: [openrouter.ai/keys](https://openrouter.ai/keys)
  - Arquivo: `.env` (raiz do projeto)

#### API Keys Acadêmicas (Opcionais - melhoram rate limits)
- ⭕ **OPENALEX_API_KEY**
  - Onde: [openalex.org](https://openalex.org)
  - Gratuito

- ⭕ **SEMANTIC_SCHOLAR_API_KEY**
  - Onde: [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api)
  - Gratuito

- ⭕ **CORE_API_KEY**
  - Onde: [core.ac.uk/services/api](https://core.ac.uk/services/api)
  - Gratuito

---

### 4. Vercel (Deploy Frontend)

#### Development
- ✅ **VITE_API_BASE_URL**
  - Valor: `http://localhost:8000/api/v1`
  - Arquivo: `frontend/.env.local`

#### Production
- ✅ **VITE_API_BASE_URL** (produção)
  - Valor: URL do seu backend (ex: `https://your-backend.fly.dev/api/v1`)
  - Onde configurar: Vercel → Project Settings → Environment Variables

---

## 📝 Resumo dos Arquivos de Configuração

### `frontend/.env.local` (criar manualmente)

```env
# Clerk (Development)
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx

# Convex (Development)
VITE_CONVEX_URL=https://amazing-cat-123.convex.cloud

# FastAPI Backend (Local)
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### `.env` na raiz (criar manualmente)

```env
# Clerk (Backend + Convex)
CLERK_FRONTEND_API_URL=https://your-app.clerk.accounts.dev
CLERK_JWKS_URL=https://your-app.clerk.accounts.dev/.well-known/jwks.json
CLERK_SECRET_KEY=sk_test_xxxxx

# LLM (escolha um)
OPENAI_API_KEY=sk-xxxxx
# OU
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# Banco de dados (se usar PostgreSQL local)
DB_USER=research
DB_PASSWORD=research123
DB_NAME=research_navigator
```

---

## 🚀 Ordem de Setup Recomendada

1. **Clerk** (primeiro)
   - Criar conta
   - Criar aplicação
   - Copiar chaves de teste

2. **Convex** (segundo)
   - Rodar `npx convex dev`
   - Copiar URL gerada
   - Adicionar `CLERK_FRONTEND_API_URL` no `.env`

3. **Frontend** (terceiro)
   - Criar `frontend/.env.local`
   - Adicionar as 3 variáveis
   - Rodar `npm install && npm run dev`

4. **Backend FastAPI** (quarto - opcional)
   - Adicionar LLM key no `.env`
   - Rodar backend

5. **Vercel** (quinto - deploy)
   - Importar projeto
   - Adicionar env vars de produção
   - Deploy!

---

## ❓ Onde Encontrar Cada Credencial?

### Clerk Dashboard
- URL: [dashboard.clerk.com](https://dashboard.clerk.com)
- **API Keys**: Menu lateral → API Keys
- **JWT Templates**: Menu lateral → JWT Templates → Convex

### Convex Dashboard
- URL: Mostrado no terminal após `npx convex dev`
- **Deployment URL**: Página inicial do dashboard
- **Deploy Keys**: Settings → Deploy Keys

### Vercel Dashboard
- URL: [vercel.com](https://vercel.com)
- **Environment Variables**: Project Settings → Environment Variables

---

## 🔒 Segurança

- **NUNCA** commitar `.env` ou `.env.local`
- **NUNCA** compartilhar Secret Keys
- **SEMPRE** usar chaves de teste em desenvolvimento
- **SEMPRE** usar chaves de produção apenas no deploy

---

## 📞 Precisa de Ajuda?

Se tiver dúvidas sobre alguma credencial:

1. Consulte a documentação em `/docs`
2. Veja o arquivo correspondente em `.env.example`
3. Verifique a dashboard do serviço específico

**Principais documentações:**
- Clerk: [clerk.com/docs](https://clerk.com/docs)
- Convex: [docs.convex.dev](https://docs.convex.dev)
- Vercel: [vercel.com/docs](https://vercel.com/docs)
