# 🚀 DEPLOY AGORA - 2 Minutos!

## ✅ Tudo Pronto!

- ✅ Código commitado e no GitHub
- ✅ App.tsx com Clerk auth real
- ✅ Convex configurado
- ✅ Env vars prontas
- ✅ vercel.json configurado

---

## 🎯 Opção 1: Deploy Via Web (Recomendado - 2 min)

### Passo 1: Importar Projeto

1. Acesse: **https://vercel.com/new**
2. Conecte GitHub (se ainda não conectou)
3. Selecione: `oguidomingos/research-navigator`
4. **NÃO clique em Deploy ainda!**

### Passo 2: Adicionar Environment Variables

Clique em "Environment Variables" e adicione (copie e cole):

```
VITE_CLERK_PUBLISHABLE_KEY=pk_test_cHJlY2lzZS1zYXR5ci0xMS5jbGVyay5hY2NvdW50cy5kZXYk
```

```
VITE_CONVEX_URL=https://oceanic-corgi-42.convex.cloud
```

```
VITE_API_BASE_URL=https://your-backend-url.com/api/v1
```

**Nota**: Por enquanto, use `http://localhost:8000/api/v1` como API_BASE_URL. Quando fizer deploy do backend, atualize.

### Passo 3: Build Settings

A Vercel deve detectar automaticamente:

- **Framework Preset**: Vite
- **Root Directory**: `./` (raiz)
- **Build Command**: `cd frontend && npm run build`
- **Output Directory**: `frontend/dist`

Se não detectar, configure manualmente.

### Passo 4: Deploy!

Clique em **Deploy** e aguarde ~2 minutos.

---

## 🎯 Opção 2: Deploy Via CLI (Avançado)

```bash
# Login (abre navegador)
vercel login

# Deploy
vercel --prod

# Configurar env vars quando perguntar:
# VITE_CLERK_PUBLISHABLE_KEY=pk_test_cHJlY2lzZS1zYXR5ci0xMS5jbGVyay5hY2NvdW50cy5kZXYk
# VITE_CONVEX_URL=https://oceanic-corgi-42.convex.cloud
# VITE_API_BASE_URL=http://localhost:8000/api/v1
```

---

## 📝 Após o Deploy

### 1. Copie a URL da Vercel

Exemplo: `https://research-navigator-abc123.vercel.app`

### 2. Configure Domínio no Clerk

1. Acesse: **https://dashboard.clerk.com**
2. Selecione seu app: "Research Navigator"
3. Vá em: **Domains** (menu lateral)
4. Clique em: **Add Domain**
5. Cole sua URL da Vercel
6. Salve

**Aguarde 1-2 minutos para propagação.**

### 3. Teste o App!

Acesse sua URL da Vercel e teste:

- ✅ Redireciona para `/login`
- ✅ Modal do Clerk aparece
- ✅ Consegue fazer login
- ✅ Email aparece no header
- ✅ Logout funciona

---

## 🔧 Se Algo Não Funcionar

### Erro: "Missing VITE_CLERK_PUBLISHABLE_KEY"

**Solução:**
1. Vercel Dashboard → Seu Projeto
2. Settings → Environment Variables
3. Adicione a variável
4. Deployments → Redeploy (último deploy)

### Erro: "Clerk redirect error"

**Solução:**
1. Verifique que adicionou URL no Clerk Domains
2. Aguarde 2 minutos
3. Limpe cache do navegador
4. Tente novamente

### Erro: "Convex deployment not found"

**Solução:**
1. Verifique que `VITE_CONVEX_URL` está correta
2. Deve ser: `https://oceanic-corgi-42.convex.cloud`
3. Redeploy na Vercel

---

## ✨ Deploy Contínuo

Agora configurado! Toda vez que você fizer:

```bash
git push origin main
```

A Vercel automaticamente:
1. ✅ Detecta mudanças
2. ✅ Roda build
3. ✅ Deploy automático
4. ✅ Notifica você

---

## 🎁 URLs Finais

Após deploy, você tem:

| Serviço | URL |
|---------|-----|
| **Frontend (Vercel)** | `https://research-navigator-xyz.vercel.app` |
| **Convex Dev** | `https://calculating-scorpion-259.convex.cloud` |
| **Convex Prod** | `https://oceanic-corgi-42.convex.cloud` |
| **Clerk Dashboard** | `https://dashboard.clerk.com` |
| **Vercel Dashboard** | `https://vercel.com/dashboard` |

---

## 📊 Status do Deploy

### Já Feito:
- ✅ Código commitado
- ✅ Código no GitHub
- ✅ Credenciais configuradas
- ✅ App migrado para Clerk
- ✅ Documentação completa

### Falta Fazer (você):
1. ⭕ Importar projeto na Vercel
2. ⭕ Adicionar env vars
3. ⭕ Clicar em Deploy
4. ⭕ Adicionar URL no Clerk
5. ⭕ Testar app

**Tempo total: ~3 minutos** ⏱️

---

## 🚀 Vai Lá!

Acesse agora: **https://vercel.com/new**

E em 3 minutos seu app está no ar! 🎉
