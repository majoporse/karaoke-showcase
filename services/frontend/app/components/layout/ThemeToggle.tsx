import { Moon, Sun } from "lucide-react";
import { useTheme } from "../contexts/ThemeContext";
import { useEffect, useState } from "react";

function ThemeToggleContent() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      onClick={toggleTheme}
      className="fixed top-6 right-6 z-50 w-12 h-12 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors flex items-center justify-center shadow-lg"
      aria-label="Toggle dark mode"
    >
      <div className="flex items-center justify-center">
        {theme === "light" ? (
          <Moon className="w-5 h-5 text-slate-700" />
        ) : (
          <Sun className="w-5 h-5 text-slate-400" />
        )}
      </div>
    </button>
  );
}

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Only render after hydration to avoid context errors during SSR
  if (!mounted) {
    return null;
  }

  return <ThemeToggleContent />;
}
