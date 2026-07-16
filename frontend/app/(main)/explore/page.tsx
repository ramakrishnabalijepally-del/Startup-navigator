"use client";

import { useEffect, useState, useCallback, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import type { Article } from "@/lib/types";
import { CATEGORIES, CATEGORY_COLORS } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { ArticleCardSkeleton } from "@/components/ui/Skeleton";
import { Search, X, BookOpen } from "lucide-react";
import { formatDate, truncate } from "@/lib/utils";
import Link from "next/link";
import toast from "react-hot-toast";

function ExploreContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const activeCategory = searchParams.get("category") || "";

  const load = useCallback(async (cat: string, q: string) => {
    setLoading(true);
    try {
      const data = await api.articles.list({ category: cat || undefined, search: q || undefined }) as Article[];
      setArticles(data);
    } catch {
      toast.error("Failed to load articles");
    } finally {
      setLoading(false);
    }
  }, []);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => { load(activeCategory, search); }, [activeCategory, load]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    load(activeCategory, search);
  };

  const setCategory = (cat: string) => {
    const params = new URLSearchParams(searchParams.toString());
    if (cat) params.set("category", cat);
    else params.delete("category");
    router.push(`/explore?${params}`);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
      {/* Header */}
      <div className="mb-8">
        <h1 className="section-heading mb-2">Explore Topics</h1>
        <p className="text-slate-500 dark:text-slate-400">Browse curated guides across every stage of your startup journey</p>
      </div>

      {/* Search bar */}
      <form onSubmit={handleSearch} className="relative max-w-xl mb-6">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <input
          className="input pl-10 pr-10"
          placeholder="Search articles…"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
        {search && (
          <button type="button" onClick={() => { setSearch(""); load(activeCategory, ""); }}
            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
            <X className="w-4 h-4" />
          </button>
        )}
      </form>

      {/* Category filters */}
      <div className="flex flex-wrap gap-2 mb-8">
        <button
          onClick={() => setCategory("")}
          className={`badge px-3 py-1.5 text-sm cursor-pointer transition-all ${!activeCategory ? "bg-navy-900 text-white dark:bg-teal-500" : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"}`}>
          All
        </button>
        {CATEGORIES.map(cat => (
          <button key={cat} onClick={() => setCategory(cat)}
            className={`badge px-3 py-1.5 text-sm cursor-pointer transition-all ${activeCategory === cat ? CATEGORY_COLORS[cat] + " ring-2 ring-offset-1 ring-current" : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"}`}>
            {cat}
          </button>
        ))}
      </div>

      {/* Results count */}
      {!loading && (
        <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">
          {articles.length} {articles.length === 1 ? "article" : "articles"}
          {activeCategory && <> in <strong>{activeCategory}</strong></>}
        </p>
      )}

      {/* Grid */}
      {loading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {Array.from({ length: 6 }).map((_, i) => <ArticleCardSkeleton key={i} />)}
        </div>
      ) : articles.length === 0 ? (
        <div className="text-center py-20">
          <BookOpen className="w-10 h-10 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
          <p className="text-slate-500 dark:text-slate-400 font-medium">No articles found</p>
          <p className="text-sm text-slate-400 mt-1">Try a different category or search term</p>
        </div>
      ) : (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {articles.map(article => (
            <Link key={article.id} href={`/explore/${article.id}`}
              className="card p-5 flex flex-col gap-3 group hover:border-teal-400 dark:hover:border-teal-500 hover:shadow-md transition-all duration-200 hover:-translate-y-1">
              <div className="flex items-start justify-between gap-2">
                <Badge variant="category" category={article.category}>{article.category}</Badge>
                <span className="text-xs text-slate-400 shrink-0">{formatDate(article.created_at)}</span>
              </div>
              <h3 className="font-semibold text-slate-900 dark:text-white group-hover:text-teal-600 dark:group-hover:text-teal-400 transition-colors leading-snug">
                {article.title}
              </h3>
              {article.summary && (
                <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">
                  {truncate(article.summary, 120)}
                </p>
              )}
              {article.tags && article.tags.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-auto pt-1">
                  {article.tags.slice(0, 3).map(tag => (
                    <span key={tag} className="badge bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400">{tag}</span>
                  ))}
                </div>
              )}
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}

export default function ExplorePage() {
  return (
    <Suspense fallback={<div className="max-w-7xl mx-auto px-4 py-10"><div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">{Array.from({length:6}).map((_,i)=><div key={i} className="skeleton h-48 rounded-2xl"/>)}</div></div>}>
      <ExploreContent />
    </Suspense>
  );
}
