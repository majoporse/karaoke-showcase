import type { Chunk } from "clients/orchestrator";
import { KaraokeSync } from "./KaraokeSync";

interface LyricsPreviewSectionProps {
  vocalsSrc: string | null;
  accompanimentSrc: string | null;
  title: string;
  chunks: Chunk[];
}

export function LyricsPreviewSection({
  vocalsSrc,
  accompanimentSrc,
  title,
  chunks,
}: LyricsPreviewSectionProps) {
  if (chunks.length === 0) {
    return null;
  }

  return (
    <div className="space-y-6 pt-4">
      <div className="space-y-4">
        <h2 className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide">
          Lyrics Preview
        </h2>
        <KaraokeSync
          vocalsSrc={vocalsSrc}
          accompanimentSrc={accompanimentSrc}
          title={title}
          chunks={chunks}
        />
      </div>
    </div>
  );
}
