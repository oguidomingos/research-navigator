export type BadgeType = 'Revisao' | 'Ensaio' | 'Open Access' | 'Artigo' | 'Preprint';

export interface Article {
  id: number;
  title: string;
  authors: string[];
  year: number;
  journal: string;
  shortAbstract: string;
  abstract: string;
  methodology: string;
  conclusions: string[];
  limitations: string[];
  doi: string;
  url: string;
  badges: BadgeType[];
}

export interface SavedArticle {
  articleId: number;
  note: string;
  savedAt: string;
}

export interface StructuredSummary {
  objetivo: string;
  metodologia: string;
  achados: string;
  limitacoes: string;
  implicacoes: string;
}
