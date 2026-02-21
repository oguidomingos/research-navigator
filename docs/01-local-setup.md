# Setup Local - Clerk + Convex + Vite

## 📋 Pré-requisitos

- Node.js 18+ (LTS recomendado)
- Python 3.11+ (para backend FastAPI)
- Conta no [Clerk](https://clerk.com)
- Conta no [Convex](https://convex.dev)

## 🚀 Passo a Passo

### 1. Clonar e instalar dependências

```bash
cd research-navigator/frontend
npm install
```

### 2. Criar aplicação no Clerk

1. Acesse [dashboard.clerk.com](https://dashboard.clerk.com)
2. Clique em "Create Application"
3. Nome: **Research Navigator**
4. Ative os providers desejados:
   - Email + Password
   - Google (opcional)
   - GitHub (opcional)

5. **Copie as credenciais**:
   - `Publishable Key` (começa com `pk_test_...`)
   - `Secret Key` (começa com `sk_test_...`)

### 3. Inicializar Convex

No diretório raiz do projeto:

```bash
npx convex dev
```

Isso vai:
- Pedir login (use GitHub ou outra opção)
- Criar um novo projeto Convex
- Criar a pasta `convex/` na raiz
- Gerar `VITE_CONVEX_URL` automaticamente

**⚠️ Importante**: O comando vai perguntar algumas coisas:
- "Create a new project?": **Yes**
- "Project name": **research-navigator**
- "Production deployment?": **No** (primeiro vamos testar local)

Após finalizar, você verá no terminal algo como:

```
✔ Created convex/ directory
✔ Deployment URL: https://amazing-cat-123.convex.cloud
```

Copie essa URL, você vai precisar dela!

### 4. Configurar integração Clerk ↔ Convex

No Clerk Dashboard:

1. Vá em **JWT Templates** (menu lateral)
2. Clique em **New Template**
3. Selecione **Convex** (template pré-configurado)
4. Clique em **Create**
5. Copie o **Issuer URL** (algo como `https://your-app.clerk.accounts.dev`)

Esse é o `CLERK_FRONTEND_API_URL` que você vai usar.

### 5. Criar arquivo `.env.local` no frontend

```bash
cd frontend
touch .env.local
```

Adicione:

```env
# Clerk (pegar no dashboard.clerk.com)
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...

# Convex (gerado após npx convex dev)
VITE_CONVEX_URL=https://amazing-cat-123.convex.cloud
```

### 6. Criar arquivo `.env` na raiz (para Convex backend)

```bash
cd ..  # voltar para raiz
touch .env
```

Adicione:

```env
# Clerk Frontend API URL (para Convex validar JWT)
CLERK_FRONTEND_API_URL=https://your-app.clerk.accounts.dev
```

### 7. Configurar autenticação no Convex

Crie o arquivo `convex/auth.config.js`:

```javascript
export default {
  providers: [
    {
      domain: process.env.CLERK_FRONTEND_API_URL,
      applicationID: "convex",
    },
  ],
};
```

O `npx convex dev` vai detectar automaticamente e sincronizar.

### 8. Testar instalação

**Terminal 1** - Convex (deixe rodando):
```bash
npx convex dev
```

**Terminal 2** - Frontend:
```bash
cd frontend
npm run dev
```

Acesse `http://localhost:5173` e teste o login!

## 🔍 Verificar se está funcionando

### Checklist Local:

- [ ] `npx convex dev` rodando sem erros
- [ ] Frontend abre em `http://localhost:5173`
- [ ] Botão de login aparece
- [ ] Ao clicar em login, modal do Clerk abre
- [ ] Após login, mostra email do usuário
- [ ] Console do navegador sem erros de CORS

## 🐛 Troubleshooting

### Erro: "Missing VITE_CLERK_PUBLISHABLE_KEY"

- Verifique que o arquivo `frontend/.env.local` existe
- Verifique que a variável começa com `VITE_`
- Reinicie o servidor Vite (`npm run dev`)

### Erro: "Clerk: Invalid publishable key"

- Confirme que copiou a chave correta do dashboard
- Use a chave de **test** (começa com `pk_test_`)
- Não use a chave de produção ainda

### Erro: "Convex deployment not found"

- Verifique que `npx convex dev` está rodando
- Confirme que `VITE_CONVEX_URL` está em `.env.local`
- A URL deve ser HTTPS (não HTTP)

### Erro: "Failed to fetch convex functions"

- Verifique que `convex/auth.config.js` existe
- Confirme que `CLERK_FRONTEND_API_URL` está no `.env` da raiz
- Rode `npx convex dev --once` para forçar sync

## 📝 Estrutura de Arquivos Esperada

```
research-navigator/
├── .env                          # Convex env vars
├── .env.example
├── convex/
│   ├── auth.config.js           # 🆕 Config Clerk
│   ├── schema.ts                # 🆕 (próximo passo)
│   └── _generated/              # Auto-gerado
├── frontend/
│   ├── .env.local               # 🆕 Clerk + Convex URLs
│   ├── .env.example
│   └── src/
│       ├── main.tsx             # 🆕 (atualizar com providers)
│       └── ...
└── backend/                      # FastAPI (inalterado)
```

## ✅ Próximo Passo

Leia `02-convex-backend.md` para criar o schema e funções Convex.
