# 🚀 Como Rodar o App - Research Navigator

## ✅ Setup Completo!

Todas as credenciais foram configuradas:
- ✅ Clerk: Autenticação configurada
- ✅ Convex: URLs configuradas (dev + prod)
- ✅ OpenRouter: API key configurada
- ✅ Dependências instaladas

---

## 🎯 Rodar Local (3 passos)

### 1️⃣ Terminal 1 - Convex Backend

```bash
npx convex dev
```

**Aguarde ver:**
```
✔ Deployment URL: https://calculating-scorpion-259.convex.cloud
✔ Watching for file changes in convex/
```

### 2️⃣ Terminal 2 - Frontend Vite

```bash
cd frontend
npm run dev
```

**Aguarde ver:**
```
  VITE ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

### 3️⃣ Terminal 3 - Backend FastAPI (Opcional)

```bash
cd backend
source venv/bin/activate  # ou .venv/bin/activate
uvicorn main:app --reload
```

**Se não tiver venv:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🌐 Acessar o App

1. Abra: **http://localhost:5173**
2. Clique em "Login"
3. Modal do Clerk abre
4. Crie uma conta de teste ou faça login
5. Pronto! ✨

---

## ✅ Verificar se Funcionou

### Clerk (Auth) ✓
- [ ] Modal de login aparece
- [ ] Consegue criar conta
- [ ] Após login, redireciona para dashboard
- [ ] Email aparece no header

### Convex (Realtime) ✓
- [ ] `npx convex dev` rodando sem erros
- [ ] Console do navegador sem erros de Convex

### FastAPI (Buscas) ✓
- [ ] Backend rodando em http://localhost:8000
- [ ] Pode fazer buscas de artigos
- [ ] Resumos LLM funcionam

---

## 🐛 Problemas Comuns

### "Missing VITE_CLERK_PUBLISHABLE_KEY"

**Solução:**
```bash
# Verifique que o arquivo existe
cat frontend/.env.local

# Se não existir, foi criado! Reinicie o Vite:
cd frontend
npm run dev
```

### "Convex deployment not found"

**Solução:**
```bash
# Verifique que convex está rodando
npx convex dev

# Aguarde mensagem de sucesso
```

### "Failed to fetch"

**Solução:**
- Verifique que TODOS os 3 terminais estão rodando
- Backend FastAPI em http://localhost:8000
- Frontend em http://localhost:5173
- Convex em background

---

## 🎁 Features Disponíveis

### ✅ Funcionando Agora:
- Login/Logout com Clerk
- Busca de artigos (8 APIs)
- Filtros dinâmicos
- Resumos rápidos (LLM)
- Síntese multi-artigos
- Dark mode
- Assistente IA de seleção

### 🔄 Convex (Realtime):
Para usar as features Convex, você precisa:
1. Migrar coleções do localStorage para Convex
2. Ver guia em `/docs/06-app-tsx-migration.md`

---

## 📱 Próximos Passos

### Hoje:
1. ✅ Testar login
2. ✅ Fazer uma busca de artigo
3. ✅ Salvar artigos (localStorage por enquanto)
4. ✅ Testar resumo LLM

### Amanhã:
1. Migrar App.tsx (seguir `/docs/06-app-tsx-migration.md`)
2. Implementar coleções Convex (realtime)
3. Adicionar notas sincronizadas

### Semana que vem:
1. Deploy na Vercel (seguir `/docs/04-deploy-vercel.md`)
2. Configurar domínio custom (opcional)

---

## 🔧 Comandos Úteis

### Parar tudo:
```bash
# Ctrl+C em cada terminal
```

### Limpar e reiniciar:
```bash
# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev

# Convex
npx convex dev --once  # Força resync
```

### Ver logs Convex:
```bash
npx convex logs
```

---

## 📊 URLs Importantes

- **Frontend**: http://localhost:5173
- **Backend FastAPI**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **Convex Dev**: https://calculating-scorpion-259.convex.cloud
- **Convex Prod**: https://oceanic-corgi-42.convex.cloud
- **Clerk Dashboard**: https://dashboard.clerk.com

---

## 🆘 Precisa de Ajuda?

1. **Documentação**: Leia `/docs/00-overview.md`
2. **Setup**: Veja `QUICKSTART.md`
3. **App.tsx**: Veja `/docs/06-app-tsx-migration.md`
4. **Deploy**: Veja `/docs/04-deploy-vercel.md`

---

## ✨ Está Tudo Pronto!

Você tem:
- ✅ Credenciais configuradas
- ✅ Dependências instaladas
- ✅ Arquivos .env criados
- ✅ Convex sincronizado
- ✅ Backend rodando

**Só executar os 3 comandos acima e começar a usar!** 🎉
