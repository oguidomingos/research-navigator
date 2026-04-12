# Research Navigator - Funcionalidades, Status e Benchmark de Custo

Data: 2026-03-14  
Ambiente live: https://research.icebergcompany.com.br  
Commit de referencia no deploy: `70ba781`

## Status de deploy

O frontend em producao esta ativo e respondendo `200` em `https://research.icebergcompany.com.br`.

## Correcoes aplicadas (salvar e colecoes)

- O botao `Salvar` agora salva o artigo na colecao ativa.
- O botao `Remover` remove da colecao ativa (sem afetar outras colecoes).
- Foi adicionado controle de colecoes no frontend:
- Criar colecao
- Selecionar colecao ativa
- Renomear colecao ativa
- Excluir colecao ativa (com protecao para manter ao menos uma colecao)
- A geracao de sintese considera apenas os artigos da colecao ativa.

Arquivos alterados nessas correcoes:

- `frontend/src/App.tsx`
- `frontend/src/types.ts`

## Funcionalidades presentes na aplicacao

- Autenticacao com Clerk:
- Login
- Cadastro
- Logout
- Busca de artigos cientificos via backend (`/search/articles`).
- Filtros dinamicos:
- Tipo
- Open Access
- Journal
- Autor
- Ano
- Assistente de selecao IA (`/llm/recommend-results`).
- Chat de pesquisa (`/assistant`) com contexto de:
- Busca atual
- Resultados atuais
- Artigos salvos
- Pagina de detalhes do artigo.
- Perguntas ao artigo (`/llm/ask-article`).
- Resumo rapido estruturado (`/llm/quick-summary`).
- Colecoes locais com notas por artigo.
- Sintese multiartigo (`/llm/synthesize`).
- Copia de citacao e conteudo para area de transferencia.
- Modo claro/escuro.
- Historico local de buscas.
- Integracao de GTM no frontend.

## Riscos/pendencias tecnicas atuais

- Endpoint TheSys no backend da VPS pode nao estar publicado na versao rodando.
- Sintoma: `404` em `/api/v1/thesys/chat`.
- Impacto: chat do assistente pode falhar mesmo com frontend correto.
- Necessario garantir no backend live:
- rota `/api/v1/thesys/chat` disponivel
- `THESYS_API_KEY`, `THESYS_BASE_URL`, `THESYS_MODEL` no ambiente

## Benchmark rapido de custo para ferramenta semelhante

### Escopo comparavel ao atual

- Auth + busca academica + assistente IA + resumo/sintese + colecoes + deploy web.

### Faixa de esforco estimada

- MVP funcional: `8 a 14 semanas`
- Esforco total: `350 a 800 horas` (dependendo de qualidade, testes e robustez)

### Faixa de custo de desenvolvimento

- Freelancer senior BR: `R$ 45 mil a R$ 180 mil`
- Time/agencia enxuta: `R$ 180 mil a R$ 650 mil`
- Produto mais robusto (multi-tenant forte, observabilidade, QA alto): acima dessa faixa

### Custos mensais tipicos de stack (ordem de grandeza)

- Vercel Pro: `US$20/mes + consumo`
- Clerk: plano free + planos pagos por uso
- Convex: free / paid por desenvolvedor + consumo
- OpenRouter/LLM: pay-as-you-go por token/modelo

## Referencias usadas para benchmark

- Vercel Pricing: https://vercel.com/pricing
- Clerk Pricing: https://clerk.com/pricing
- Convex Pricing: https://www.convex.dev/pricing
- OpenRouter Pricing: https://openrouter.ai/pricing
- BLS (salario mediano software dev nos EUA): https://www.bls.gov/ooh/computer-and-information-technology/software-developers.htm
- Stack Overflow Developer Survey 2025: https://survey.stackoverflow.co/2025/work
