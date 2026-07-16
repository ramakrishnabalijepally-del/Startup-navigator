"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/components/providers/AuthProvider";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import type { DashboardData } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { StatCardSkeleton, Skeleton } from "@/components/ui/Skeleton";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Search, TrendingUp, Clock, BarChart2, MessageSquare } from "lucide-react";
import { formatRelative } from "@/lib/utils";
import Link from "next/link";
import toast from "react-hot-toast";

export default function DashboardPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) router.push("/login");
  }, [user, authLoading, router]);

  useEffect(() => {
    if (!user) return;
    api.dashboard.me()
      .then(d => setData(d as DashboardData))
      .catch(() => toast.error("Failed to load dashboard"))
      .finally(() => setLoading(false));
  }, [user]);

  return (
    <div className="min-h-screen flex flex-col bg-[var(--background)]">
      <Navbar />
      <main className="flex-1 max-w-5xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
        <div className="mb-8">
          <h1 className="section-heading mb-1">
            {user ? `Hi, ${user.full_name?.split(" ")[0] || "there"} 👋` : "Dashboard"}
          </h1>
          <p className="text-slate-500 dark:text-slate-400 text-sm">{user?.email}</p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
          {loading ? (
            Array.from({ length: 3 }).map((_, i) => <StatCardSkeleton key={i} />)
          ) : (
            <>
              <div className="card p-5">
                <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-1">
                  <Search className="w-3.5 h-3.5" /> Total Searches
                </div>
                <div className="text-3xl font-bold text-navy-900 dark:text-white font-heading">
                  {data?.stats.total_searches ?? 0}
                </div>
              </div>
              <div className="card p-5">
                <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-1">
                  <TrendingUp className="w-3.5 h-3.5" /> Top Category
                </div>
                <div className="text-lg font-bold text-navy-900 dark:text-white font-heading">
                  {data?.stats.most_searched_category ?? "—"}
                </div>
              </div>
              <div className="card p-5 col-span-2 md:col-span-1">
                <div className="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-1">
                  <Clock className="w-3.5 h-3.5" /> Last Active
                </div>
                <div className="text-sm font-semibold text-navy-900 dark:text-white">
                  {data?.stats.last_active ? formatRelative(data.stats.last_active) : "No activity yet"}
                </div>
              </div>
            </>
          )}
        </div>

        {/* Search History */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-slate-900 dark:text-white flex items-center gap-2 font-heading">
              <MessageSquare className="w-4 h-4 text-teal-500" /> Search History
            </h2>
            <Link href="/search" className="btn-primary !py-1.5 !px-4 text-xs">New Search</Link>
          </div>

          {loading ? (
            <div className="space-y-3">
              {Array.from({ length: 4 }).map((_, i) => <Skeleton key={i} className="h-24" />)}
            </div>
          ) : !data?.search_history.length ? (
            <div className="card p-10 text-center">
              <BarChart2 className="w-8 h-8 text-slate-300 dark:text-slate-600 mx-auto mb-3" />
              <p className="font-medium text-slate-500 dark:text-slate-400">No search history yet</p>
              <p className="text-sm text-slate-400 mt-1 mb-4">Try asking a question in AI Search</p>
              <Link href="/search" className="btn-primary inline-flex">Start Searching</Link>
            </div>
          ) : (
            <div className="space-y-3">
              {data.search_history.map(item => (
                <div key={item.id} className="card p-4 hover:border-teal-400 dark:hover:border-teal-500 transition-colors">
                  <div className="flex items-start justify-between gap-4">
                    <div className="min-w-0 flex-1">
                      <p className="font-medium text-sm text-slate-900 dark:text-white truncate">{item.query}</p>
                      {item.answer && (
                        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 line-clamp-2">{item.answer}</p>
                      )}
                    </div>
                    <div className="flex flex-col items-end gap-1.5 shrink-0">
                      {item.category_hint && (
                        <Badge variant="category" category={item.category_hint}>{item.category_hint}</Badge>
                      )}
                      <span className="text-xs text-slate-400">{formatRelative(item.created_at)}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
      <Footer />
    </div>
  );
}
