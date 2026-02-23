import { useEffect, useMemo, useState } from 'react';
import { BrowserRouter, Link, Navigate, Route, Routes, useLocation, useParams, useNavigate } from 'react-router-dom';
import {
  BookMarked,
  ChevronDown,
  FileDown,
  FileText,
  History,
  LayoutDashboard,
  Moon,
  MessageCircle,
  Search,
  Settings,
  SlidersHorizontal,
  Sparkles,
  Sun,
  Trash2,
  User,
} from 'lucide-react';
import './App.css';
import { synthesisTemplate } from './mockData';
import type { Article, BadgeType, SavedArticle, StructuredSummary } from './types';

type SynthesisType = 'Revisao comparativa' | 'Mapa de evidencias' | 'Aplicacao clinica';
type SynthesisSize = 'Curto' | 'Medio' | 'Longo';

const APP_STORAGE = 'ibpr_mvp_state';
const RESULTS_STORAGE = 'ibpr_real_results';
const API_BASE = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1';

interface AppState {
  darkMode: boolean;
  saved: SavedArticle[];
  history: string[];
}

interface SearchApiArticle {
  id?: number;
  title: string;
  authors?: Array<{ name?: string }>;
  abstract?: string;
  year?: number;
  journal?: string;
  doi?: string;
  paper_type?: string;
  open_access?: boolean;
  url?: string;
}

interface LLMArticlePayload {
  local_id?: number;
  title: string;
  authors: string[];
  year?: number;
  journal?: string;
  doi?: string;
  abstract?: string;
  methodology?: string;
  limitations: string[];
  conclusions: string[];
}

const initialState: AppState = {
  darkMode: false,
  saved: [],
  history: [],
};

function usePersistedState() {
  const [state, setState] = useState<AppState>(() => {
    const raw = localStorage.getItem(APP_STORAGE);
    if (!raw) return initialState;
    try {
      return { ...initialState, ...JSON.parse(raw) } as AppState;
    } catch {
      return initialState;
    }
  });

  useEffect(() => {
    localStorage.setItem(APP_STORAGE, JSON.stringify(state));
    document.body.classList.toggle('dark', state.darkMode);
  }, [state]);

  return [state, setState] as const;
}

function citationAPA(article: Article) {
  const first = article.authors[0] ?? 'Autor';
  const rest = article.authors.length > 1 ? ' et al.' : '';
  const doiOrUrl = article.doi ? `https://doi.org/${article.doi}` : article.url;
  return `${first}${rest} (${article.year}). ${article.title}. ${article.journal}. ${doiOrUrl}`;
}

function mapBadges(type?: string, openAccess?: boolean): BadgeType[] {
  const badges: BadgeType[] = [];
  const normalizedType = (type ?? '').toLowerCase();
  if (normalizedType.includes('review')) badges.push('Revisao');
  if (normalizedType.includes('essay')) badges.push('Ensaio');
  if (normalizedType.includes('preprint')) badges.push('Preprint');
  if (badges.length === 0) badges.push('Artigo');
  if (openAccess) badges.push('Open Access');
  return badges;
}

function mapApiArticle(item: SearchApiArticle, idx: number): Article {
  const abstract = (item.abstract ?? '').trim();
  const short = abstract ? `${abstract.slice(0, 240)}${abstract.length > 240 ? '...' : ''}` : 'Resumo não disponível na fonte.';
  const year = item.year ?? new Date().getFullYear();

  return {
    id: item.id ?? idx + 1,
    title: item.title || 'Sem título',
    authors: (item.authors ?? []).map((a) => a.name ?? '').filter(Boolean),
    year,
    journal: item.journal || 'Periódico não informado',
    shortAbstract: short,
    abstract: abstract || 'Abstract não disponível.',
    methodology: 'Informação metodológica não estruturada nesta fonte. Use o resumo rápido para apoio.',
    conclusions: ['Conclusões não estruturadas automaticamente para este registro.'],
    limitations: ['Limitações não informadas diretamente pelo endpoint de busca.'],
    doi: item.doi ?? '',
    url: item.url ?? '',
    badges: mapBadges(item.paper_type, item.open_access),
  };
}

