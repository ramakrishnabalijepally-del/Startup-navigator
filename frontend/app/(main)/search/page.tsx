"use client";

import { useState, useRef, useEffect } from "react";
import { useAuth } from "@/components/providers/AuthProvider";
import { api, ApiError } from "@/lib/api";
import type { SearchResult } from "@/lib/types";
import { Badge } from "@/components/ui/Badge";
import { Send, Bot, User, AlertCircle, Sparkles, Lock, ExternalLink } from "lucide-react";
import { cn, formatRelative } from "@/lib/utils";
import Link from "next/link";
import toast from "react-hot-toast";

interface Message {
  role: "user" | "assistant";
  content: string;
  sources?: SearchResult["sources"];
  timestamp: Date;
  error?: boolean;
}

export default function SearchPage() {
  const { user, loading } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [query, setQuery] = useState("");
  const [searching, setSearching] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const q = query.trim();
    if (!q || searching) return;

    const userMsg: Message = { role: "user", content: q, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setQuery("");
    setSearching(true);

    try {
      const result = await api.search.query(q) as SearchResult;
      setMessages(prev => [...prev, {
        role: "assistant",
        content: result.answer,
        sources: result.sources,
        timestamp: new Date(),
      }]);
    } catch (err) {
      const msg = err instanceof ApiError ? err.message : "Something went wrong. Please try again.";
      setMessages(prev => [...prev, {
        role: "assistant",
        content: msg,
        timestamp: new Date(),
        error: true,
      }]);
      if (err instanceof ApiError && err.status !== 503) toast.error(msg);
    } finally {
      setSearching(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  if (loading) return null;

  if (!user) return (
    <div className="max-w-lg mx-auto px-4 py-24 text-center animate-fade-in">
      <div className="w-14 h-14 rounded-2xl bg-teal-50 dark:bg-teal-900/20 flex items-center justify-center mx-auto mb-5">
        <Lock className="w-6 h-6 text-teal-500" />
      </div>
      <h2 className="section-heading mb-3">Sign in to use AI Search</h2>
      <p className="text-slate-500 dark:text-slate-400 mb-6">Create a free account to ask questions and get AI-powered answers from our startup knowledge base.</p>
      <div className="flex gap-3 justify-center">
        <Link href="/login"  className="btn-outline">Log in</Link>
        <Link href="/signup" className="btn-primary">Sign up free</Link>
      </div>
    </div>
  );

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8 flex flex-col h-[calc(100vh-4rem)] animate-fade-in">
      {/* Header */}
      <div className="mb-6 flex-shrink-0">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-8 h-8 rounded-xl bg-teal-500 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <h1 className="text-xl font-bold text-navy-900 dark:text-white font-heading">AI Search</h1>
        </div>
        <p className="text-sm text-slate-500 dark:text-slate-400 ml-10">
          Ask anything about startups — answers are drawn from our curated knowledge base
        </p>
      </div>

      {/* Chat area */}
      <div className="flex-1 overflow-y-auto space-y-5 pb-4 pr-1">
        {messages.length === 0 && (
          <div className="text-center py-16">
            <Bot className="w-12 h-12 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
            <p className="text-slate-500 dark:text-slate-400 font-medium">Start a conversation</p>
            <p className="text-sm text-slate-400 mt-1 mb-6">Try asking about registration, funding, legal compliance, and more</p>
            <div className="flex flex-wrap gap-2 justify-center">
              {[
                "How do I register a Pvt Ltd company?",
                "What is DPIIT recognition?",
                "How much equity should I give a co-founder?",
                "What is GST for SaaS startups?",
              ].map(q => (
                <button key={q} onClick={() => setQuery(q)}
                  className="text-xs px-3 py-1.5 rounded-full border border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 hover:border-teal-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={cn("flex gap-3 animate-slide-up", msg.role === "user" ? "flex-row-reverse" : "flex-row")}>
            {/* Avatar */}
            <div className={cn("w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center text-white text-xs font-bold",
              msg.role === "user" ? "bg-navy-900 dark:bg-slate-600" : "bg-teal-500")}>
              {msg.role === "user" ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            <div className={cn("max-w-[80%] space-y-2", msg.role === "user" ? "items-end" : "items-start")}>
              <div className={cn("rounded-2xl px-4 py-3 text-sm leading-relaxed",
                msg.role === "user"
                  ? "bg-navy-900 dark:bg-slate-700 text-white rounded-tr-sm"
                  : msg.error
                    ? "bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 border border-red-200 dark:border-red-800 rounded-tl-sm"
                    : "card text-slate-700 dark:text-slate-200 rounded-tl-sm"
              )}>
                {msg.error && <AlertCircle className="w-4 h-4 inline mr-1.5 -mt-0.5" />}
                <span className="whitespace-pre-wrap">{msg.content}</span>
              </div>

              {/* Sources */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="space-y-1.5">
                  <p className="text-xs text-slate-400 font-medium px-1">Sources</p>
                  {msg.sources.map((src, j) => (
                    <div key={j} className="card px-3 py-2 flex items-start gap-2">
                      <Badge variant="category" category={src.category} className="mt-0.5 shrink-0">{src.category}</Badge>
                      <div className="min-w-0">
                        <p className="text-xs font-medium text-slate-700 dark:text-slate-200 truncate">{src.title}</p>
                        {src.excerpt && <p className="text-xs text-slate-400 mt-0.5 line-clamp-2">{src.excerpt}</p>}
                        {src.article_id && (
                          <Link href={`/explore/${src.article_id}`}
                            className="inline-flex items-center gap-1 text-xs text-teal-600 dark:text-teal-400 mt-1 hover:underline">
                            Read article <ExternalLink className="w-3 h-3" />
                          </Link>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              <p className={cn("text-xs text-slate-400 px-1", msg.role === "user" ? "text-right" : "text-left")}>
                {formatRelative(msg.timestamp.toISOString())}
              </p>
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {searching && (
          <div className="flex gap-3 animate-slide-up">
            <div className="w-8 h-8 rounded-full bg-teal-500 flex-shrink-0 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="card px-4 py-3 rounded-tl-sm">
              <div className="flex gap-1 items-center h-4">
                {[0, 1, 2].map(i => (
                  <div key={i} className="w-1.5 h-1.5 rounded-full bg-teal-400 animate-bounce"
                    style={{ animationDelay: `${i * 0.15}s` }} />
                ))}
              </div>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex-shrink-0 pt-4 border-t border-slate-200 dark:border-slate-800">
        <div className="flex gap-3 items-end">
          <textarea
            ref={inputRef}
            className="input flex-1 resize-none min-h-[44px] max-h-32 py-3"
            placeholder="Ask about registration, funding, legal, hiring…"
            value={query}
            onChange={e => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
            disabled={searching}
          />
          <button type="submit" disabled={!query.trim() || searching}
            className="btn-primary !px-4 !py-3 flex-shrink-0">
            <Send className="w-4 h-4" />
          </button>
        </div>
        <p className="text-xs text-slate-400 mt-2">Press Enter to send · Shift+Enter for new line</p>
      </form>
    </div>
  );
}
