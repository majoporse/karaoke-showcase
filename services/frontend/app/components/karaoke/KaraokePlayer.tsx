"use client";

import { useRef, useState, forwardRef, useImperativeHandle, useEffect } from "react";
import { Button } from "../ui/button";
import { Card, CardContent } from "../ui/card";
import { Slider } from "../ui/slider";
import { Play, Pause, Volume2, VolumeX } from "lucide-react";
import type { Chunk } from "clients/orchestrator";
import {
  downloadAudioFile,
  createAudioUrl,
  revokeAudioUrl,
} from "../../../src/services/audio/download";

interface KaraokePlayerProps {
  vocalsSrc: string | null;
  accompanimentSrc: string | null;
  title: string;
  chunks?: Chunk[] | null;
  onTimeUpdate?: (time: number, chunkIndex: number) => void;
}

export interface KaraokePlayerRef {
  seek: (time: number) => void;
}

export const KaraokePlayer = forwardRef<KaraokePlayerRef, KaraokePlayerProps>(
  function KaraokePlayer(
    { vocalsSrc, accompanimentSrc, title, chunks, onTimeUpdate }: KaraokePlayerProps,
    ref
  ) {
    const vocalsRef = useRef<HTMLAudioElement>(null);
    const accompanimentRef = useRef<HTMLAudioElement>(null);

    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [vocalsVolume, setVocalsVolume] = useState(1);
    const [accompanimentVolume, setAccompanimentVolume] = useState(1);
    const [vocalsBlobUrl, setVocalsBlobUrl] = useState<string | null>(null);
    const [accompanimentBlobUrl, setAccompanimentBlobUrl] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    // Expose seek method to parent
    useImperativeHandle(ref, () => ({
      seek: (time: number) => {
        if (vocalsRef.current && accompanimentRef.current) {
          vocalsRef.current.currentTime = time;
          accompanimentRef.current.currentTime = time;
        }
      },
    }));

    // Download audio files when paths are provided
    useEffect(() => {
      const downloadFiles = async () => {
        if (!vocalsSrc || !accompanimentSrc) {
          return;
        }

        try {
          setIsLoading(true);

          // Download both files in parallel
          const [vocalsBlob, accompanimentBlob] = await Promise.all([
            downloadAudioFile(vocalsSrc),
            downloadAudioFile(accompanimentSrc),
          ]);

          // Create object URLs from blobs
          const vocalsUrl = createAudioUrl(vocalsBlob);
          const accompanimentUrl = createAudioUrl(accompanimentBlob);
          console.log("Vocals URL:", vocalsUrl);
          console.log("Accompaniment URL:", accompanimentUrl);

          setVocalsBlobUrl(vocalsUrl);
          setAccompanimentBlobUrl(accompanimentUrl);
        } catch (error) {
          console.error("Failed to download audio files:", error);
        } finally {
          setIsLoading(false);
        }
      };

      downloadFiles();

      // Cleanup: revoke URLs on unmount or when paths change
      return () => {
        if (vocalsBlobUrl) {
          revokeAudioUrl(vocalsBlobUrl);
        }
        if (accompanimentBlobUrl) {
          revokeAudioUrl(accompanimentBlobUrl);
        }
      };
    }, [vocalsSrc, accompanimentSrc]);

    // Sync both audio elements
    const togglePlayPause = () => {
      if (vocalsRef.current && accompanimentRef.current) {
        if (isPlaying) {
          vocalsRef.current.pause();
          accompanimentRef.current.pause();
          setIsPlaying(false);
        } else {
          Promise.all([vocalsRef.current.play(), accompanimentRef.current.play()])
            .then(() => {
              setIsPlaying(true);
            })
            .catch((_err) => {
              setIsPlaying(true);
            });
        }
      } else {
        console.error("Missing audio refs");
      }
    };

    const handleTimeUpdate = () => {
      if (vocalsRef.current) {
        setCurrentTime(vocalsRef.current.currentTime);

        // Find current chunk
        if (chunks && chunks.length > 0) {
          const chunkIndex = chunks.findIndex(
            (chunk) =>
              vocalsRef.current!.currentTime >= chunk.start &&
              vocalsRef.current!.currentTime < chunk.end
          );
          if (chunkIndex !== -1) {
            // Notify parent component
            onTimeUpdate?.(vocalsRef.current.currentTime, chunkIndex);
          }
        }
      }
    };

    const handleLoadedMetadata = () => {
      if (vocalsRef.current) {
        setDuration(vocalsRef.current.duration);
      }
      // Sync accompaniment currentTime
      if (accompanimentRef.current && vocalsRef.current) {
        accompanimentRef.current.currentTime = vocalsRef.current.currentTime;
      }
    };

    const handleSeek = (value: number[]) => {
      const newTime = value[0];
      setCurrentTime(newTime);
      if (vocalsRef.current && accompanimentRef.current) {
        vocalsRef.current.currentTime = newTime;
        accompanimentRef.current.currentTime = newTime;
      }
    };

    const handleVocalsVolumeChange = (value: number[]) => {
      const newVolume = value[0];
      setVocalsVolume(newVolume);
      if (vocalsRef.current) {
        vocalsRef.current.volume = newVolume;
      }
    };

    const handleAccompanimentVolumeChange = (value: number[]) => {
      const newVolume = value[0];
      setAccompanimentVolume(newVolume);
      if (accompanimentRef.current) {
        accompanimentRef.current.volume = newVolume;
      }
    };

    const handleEnded = () => {
      setIsPlaying(false);
    };

    const formatTime = (time: number) => {
      if (!isFinite(time)) return "0:00";
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds.toString().padStart(2, "0")}`;
    };

    const _progress = duration > 0 ? (currentTime / duration) * 100 : 0;

    return (
      <Card>
        <CardContent className="pt-6">
          <audio
            ref={vocalsRef}
            src={vocalsBlobUrl || undefined}
            onTimeUpdate={handleTimeUpdate}
            onLoadedMetadata={handleLoadedMetadata}
            onEnded={handleEnded}
          />
          <audio ref={accompanimentRef} src={accompanimentBlobUrl || undefined} />

          <div className="space-y-6">
            {/* Title and Play Button */}
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-white">{title}</h3>
              <Button
                onClick={togglePlayPause}
                disabled={!vocalsBlobUrl || !accompanimentBlobUrl || isLoading}
                size="sm"
                className="h-10 w-10 p-0 rounded-lg text-white border-0 shadow-md transition-all disabled:opacity-50"
                style={{
                  background:
                    "linear-gradient(to right, var(--brand-primary), var(--brand-secondary))",
                  boxShadow:
                    "0 4px 6px -1px color-mix(in srgb, var(--brand-primary) 30%, transparent)",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.boxShadow =
                    "0 4px 12px -1px color-mix(in srgb, var(--brand-primary) 40%, transparent)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.boxShadow =
                    "0 4px 6px -1px color-mix(in srgb, var(--brand-primary) 30%, transparent)";
                }}
              >
                {isPlaying ? <Pause className="h-5 w-5" /> : <Play className="h-5 w-5 ml-0.5" />}
              </Button>
            </div>

            {/* Progress Bar and Time */}
            <div className="flex items-center gap-4">
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400 w-10 text-right">
                {formatTime(currentTime)}
              </span>
              <div className="flex-1">
                <Slider
                  value={[currentTime]}
                  onValueChange={handleSeek}
                  max={duration || 0}
                  step={0.1}
                  disabled={!vocalsBlobUrl || !accompanimentBlobUrl || isLoading}
                />
              </div>
              <span className="text-xs font-medium text-slate-500 dark:text-slate-400 w-10">
                {formatTime(duration)}
              </span>
            </div>

            {/* Volume Controls */}
            <div className="space-y-4">
              {/* Vocals Volume */}
              <div className="flex items-center gap-4">
                <div className="w-16">
                  <label className="text-xs font-medium text-slate-600 dark:text-slate-400 flex items-center gap-2">
                    {vocalsVolume > 0 ? (
                      <Volume2 className="h-4 w-4" />
                    ) : (
                      <VolumeX className="h-4 w-4" />
                    )}
                    Vocals
                  </label>
                </div>
                <div className="flex-1">
                  <Slider
                    value={[vocalsVolume]}
                    onValueChange={handleVocalsVolumeChange}
                    max={1}
                    step={0.05}
                    disabled={!vocalsBlobUrl || isLoading}
                  />
                </div>
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400 w-10 text-right">
                  {Math.round(vocalsVolume * 100)}
                </span>
              </div>

              {/* Background/Accompaniment Volume */}
              <div className="flex items-center gap-4">
                <div className="w-16">
                  <label className="text-xs font-medium text-slate-600 dark:text-slate-400 flex items-center gap-2">
                    {accompanimentVolume > 0 ? (
                      <Volume2 className="h-4 w-4" />
                    ) : (
                      <VolumeX className="h-4 w-4" />
                    )}
                    Karaoke
                  </label>
                </div>
                <div className="flex-1">
                  <Slider
                    value={[accompanimentVolume]}
                    onValueChange={handleAccompanimentVolumeChange}
                    max={1}
                    step={0.05}
                    disabled={!accompanimentBlobUrl || isLoading}
                  />
                </div>
                <span className="text-xs font-medium text-slate-500 dark:text-slate-400 w-10 text-right">
                  {Math.round(accompanimentVolume * 100)}
                </span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }
);
