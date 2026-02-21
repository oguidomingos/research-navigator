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
