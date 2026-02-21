# ⚡ Quick Start - Research Navigator

Setup rápido para ter o app rodando localmente em **menos de 10 minutos**.

## 🎯 Pré-requisitos

- Node.js 18+ ([nodejs.org](https://nodejs.org))
- Python 3.11+ (para backend FastAPI - opcional)
- Conta no [Clerk](https://clerk.com) (gratuita)
- Conta no [Convex](https://convex.dev) (gratuita)

## 🚀 Setup em 5 Passos

### 1️⃣ Clonar e instalar dependências (2 min)

```bash
cd research-navigator

# Frontend
cd frontend
npm install
cd ..
```

### 2️⃣ Configurar Clerk (2 min)

1. Acesse [dashboard.clerk.com](https://dashboard.clerk.com)
2. Clique em "Create Application"
3. Nome: **Research Navigator**
4. Copie o **Publishable Key** (começa com `pk_test_...`)

### 3️⃣ Inicializar Convex (2 min)

```bash
# Na raiz do projeto
npx convex dev
```

Vai perguntar:
- **Login**: Use GitHub ou Google
- **Create project?**: Yes
- **Project name**: research-navigator

Copie a URL que aparece (ex: `https://amazing-cat-123.convex.cloud`)

### 4️⃣ Obter Issuer URL do Clerk (1 min)

1. No Clerk Dashboard, vá em **JWT Templates**
2. Clique em **New Template**
3. Selecione **Convex**
4. Copie o **Issuer URL** (ex: `https://your-app.clerk.accounts.dev`)

### 5️⃣ Criar arquivos de ambiente (2 min)

**Criar `frontend/.env.local`:**

```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
VITE_CONVEX_URL=https://amazing-cat-123.convex.cloud
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

**Criar `.env` na raiz:**

```env
CLERK_FRONTEND_API_URL=https://your-app.clerk.accounts.dev
```

### ✅ Pronto! Rodar o app

**Terminal 1 - Convex:**
```bash
npx convex dev
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Acesse: `http://localhost:5173` 🎉

## 🔧 Setup Backend FastAPI (Opcional)

Se quiser usar as buscas acadêmicas:

### 1️⃣ Instalar dependências

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2️⃣ Adicionar LLM key no `.env`

```env
# Escolha um:
OPENAI_API_KEY=sk-xxxxx
# OU
OPENROUTER_API_KEY=sk-or-v1-xxxxx
```

### 3️⃣ Rodar backend

```bash
# Com banco PostgreSQL
uvicorn main:app --reload

# Sem banco (modo debug)
DISABLE_DB=true uvicorn main:app --reload
```

## ✅ Verificar se funciona

1. ✅ Acessar `http://localhost:5173`
2. ✅ Clicar em "Login"
3. ✅ Modal do Clerk abre
4. ✅ Criar conta de teste
5. ✅ Após login, ver dashboard

**Se tudo funcionou, você está pronto!** 🎉

## 🐛 Problemas Comuns

### "Missing VITE_CLERK_PUBLISHABLE_KEY"

- Verifique que criou `frontend/.env.local`
- Verifique que a chave começa com `pk_test_`
- Reinicie o servidor Vite

### "Convex deployment not found"

- Verifique que `npx convex dev` está rodando
- Confirme que copiou a URL correta
- A URL deve ser HTTPS

### "Clerk: Invalid publishable key"

- Use a chave de **Test** (não Live)
- Copie novamente do dashboard
- Não adicione espaços ou quebras de linha

## 📚 Próximos Passos

1. Leia a documentação completa em `/docs`
2. Veja as credenciais necessárias em `SETUP-CREDENTIALS.md`
3. Configure o backend FastAPI para buscas
4. Deploy na Vercel (instruções em `/docs/04-deploy-vercel.md`)

## 🆘 Precisa de Ajuda?

- Documentação completa: `/docs/00-overview.md`
- Lista de credenciais: `SETUP-CREDENTIALS.md`
- Issues: [GitHub Issues](https://github.com/oguidomingos/research-navigator/issues)
