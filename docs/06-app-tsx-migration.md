# Migração do App.tsx para Clerk + Convex

Este documento explica as mudanças necessárias no `frontend/src/App.tsx` para integrar Clerk (autenticação) e preparar para Convex (coleções).

## 🎯 Objetivo

1. Substituir autenticação mock por Clerk real
2. Manter funcionalidade de busca (FastAPI)
3. Preparar para migrar coleções para Convex
4. Manter backward compatibility

## 📝 Mudanças Necessárias

### 1. Adicionar Imports do Clerk

No início do arquivo, adicione:

```typescript
import { SignIn, SignOutButton, useUser } from "@clerk/clerk-react";
import { Authenticated, Unauthenticated, AuthLoading } from "convex/react";
import { ProtectedRoute } from "./components/ProtectedRoute";
```

### 2. Remover estado de `isLoggedIn`

O Clerk gerencia o estado de autenticação. Remova `isLoggedIn` do `AppState`:

**Antes:**
```typescript
interface AppState {
  isLoggedIn: boolean;  // ❌ Remover
  darkMode: boolean;
  saved: SavedArticle[];
  history: string[];
}

const initialState: AppState = {
  isLoggedIn: false,  // ❌ Remover
  darkMode: false,
  saved: [],
  history: [],
};
```

**Depois:**
```typescript
interface AppState {
  darkMode: boolean;
  saved: SavedArticle[];
  history: string[];
}

const initialState: AppState = {
  darkMode: false,
  saved: [],
  history: [],
};
```

### 3. Atualizar `LoginPage`

Substituir o componente inteiro:

**Antes:**
```typescript
function LoginPage({ shared }: { shared: any }) {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const login = () => {
    if (!email || !password) return;
    shared.setAppState((prev: AppState) => ({ ...prev, isLoggedIn: true }));
    navigate('/dashboard');
  };

  return (
    <div className="login-screen">
      <div className="login-card">
        <h1>IBPR Research Assistant</h1>
        <p>Assistente acadêmico para busca, análise e síntese de evidências.</p>
        <label>Email<input value={email} onChange={(e) => setEmail(e.target.value)} placeholder="seuemail@ibpr.org" type="email" /></label>
        <label>Senha<input value={password} onChange={(e) => setPassword(e.target.value)} placeholder="••••••••" type="password" /></label>
        <button className="primary" onClick={login}>Entrar</button>
        <button className="linklike" onClick={() => { shared.setAppState((prev: AppState) => ({ ...prev, isLoggedIn: true })); navigate('/dashboard'); }}>Acessar versao demo</button>
      </div>
    </div>
  );
}
```

**Depois:**
```typescript
function LoginPage() {
  return (
    <div className="login-screen">
      <div className="login-card">
        <h1>IBPR Research Assistant</h1>
        <p>Assistente acadêmico para busca, análise e síntese de evidências.</p>

        <SignIn
          routing="path"
          path="/login"
          signUpUrl="/signup"
          afterSignInUrl="/dashboard"
        />
      </div>
    </div>
  );
}
```

### 4. Atualizar `MainLayout` - Header

Usar `useUser()` do Clerk para mostrar email:

**Antes:**
```typescript
function MainLayout({ shared }: { shared: any }) {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <div className="app-frame">
      {/* ... sidebar ... */}
      <main className="content">
        <header className="topbar">
          <button className="icon-btn" onClick={() => shared.setAppState((prev: AppState) => ({ ...prev, darkMode: !prev.darkMode }))}>
            {shared.appState.darkMode ? <Sun size={16} /> : <Moon size={16} />}
          </button>
          <span className="user-pill"><User size={14} /> pesquisador@ibpr.org</span>
          <button className="icon-btn" onClick={() => { shared.setAppState((prev: AppState) => ({ ...prev, isLoggedIn: false })); navigate('/login'); }}>
            <LogOut size={16} />
          </button>
        </header>
        {/* ... */}
      </main>
    </div>
  );
}
```

