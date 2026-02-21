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
