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