function toLLMArticle(article: Article): LLMArticlePayload {
  return {
    local_id: article.id,
    title: article.title,
    authors: article.authors,
    year: article.year,
    journal: article.journal,
    doi: article.doi,
    abstract: article.abstract,
    methodology: article.methodology,
    limitations: article.limitations,
    conclusions: article.conclusions,
  };
}

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
      <Routes>
        <Route path="/*" element={<MainLayout shared={shared} />} />
      </Routes>

      {toast && <div className="toast">{toast}</div>}
      {summaryTarget && <QuickSummaryModal article={summaryTarget} onClose={() => setSummaryTarget(null)} onSave={() => saveArticle(summaryTarget.id)} />}
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

function MainLayout({ shared }: { shared: any }) {
  const location = useLocation();

  return (
    <div className="app-frame">
      <aside className="sidebar">
        <div className="logo">IBPR Research</div>
        <nav>
          <Link to="/dashboard" className={location.pathname.startsWith('/dashboard') ? 'active' : ''}><LayoutDashboard size={16} />Buscar</Link>
          <Link to="/collections" className={location.pathname.startsWith('/collections') ? 'active' : ''}><BookMarked size={16} />Minhas Colecoes</Link>
          <div className="muted-item"><History size={16} />Historico</div>
          <div className="muted-item"><Settings size={16} />Configuracoes</div>
        </nav>
      </aside>
      <main className="content">
        <header className="topbar">
          <button className="icon-btn" onClick={() => shared.setAppState((prev: AppState) => ({ ...prev, darkMode: !prev.darkMode }))}>
            {shared.appState.darkMode ? <Sun size={16} /> : <Moon size={16} />}
          </button>

          <span className="user-pill">
            <User size={14} /> Acesso livre
          </span>
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

function DashboardPage({ shared }: { shared: any }) {
  const navigate = useNavigate();
  const [filtersOpen, setFiltersOpen] = useState(false);

  return (
    <section className="page">
      <h2>Buscar Artigos</h2>
      <div className="search-box hero">
        <Search size={22} />
        <input value={shared.query} onChange={(e) => shared.setQuery(e.target.value)} placeholder="Digite tema, palavra-chave ou pergunta academica..." />
        <button className="primary" onClick={async () => { await shared.runSearch(shared.query); navigate('/results'); }}>Buscar</button>
      </div>

      <button className="collapse-btn" onClick={() => setFiltersOpen((v: boolean) => !v)}><ChevronDown size={16} className={filtersOpen ? 'rotated' : ''} /> Filtros</button>

      {filtersOpen && (
        <div className="filters-panel">
          <label>Ano (2015-2026)<input type="range" min={2015} max={2026} defaultValue={2022} /></label>
          <label>Idioma<select defaultValue="PT"><option>PT</option><option>EN</option><option>ES</option></select></label>
          <label>Tipo<select defaultValue="Artigo"><option>Artigo</option><option>Revisao</option><option>Ensaio</option></select></label>
          <label className="toggle"><input type="checkbox" defaultChecked /> Apenas Open Access</label>
        </div>
      )}

      <div className="history">
        <h4>Historico recente</h4>
        {shared.appState.history.length === 0 ? <div className="empty-state">Ainda sem buscas. Use termos como "Psicomotricidade e TEA".</div> : <div className="chips">{shared.appState.history.map((item: string) => <button key={item} onClick={() => shared.setQuery(item)}>{item}</button>)}</div>}
      </div>
    </section>
  );
}

function ResultsPage({ shared }: { shared: any }) {
  const [typeFilter, setTypeFilter] = useState<string>('Todos');
  const [openAccessFilter, setOpenAccessFilter] = useState<string>('Todos');
  const [journalFilter, setJournalFilter] = useState('');
  const [authorFilter, setAuthorFilter] = useState('');
  const [yearMinFilter, setYearMinFilter] = useState<number>(0);
  const [yearMaxFilter, setYearMaxFilter] = useState<number>(9999);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [llmStage, setLlmStage] = useState('');
  const [isUpdatingResults, setIsUpdatingResults] = useState(false);
  const [updateMessage, setUpdateMessage] = useState('');
  const [updatedAt, setUpdatedAt] = useState<string | null>(null);
  const [chatSummary, setChatSummary] = useState('');
  const [recommendedIds, setRecommendedIds] = useState<number[]>([]);
  const [recommendedReasons, setRecommendedReasons] = useState<Record<number, string>>({});

  const years = shared.results.map((article: Article) => article.year).filter((year: number) => Number.isFinite(year));
  const minYear = years.length ? Math.min(...years) : 0;
  const maxYear = years.length ? Math.max(...years) : 9999;
  const effectiveYearMin = yearMinFilter || minYear;
  const effectiveYearMax = yearMaxFilter || maxYear;
  const extractedTypes = Array.from(
    new Set(
      shared.results.flatMap((article: Article) => article.badges.filter((badge) => badge !== 'Open Access')),
    ),
  ) as string[];
  const typeOptions: string[] = ['Todos', ...extractedTypes];

  useEffect(() => {
    setYearMinFilter(minYear);
    setYearMaxFilter(maxYear);
  }, [minYear, maxYear, shared.results.length]);

  const filteredResults = shared.results.filter((article: Article) => {
    const typeOk = typeFilter === 'Todos' || article.badges.some((badge) => badge === typeFilter);
    const oaOk = openAccessFilter === 'Todos'
      || (openAccessFilter === 'Open Access' && article.badges.includes('Open Access'))
      || (openAccessFilter === 'Fechado' && !article.badges.includes('Open Access'));
    const journalOk = !journalFilter.trim() || article.journal.toLowerCase().includes(journalFilter.toLowerCase());
    const authorOk = !authorFilter.trim() || article.authors.join(' ').toLowerCase().includes(authorFilter.toLowerCase());
    const yearOk = article.year >= effectiveYearMin && article.year <= effectiveYearMax;
    const llmOk = recommendedIds.length === 0 || recommendedIds.includes(article.id);
    return typeOk && oaOk && journalOk && authorOk && yearOk && llmOk;
  });

  if (shared.isLoading) {
    return <section className="page"><h2>Resultados</h2><div className="skeleton-grid">{Array.from({ length: 6 }).map((_, idx) => <div className="skeleton-card" key={idx} />)}</div></section>;
  }

  return (
    <section className="page">
      <h2>Resultados da Busca</h2>
      {(chatLoading || isUpdatingResults) && (
        <div className="llm-progress">
          <div className="llm-progress-dot" />
          <div>
            <strong>Assistente IA em andamento</strong>
            <div className="meta">{llmStage || 'Processando sua solicitação...'}</div>
          </div>
        </div>
      )}
      {updateMessage && (
        <div className={`update-feedback ${isUpdatingResults ? 'is-updating' : ''}`}>
          <strong>{updateMessage}</strong>
          {updatedAt && <span>Atualizado às {updatedAt}</span>}
        </div>
      )}
      <div className="results-toolbar">
        <div className="toolbar-title"><SlidersHorizontal size={16} /> Filtros dinâmicos</div>
        <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
          {typeOptions.map((item) => <option key={item}>{item}</option>)}
        </select>
        <select value={openAccessFilter} onChange={(e) => setOpenAccessFilter(e.target.value)}>
          <option>Todos</option>
          <option>Open Access</option>
          <option>Fechado</option>
        </select>
        <input placeholder="Filtrar por journal..." value={journalFilter} onChange={(e) => setJournalFilter(e.target.value)} />
        <input placeholder="Filtrar por autor..." value={authorFilter} onChange={(e) => setAuthorFilter(e.target.value)} />
        <input type="number" placeholder="Ano mín." value={effectiveYearMin || ''} onChange={(e) => setYearMinFilter(Number(e.target.value) || minYear)} />
        <input type="number" placeholder="Ano máx." value={effectiveYearMax || ''} onChange={(e) => setYearMaxFilter(Number(e.target.value) || maxYear)} />
        <button
          onClick={() => {
            setTypeFilter('Todos');
            setOpenAccessFilter('Todos');
            setJournalFilter('');
            setAuthorFilter('');
            setYearMinFilter(minYear);
            setYearMaxFilter(maxYear);
            setRecommendedIds([]);
            setRecommendedReasons({});
            setChatSummary('');
            setUpdateMessage('Filtros e recomendações limpos.');
            setUpdatedAt(new Date().toLocaleTimeString());
          }}
        >
          Limpar
        </button>
      </div>
      {chatSummary && <div className="chat-insight">{chatSummary}</div>}
      {shared.results.length === 0 ? (
        <div className="empty-state">Nenhum resultado real retornou. Verifique se backend está ativo em <code>{API_BASE}</code>.</div>
      ) : (
        <div className="cards-list">
          {filteredResults.map((article: Article) => (
            <ArticleCard
              key={article.id}
              article={article}
              onSave={() => shared.saveArticle(article.id)}
              onSummary={() => shared.setSummaryTarget(article)}
              llmReason={recommendedReasons[article.id]}
            />
          ))}
        </div>
      )}
      <button className="chat-fab" onClick={() => setChatOpen((prev) => !prev)}>
        <MessageCircle size={16} /> Assistente de seleção
      </button>
      {chatOpen && (
        <div className="chat-popup">
          <h4>Selecionar Artigos com IA</h4>
          <p className="meta">Descreva seu critério. Ex: \"quero estudos de revisão recentes e com foco clínico\".</p>
          <textarea value={chatInput} onChange={(e) => setChatInput(e.target.value)} placeholder="Escreva seu pedido..." />
          <div className="actions">
            <button
              className="primary"
              disabled={chatLoading || !chatInput.trim() || shared.results.length === 0}
              onClick={async () => {
                const started = Date.now();
                setChatLoading(true);
                setIsUpdatingResults(true);
                setLlmStage('Preparando contexto dos artigos...');
                setUpdateMessage('Analisando correspondência entre seu pedido e os artigos.');
                try {
                  await new Promise((resolve) => setTimeout(resolve, 250));
                  setLlmStage('Consultando modelo LLM...');
                  const response = await fetch(`${API_BASE}/llm/recommend-results`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                      instruction: chatInput,
                      language: 'pt-BR',
                      articles: shared.results.map((article: Article) => toLLMArticle(article)),
                    }),
                  });
                  if (!response.ok) throw new Error('Falha recomendação');
                  setLlmStage('Interpretando resposta e aplicando seleção...');
                  const data = await response.json();
                  const ids: number[] = (data.recommendations ?? []).map((item: { local_id: number }) => item.local_id);
                  const reasons: Record<number, string> = {};
                  for (const item of data.recommendations ?? []) {
                    reasons[item.local_id] = item.reason;
                  }
                  setRecommendedIds(ids);
                  setRecommendedReasons(reasons);
                  setChatSummary(data.summary || `A IA selecionou ${ids.length} artigos relevantes.`);
                  setUpdateMessage(`Atualização concluída: ${ids.length} artigos recomendados e filtros ajustados.`);

                  const suggested = data.suggested_filters || {};
                  if (typeof suggested.year_min === 'number') setYearMinFilter(suggested.year_min);
                  if (typeof suggested.year_max === 'number') setYearMaxFilter(suggested.year_max);
                  if (typeof suggested.open_access_only === 'boolean') {
                    setOpenAccessFilter(suggested.open_access_only ? 'Open Access' : 'Todos');
                  }
                  if (typeof suggested.journal_contains === 'string') setJournalFilter(suggested.journal_contains);
                  if (typeof suggested.author_contains === 'string') setAuthorFilter(suggested.author_contains);
                } catch {
                  setChatSummary('Não foi possível analisar com IA agora. Tente novamente em alguns segundos.');
                  setUpdateMessage('Falha na atualização por IA. Nenhuma alteração foi aplicada.');
                } finally {
                  const elapsed = Date.now() - started;
                  if (elapsed < 1200) {
                    await new Promise((resolve) => setTimeout(resolve, 1200 - elapsed));
                  }
                  setUpdatedAt(new Date().toLocaleTimeString());
                  setChatLoading(false);
                  setLlmStage('');
                  setIsUpdatingResults(false);
                }
              }}
            >
              {chatLoading ? 'Analisando...' : 'Analisar resultados'}
            </button>
            <button onClick={() => setChatOpen(false)}>Fechar</button>
          </div>
        </div>
      )}
    </section>
  );
}

