"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useTheme } from "next-themes";
import { useAuth } from "@/components/providers/AuthProvider";
import { Sun, Moon, Menu, X, Compass, ChevronDown, LogOut, LayoutDashboard, Shield } from "lucide-react";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import toast from "react-hot-toast";
import { useRouter } from "next/navigation";

const NAV_LINKS = [
  { href: "/",         label: "Home" },
  { href: "/explore",  label: "Explore" },
  { href: "/search",   label: "AI Search" },
  { href: "/resources",label: "Resources" },
  { href: "/about",    label: "About" },
  { href: "/contact",  label: "Contact" },
];

export function Navbar() {
  const pathname = usePathname();
  const { theme, setTheme } = useTheme();
  const { user, logout, loading } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const router = useRouter();

  useEffect(() => setMounted(true), []);

  const handleLogout = async () => {
    await logout();
    toast.success("Logged out");
    router.push("/");
    setUserMenuOpen(false);
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-navy-950/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2 font-heading font-bold text-lg text-navy-900 dark:text-white">
            <Compass className="w-6 h-6 text-teal-500" />
            <span>Startup <span className="text-teal-500">Navigator</span></span>
          </Link>

          {/* Desktop nav */}
          <div className="hidden md:flex items-center gap-6">
            {NAV_LINKS.map(({ href, label }) => (
              <Link
                key={href}
                href={href}
                className={cn(
                  "nav-link",
                  pathname === href && "text-teal-600 dark:text-teal-400 font-semibold"
                )}
              >
                {label}
              </Link>
            ))}
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            {/* Theme toggle */}
            {mounted && (
              <button
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                className="p-2 rounded-lg text-slate-500 hover:text-slate-700 dark:text-slate-400 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                aria-label="Toggle theme"
              >
                {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            )}

            {/* Auth */}
            {!loading && (
              <>
                {user ? (
                  <div className="relative">
                    <button
                      onClick={() => setUserMenuOpen(!userMenuOpen)}
                      className="hidden md:flex items-center gap-2 px-3 py-1.5 rounded-xl text-sm font-medium text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
                    >
                      <div className="w-7 h-7 rounded-full bg-teal-500 flex items-center justify-center text-white text-xs font-bold">
                        {user.email[0].toUpperCase()}
                      </div>
                      <span className="max-w-[120px] truncate">{user.full_name || user.email}</span>
                      <ChevronDown className="w-3 h-3" />
                    </button>
                    {userMenuOpen && (
                      <div className="absolute right-0 top-full mt-2 w-48 card shadow-lg py-1 animate-fade-in">
                        <Link href="/dashboard" onClick={() => setUserMenuOpen(false)}
                          className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800">
                          <LayoutDashboard className="w-4 h-4" /> Dashboard
                        </Link>
                        {user.role === "admin" && (
                          <Link href="/admin" onClick={() => setUserMenuOpen(false)}
                            className="flex items-center gap-2 px-4 py-2 text-sm text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800">
                            <Shield className="w-4 h-4" /> Admin Panel
                          </Link>
                        )}
                        <hr className="my-1 border-slate-200 dark:border-slate-700" />
                        <button onClick={handleLogout}
                          className="w-full flex items-center gap-2 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-slate-50 dark:hover:bg-slate-800">
                          <LogOut className="w-4 h-4" /> Log out
                        </button>
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="hidden md:flex items-center gap-2">
                    <Link href="/login" className="btn-outline !py-1.5 !px-4">Log in</Link>
                    <Link href="/signup" className="btn-primary !py-1.5 !px-4">Sign up</Link>
                  </div>
                )}
              </>
            )}

            {/* Mobile menu toggle */}
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors"
            >
              {mobileOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-navy-950 animate-slide-up">
          <div className="px-4 py-3 space-y-1">
            {NAV_LINKS.map(({ href, label }) => (
              <Link key={href} href={href} onClick={() => setMobileOpen(false)}
                className={cn(
                  "block px-3 py-2 rounded-lg text-sm font-medium transition-colors",
                  pathname === href
                    ? "bg-teal-50 dark:bg-teal-900/20 text-teal-600 dark:text-teal-400"
                    : "text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                )}>
                {label}
              </Link>
            ))}
            <hr className="border-slate-200 dark:border-slate-700 my-2" />
            {user ? (
              <>
                <Link href="/dashboard" onClick={() => setMobileOpen(false)}
                  className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800">
                  Dashboard
                </Link>
                {user.role === "admin" && (
                  <Link href="/admin" onClick={() => setMobileOpen(false)}
                    className="block px-3 py-2 rounded-lg text-sm font-medium text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800">
                    Admin Panel
                  </Link>
                )}
                <button onClick={handleLogout}
                  className="w-full text-left px-3 py-2 rounded-lg text-sm font-medium text-red-600 dark:text-red-400 hover:bg-slate-50 dark:hover:bg-slate-800">
                  Log out
                </button>
              </>
            ) : (
              <div className="flex gap-2 pt-1">
                <Link href="/login" onClick={() => setMobileOpen(false)} className="btn-outline flex-1 justify-center">Log in</Link>
                <Link href="/signup" onClick={() => setMobileOpen(false)} className="btn-primary flex-1 justify-center">Sign up</Link>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}
