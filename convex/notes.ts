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