function ArticleCard({ article, onSave, onSummary, llmReason }: { article: Article; onSave: () => void; onSummary: () => void; llmReason?: string }) {
  return (
    <article className="article-card">
      <Link to={`/article/${article.id}`} className="title-link">{article.title}</Link>
      <p className="meta">{article.authors.join(', ') || 'Autores não informados'} • {article.year} • {article.journal}</p>
      <p>{article.shortAbstract}</p>
      {llmReason && <p className="llm-match">Sugestão IA: {llmReason}</p>}
      <div className="badges">{article.badges.map((badge) => <span key={badge} className="badge">{badge}</span>)}</div>
      <div className="actions">
        <Link to={`/article/${article.id}`} className="ghost">Ver detalhes</Link>
        <button onClick={onSave}>Salvar</button>
        <button onClick={onSummary}>Resumo rapido</button>
        <button onClick={() => navigator.clipboard.writeText(citationAPA(article))}>Citar</button>
      </div>
    </article>
  );
}

function ArticlePage({ shared }: { shared: any }) {
  const { id } = useParams();
  const article = shared.results.find((item: Article) => String(item.id) === id);
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [asking, setAsking] = useState(false);

  if (!article) return <section className="page"><div className="empty-state">Artigo não encontrado no cache da busca. Faça uma nova busca e abra novamente.</div></section>;

  return (
    <section className="page">
      <div className="article-header">
        <div>
          <h2>{article.title}</h2>
          <p className="meta">{article.authors.join(', ') || 'Autores não informados'} • {article.year} • DOI: {article.doi || 'não informado'}</p>
        </div>
        <button className="primary" onClick={() => article.url && window.open(article.url, '_blank')}>Ver na fonte</button>
      </div>

      <section className="detail-box"><h3>Abstract Completo</h3><p>{article.abstract}</p></section>
      <section className="detail-box"><h3>Principais Conclusoes</h3><ul>{article.conclusions.map((c: string) => <li key={c}>{c}</li>)}</ul></section>
      <section className="detail-box"><h3>Metodologia</h3><p>{article.methodology}</p></section>
      <section className="detail-box"><h3>Limitacoes</h3><ul>{article.limitations.map((l: string) => <li key={l}>{l}</li>)}</ul></section>

      <section className="detail-box">
        <h3>Perguntar ao Artigo</h3>
        <div className="ask-row">
          <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="Ex: Quais resultados são clinicamente mais relevantes?" />
          <button
            onClick={async () => {
              if (!question.trim()) return;
              setAsking(true);
              try {
                const response = await fetch(`${API_BASE}/llm/ask-article`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ article: toLLMArticle(article), question, language: 'pt-BR' }),
                });
                if (!response.ok) throw new Error('Falha LLM');
                const data = await response.json();
                setAnswer(`${data.answer}\n\n${data.citation}`);
              } catch {
                setAnswer('Não foi possível gerar resposta LLM agora. Verifique OPENROUTER_API_KEY e tente novamente.');
              } finally {
                setAsking(false);
              }
            }}
            disabled={asking}
          >
            {asking ? 'Perguntando...' : 'Perguntar'}
          </button>
        </div>
        {answer && <p className="llm-answer">{answer}</p>}
      </section>
      <button onClick={() => shared.saveArticle(article.id)} className="primary">Salvar artigo</button>
    </section>
  );
}

