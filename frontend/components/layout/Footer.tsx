import Link from "next/link";
import { Compass, Code2, MessageCircle, Globe } from "lucide-react";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-navy-950 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="md:col-span-2">
            <Link href="/" className="flex items-center gap-2 font-heading font-bold text-lg text-navy-900 dark:text-white mb-3">
              <Compass className="w-5 h-5 text-teal-500" />
              Startup <span className="text-teal-500 ml-1">Navigator</span>
            </Link>
            <p className="text-sm text-slate-500 dark:text-slate-400 max-w-xs leading-relaxed">
              Your comprehensive guide to starting, funding, and growing a successful startup in India.
            </p>
          </div>

          {/* Links */}
          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-3">Explore</h4>
            <ul className="space-y-2">
              {["Registration", "Funding", "Legal", "Hiring", "Branding"].map(c => (
                <li key={c}>
                  <Link href={`/explore?category=${c}`}
                    className="text-sm text-slate-500 dark:text-slate-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                    {c}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-slate-900 dark:text-white mb-3">Company</h4>
            <ul className="space-y-2">
              {[
                { href: "/about",   label: "About" },
                { href: "/contact", label: "Contact" },
                { href: "/search",  label: "AI Search" },
                { href: "/resources", label: "Resources" },
              ].map(({ href, label }) => (
                <li key={href}>
                  <Link href={href}
                    className="text-sm text-slate-500 dark:text-slate-400 hover:text-teal-600 dark:hover:text-teal-400 transition-colors">
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-xs text-slate-400">© {new Date().getFullYear()} Startup Navigator. Built for Indian entrepreneurs.</p>
          <div className="flex items-center gap-4">
            <a href="#" className="text-slate-400 hover:text-teal-500 transition-colors"><Code2 className="w-4 h-4" /></a>
            <a href="#" className="text-slate-400 hover:text-teal-500 transition-colors"><MessageCircle className="w-4 h-4" /></a>
            <a href="#" className="text-slate-400 hover:text-teal-500 transition-colors"><Globe className="w-4 h-4" /></a>
          </div>
        </div>
      </div>
    </footer>
  );
}
