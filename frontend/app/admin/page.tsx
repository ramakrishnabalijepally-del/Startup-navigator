"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/components/providers/AuthProvider";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import type { AdminAnalytics, Article, Resource } from "@/lib/types";
import { CATEGORIES } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { StatCardSkeleton, Skeleton } from "@/components/ui/Skeleton";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Users, FileText, Link2, Search, RefreshCw, Plus, Pencil, Trash2, X, Check } from "lucide-react";
import toast from "react-hot-toast";

type Tab = "analytics" | "articles" | "resources";

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [tab, setTab] = useState<Tab>("analytics");
  const [analytics, setAnalytics] = useState<AdminAnalytics | null>(null);
  const [articles, setArticles] = useState<Article[]>([]);
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [reindexing, setReindexing] = useState(false);

  // Article form state
  const [editingArticle, setEditingArticle] = useState<Partial<Article> | null>(null);
  const [articleForm, setArticleForm] = useState({ title: "", category: "Registration", content: "", summary: "", tags: "" });

  useEffect(() => {
    if (!authLoading && (!user || user.role !== "admin")) router.push("/");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user || user.role !== "admin") return;
    loadAll();
  }, [user]);

  const loadAll = async () => {
    setLoading(true);
    try {
      const [a, arts, ress] = await Promise.all([
        api.admin.analytics(),
        api.articles.list({ limit: 100 }),
        api.resources.list(),
      ]);
      setAnalytics(a as AdminAnalytics);
      setArticles(arts as Article[]);
      setResources(ress as Resource[]);
    } catch { toast.error("Failed to load admin data"); }
    finally { setLoading(false); }
  };

  const handleReindex = async () => {
    setReindexing(true);
    try {
      await api.admin.reindex();
      toast.success("Reindexing started in background");
    } catch { toast.error("Reindex failed"); }
    finally { setReindexing(false); }
  };

  const handleSaveArticle = async () => {
    const payload = {
      ...articleForm,
      tags: articleForm.tags.split(",").map(t => t.trim()).filter(Boolean),
    };
    try {
      if (editingArticle?.id) {
        await api.articles.update(editingArticle.id, payload);
        toast.success("Article updated");
      } else {
        await api.articles.create(payload);
        toast.success("Article created");
      }
      setEditingArticle(null);
      loadAll();
    } catch { toast.error("Save failed"); }
  };

  const handleDeleteArticle = async (id: number) => {
    if (!confirm("Delete this article?")) return;
    try {
      await api.articles.delete(id);
      toast.success("Article deleted");
      loadAll();
    } catch { toast.error("Delete failed"); }
  };

  const startEditArticle = (a?: Article) => {
    if (a) {
      setEditingArticle(a);
      setArticleForm({ title: a.title, category: a.category, content: a.content || "", summary: a.summary || "", tags: (a.tags || []).join(", ") });
    } else {
      setEditingArticle({});
      setArticleForm({ title: "", category: "Registration", content: "", summary: "", tags: "" });
    }
  };

  if (authLoading || (user && user.role !== "admin")) return null;

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)]">
      <Navbar />
      <main className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
        <div className="flex items-center justify-between mb-8">
          <h1 className="section-heading">Admin Panel</h1>
          <button onClick={handleReindex} disabled={reindexing} className="btn-outline text-xs gap-1.5">
            <RefreshCw className={`w-3.5 h-3.5 ${reindexing ? "animate-spin" : ""}`} />
            {reindexing ? "Reindexing…" : "Reindex AI"}
          </button>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 mb-8 p-1 bg-slate-100 dark:bg-slate-800 rounded-xl w-fit">
          {(["analytics", "articles", "resources"] as Tab[]).map(t => (
            <button key={t} onClick={() => setTab(t)}
              className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-all ${tab === t ? "bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-sm" : "text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200"}`}>
              {t}
            </button>
          ))}
        </div>

        {/* Analytics Tab */}
        {tab === "analytics" && (
          <div className="space-y-8 animate-fade-in">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {loading ? Array.from({ length: 4 }).map((_, i) => <StatCardSkeleton key={i} />) : (
                [
                  { label: "Total Users",     value: analytics?.totals.users,     icon: <Users className="w-4 h-4" /> },
                  { label: "Articles",         value: analytics?.totals.articles,  icon: <FileText className="w-4 h-4" /> },
                  { label: "Resources",        value: analytics?.totals.resources, icon: <Link2 className="w-4 h-4" /> },
                  { label: "Total Searches",   value: analytics?.totals.searches,  icon: <Search className="w-4 h-4" /> },
                ].map(({ label, value, icon }) => (
                  <div key={label} className="card p-5">
                    <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-1">{icon}{label}</div>
                    <div className="text-3xl font-bold text-navy-900 dark:text-white font-heading">{value ?? 0}</div>
                  </div>
                ))
              )}
            </div>

            {analytics && (
              <div className="grid md:grid-cols-2 gap-6">
                <div className="card p-5">
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-4 font-heading">Popular Topics</h3>
                  {analytics.popular_topics.length === 0 ? (
                    <p className="text-sm text-slate-400">No data yet</p>
                  ) : analytics.popular_topics.map(t => (
                    <div key={t.category} className="flex items-center justify-between py-2 border-b border-slate-100 dark:border-slate-800 last:border-0">
                      <Badge variant="category" category={t.category}>{t.category}</Badge>
                      <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">{t.count} searches</span>
                    </div>
                  ))}
                </div>
                <div className="card p-5">
                  <h3 className="font-semibold text-slate-900 dark:text-white mb-4 font-heading">Recent Searches</h3>
                  {analytics.recent_searches.length === 0 ? (
                    <p className="text-sm text-slate-400">No searches yet</p>
                  ) : analytics.recent_searches.map(s => (
                    <div key={s.id} className="py-2 border-b border-slate-100 dark:border-slate-800 last:border-0">
                      <p className="text-sm text-slate-700 dark:text-slate-200 truncate">{s.query}</p>
                      <p className="text-xs text-slate-400 mt-0.5">User #{s.user_id}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Articles Tab */}
        {tab === "articles" && (
          <div className="animate-fade-in">
            <div className="flex justify-between items-center mb-4">
              <p className="text-sm text-slate-500 dark:text-slate-400">{articles.length} articles</p>
              <button onClick={() => startEditArticle()} className="btn-primary !py-1.5 !px-4 text-sm">
                <Plus className="w-4 h-4" /> New Article
              </button>
            </div>

            {/* Inline form */}
            {editingArticle !== null && (
              <div className="card p-6 mb-6 space-y-4 animate-slide-up">
                <h3 className="font-semibold text-slate-900 dark:text-white font-heading">
                  {editingArticle.id ? "Edit Article" : "New Article"}
                </h3>
                <div className="grid sm:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Title *</label>
                    <input className="input" value={articleForm.title} onChange={e => setArticleForm(f => ({ ...f, title: e.target.value }))} />
                  </div>
                  <div>
                    <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Category *</label>
                    <select className="input" value={articleForm.category} onChange={e => setArticleForm(f => ({ ...f, category: e.target.value }))}>
                      {CATEGORIES.map(c => <option key={c}>{c}</option>)}
                    </select>
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Summary</label>
                  <input className="input" value={articleForm.summary} onChange={e => setArticleForm(f => ({ ...f, summary: e.target.value }))} />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Content *</label>
                  <textarea className="input min-h-[160px] resize-y font-mono text-xs" value={articleForm.content} onChange={e => setArticleForm(f => ({ ...f, content: e.target.value }))} />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-600 dark:text-slate-400 mb-1">Tags (comma-separated)</label>
                  <input className="input" placeholder="e.g. funding, VC, seed" value={articleForm.tags} onChange={e => setArticleForm(f => ({ ...f, tags: e.target.value }))} />
                </div>
                <div className="flex gap-3">
                  <button onClick={handleSaveArticle} className="btn-primary"><Check className="w-4 h-4" /> Save</button>
                  <button onClick={() => setEditingArticle(null)} className="btn-outline"><X className="w-4 h-4" /> Cancel</button>
                </div>
              </div>
            )}

            {loading ? (
              <div className="space-y-3">{Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-16" />)}</div>
            ) : (
              <div className="space-y-2">
                {articles.map(a => (
                  <div key={a.id} className="card px-4 py-3 flex items-center justify-between gap-4 hover:border-slate-300 dark:hover:border-slate-600 transition-colors">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 mb-0.5">
                        <Badge variant="category" category={a.category}>{a.category}</Badge>
                      </div>
                      <p className="text-sm font-medium text-slate-800 dark:text-slate-100 truncate">{a.title}</p>
                    </div>
                    <div className="flex gap-2 shrink-0">
                      <button onClick={() => startEditArticle(a)} className="p-1.5 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-teal-500 transition-colors">
                        <Pencil className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDeleteArticle(a.id)} className="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-slate-400 hover:text-red-500 transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Resources Tab */}
        {tab === "resources" && (
          <div className="animate-fade-in">
            <p className="text-sm text-slate-500 dark:text-slate-400 mb-4">{resources.length} resources</p>
            {loading ? (
              <div className="space-y-3">{Array.from({ length: 5 }).map((_, i) => <Skeleton key={i} className="h-14" />)}</div>
            ) : (
              <div className="space-y-2">
                {resources.map(r => (
                  <div key={r.id} className="card px-4 py-3 flex items-center justify-between gap-4">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-2 mb-0.5">
                        <Badge variant="category" category={r.category}>{r.category}</Badge>
                        <span className="text-xs text-slate-400 capitalize">{r.resource_type}</span>
                      </div>
                      <p className="text-sm font-medium text-slate-800 dark:text-slate-100 truncate">{r.title}</p>
                    </div>
                    <button onClick={async () => { if (confirm("Delete?")) { await api.resources.delete(r.id); toast.success("Deleted"); loadAll(); } }}
                      className="p-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 text-slate-400 hover:text-red-500 transition-colors shrink-0">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </main>
      <Footer />
    </div>
  );
}