function CollectionsPage({ shared }: { shared: any }) {
  return (
    <section className="page">
      <div className="page-inline-header">
        <h2>Minhas Colecoes</h2>
        <button className="primary" onClick={() => shared.setSynthesisOpen(true)} disabled={shared.savedArticles.length < 2}><Sparkles size={16} /> Gerar sintese</button>
      </div>

      {shared.savedArticles.length === 0 ? (
        <div className="empty-state">Sua coleção está vazia. Salve artigos reais para gerar síntese.</div>
      ) : (
        <div className="cards-list">
          {shared.savedArticles.map((article: Article) => {
            const saved = shared.appState.saved.find((item: SavedArticle) => item.articleId === article.id);
            return (
              <article className="article-card" key={article.id}>
                <h3>{article.title}</h3>
                <p className="meta">{article.authors.join(', ') || 'Autores não informados'} • {article.year}</p>
                <label>Nota pessoal<textarea value={saved?.note ?? ''} onChange={(e) => shared.updateNote(article.id, e.target.value)} placeholder="Escreva um insight clinico ou metodologico..." /></label>
                <div className="actions">
                  <button onClick={() => shared.setSynthesisOpen(true)}>Gerar sintese</button>
                  <button className="danger" onClick={() => shared.removeArticle(article.id)}><Trash2 size={14} /> Remover</button>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}

function QuickSummaryModal({ article, onClose, onSave }: { article: Article; onClose: () => void; onSave: () => void }) {
  const [summary, setSummary] = useState<StructuredSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const run = async () => {
      try {
        const response = await fetch(`${API_BASE}/llm/quick-summary`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ article: toLLMArticle(article), language: 'pt-BR' }),
        });
        if (!response.ok) throw new Error('Falha LLM');
        const data = await response.json();
        setSummary({
          objetivo: data.objetivo || '',
          metodologia: data.metodologia || '',
          achados: data.principais_achados || '',
          limitacoes: data.limitacoes || '',
          implicacoes: data.implicacoes_praticas || '',
        });
      } catch {
        setSummary({
          objetivo: `Sintetizar rapidamente o artigo: ${article.title}.`,
          metodologia: article.methodology,
          achados: article.abstract || article.shortAbstract,
          limitacoes: article.limitations.join(' '),
          implicacoes: 'Não foi possível usar o LLM agora. Resultado exibido em fallback local.',
        });
      } finally {
        setLoading(false);
      }
    };

    void run();
  }, [article]);

  return (
    <div className="modal-backdrop">
      <div className="modal">
        <h3>Resumo Estruturado</h3>
        {loading && <p className="meta">Gerando resumo com LLM...</p>}
        {summary && (
          <>
            <p><strong>Objetivo:</strong> {summary.objetivo}</p>
            <p><strong>Metodologia:</strong> {summary.metodologia}</p>
            <p><strong>Principais achados:</strong> {summary.achados}</p>
            <p><strong>Limitacoes:</strong> {summary.limitacoes}</p>
            <p><strong>Implicacoes praticas:</strong> {summary.implicacoes}</p>
          </>
        )}
        <div className="actions">
          <button
            onClick={() =>
              summary &&
              navigator.clipboard.writeText(
                `Objetivo: ${summary.objetivo}\nMetodologia: ${summary.metodologia}\nAchados: ${summary.achados}\nLimitacoes: ${summary.limitacoes}\nImplicacoes: ${summary.implicacoes}`,
              )
            }
          >
            Copiar
          </button>
          <button onClick={onSave}>Salvar na colecao</button>
          <button className="ghost" onClick={onClose}>Fechar</button>
        </div>
      </div>
    </div>
  );
}

function SynthesisModal({ articles, type, size, setType, setSize, articleCount, showResult, setShowResult, onClose, toast }: { articles: Article[]; type: SynthesisType; size: SynthesisSize; setType: (value: SynthesisType) => void; setSize: (value: SynthesisSize) => void; articleCount: number; showResult: boolean; setShowResult: (value: boolean) => void; onClose: () => void; toast: (message: string) => void; }) {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{
    introducao: string;
    convergencias: string;
    divergencias: string;
    lacunas: string;
    recomendacoes: string;
    referencias_apa: string[];
  } | null>(null);

  return (
    <div className="modal-backdrop">
      <div className="modal large">
        <h3>Gerar Sintese</h3>
        <label>Tipo de sintese<select value={type} onChange={(e) => setType(e.target.value as SynthesisType)}><option>Revisao comparativa</option><option>Mapa de evidencias</option><option>Aplicacao clinica</option></select></label>
        <label>Tamanho<select value={size} onChange={(e) => setSize(e.target.value as SynthesisSize)}><option>Curto</option><option>Medio</option><option>Longo</option></select></label>
        <p className="meta">Base: {articleCount} artigos salvos</p>
        <button
          className="primary"
          disabled={loading}
          onClick={async () => {
            setLoading(true);
            setShowResult(true);
            try {
              const response = await fetch(`${API_BASE}/llm/synthesize`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  articles: articles.map((item) => toLLMArticle(item)),
                  synthesis_type: type,
                  size,
                  language: 'pt-BR',
                }),
              });
              if (!response.ok) throw new Error('Falha síntese');
              const data = await response.json();
              setResult(data);
            } catch {
              setResult({
                introducao: synthesisTemplate.introducao,
                convergencias: synthesisTemplate.convergencias,
                divergencias: synthesisTemplate.divergencias,
                lacunas: synthesisTemplate.lacunas,
                recomendacoes: synthesisTemplate.recomendacoes,
                referencias_apa: ['Não foi possível gerar referências com LLM neste momento.'],
              });
            } finally {
              setLoading(false);
            }
          }}
        >
          {loading ? 'Gerando...' : 'Gerar'}
        </button>

        {showResult && (
          <div className="synthesis-output">
            <h4>{type} ({size})</h4>
            <p><strong>Introducao:</strong> {result?.introducao ?? synthesisTemplate.introducao}</p>
            <p><strong>Convergencias:</strong> {result?.convergencias ?? synthesisTemplate.convergencias}</p>
            <p><strong>Divergencias:</strong> {result?.divergencias ?? synthesisTemplate.divergencias}</p>
            <p><strong>Lacunas:</strong> {result?.lacunas ?? synthesisTemplate.lacunas}</p>
            <p><strong>Recomendacoes:</strong> {result?.recomendacoes ?? synthesisTemplate.recomendacoes}</p>
            <p><strong>Referencias (APA):</strong> {(result?.referencias_apa ?? []).join(' ; ') || 'geradas a partir dos artigos salvos.'}</p>
            <div className="actions">
              <button onClick={() => toast('Sintese copiada')}>Copiar</button>
              <button onClick={() => toast('Exportacao PDF simulada')}><FileDown size={14} /> Exportar PDF</button>
              <button onClick={() => toast('Exportacao DOCX simulada')}><FileText size={14} /> Exportar DOCX</button>
            </div>
          </div>
        )}
        <button className="ghost" onClick={onClose}>Fechar</button>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppShell />
    </BrowserRouter>
  );
}
