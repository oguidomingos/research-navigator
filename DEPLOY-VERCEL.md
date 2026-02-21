# 🚀 Deploy na Vercel - Pronto!

## ✅ Tudo Configurado!

**Credenciais já configuradas:**
- ✅ Clerk Publishable Key
- ✅ Convex URL (dev + prod)
- ✅ .env files criados
- ✅ vercel.json configurado
- ✅ App.tsx migrado para auth real

---

## 🎯 Deploy Agora (3 passos)

### 1️⃣ Commit e Push

```bash
git add .
git commit -m "feat: integrar Clerk + Convex auth real"
git push origin main
```

### 2️⃣ Importar na Vercel

1. Acesse [vercel.com/new](https://vercel.com/new)
2. Conecte seu GitHub
3. Selecione `research-navigator`
4. **NÃO clique em Deploy ainda!**

### 3️⃣ Configurar Environment Variables

Na tela de import, clique em "Environment Variables" e adicione:

#### Production:
```
VITE_CLERK_PUBLISHABLE_KEY=pk_test_cHJlY2lzZS1zYXR5ci0xMS5jbGVyay5hY2NvdW50cy5kZXYk
VITE_CONVEX_URL=https://oceanic-corgi-42.convex.cloud
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

**Pronto!** Clique em **Deploy**

---

## ⚙️ Build Settings (Já Configurado)

O `vercel.json` já tem tudo configurado:

- ✅ **Framework**: Vite
- ✅ **Build Command**: `cd frontend && npm run build`
- ✅ **Output Directory**: `frontend/dist`
- ✅ **Root Directory**: auto-detectado

---

## 🌐 Após Deploy

### 1. Copie a URL da Vercel

Exemplo: `research-navigator-abc123.vercel.app`

### 2. Adicione no Clerk

1. Acesse [dashboard.clerk.com](https://dashboard.clerk.com)
2. Vá em **Domains**
3. Adicione sua URL Vercel
4. Salve

### 3. Teste o App!

Acesse sua URL e:
- ✅ Login funciona
- ✅ Email aparece no header
- ✅ Busca funciona (se backend rodando)
- ✅ Logout funciona

---

## 🔄 Deploy Contínuo

Agora, toda vez que você fizer:

```bash
git push origin main
```

A Vercel automaticamente:
1. Detecta mudanças
2. Roda build
3. Deploy automático
4. Notifica você

---

## 🎁 URLs Importantes

Após deploy, você terá:

- **Frontend (Vercel)**: `https://research-navigator-xyz.vercel.app`
- **Convex Dev**: `https://calculating-scorpion-259.convex.cloud`
- **Convex Prod**: `https://oceanic-corgi-42.convex.cloud`
- **Clerk Dashboard**: `https://dashboard.clerk.com`

---

## 📊 Variáveis por Ambiente

| Variável | Development | Production |
|----------|-------------|------------|
| `VITE_CLERK_PUBLISHABLE_KEY` | `pk_test_...` | `pk_test_...` |
| `VITE_CONVEX_URL` | `calculating-scorpion-259` | `oceanic-corgi-42` |
| `VITE_API_BASE_URL` | `localhost:8000` | `seu-backend-prod` |

---

## 🐛 Troubleshooting

### Build falha na Vercel

```bash
# Local: testar build
cd frontend
npm run build

# Se funcionar local, o problema é env vars
```

### "Missing VITE_CLERK_PUBLISHABLE_KEY"

- Verifique que adicionou env vars na Vercel
- Redeploy manual: Vercel Dashboard → Deployments → Redeploy

### Clerk redirect error

- Adicione URL da Vercel no Clerk Dashboard → Domains
- Aguarde 1-2 minutos para propagação

---

## ✨ Está Pronto!

Seu app vai estar rodando em:
- ✅ Produção (Vercel)
- ✅ Auth real (Clerk)
- ✅ Realtime (Convex)
- ✅ Deploy contínuo (GitHub → Vercel)

**Bora fazer o deploy?** 🚀
