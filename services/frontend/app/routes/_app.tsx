import { Outlet } from "react-router";
import { Header } from "../components/layout/Header";
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

export default function AppLayout() {
  const { theme } = useTheme();
  const [orbPositions, setOrbPositions] = useState<OrbPosition[]>(
    ORBS.map(() => ({ x: 0, y: 0 }))
  );
  const noiseRef = useRef(createNoise2D());
  const timeRef = useRef(0);

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
      className="flex flex-col flex-1 min-h-screen min-w-screen overflow-x-hidden"
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
          className="fixed rounded-full transition-transform duration-100 pointer-events-none"
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
            zIndex: 0,
          }}
        />
      ))}

      <Header />
      <div className="relative z-10 flex-1">
        <Outlet />
      </div>
    </div>
  );
}
