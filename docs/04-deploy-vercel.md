# Deploy na Vercel

## 🎯 Objetivo

Deploy do frontend na Vercel com variáveis de ambiente corretas.

## 📋 Pré-requisitos

- Conta no [Vercel](https://vercel.com)
- Repositório GitHub conectado
- Clerk em produção (chaves `pk_live_...`)
- Convex em produção (deployment prod)

## 🚀 Passo a Passo

### 1. Criar deployment de produção no Convex

```bash
# Na raiz do projeto
npx convex deploy

# Isso vai:
# 1. Criar deployment de produção
# 2. Aplicar schema e funções
# 3. Retornar URL de produção
```

Exemplo de output:

```
✔ Deployment created: https://amazing-cat-456.convex.cloud
✔ Schema synced
✔ Functions deployed
```

**⚠️ Copie a URL de produção!**

### 2. Configurar Clerk para produção

No Clerk Dashboard:

1. Vá em **Domains** (menu lateral)
2. Adicione seu domínio da Vercel:
   - `your-app.vercel.app` (ou custom domain)

3. Vá em **API Keys**
4. Copie as chaves de **Production**:
   - `Publishable Key` (começa com `pk_live_...`)
   - `Secret Key` (começa com `sk_live_...`)

5. Vá em **JWT Templates**
6. Edite o template **Convex**
7. Copie o **Issuer URL** de produção

### 3. Importar projeto na Vercel

1. Acesse [vercel.com/new](https://vercel.com/new)
2. Conecte seu repositório GitHub
3. Selecione o repositório `research-navigator`

### 4. Configurar Build Settings

Na tela de import:

- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### 5. Adicionar Environment Variables

Clique em **Environment Variables** e adicione:

#### Produção (Production)

```env
VITE_CLERK_PUBLISHABLE_KEY=pk_live_xxxxx
VITE_CONVEX_URL=https://amazing-cat-456.convex.cloud
VITE_API_BASE_URL=https://your-fastapi-backend.com/api/v1
```

#### Preview (opcional - para branches)

```env
VITE_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
VITE_CONVEX_URL=https://amazing-cat-123.convex.cloud
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 6. Deploy!

Clique em **Deploy** e aguarde.

Vercel vai:
1. ✅ Clonar o repositório
2. ✅ Instalar dependências
3. ✅ Rodar build do Vite
4. ✅ Deploy do `dist/`
5. ✅ Gerar URL única

### 7. Configurar domínio no Clerk (após deploy)

Após o deploy finalizar, copie a URL da Vercel (ex: `your-app.vercel.app`).

No Clerk Dashboard:

1. Vá em **Domains**
2. Adicione:
   - Production URL: `https://your-app.vercel.app`
   - Development URL: `http://localhost:5173` (já deve estar)

3. Salve e aguarde propagação (1-2 min)

### 8. Atualizar variáveis no Convex (produção)

No Convex Dashboard (deployment de produção):

1. Vá em **Settings** → **Environment Variables**
2. Adicione:

```env
CLERK_FRONTEND_API_URL=https://your-app.clerk.accounts.dev
```

3. Salve e aguarde restart automático

## ✅ Verificar Deploy

1. Acesse sua URL da Vercel
2. Deve redirecionar para `/login`
3. Teste login com Clerk
4. Verifique que consegue:
   - Fazer buscas (se backend estiver rodando)
   - Salvar artigos (Convex)
   - Ver coleções (Convex)

## 🐛 Troubleshooting

### Erro: "Clerk: Invalid publishable key"

- Verifique que está usando `pk_live_...` (não `pk_test_`)
- Confirme que a variável está em **Production** no Vercel
- Redeploy: `vercel --prod`

### Erro: "Failed to fetch convex functions"

- Verifique que `VITE_CONVEX_URL` é HTTPS
- Confirme que deployment Convex está ativo
- Verifique que `CLERK_FRONTEND_API_URL` está no Convex (prod)

### Erro: CORS na busca de artigos

- Verifique que FastAPI permite origem da Vercel
- Adicione no backend `CORS_ORIGINS`:

```python
# backend/app/core/config.py
CORS_ORIGINS = [
    "http://localhost:5173",
    "https://your-app.vercel.app",  # 🆕 Adicionar
]
```

### Build falha na Vercel

- Verifique que `Root Directory` é `frontend`
- Confirme que todas as env vars estão definidas
- Veja logs detalhados no dashboard Vercel

## 🔄 Deploy Contínuo

Toda vez que você fizer push para `main`:

1. Vercel detecta automaticamente
2. Roda build
3. Deploy automático
4. Notificação no Slack/Discord (configurável)

Para branches (preview):

1. Crie branch: `git checkout -b feature/nova-feature`
2. Commit e push: `git push origin feature/nova-feature`
3. Vercel cria preview automático
4. URL única gerada

## 🌐 Custom Domain (opcional)

1. Compre domínio (Namecheap, Google Domains, etc)
2. No Vercel:
   - Vá em **Settings** → **Domains**
   - Adicione seu domínio
   - Siga instruções DNS
3. No Clerk:
   - Atualize **Domains** com domínio custom

## 📊 Monitoramento

Vercel fornece:

- **Analytics**: Pageviews, usuários únicos
- **Speed Insights**: Core Web Vitals
- **Logs**: Runtime logs (serverless functions)

Acesse em: `https://vercel.com/your-team/your-app/analytics`

## 🎁 Recursos Extras da Vercel

- **Preview Deployments**: Toda branch gera preview
- **Rollback**: Voltar para deploy anterior com 1 clique
- **Environment Variables**: Por ambiente (prod/preview/dev)
- **Edge Functions**: Serverless no edge (opcional)

## ✅ Próximo Passo

Leia `05-checklist.md` para checklist final de verificação.
