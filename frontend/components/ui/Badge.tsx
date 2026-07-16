import { cn } from "@/lib/utils";
import { CATEGORY_COLORS } from "@/lib/types";

interface BadgeProps {
  children: React.ReactNode;
  variant?: "category" | "default" | "success" | "warning";
  category?: string;
  className?: string;
}

export function Badge({ children, variant = "default", category, className }: BadgeProps) {
  const base = "badge";
  const variants = {
    default:  "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
    success:  "bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300",
    warning:  "bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300",
    category: category ? CATEGORY_COLORS[category] ?? CATEGORY_COLORS["Registration"] : "",
  };
  return (
    <span className={cn(base, variants[variant], className)}>
      {children}
    </span>
  );
}
