# Research Navigator - Stack Completa

## 🎯 Visão Geral

O Research Navigator é uma aplicação híbrida que combina o melhor de múltiplas tecnologias:

### Stack Tecnológica

**Frontend**
- Vite + React + TypeScript
- Clerk (autenticação SPA)
- Convex (banco realtime + backend)
- React Router (navegação)
- Lucide Icons

**Backend Principal (FastAPI)**
- FastAPI (Python 3.11)
- PostgreSQL 15 + pgvector
- Redis 7 (cache)
- Celery (processamento assíncrono)
- OpenAI/OpenRouter (LLM)

**Backend Realtime (Convex)**
- Convex (database + functions + auth)
- TypeScript
- Integração automática com Clerk

**Deploy**
- Vercel (frontend)
- Fly.io / Railway (FastAPI backend - opcional)

## 🏗️ Arquitetura Híbrida

### Por que duas backends?

**FastAPI** → Operações pesadas e específicas
- Busca paralela em 8 APIs acadêmicas
- Processamento LLM (resumos, sínteses)
- Deduplicação e ranqueamento
- Exportação de citações
- Operações que exigem Python

**Convex** → Dados do usuário e colaboração
- Coleções de artigos (salvar/organizar)
- Notas pessoais (sincronização realtime)
- Comentários colaborativos
- Compartilhamento entre pesquisadores
- Notificações e subscriptions

**Clerk** → Autenticação unificada
- Login/logout/signup
- Gerenciamento de perfil
- Organizações (equipes de pesquisa)
- JWT tokens para ambos backends

## 📊 Fluxo de Dados

```
┌─────────────┐
│   Usuário   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│   Frontend (Vite + React)       │
│                                 │
│  ┌─────────┐   ┌─────────┐    │
│  │  Clerk  │   │ Convex  │    │
│  └────┬────┘   └────┬────┘    │
└───────┼─────────────┼──────────┘
        │             │
        │             │
        ▼             ▼
   ┌────────┐   ┌──────────┐
   │ FastAPI│   │  Convex  │
   │Backend │   │  Cloud   │
   └────┬───┘   └──────────┘
        │
        ▼
   ┌─────────────────┐
   │  PostgreSQL +   │
   │  Redis + APIs   │
   └─────────────────┘
```

## 🎁 Features por Camada

### Frontend (Vite + React)
- ✅ Busca de artigos científicos
- ✅ Visualização de resultados
- ✅ Filtros dinâmicos
- ✅ Assistente IA para seleção
- ✅ Resumos rápidos (LLM)
- ✅ Síntese multi-artigos
- ✅ Dark mode
- 🆕 Login real (Clerk)
- 🆕 Sincronização realtime (Convex)

### FastAPI Backend
- ✅ Busca paralela em 8 APIs
- ✅ Deduplicação inteligente
- ✅ Ranqueamento híbrido
- ✅ Resumos com GPT-4
- ✅ Síntese de literatura
- ✅ Exportação BibTeX/APA
- 🆕 Autenticação JWT (Clerk)

### Convex Backend
- 🆕 Coleções de usuários
- 🆕 Notas pessoais (realtime)
- 🆕 Comentários colaborativos
- 🆕 Compartilhamento entre equipes
- 🆕 Notificações de atualizações
- 🆕 Analytics de uso

## 🔐 Autenticação

Clerk fornece JWT tokens que são validados por ambos backends:

1. **Frontend**: `<ClerkProvider>` + `<ConvexProviderWithClerk>`
2. **FastAPI**: Middleware JWT valida token Clerk
3. **Convex**: Integração nativa via `auth.config.js`

## 📦 O que você vai ter ao final

1. ✅ App Vite rodando localmente
2. ✅ Login/logout real com Clerk
3. ✅ Coleções sincronizadas via Convex
4. ✅ Buscas científicas via FastAPI
5. ✅ Resumos LLM funcionando
6. ✅ Deploy na Vercel pronto
7. ✅ Colaboração em tempo real
8. ✅ Offline-first com sync automático

## 📚 Próximos Passos

1. Leia `01-local-setup.md` para setup local
2. Configure Clerk + Convex
3. Atualize o frontend
4. Adicione middleware no FastAPI
5. Deploy na Vercel

## 🆘 Recursos

- [Clerk Docs](https://clerk.com/docs)
- [Convex Docs](https://docs.convex.dev)
- [Vite Docs](https://vitejs.dev)
- [FastAPI Docs](https://fastapi.tiangolo.com)