**Depois:**
```typescript
function MainLayout({ shared }: { shared: any }) {
  const location = useLocation();
  const { user } = useUser(); // 🆕 Hook do Clerk

  return (
    <div className="app-frame">
      {/* ... sidebar inalterado ... */}
      <main className="content">
        <header className="topbar">
          <button className="icon-btn" onClick={() => shared.setAppState((prev: AppState) => ({ ...prev, darkMode: !prev.darkMode }))}>
            {shared.appState.darkMode ? <Sun size={16} /> : <Moon size={16} />}
          </button>

          {/* 🆕 Mostrar email real do usuário */}
          <span className="user-pill">
            <User size={14} /> {user?.primaryEmailAddress?.emailAddress || "Usuário"}
          </span>

          {/* 🆕 Botão de logout do Clerk */}
          <SignOutButton>
            <button className="icon-btn">
              <LogOut size={16} />
            </button>
          </SignOutButton>
        </header>
        {/* ... rotas inalteradas ... */}
      </main>
    </div>
  );
}
```

### 5. Atualizar `AppShell` - Rotas

Substituir lógica de autenticação manual por componentes do Clerk:

**Antes:**
```typescript
return (
  <>
    <Routes>
      <Route path="/login" element={<LoginPage shared={shared} />} />
      <Route
        path="/*"
        element={appState.isLoggedIn ? <MainLayout shared={shared} /> : <Navigate to="/login" replace />}
      />
    </Routes>
    {/* modais... */}
  </>
);
```

**Depois:**
```typescript
return (
  <>
    <AuthLoading>
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh"
      }}>
        <p>Carregando autenticação...</p>
      </div>
    </AuthLoading>

    <Unauthenticated>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Unauthenticated>

    <Authenticated>
      <Routes>
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <MainLayout shared={shared} />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Authenticated>

    {/* modais inalterados */}
    {toast && <div className="toast">{toast}</div>}
    {summaryTarget && <QuickSummaryModal /* ... */ />}
    {synthesisOpen && <SynthesisModal /* ... */ />}
  </>
);
```

## ✅ Verificação

Após fazer as mudanças:

1. ✅ Não deve haver erros de TypeScript
2. ✅ App compila sem warnings
3. ✅ Ao acessar `/`, redireciona para `/login`
4. ✅ Modal do Clerk aparece
5. ✅ Após login, vai para `/dashboard`
6. ✅ Email do usuário aparece no header
7. ✅ Logout funciona
8. ✅ Busca de artigos continua funcionando

## 🚀 Próximos Passos (Opcional)

Depois que tudo estiver funcionando, você pode:

1. **Migrar coleções para Convex** (atualmente em localStorage)
2. **Adicionar notas sincronizadas**
3. **Implementar comentários colaborativos**
4. **Adicionar compartilhamento de coleções**

Essas features estão documentadas em `/docs/02-convex-backend.md`.

## 🐛 Troubleshooting

### Erro: "Cannot read property 'isLoggedIn'"

- Você esqueceu de remover alguma referência a `isLoggedIn`
- Busque por `isLoggedIn` no arquivo e remova

### Erro: "SignIn is not exported from '@clerk/clerk-react'"

- Verifique que instalou as dependências: `npm install`
- Reinicie o servidor Vite

### Login redireciona mas não mostra email

- Verifique que adicionou `useUser()` no `MainLayout`
- Confirme que `user?.primaryEmailAddress?.emailAddress` está correto

## 📝 Resumo das Mudanças

| Componente | Mudança | Motivo |
|-----------|---------|--------|
| `AppState` | Removeu `isLoggedIn` | Clerk gerencia estado |
| `LoginPage` | Substituiu por `<SignIn>` | UI nativa do Clerk |
| `MainLayout` | Adicionou `useUser()` | Mostrar email real |
| `MainLayout` | Substituiu logout manual | `<SignOutButton>` do Clerk |
| `AppShell` | Adicionou `<Authenticated>` | Rotas protegidas pelo Clerk |

## ✨ Benefícios

- ✅ Autenticação segura e profissional
- ✅ Menos código para manter
- ✅ UI consistente (Clerk)
- ✅ Integração pronta com Convex
- ✅ Suporte a OAuth (Google, GitHub, etc)
- ✅ Gerenciamento de sessões automático
