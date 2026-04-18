import { useRef, useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import type { Chunk } from "clients/orchestrator";
import { Lock } from "lucide-react";

interface LyricsDisplayProps {
  chunks: Chunk[] | null | undefined;
  currentTime: number;
  currentChunkIndex: number;
  onSeek?: (time: number) => void;
}

const SCROLL_ANIMATION_DURATION = 800; // Duration in milliseconds for custom smooth scroll

export function LyricsDisplay({
  chunks,
  currentTime: _currentTime,
  currentChunkIndex,
  onSeek,
}: LyricsDisplayProps) {
  const LINES_VISIBLE = 5;
  const LINE_HEIGHT = 100;
  const MIDDLE_INDEX = Math.floor(LINES_VISIBLE / 2);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [isAutoScroll, setIsAutoScroll] = useState(true);
  const scrollAnimationRef = useRef<number | null>(null);
  const scrollStartTimeRef = useRef<number | null>(null);
  const scrollStartPositionRef = useRef<number>(0);

  // Easing function for smooth deceleration (cubic ease-out)
  const easeOutCubic = (t: number): number => {
    return 1 - Math.pow(1 - t, 3);
  };

  // Auto-scroll to keep current chunk in the middle with smooth animation
  const handleAutoScroll = () => {
    if (isAutoScroll && scrollContainerRef.current && chunks && chunks.length > 0) {
      const targetPosition = Math.max(
        0,
        currentChunkIndex * LINE_HEIGHT - MIDDLE_INDEX * LINE_HEIGHT
      );

      // Cancel any ongoing animation
      if (scrollAnimationRef.current !== null) {
        cancelAnimationFrame(scrollAnimationRef.current);
      }

      const currentScroll = scrollContainerRef.current.scrollTop;

      // Only animate if we're not already at the target position
      if (Math.abs(currentScroll - targetPosition) > 1) {
        scrollStartPositionRef.current = currentScroll;
        scrollStartTimeRef.current = performance.now();

        const animateScroll = (currentTime: number) => {
          if (scrollStartTimeRef.current === null) return;

          const elapsed = currentTime - scrollStartTimeRef.current;
          const progress = Math.min(elapsed / SCROLL_ANIMATION_DURATION, 1);
          const easedProgress = easeOutCubic(progress);

          const newPosition =
            scrollStartPositionRef.current +
            (targetPosition - scrollStartPositionRef.current) * easedProgress;

          if (scrollContainerRef.current) {
            scrollContainerRef.current.scrollTop = newPosition;
          }

          if (progress < 1) {
            scrollAnimationRef.current = requestAnimationFrame(animateScroll);
          } else {
            scrollAnimationRef.current = null;
            scrollStartTimeRef.current = null;
          }
        };

        scrollAnimationRef.current = requestAnimationFrame(animateScroll);
      }
    }
  };

  // Use effect to handle auto-scrolling
  useEffect(() => {
    handleAutoScroll();
  }, [currentChunkIndex, isAutoScroll, chunks]);

  // Cleanup animation on unmount
  useEffect(() => {
    return () => {
      if (scrollAnimationRef.current !== null) {
        cancelAnimationFrame(scrollAnimationRef.current);
      }
    };
  }, []);

  // Reset to manual scroll when clicking the sync button
  const handleSyncClick = () => {
    setIsAutoScroll(!isAutoScroll);
  };

  if (!chunks || chunks.length === 0) {
    return (
      <Card>
        <CardContent
          className="flex flex-col items-center justify-center"
          style={{ minHeight: `${LINES_VISIBLE * LINE_HEIGHT}px` }}
        >
          <p className="text-sm text-slate-500 dark:text-slate-400">No lyrics available</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide">
            Lyrics
          </CardTitle>
          <button
            onClick={handleSyncClick}
            className={`p-1.5 rounded-md transition-colors text-xs font-medium flex items-center gap-1 ${
              isAutoScroll
                ? "bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300"
                : "bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-slate-600"
            }`}
          >
            <Lock className="h-3 w-3" />
            {isAutoScroll ? "Synced" : "Tap to Sync"}
          </button>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        {/* Lyrics Container - locked when synced, scrollable when desynced */}
        <div
          ref={scrollContainerRef}
          className={`bg-slate-50 dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700 ${
            isAutoScroll ? "overflow-hidden" : "overflow-y-auto"
          }`}
          style={{
            height: `${LINES_VISIBLE * LINE_HEIGHT}px`,
            scrollBehavior: "auto",
          }}
        >
          {chunks.map((chunk, index) => {
            const isCurrentChunk = index === currentChunkIndex;
            const distanceFromCurrent = index - currentChunkIndex;
            // Calculate opacity based on distance from current chunk
            let opacity = 0.4;

            if (isCurrentChunk) {
              opacity = 1; // Current chunk is fully visible
            } else if (Math.abs(distanceFromCurrent) === 1) {
              opacity = 0.7; // Adjacent chunks
            } else if (Math.abs(distanceFromCurrent) === 2) {
              opacity = 0.5; // Two lines away
            }

            return (
              <div
                key={index}
                onClick={() => {
                  onSeek?.(chunk.start);
                  setIsAutoScroll(true);
                }}
                className={`flex items-center px-6 py-4 text-2xl transition-all duration-500 cursor-pointer ${
                  isCurrentChunk
                    ? "font-bold text-white bg-gradient-to-r from-blue-500 to-purple-500 dark:from-blue-400 dark:to-purple-400 rounded-md shadow-lg shadow-blue-500/50 dark:shadow-blue-400/30"
                    : "text-slate-700 dark:text-slate-300 hover:bg-slate-200/50 dark:hover:bg-slate-700/50"
                }`}
                style={{
                  opacity,
                  minHeight: `${LINE_HEIGHT}px`,
                  lineHeight: "1.5",
                  display: "flex",
                  alignItems: "center",
                  wordWrap: "break-word",
                  overflowWrap: "break-word",
                  transition:
                    "opacity 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), background-color 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94), color 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94)",
                }}
              >
                {chunk.text}
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}
