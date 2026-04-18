import { Link } from "react-router";
import { SingSyncLogo } from "../components/layout/SingSyncLogo";
import { ArrowRight, Moon, Sun } from "lucide-react";
import { useTheme } from "../contexts/ThemeContext";
import { useEffect, useState, useRef } from "react";
import { createNoise2D } from "simplex-noise";

interface OrbPosition {
  x: number;
  y: number;
}

interface OrbConfig {
  id: number;
  color: string;
  size: number;
  opacity: number;
  speed: number;
  offset: number;
  initialX: number;
  initialY: number;
}

// Generate 5 orbs with varied properties
const generateOrbs = (): OrbConfig[] => {
  const colors = [
    "rgba(236, 72, 153, 1)",      // Pink
    "rgba(147, 197, 253, 1)",     // Blue
    "rgba(168, 85, 247, 1)",      // Purple
    "rgba(59, 130, 246, 1)",      // Dark Blue
    "rgba(249, 115, 22, 1)",      // Orange
  ];

  const sizes = [200, 280, 360, 440, 480];
  const orbs: OrbConfig[] = [];

  for (let i = 0; i < 5; i++) {
    orbs.push({
      id: i,
      color: colors[i % colors.length],
      size: sizes[i % sizes.length],
      opacity: 0.15 + (Math.random() * 0.25),
      speed: 0.5 + (Math.random() * 1.5),
      offset: Math.random() * 1000,
      initialX: Math.random() * 100,
      initialY: Math.random() * 100,
    });
  }

  return orbs;
};

const ORBS = generateOrbs();

export default function Welcome() {
  const { theme, toggleTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const [orbPositions, setOrbPositions] = useState<OrbPosition[]>(
    ORBS.map(() => ({ x: 0, y: 0 }))
  );
  const noiseRef = useRef(createNoise2D());
  const timeRef = useRef(0);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const animationFrame = setInterval(() => {
      timeRef.current += 0.01;
      const noise = noiseRef.current;

      const newPositions: OrbPosition[] = [];
      for (let i = 0; i < ORBS.length; i++) {
        const orb = ORBS[i];
        const x = noise(timeRef.current * orb.speed + orb.offset, i * 50) * 120;
        const y = noise(i * 50, timeRef.current * orb.speed + orb.offset) * 150;
        newPositions.push({ x, y });
      }
      setOrbPositions(newPositions);
    }, 50);

    return () => clearInterval(animationFrame);
  }, []);

  return (
    <div 
      className="min-h-screen flex items-center justify-center overflow-hidden relative bg-gradient-to-br from-blue-100 via-purple-100 to-blue-100 dark:from-slate-950 dark:via-slate-950 dark:to-slate-950"
      style={{
        backgroundImage: `
          radial-gradient(circle at 50% 50%, ${theme === "light" ? "rgba(59, 130, 246, 0.03)" : "rgba(147, 197, 253, 0.15), rgba(196, 181, 253, 0.08)"} 0%, ${theme === "light" ? "transparent 60%" : "transparent 70%"}),
          linear-gradient(to bottom right, ${theme === "light" ? "rgb(219, 234, 254), rgb(243, 232, 255), rgb(219, 234, 254)" : "rgb(15, 23, 42), rgb(15, 23, 42), rgb(15, 23, 42)"})
        `,
        backgroundAttachment: "fixed",
      }}
    >
      {/* Floating orbs with Perlin noise movement */}
      {ORBS.map((orb) => (
        <div
          key={orb.id}
          className="absolute rounded-full transition-transform duration-100 pointer-events-none"
          style={{
            width: `${orb.size}px`,
            height: `${orb.size}px`,
            background: `radial-gradient(circle, ${orb.color}, rgba(0, 0, 0, 0))`,
            opacity: orb.opacity,
            transform: `translate(${orbPositions[orb.id]?.x || 0}px, ${orbPositions[orb.id]?.y || 0}px)`,
            left: `${orb.initialX}%`,
            top: `${orb.initialY}%`,
            filter: "blur(80px)",
            mixBlendMode: "normal",
          }}
        />
      ))}

      {/* Theme Toggle */}
      {mounted && (
        <button
          onClick={toggleTheme}
          className="fixed top-6 right-6 z-50 w-12 h-12 rounded-lg bg-gradient-to-br from-white/40 via-blue-50/20 to-white/40 dark:from-white/10 dark:via-white/5 dark:to-white/10 border border-blue-200/40 dark:border-white/20 hover:border-blue-300/60 dark:hover:border-white/30 backdrop-blur-md transition-all flex items-center justify-center shadow-sm"
          aria-label="Toggle dark mode"
        >
          {theme === "light" ? (
            <Moon className="w-5 h-5 text-slate-700" />
          ) : (
            <Sun className="w-5 h-5 text-slate-300" />
          )}
        </button>
      )}

      {/* Main content */}
      <div className="relative z-10 flex flex-col items-center text-center max-w-3xl px-4 py-12">
        {/* Logo */}
        <div className="mb-8 lg:mb-12">
          <SingSyncLogo />
        </div>

        {/* Heading */}
        <h1 className="text-5xl lg:text-7xl font-light tracking-tighter mb-6 leading-tight">
          Create Your
          <span
            className="block bg-clip-text text-transparent font-semibold px-1"
            style={{
              background: "linear-gradient(to right, var(--brand-primary), var(--brand-secondary))",
              WebkitBackgroundClip: "text",
              WebkitTextFillColor: "transparent",
              backgroundClip: "text",
            }}
          >
            Karaoke
          </span>
        </h1>

        {/* Description */}
        <p className="text-lg lg:text-2xl text-slate-600 dark:text-slate-300 font-light mb-10 lg:mb-12 leading-relaxed max-w-lg">
          Turn any YouTube song into a perfect karaoke backing track. Remove vocals with AI
          precision and get ready to sing.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row gap-4">
          <Link
            to="/create"
            className="inline-flex items-center gap-2 px-8 py-4 text-lg font-semibold text-white rounded-xl transition-all duration-300 group"
            style={{
              background: "linear-gradient(to right, var(--brand-primary), var(--brand-secondary))",
              boxShadow:
                "0 20px 25px -5px color-mix(in srgb, var(--brand-primary) 50%, transparent)",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow =
                "0 25px 50px -12px color-mix(in srgb, var(--brand-primary) 60%, transparent)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow =
                "0 20px 25px -5px color-mix(in srgb, var(--brand-primary) 50%, transparent)";
            }}
          >
            Start Karaoke
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>

           <Link
             to="/search"
             className="inline-flex items-center gap-2 px-8 py-4 text-lg font-semibold rounded-xl transition-all duration-300 group border-2"
            style={{
              borderColor: "var(--brand-primary)",
              color: "var(--brand-primary)",
              background: "transparent",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background =
                "color-mix(in srgb, var(--brand-primary) 10%, transparent)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = "transparent";
            }}
          >
            Search
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
        </div>
      </div>
    </div>
  );
}
