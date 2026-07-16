"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import { Mail, Send, CheckCircle } from "lucide-react";
import toast from "react-hot-toast";

export default function ContactPage() {
  const [form, setForm] = useState({ name: "", email: "", subject: "", message: "" });
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.contact.submit(form);
      setSent(true);
      toast.success("Message sent successfully!");
    } catch {
      toast.error("Failed to send message. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (sent) return (
    <div className="max-w-md mx-auto px-4 py-24 text-center animate-fade-in">
      <div className="w-14 h-14 rounded-2xl bg-green-50 dark:bg-green-900/20 flex items-center justify-center mx-auto mb-5">
        <CheckCircle className="w-7 h-7 text-green-500" />
      </div>
      <h2 className="section-heading mb-3">Message Sent!</h2>
      <p className="text-slate-500 dark:text-slate-400">Thanks for reaching out. We'll get back to you shortly.</p>
      <button onClick={() => { setSent(false); setForm({ name: "", email: "", subject: "", message: "" }); }}
        className="btn-outline mt-6">Send another message</button>
    </div>
  );

  return (
    <div className="max-w-xl mx-auto px-4 sm:px-6 lg:px-8 py-14 animate-fade-in">
      <div className="text-center mb-10">
        <div className="w-12 h-12 rounded-2xl bg-teal-50 dark:bg-teal-900/20 flex items-center justify-center mx-auto mb-4">
          <Mail className="w-5 h-5 text-teal-500" />
        </div>
        <h1 className="section-heading mb-2">Contact Us</h1>
        <p className="text-slate-500 dark:text-slate-400">Have a question or suggestion? We'd love to hear from you.</p>
      </div>

      <form onSubmit={handleSubmit} className="card p-6 md:p-8 space-y-5">
        <div className="grid sm:grid-cols-2 gap-5">
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Name *</label>
            <input className="input" required placeholder="Your name"
              value={form.name} onChange={e => setForm(f => ({ ...f, name: e.target.value }))} />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Email *</label>
            <input className="input" type="email" required placeholder="you@example.com"
              value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} />
          </div>
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Subject</label>
          <input className="input" placeholder="What's this about?"
            value={form.subject} onChange={e => setForm(f => ({ ...f, subject: e.target.value }))} />
        </div>
        <div>
          <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1.5">Message *</label>
          <textarea className="input min-h-[140px] resize-none" required placeholder="Your message…"
            value={form.message} onChange={e => setForm(f => ({ ...f, message: e.target.value }))} />
        </div>
        <button type="submit" disabled={loading} className="btn-primary w-full justify-center">
          {loading ? "Sending…" : <><Send className="w-4 h-4" /> Send Message</>}
        </button>
      </form>
    </div>
  );
}
