import Link from "next/link";
import { ArrowRight, Search, BookOpen, Zap, Shield, TrendingUp, Users, DollarSign, Scale, Megaphone, Receipt, PiggyBank, Bot, Rocket, Building2 } from "lucide-react";

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  Registration: <Building2 className="w-5 h-5" />,
  Funding:      <DollarSign className="w-5 h-5" />,
  Legal:        <Scale className="w-5 h-5" />,
  Hiring:       <Users className="w-5 h-5" />,
  Branding:     <Zap className="w-5 h-5" />,
  Marketing:    <Megaphone className="w-5 h-5" />,
  Taxation:     <Receipt className="w-5 h-5" />,
  Fundraising:  <PiggyBank className="w-5 h-5" />,
  "AI Tools":   <Bot className="w-5 h-5" />,
  Growth:       <TrendingUp className="w-5 h-5" />,
};

const CATEGORY_COLORS: Record<string, string> = {
  Registration: "from-blue-500 to-blue-600",
  Funding:      "from-green-500 to-green-600",
  Legal:        "from-purple-500 to-purple-600",
  Hiring:       "from-orange-500 to-orange-600",
  Branding:     "from-pink-500 to-pink-600",
  Marketing:    "from-yellow-500 to-yellow-600",
  Taxation:     "from-red-500 to-red-600",
  Fundraising:  "from-teal-500 to-teal-600",
  "AI Tools":   "from-indigo-500 to-indigo-600",
  Growth:       "from-emerald-500 to-emerald-600",
};

const STATS = [
  { label: "Articles & Guides",  value: "20+" },
  { label: "Startup Categories", value: "10" },
  { label: "Topics Covered",     value: "50+" },
  { label: "AI-Powered Search",  value: "✓" },
];

export default function HomePage() {
  return (
    <div className="animate-fade-in">
      {/* Hero */}
      <section className="relative overflow-hidden bg-gradient-to-br from-navy-900 via-navy-800 to-navy-900 text-white">
        <div className="absolute inset-0 opacity-10"
          style={{ backgroundImage: "radial-gradient(circle at 20% 50%, #14B8A6 0%, transparent 50%), radial-gradient(circle at 80% 20%, #6366f1 0%, transparent 40%)" }} />
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-teal-500/20 text-teal-300 text-sm font-medium mb-6 border border-teal-500/30">
              <Rocket className="w-3.5 h-3.5" />
              Your complete startup playbook
            </div>
            <h1 className="text-4xl md:text-6xl font-bold leading-tight mb-6">
              Navigate Your
              <span className="text-teal-400"> Startup Journey</span>
              <br />with Confidence
            </h1>
            <p className="text-lg md:text-xl text-slate-300 mb-8 leading-relaxed max-w-2xl">
              From company registration to fundraising, legal compliance to AI tools —
              everything an Indian founder needs, powered by AI-driven search.
            </p>
            <div className="flex flex-col sm:flex-row gap-3">
              <Link href="/explore" className="btn-primary text-base !px-6 !py-3">
                Explore Topics <ArrowRight className="w-4 h-4" />
              </Link>
              <Link href="/search"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl font-medium text-base border border-white/20 text-white hover:bg-white/10 transition-all duration-200">
                <Search className="w-4 h-4" /> Try AI Search
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-white dark:bg-navy-950 border-b border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {STATS.map(({ label, value }) => (
              <div key={label} className="text-center">
                <div className="text-2xl md:text-3xl font-bold text-teal-500 font-heading">{value}</div>
                <div className="text-sm text-slate-500 dark:text-slate-400 mt-1">{label}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-20">
        <div className="text-center mb-12">
          <h2 className="section-heading mb-3">Explore by Topic</h2>
          <p className="text-slate-500 dark:text-slate-400 max-w-xl mx-auto">
            Deep-dive guides across every stage of your startup journey
          </p>
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {Object.entries(CATEGORY_ICONS).map(([cat, icon]) => (
            <Link key={cat} href={`/explore?category=${cat}`}
              className="card p-5 flex flex-col items-center gap-3 text-center group hover:border-teal-400 dark:hover:border-teal-500 hover:shadow-md transition-all duration-200 hover:-translate-y-1">
              <div className={`w-10 h-10 rounded-xl bg-gradient-to-br ${CATEGORY_COLORS[cat]} flex items-center justify-center text-white group-hover:scale-110 transition-transform duration-200`}>
                {icon}
              </div>
              <span className="text-sm font-medium text-slate-700 dark:text-slate-200">{cat}</span>
            </Link>
          ))}
        </div>
      </section>

      {/* AI Search CTA */}
      <section className="bg-gradient-to-br from-teal-500 to-teal-600 mx-4 sm:mx-6 lg:mx-8 rounded-2xl mb-16 md:mb-20 max-w-7xl lg:mx-auto">
        <div className="px-8 md:px-12 py-12 md:py-16 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="text-white">
            <div className="flex items-center gap-2 text-teal-100 text-sm font-medium mb-3">
              <Bot className="w-4 h-4" /> Powered by Google Gemini
            </div>
            <h2 className="text-2xl md:text-3xl font-bold mb-3 font-heading">
              Ask anything about startups
            </h2>
            <p className="text-teal-100 max-w-md">
              Our AI searches our curated knowledge base and gives you precise, cited answers —
              not generic web results.
            </p>
          </div>
          <Link href="/search"
            className="flex-shrink-0 inline-flex items-center gap-2 px-6 py-3 rounded-xl font-semibold text-teal-600 bg-white hover:bg-teal-50 transition-colors shadow-lg whitespace-nowrap">
            <Search className="w-4 h-4" /> Start Searching
          </Link>
        </div>
      </section>

      {/* Features */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { icon: <BookOpen className="w-5 h-5" />, title: "Expert-Curated Content", desc: "Every guide is written and reviewed for accuracy — covering Indian laws, regulations, and best practices." },
            { icon: <Search className="w-5 h-5" />,   title: "AI-Powered Search", desc: "Ask questions in plain English. Our RAG pipeline retrieves the most relevant content and generates precise answers." },
            { icon: <Shield className="w-5 h-5" />,   title: "Always Up-to-Date", desc: "Admin-managed content ensures guides reflect the latest regulatory changes, budget updates, and market trends." },
          ].map(({ icon, title, desc }) => (
            <div key={title} className="card p-6">
              <div className="w-10 h-10 rounded-xl bg-teal-50 dark:bg-teal-900/20 flex items-center justify-center text-teal-500 mb-4">
                {icon}
              </div>
              <h3 className="font-semibold text-slate-900 dark:text-white mb-2 font-heading">{title}</h3>
              <p className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
