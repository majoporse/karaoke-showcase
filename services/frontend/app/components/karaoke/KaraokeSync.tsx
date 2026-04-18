"use client";

import { useRef, useState } from "react";
import { KaraokePlayer } from "./KaraokePlayer";
import type { KaraokePlayerRef } from "./KaraokePlayer";
import { LyricsDisplay } from "./LyricsDisplay";
import type { Chunk } from "clients/orchestrator";

interface KaraokeSyncProps {
  vocalsSrc: string | null;
  accompanimentSrc: string | null;
  title: string;
  chunks: Chunk[];
}

export function KaraokeSync({ vocalsSrc, accompanimentSrc, title, chunks }: KaraokeSyncProps) {
  const [currentTime, setCurrentTime] = useState(0);
  const [currentChunkIndex, setCurrentChunkIndex] = useState(0);
  const playerRef = useRef<KaraokePlayerRef>(null);

  return (
    <>
      <KaraokePlayer
        ref={playerRef}
        vocalsSrc={vocalsSrc}
        accompanimentSrc={accompanimentSrc}
        title={title}
        chunks={chunks}
        onTimeUpdate={(time, chunkIndex) => {
          setCurrentTime(time);
          setCurrentChunkIndex(chunkIndex);
        }}
      />
      <LyricsDisplay
        chunks={chunks}
        currentTime={currentTime}
        currentChunkIndex={currentChunkIndex}
        onSeek={(time) => {
          playerRef.current?.seek(time);
        }}
      />
    </>
  );
}
