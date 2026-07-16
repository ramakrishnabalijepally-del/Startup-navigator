import { Compass, Target, Zap, Users } from "lucide-react";

export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 animate-fade-in">
      <div className="text-center mb-14">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-teal-500 mb-5">
          <Compass className="w-7 h-7 text-white" />
        </div>
        <h1 className="section-heading mb-4">About Startup Navigator</h1>
        <p className="text-lg text-slate-500 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
          We built Startup Navigator to be the resource we wished existed when we were starting out —
          practical, accurate, and tailored to the Indian startup ecosystem.
        </p>
      </div>

      <div className="grid md:grid-cols-3 gap-6 mb-14">
        {[
          { icon: <Target className="w-5 h-5" />, title: "Our Mission", desc: "Democratise access to startup knowledge. Every founder — regardless of their background or network — deserves clear, actionable guidance on building a company." },
          { icon: <Zap className="w-5 h-5" />,    title: "AI-First Approach", desc: "We combine curated expert content with Google Gemini's AI to give you precise, cited answers — not generic search results or hallucinated advice." },
          { icon: <Users className="w-5 h-5" />,  title: "Who It's For", desc: "First-time founders in India navigating company registration, early-stage startups seeking funding guidance, and growing companies managing compliance." },
        ].map(({ icon, title, desc }) => (
          <div key={title} className="card p-6">
            <div className="w-10 h-10 rounded-xl bg-teal-50 dark:bg-teal-900/20 flex items-center justify-center text-teal-500 mb-4">{icon}</div>
            <h3 className="font-semibold text-slate-900 dark:text-white mb-2 font-heading">{title}</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
          </div>
        ))}
      </div>

      <div className="card p-8 bg-gradient-to-br from-navy-900 to-navy-800 text-white border-0">
        <h2 className="text-xl font-bold mb-3 font-heading">Tech Stack</h2>
        <p className="text-slate-300 text-sm mb-5">Built with modern, production-grade technology:</p>
        <div className="grid sm:grid-cols-2 gap-3">
          {[
            ["Frontend", "Next.js 14 (App Router), TypeScript, Tailwind CSS"],
            ["Backend",  "FastAPI (Python 3.11), SQLAlchemy, Alembic"],
            ["Database", "PostgreSQL on Neon"],
            ["AI / RAG", "LangChain + ChromaDB + Google Gemini (gemini-2.0-flash)"],
            ["Auth",     "JWT (access + refresh tokens), bcrypt, httpOnly cookies"],
            ["Hosting",  "Vercel (frontend) + Render (backend)"],
          ].map(([label, value]) => (
            <div key={label} className="bg-white/5 rounded-xl p-3">
              <div className="text-xs text-teal-400 font-medium mb-0.5">{label}</div>
              <div className="text-sm text-slate-200">{value}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
