# Convex Backend - Schema e Funções

## 📊 Schema do Banco de Dados

O Convex usa um schema TypeScript fortemente tipado. Vamos criar tabelas para:

1. **collections** - Coleções de artigos do usuário
2. **saved_articles** - Artigos salvos em coleções
3. **notes** - Notas pessoais em artigos
4. **comments** - Comentários colaborativos

### Criar `convex/schema.ts`

```typescript
import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  // Coleções de artigos
  collections: defineTable({
    userId: v.string(), // Clerk user ID
    name: v.string(),
    description: v.optional(v.string()),
    isPublic: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user", ["userId"])
    .index("by_public", ["isPublic"]),

  // Artigos salvos em coleções
  saved_articles: defineTable({
    collectionId: v.id("collections"),
    userId: v.string(), // Dono da coleção

    // Dados do artigo (copiados do resultado da busca)
    articleId: v.string(), // ID único (DOI ou hash)
    title: v.string(),
    authors: v.array(v.string()),
    year: v.number(),
    journal: v.optional(v.string()),
    doi: v.optional(v.string()),
    abstract: v.optional(v.string()),
    url: v.optional(v.string()),

    // Metadados
    savedAt: v.number(),
    order: v.optional(v.number()), // Para ordenação customizada
  })
    .index("by_collection", ["collectionId"])
    .index("by_user", ["userId"])
    .index("by_article", ["articleId"]),

  // Notas pessoais em artigos
  notes: defineTable({
    userId: v.string(),
    articleId: v.string(), // Referência ao artigo
    content: v.string(),
    isPrivate: v.boolean(),
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_user_article", ["userId", "articleId"])
    .index("by_article", ["articleId"]),

  // Comentários colaborativos
  comments: defineTable({
    userId: v.string(),
    userName: v.string(), // Nome do usuário (cache do Clerk)
    userEmail: v.string(),
    articleId: v.string(),
    content: v.string(),
    parentId: v.optional(v.id("comments")), // Para threads
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_article", ["articleId"])
    .index("by_user", ["userId"])
    .index("by_parent", ["parentId"]),
});
```

### Sincronizar schema

Após criar o arquivo, o `npx convex dev` detecta automaticamente e aplica:

```bash
# Se não estiver rodando, execute:
npx convex dev
```

Você verá no terminal:

```
✔ Schema updated successfully
```

## 🔧 Funções Convex

### 1. Collections - `convex/collections.ts`

```typescript
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Listar coleções do usuário
export const list = query({
  args: {},
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    return await ctx.db
      .query("collections")
      .withIndex("by_user", (q) => q.eq("userId", identity.subject))
      .order("desc")
      .collect();
  },
});

// Criar nova coleção
export const create = mutation({
  args: {
    name: v.string(),
    description: v.optional(v.string()),
    isPublic: v.boolean(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const now = Date.now();
    return await ctx.db.insert("collections", {
      userId: identity.subject,
      name: args.name,
      description: args.description,
      isPublic: args.isPublic,
      createdAt: now,
      updatedAt: now,
    });
  },
});

// Atualizar coleção
export const update = mutation({
  args: {
    id: v.id("collections"),
    name: v.optional(v.string()),
    description: v.optional(v.string()),
    isPublic: v.optional(v.boolean()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const collection = await ctx.db.get(args.id);
    if (!collection) throw new Error("Collection not found");
    if (collection.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    await ctx.db.patch(args.id, {
      ...args,
      updatedAt: Date.now(),
    });
  },
});

// Deletar coleção
export const remove = mutation({
  args: { id: v.id("collections") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const collection = await ctx.db.get(args.id);
    if (!collection) throw new Error("Collection not found");
    if (collection.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    // Deletar todos os artigos da coleção
    const articles = await ctx.db
      .query("saved_articles")
      .withIndex("by_collection", (q) => q.eq("collectionId", args.id))
      .collect();

    for (const article of articles) {
      await ctx.db.delete(article._id);
    }

    await ctx.db.delete(args.id);
  },
});
```

### 2. Saved Articles - `convex/articles.ts`

