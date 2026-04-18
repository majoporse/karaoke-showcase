import { Music, Moon, Sun } from "lucide-react";
import { Link } from "react-router";
import { useTheme } from "../../contexts/ThemeContext";
import { useEffect, useState } from "react";

export function Header() {
  const { theme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <header className="w-full border-b border-blue-200/30 dark:border-white/20 bg-gradient-to-br from-white/40 via-blue-50/20 to-white/40 dark:from-white/10 dark:via-white/5 dark:to-white/10 backdrop-blur-md sticky top-0 z-40 shadow-sm">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3 hover:opacity-80 transition-opacity">
          <div
            className="flex items-center justify-center w-10 h-10 rounded-lg shadow-lg"
            style={{
              background:
                "linear-gradient(to bottom right, var(--brand-primary), var(--brand-secondary))",
              boxShadow:
                "0 10px 15px -3px color-mix(in srgb, var(--brand-primary) 30%, transparent)",
            }}
          >
            <Music className="w-5 h-5 text-white" strokeWidth={2.5} />
          </div>
          <div className="flex flex-col">
            <h1
              className="text-lg font-semibold bg-clip-text text-transparent"
              style={{
                background:
                  "linear-gradient(to right, var(--brand-primary), var(--brand-secondary))",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              SingSync
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400 -mt-0.5">Voice Separator</p>
          </div>
        </Link>
        <nav className="flex items-center gap-6">
           <Link
             to="/create"
             className="text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
           >
             Create
           </Link>
           <Link
             to="/search"
             className="text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
           >
             Search
           </Link>
          {mounted && (
            <button
              onClick={toggleTheme}
              className="w-10 h-10 rounded-lg bg-gradient-to-br from-white/30 via-blue-50/20 to-white/30 dark:from-white/10 dark:via-white/5 dark:to-white/10 border border-blue-200/40 dark:border-white/20 hover:border-blue-300/60 dark:hover:border-white/30 backdrop-blur-sm transition-all flex items-center justify-center"
              aria-label="Toggle dark mode"
            >
              {theme === "light" ? (
                <Moon className="w-4 h-4 text-slate-700" />
              ) : (
                <Sun className="w-4 h-4 text-slate-300" />
              )}
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}
