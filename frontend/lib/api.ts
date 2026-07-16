const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type RequestOptions = {
  method?: string;
  body?: unknown;
  headers?: Record<string, string>;
};

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, opts: RequestOptions = {}): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    method: opts.method || "GET",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...opts.headers,
    },
    body: opts.body ? JSON.stringify(opts.body) : undefined,
  });

  if (!res.ok) {
    let message = `Request failed: ${res.status}`;
    try {
      const err = await res.json();
      message = err.detail || message;
    } catch {}
    throw new ApiError(res.status, message);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// Auth
export const api = {
  auth: {
    register: (data: { email: string; password: string; full_name?: string }) =>
      request("/auth/register", { method: "POST", body: data }),
    login: (data: { email: string; password: string }) =>
      request("/auth/login", { method: "POST", body: data }),
    logout: () => request("/auth/logout", { method: "POST" }),
    me: () => request("/auth/me"),
    refresh: () => request("/auth/refresh", { method: "POST" }),
  },

  articles: {
    list: (params?: { category?: string; search?: string; limit?: number; offset?: number }) => {
      const q = new URLSearchParams();
      if (params?.category) q.set("category", params.category);
      if (params?.search) q.set("search", params.search);
      if (params?.limit) q.set("limit", String(params.limit));
      if (params?.offset) q.set("offset", String(params.offset));
      return request(`/articles${q.toString() ? "?" + q : ""}`);
    },
    get: (id: number) => request(`/articles/${id}`),
    create: (data: unknown) => request("/articles", { method: "POST", body: data }),
    update: (id: number, data: unknown) => request(`/articles/${id}`, { method: "PUT", body: data }),
    delete: (id: number) => request(`/articles/${id}`, { method: "DELETE" }),
  },

  resources: {
    list: (params?: { category?: string; resource_type?: string }) => {
      const q = new URLSearchParams();
      if (params?.category) q.set("category", params.category);
      if (params?.resource_type) q.set("resource_type", params.resource_type);
      return request(`/resources${q.toString() ? "?" + q : ""}`);
    },
    create: (data: unknown) => request("/resources", { method: "POST", body: data }),
    update: (id: number, data: unknown) => request(`/resources/${id}`, { method: "PUT", body: data }),
    delete: (id: number) => request(`/resources/${id}`, { method: "DELETE" }),
  },

  search: {
    query: (q: string) => request("/search", { method: "POST", body: { query: q } }),
  },

  dashboard: {
    me: () => request("/dashboard/me"),
  },

  admin: {
    analytics: () => request("/admin/analytics"),
    reindex: () => request("/admin/reindex", { method: "POST" }),
    contacts: () => request("/contact"),
  },

  contact: {
    submit: (data: { name: string; email: string; subject?: string; message: string }) =>
      request("/contact", { method: "POST", body: data }),
  },
};

export { ApiError };