```typescript
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Listar artigos de uma coleção
export const listByCollection = query({
  args: { collectionId: v.id("collections") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    return await ctx.db
      .query("saved_articles")
      .withIndex("by_collection", (q) =>
        q.eq("collectionId", args.collectionId)
      )
      .order("desc")
      .collect();
  },
});

// Salvar artigo em coleção
export const save = mutation({
  args: {
    collectionId: v.id("collections"),
    articleId: v.string(),
    title: v.string(),
    authors: v.array(v.string()),
    year: v.number(),
    journal: v.optional(v.string()),
    doi: v.optional(v.string()),
    abstract: v.optional(v.string()),
    url: v.optional(v.string()),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    // Verificar se usuário é dono da coleção
    const collection = await ctx.db.get(args.collectionId);
    if (!collection) throw new Error("Collection not found");
    if (collection.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    // Verificar se artigo já existe nesta coleção
    const existing = await ctx.db
      .query("saved_articles")
      .withIndex("by_collection", (q) =>
        q.eq("collectionId", args.collectionId)
      )
      .filter((q) => q.eq(q.field("articleId"), args.articleId))
      .first();

    if (existing) {
      throw new Error("Article already in collection");
    }

    return await ctx.db.insert("saved_articles", {
      ...args,
      userId: identity.subject,
      savedAt: Date.now(),
    });
  },
});

// Remover artigo da coleção
export const remove = mutation({
  args: { id: v.id("saved_articles") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const article = await ctx.db.get(args.id);
    if (!article) throw new Error("Article not found");
    if (article.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    await ctx.db.delete(args.id);
  },
});
```

### 3. Notes - `convex/notes.ts`

```typescript
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Listar notas do usuário para um artigo
export const listByArticle = query({
  args: { articleId: v.string() },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    return await ctx.db
      .query("notes")
      .withIndex("by_user_article", (q) =>
        q.eq("userId", identity.subject).eq("articleId", args.articleId)
      )
      .collect();
  },
});

// Criar/atualizar nota
export const upsert = mutation({
  args: {
    articleId: v.string(),
    content: v.string(),
    isPrivate: v.boolean(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    // Buscar nota existente
    const existing = await ctx.db
      .query("notes")
      .withIndex("by_user_article", (q) =>
        q.eq("userId", identity.subject).eq("articleId", args.articleId)
      )
      .first();

    const now = Date.now();

    if (existing) {
      // Atualizar
      await ctx.db.patch(existing._id, {
        content: args.content,
        isPrivate: args.isPrivate,
        updatedAt: now,
      });
      return existing._id;
    } else {
      // Criar nova
      return await ctx.db.insert("notes", {
        userId: identity.subject,
        articleId: args.articleId,
        content: args.content,
        isPrivate: args.isPrivate,
        createdAt: now,
        updatedAt: now,
      });
    }
  },
});

// Deletar nota
export const remove = mutation({
  args: { id: v.id("notes") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const note = await ctx.db.get(args.id);
    if (!note) throw new Error("Note not found");
    if (note.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    await ctx.db.delete(args.id);
  },
});
```

### 4. Comments - `convex/comments.ts`

```typescript
import { v } from "convex/values";
import { mutation, query } from "./_generated/server";

// Listar comentários de um artigo
export const listByArticle = query({
  args: { articleId: v.string() },
  handler: async (ctx, args) => {
    return await ctx.db
      .query("comments")
      .withIndex("by_article", (q) => q.eq("articleId", args.articleId))
      .order("desc")
      .collect();
  },
});

// Criar comentário
export const create = mutation({
  args: {
    articleId: v.string(),
    content: v.string(),
    parentId: v.optional(v.id("comments")),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const now = Date.now();
    return await ctx.db.insert("comments", {
      userId: identity.subject,
      userName: identity.name || "Usuário",
      userEmail: identity.email || "",
      articleId: args.articleId,
      content: args.content,
      parentId: args.parentId,
      createdAt: now,
      updatedAt: now,
    });
  },
});

// Atualizar comentário
export const update = mutation({
  args: {
    id: v.id("comments"),
    content: v.string(),
  },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const comment = await ctx.db.get(args.id);
    if (!comment) throw new Error("Comment not found");
    if (comment.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    await ctx.db.patch(args.id, {
      content: args.content,
      updatedAt: Date.now(),
    });
  },
});

// Deletar comentário
export const remove = mutation({
  args: { id: v.id("comments") },
  handler: async (ctx, args) => {
    const identity = await ctx.auth.getUserIdentity();
    if (!identity) throw new Error("Not authenticated");

    const comment = await ctx.db.get(args.id);
    if (!comment) throw new Error("Comment not found");
    if (comment.userId !== identity.subject) {
      throw new Error("Unauthorized");
    }

    await ctx.db.delete(args.id);
  },
});
```

## ✅ Verificar funções

Após criar os arquivos, o Convex sincroniza automaticamente. Você pode testar no dashboard:

1. Acesse o Convex Dashboard (URL mostrada no terminal)
2. Vá em **Functions**
3. Teste manualmente as queries/mutations

## 📝 Próximo Passo

Leia `03-clerk-auth.md` para integrar Clerk no frontend.
