"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Article } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import { ArrowLeft, User, Calendar } from "lucide-react";
import { formatDate } from "@/lib/utils";
import Link from "next/link";
import { useParams } from "next/navigation";
import toast from "react-hot-toast";

export default function ArticlePage() {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.articles.get(Number(id))
      .then(data => setArticle(data as Article))
      .catch(() => toast.error("Article not found"))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10 space-y-4">
      <Skeleton className="h-6 w-24" />
      <Skeleton className="h-10 w-full" />
      <Skeleton className="h-4 w-48" />
      {Array.from({ length: 8 }).map((_, i) => <Skeleton key={i} className="h-4 w-full" />)}
    </div>
  );

  if (!article) return (
    <div className="text-center py-20">
      <p className="text-slate-500">Article not found.</p>
      <Link href="/explore" className="btn-primary mt-4 inline-flex">Back to Explore</Link>
    </div>
  );

  // Convert markdown-style content to simple HTML paragraphs
  const sections = article.content.split(/\n\n+/);

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
      <Link href="/explore" className="inline-flex items-center gap-1.5 text-sm text-slate-500 hover:text-teal-600 dark:hover:text-teal-400 mb-6 transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to Explore
      </Link>

      <div className="mb-6">
        <Badge variant="category" category={article.category} className="mb-3">{article.category}</Badge>
        <h1 className="text-2xl md:text-3xl font-bold text-navy-900 dark:text-white leading-tight mb-4 font-heading">
          {article.title}
        </h1>
        <div className="flex flex-wrap items-center gap-4 text-sm text-slate-500 dark:text-slate-400">
          {article.author && (
            <span className="flex items-center gap-1.5"><User className="w-3.5 h-3.5" />{article.author}</span>
          )}
          <span className="flex items-center gap-1.5"><Calendar className="w-3.5 h-3.5" />{formatDate(article.created_at)}</span>
        </div>
        {article.tags && article.tags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-4">
            {article.tags.map(tag => (
              <span key={tag} className="badge bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400">{tag}</span>
            ))}
          </div>
        )}
      </div>

      <article className="prose-custom">
        {sections.map((section, i) => {
          if (section.startsWith("## ")) return (
            <h2 key={i} className="text-xl font-bold text-navy-900 dark:text-white mt-8 mb-3 font-heading">
              {section.replace("## ", "")}
            </h2>
          );
          if (section.startsWith("### ")) return (
            <h3 key={i} className="text-base font-semibold text-slate-800 dark:text-slate-100 mt-6 mb-2 font-heading">
              {section.replace("### ", "")}
            </h3>
          );
          if (section.startsWith("- ") || section.startsWith("* ")) {
            const items = section.split("\n").filter(l => l.startsWith("- ") || l.startsWith("* "));
            return (
              <ul key={i} className="list-disc list-inside space-y-1 text-slate-600 dark:text-slate-300 text-sm my-3">
                {items.map((item, j) => <li key={j}>{item.replace(/^[-*] /, "")}</li>)}
              </ul>
            );
          }
          if (section.startsWith("**") && section.includes(":**")) {
            return (
              <p key={i} className="text-sm text-slate-600 dark:text-slate-300 my-3 leading-relaxed">
                <strong className="text-slate-800 dark:text-slate-100">{section.split(":**")[0].replace(/\*\*/g, "")}:</strong>
                {section.split(":**")[1]}
              </p>
            );
          }
          return (
            <p key={i} className="text-sm text-slate-600 dark:text-slate-300 my-3 leading-relaxed">{section}</p>
          );
        })}
      </article>
    </div>
  );
}
