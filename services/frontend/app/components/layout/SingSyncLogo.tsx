export function SingSyncLogo() {
  return (
    <div className="relative w-32 h-32 lg:w-48 lg:h-48">
      {/* Animated gradient background */}
      <div
        className="absolute inset-0 rounded-3xl blur-2xl opacity-60 animate-pulse"
        style={{
          background:
            "linear-gradient(to bottom right, var(--brand-primary), var(--brand-secondary), var(--brand-primary-dark))",
        }}
      />

      {/* Main logo container */}
      <div
        className="relative w-full h-full rounded-3xl shadow-2xl flex items-center justify-center overflow-hidden group"
        style={{
          background:
            "linear-gradient(to bottom right, var(--brand-primary), var(--brand-secondary))",
          boxShadow: "0 25px 50px -12px color-mix(in srgb, var(--brand-primary) 50%, transparent)",
        }}
      >
        {/* Animated background pattern */}
        <div className="absolute inset-0 opacity-10">
          <svg className="w-full h-full" viewBox="0 0 200 200">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="200" height="200" fill="url(#grid)" />
          </svg>
        </div>

        {/* Music note icons */}
        <div className="relative flex items-center justify-center gap-2 group-hover:scale-110 transition-transform duration-300">
          {/* Left note */}
          <div className="animate-bounce" style={{ animationDelay: "0s" }}>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="w-12 h-12 lg:w-20 lg:h-20 text-white"
            >
              <path d="M9 18v-13l8-3" />
              <circle cx="6" cy="18" r="3" fill="white" />
              <circle cx="17" cy="15" r="3" fill="white" />
            </svg>
          </div>

          {/* Center accent */}
          <div className="w-1 h-16 lg:h-24 bg-white/50 rounded-full" />

          {/* Right note */}
          <div className="animate-bounce" style={{ animationDelay: "0.2s" }}>
            <svg
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="w-12 h-12 lg:w-20 lg:h-20 text-white"
            >
              <path d="M9 18v-13l8-3" />
              <circle cx="6" cy="18" r="3" fill="white" />
              <circle cx="17" cy="15" r="3" fill="white" />
            </svg>
          </div>
        </div>

        {/* Glow effect */}
        <div
          className="absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"
          style={{
            background: `linear-gradient(to top, color-mix(in srgb, var(--brand-primary-dark) 20%, transparent), transparent)`,
          }}
        />
      </div>
    </div>
  );
}
