"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Resource } from "@/lib/types";
import { CATEGORIES, CATEGORY_COLORS } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Skeleton } from "@/components/ui/Skeleton";
import { ExternalLink, Link2, FileText, Wrench, FileCode } from "lucide-react";
import toast from "react-hot-toast";

const TYPE_ICONS: Record<string, React.ReactNode> = {
  link:     <Link2 className="w-4 h-4" />,
  pdf:      <FileText className="w-4 h-4" />,
  tool:     <Wrench className="w-4 h-4" />,
  template: <FileCode className="w-4 h-4" />,
};

export default function ResourcesPage() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState("");

  useEffect(() => {
    api.resources.list(activeCategory ? { category: activeCategory } : undefined)
      .then(data => setResources(data as Resource[]))
      .catch(() => toast.error("Failed to load resources"))
      .finally(() => setLoading(false));
  }, [activeCategory]);

  // Group by category
  const grouped = resources.reduce<Record<string, Resource[]>>((acc, r) => {
    if (!acc[r.category]) acc[r.category] = [];
    acc[r.category].push(r);
    return acc;
  }, {});

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 animate-fade-in">
      <div className="mb-8">
        <h1 className="section-heading mb-2">Resources</h1>
        <p className="text-slate-500 dark:text-slate-400">Curated external tools, templates, and links for founders</p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2 mb-8">
        <button onClick={() => setActiveCategory("")}
          className={`badge px-3 py-1.5 text-sm cursor-pointer transition-all ${!activeCategory ? "bg-navy-900 text-white dark:bg-teal-500" : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"}`}>
          All
        </button>
        {CATEGORIES.map(cat => (
          <button key={cat} onClick={() => setActiveCategory(cat)}
            className={`badge px-3 py-1.5 text-sm cursor-pointer transition-all ${activeCategory === cat ? CATEGORY_COLORS[cat] : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700"}`}>
            {cat}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {Array.from({ length: 9 }).map((_, i) => <Skeleton key={i} className="h-32" />)}
        </div>
      ) : (
        <div className="space-y-10">
          {Object.entries(grouped).map(([category, items]) => (
            <div key={category}>
              <div className="flex items-center gap-3 mb-4">
                <Badge variant="category" category={category} className="text-sm px-3 py-1">{category}</Badge>
                <div className="flex-1 h-px bg-slate-200 dark:bg-slate-800" />
                <span className="text-xs text-slate-400">{items.length} resource{items.length > 1 ? "s" : ""}</span>
              </div>
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {items.map(resource => (
                  <a key={resource.id} href={resource.url} target="_blank" rel="noopener noreferrer"
                    className="card p-4 flex flex-col gap-2 group hover:border-teal-400 dark:hover:border-teal-500 hover:shadow-md transition-all duration-200 hover:-translate-y-1">
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 rounded-lg bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-slate-500 dark:text-slate-400">
                          {TYPE_ICONS[resource.resource_type || "link"] || <Link2 className="w-4 h-4" />}
                        </div>
                        <span className="text-xs text-slate-400 capitalize">{resource.resource_type || "link"}</span>
                      </div>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-teal-500 transition-colors shrink-0 mt-1" />
                    </div>
                    <h3 className="font-medium text-sm text-slate-900 dark:text-white group-hover:text-teal-600 dark:group-hover:text-teal-400 transition-colors leading-snug">
                      {resource.title}
                    </h3>
                    {resource.description && (
                      <p className="text-xs text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2">{resource.description}</p>
                    )}
                  </a>
                ))}
              </div>
            </div>
          ))}
          {Object.keys(grouped).length === 0 && (
            <div className="text-center py-16 text-slate-400">No resources found</div>
          )}
        </div>
      )}
    </div>
  );
}
