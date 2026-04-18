interface HeroSectionProps {
  title?: string | null;
  uploader?: string | null;
  errorMessage?: string | null;
}

export function HeroSection({ title, uploader, errorMessage }: HeroSectionProps) {
  return (
    <div className="space-y-4">
      <h1 className="text-5xl lg:text-6xl font-light tracking-tight text-slate-900 dark:text-white">
        {title || "Untitled"}
      </h1>
      <p className="text-lg text-slate-600 dark:text-slate-400 font-light">
        by{" "}
        <span className="font-semibold text-slate-900 dark:text-white">
          {uploader || "Unknown artist"}
        </span>
      </p>
      {errorMessage && (
        <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-900 rounded-lg p-3">
          <p className="text-xs text-red-600 dark:text-red-400 uppercase tracking-wide mb-1">
            Error
          </p>
          <p className="text-xs text-red-700 dark:text-red-300">{errorMessage}</p>
        </div>
      )}
    </div>
  );
}
