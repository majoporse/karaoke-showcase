interface SearchHeroProps {
  description?: string;
}

export function SearchHero({
  description = "Search through all the karaoke tracks that have been created. Find your favorite songs and start singing!",
}: SearchHeroProps) {
  return (
    <div className="space-y-4">
      <h1 className="text-5xl lg:text-6xl font-light tracking-tight text-slate-900 dark:text-white">
        Browse{" "}
        <span
          className="font-semibold bg-clip-text text-transparent"
          style={{
            background: "linear-gradient(to right, var(--brand-primary), var(--brand-secondary))",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
          }}
        >
          Results
        </span>
      </h1>
      <p className="text-lg text-slate-600 dark:text-slate-300 font-light">{description}</p>
    </div>
  );
}
