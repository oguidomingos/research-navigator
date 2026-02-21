# Integração Clerk - Autenticação

## 🎯 Objetivo

Substituir a autenticação mock (localStorage) por autenticação real com Clerk.

## 📦 Instalar Dependências

```bash
cd frontend
npm install @clerk/clerk-react convex
```

## 🔧 Atualizar `frontend/src/main.tsx`

Substituir o conteúdo atual por:

```typescript
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

import { ClerkProvider, useAuth } from "@clerk/clerk-react";
import { ConvexProviderWithClerk } from "convex/react-clerk";
import { ConvexReactClient } from "convex/react";

// Validar env vars
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;
if (!PUBLISHABLE_KEY) {
  throw new Error("Missing VITE_CLERK_PUBLISHABLE_KEY in .env.local");
}

const CONVEX_URL = import.meta.env.VITE_CONVEX_URL;
if (!CONVEX_URL) {
  throw new Error("Missing VITE_CONVEX_URL in .env.local");
}

// Criar cliente Convex
const convex = new ConvexReactClient(CONVEX_URL);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ClerkProvider publishableKey={PUBLISHABLE_KEY} afterSignOutUrl="/login">
      <ConvexProviderWithClerk client={convex} useAuth={useAuth}>
        <App />
      </ConvexProviderWithClerk>
    </ClerkProvider>
  </React.StrictMode>
);
```

## 🛡️ Criar componente `ProtectedRoute`

Criar `frontend/src/components/ProtectedRoute.tsx`:

```typescript
import { useAuth } from "@clerk/clerk-react";
import { Navigate } from "react-router-dom";

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { isLoaded, userId } = useAuth();

  // Aguardar carregamento
  if (!isLoaded) {
    return (
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        height: "100vh"
      }}>
        <p>Carregando...</p>
      </div>
    );
  }

  // Redirecionar para login se não autenticado
  if (!userId) {
    return <Navigate to="/login" replace />;
  }

  return <>{children}</>;
}
```

## 📝 Atualizar `App.tsx` - Autenticação

### 1. Importar componentes do Clerk

No topo do `frontend/src/App.tsx`, adicione:

```typescript
import { SignIn, SignOutButton, UserButton, useUser } from "@clerk/clerk-react";
import { Authenticated, Unauthenticated, AuthLoading } from "convex/react";
import { ProtectedRoute } from "./components/ProtectedRoute";
```

### 2. Atualizar `LoginPage`

Substituir o componente `LoginPage` por:

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

### 3. Atualizar `MainLayout` - User Info

Substituir a parte do header que mostra o email:

```typescript
function MainLayout({ shared }: { shared: any }) {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useUser(); // 🆕 Hook do Clerk

  return (
    <div className="app-frame">
      <aside className="sidebar">
        <div className="logo">IBPR Research</div>
        <nav>
          <Link to="/dashboard" className={location.pathname.startsWith('/dashboard') ? 'active' : ''}>
            <LayoutDashboard size={16} />Buscar
          </Link>
          <Link to="/collections" className={location.pathname.startsWith('/collections') ? 'active' : ''}>
            <BookMarked size={16} />Minhas Colecoes
          </Link>
          <div className="muted-item"><History size={16} />Historico</div>
          <div className="muted-item"><Settings size={16} />Configuracoes</div>
        </nav>
      </aside>

      <main className="content">
        <header className="topbar">
          <button
            className="icon-btn"
            onClick={() => shared.setAppState((prev: AppState) => ({ ...prev, darkMode: !prev.darkMode }))}
          >
            {shared.appState.darkMode ? <Sun size={16} /> : <Moon size={16} />}
          </button>

          {/* 🆕 Mostrar info real do usuário */}
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

        <Routes>
          <Route path="/dashboard" element={<DashboardPage shared={shared} />} />
          <Route path="/results" element={<ResultsPage shared={shared} />} />
          <Route path="/article/:id" element={<ArticlePage shared={shared} />} />
          <Route path="/collections" element={<CollectionsPage shared={shared} />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </main>
    </div>
  );
}
```

### 4. Atualizar `AppShell` - Rotas protegidas

Substituir o componente `AppShell`:

```typescript
function AppShell() {
  const [appState, setAppState] = usePersistedState();
  const [results, setResults] = useState<Article[]>(() => {
    const raw = localStorage.getItem(RESULTS_STORAGE);
    if (!raw) return [];
    try {
      return JSON.parse(raw) as Article[];
    } catch {
      return [];
    }
  });
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [summaryTarget, setSummaryTarget] = useState<Article | null>(null);
  const [synthesisOpen, setSynthesisOpen] = useState(false);
  const [synthesisType, setSynthesisType] = useState<SynthesisType>('Revisao comparativa');
  const [synthesisSize, setSynthesisSize] = useState<SynthesisSize>('Medio');
  const [showSynthesisResult, setShowSynthesisResult] = useState(false);

  const savedArticles = useMemo(
    () => appState.saved.map((item) => results.find((article) => article.id === item.articleId)).filter(Boolean) as Article[],
    [appState.saved, results],
  );

  useEffect(() => {
    localStorage.setItem(RESULTS_STORAGE, JSON.stringify(results));
  }, [results]);

  useEffect(() => {
    if (!toast) return;
    const timer = window.setTimeout(() => setToast(null), 2400);
    return () => window.clearTimeout(timer);
  }, [toast]);

  const saveArticle = (articleId: number) => {
    setAppState((prev) => {
      if (prev.saved.some((item) => item.articleId === articleId)) return prev;
      return { ...prev, saved: [...prev.saved, { articleId, note: '', savedAt: new Date().toISOString() }] };
    });
    setToast('Artigo salvo com sucesso');
  };

  const removeArticle = (articleId: number) => {
    setAppState((prev) => ({ ...prev, saved: prev.saved.filter((item) => item.articleId !== articleId) }));
    setToast('Artigo removido da coleção');
  };

  const updateNote = (articleId: number, note: string) => {
    setAppState((prev) => ({
      ...prev,
      saved: prev.saved.map((item) => (item.articleId === articleId ? { ...item, note } : item)),
    }));
  };

  const runSearch = async (term: string) => {
    const normalized = term.trim();
    if (!normalized) return;
    setIsLoading(true);
    setResults([]);

    try {
      const response = await fetch(`${API_BASE}/search/articles`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: normalized,
          limit: 20,
          offset: 0,
          sort_by: 'relevance',
          filters: { sources: ['openalex', 'pubmed', 'crossref', 'arxiv'] },
        }),
      });

      if (!response.ok) throw new Error('Falha na busca');

      const data = await response.json();
      const mapped = (data.results ?? []).map((item: SearchApiArticle, idx: number) => mapApiArticle(item, idx));
      setResults(mapped);
      setAppState((prev) => ({ ...prev, history: [normalized, ...prev.history.filter((h) => h !== normalized)].slice(0, 8) }));
      setToast(`${mapped.length} artigos recuperados`);
    } catch {
      setToast('Erro ao buscar dados reais. Verifique backend/CORS.');
    } finally {
      setIsLoading(false);
    }
  };

  const shared = {
    appState,
    setAppState,
    query,
    setQuery,
    results,
    isLoading,
    runSearch,
    saveArticle,
    removeArticle,
    savedArticles,
    updateNote,
    toast,
    summaryTarget,
    setSummaryTarget,
    synthesisOpen,
    setSynthesisOpen,
    synthesisType,
    setSynthesisType,
    synthesisSize,
    setSynthesisSize,
    showSynthesisResult,
    setShowSynthesisResult,
  };

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

      {toast && <div className="toast">{toast}</div>}
      {summaryTarget && (
        <QuickSummaryModal
          article={summaryTarget}
          onClose={() => setSummaryTarget(null)}
          onSave={() => saveArticle(summaryTarget.id)}
        />
      )}
      {synthesisOpen && (
        <SynthesisModal
          articles={savedArticles}
          type={synthesisType}
          size={synthesisSize}
          setType={setSynthesisType}
          setSize={setSynthesisSize}
          articleCount={savedArticles.length}
          showResult={showSynthesisResult}
          setShowResult={setShowSynthesisResult}
          onClose={() => {
            setSynthesisOpen(false);
            setShowSynthesisResult(false);
          }}
          toast={(message: string) => setToast(message)}
        />
      )}
    </>
  );
}
```

## 🎨 Estilizar componente do Clerk (opcional)

Criar `frontend/src/clerk.css`:

```css
/* Customizar tema do Clerk para combinar com o app */
.cl-rootBox {
  margin: 0 auto;
}

.cl-card {
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
```

Importar no `main.tsx`:

```typescript
import "./clerk.css";
```

## ✅ Testar Autenticação

1. Reinicie o frontend: `npm run dev`
2. Acesse `http://localhost:5173`
3. Deve redirecionar para `/login`
4. Crie uma conta de teste
5. Após login, deve ir para `/dashboard`
6. Verifique que o email aparece no header

## 🔐 Próximo Passo

Leia `04-deploy-vercel.md` para configurar deploy.
