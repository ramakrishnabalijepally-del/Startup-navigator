export type UserRole = "user" | "admin";

export interface User {
  id: number;
  email: string;
  full_name: string | null;
  role: UserRole;
  is_active: boolean;
  created_at: string;
}

export interface Article {
  id: number;
  title: string;
  category: string;
  content?: string;
  summary: string | null;
  tags: string[] | null;
  author: string | null;
  is_published: number;
  created_at: string;
  updated_at?: string | null;
}

export interface Resource {
  id: number;
  title: string;
  category: string;
  url: string;
  description: string | null;
  resource_type: string | null;
  tags: string[] | null;
  is_active: number;
  created_at: string;
  updated_at?: string | null;
}

export interface SourceDoc {
  article_id: number | null;
  title: string;
  category: string;
  excerpt: string | null;
}

export interface SearchResult {
  query: string;
  answer: string;
  sources: SourceDoc[];
  history_id: number;
}

export interface SearchHistoryItem {
  id: number;
  query: string;
  answer: string | null;
  sources: SourceDoc[] | null;
  category_hint: string | null;
  created_at: string;
}

export interface DashboardData {
  user: { id: number; email: string; full_name: string | null };
  stats: {
    total_searches: number;
    most_searched_category: string | null;
    last_active: string | null;
  };
  search_history: SearchHistoryItem[];
}

export interface AdminAnalytics {
  totals: { users: number; articles: number; resources: number; searches: number };
  popular_topics: { category: string; count: number }[];
  recent_searches: { id: number; query: string; user_id: number; created_at: string }[];
}

export const CATEGORIES = [
  "Registration",
  "Funding",
  "Legal",
  "Hiring",
  "Branding",
  "Marketing",
  "Taxation",
  "Fundraising",
  "AI Tools",
  "Growth",
] as const;

export type Category = typeof CATEGORIES[number];

export const CATEGORY_COLORS: Record<string, string> = {
  Registration: "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300",
  Funding:      "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
  Legal:        "bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300",
  Hiring:       "bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-300",
  Branding:     "bg-pink-100 text-pink-700 dark:bg-pink-900/30 dark:text-pink-300",
  Marketing:    "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300",
  Taxation:     "bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300",
  Fundraising:  "bg-teal-100 text-teal-700 dark:bg-teal-900/30 dark:text-teal-300",
  "AI Tools":   "bg-indigo-100 text-indigo-700 dark:bg-indigo-900/30 dark:text-indigo-300",
  Growth:       "bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300",
};
