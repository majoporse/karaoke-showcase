import { useParams, useNavigate } from "react-router";
import { Button } from "../components/ui/button";
import { ArrowLeft } from "lucide-react";
import { useEffect } from "react";
import type { Chunk } from "clients/orchestrator";
import { ProcessingApi } from "clients/orchestrator";
import { useQuery } from "@tanstack/react-query";
import { config } from "~/configs";
import { revokeAudioUrl } from "../../src/services/audio/download";
import { HeroSection } from "../components/karaoke/HeroSection";
import { LyricsPreviewSection } from "../components/karaoke/LyricsPreviewSection";
import { ResultDetailsCard } from "../components/karaoke/ResultDetailsCard";
import { ThumbnailCard } from "../components/karaoke/ThumbnailCard";
import { LyricsInfoCard } from "../components/karaoke/LyricsInfoCard";
import { usePresignedUrls } from "../hooks/usePresignedUrls";
import { useYouTubeThumbnail } from "../hooks/useYouTubeThumbnail";

export default function SongDetailsPage() {
  const { resultId } = useParams<{ resultId: string }>();
  const navigate = useNavigate();

  const api = new ProcessingApi(config);

  const { isPending, isError, data, error } = useQuery({
    queryKey: ["details", resultId],
    queryFn: async () => {
      if (!resultId) {
        throw new Error("Invalid result ID");
      }
      const response = await api.getProcessingResultByIdProcessProcessingIdGet(resultId);
      return response.data;
    },
  });

  const result = data;

  const { data: presignedUrls } = usePresignedUrls(
    result?.vocals_minio_path,
    result?.accompaniment_minio_path
  );

  const vocalsUrl = presignedUrls?.vocalsUrl ?? null;
  const accompanimentUrl = presignedUrls?.accompanimentUrl ?? null;

  useEffect(() => {
    return () => {
      if (vocalsUrl) {
        revokeAudioUrl(vocalsUrl as string);
      }
      if (accompanimentUrl) {
        revokeAudioUrl(accompanimentUrl as string);
      }
    };
  }, [vocalsUrl, accompanimentUrl]);

  const { thumbnailUrl } = useYouTubeThumbnail(result?.youtube_url, result?.thumbnail);

  if (!resultId) {
    return (
      <div className="flex items-center justify-center py-12">
        <p className="text-red-600 dark:text-red-400">Invalid result ID</p>
      </div>
    );
  }

  if (isPending) {
    return (
      <div className="flex items-center justify-center py-12">
        <p className="text-slate-600 dark:text-slate-400">Loading...</p>
      </div>
    );
  }

  if (isError || !result) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <p className="text-red-600 dark:text-red-400 mb-4">
          {error instanceof Error ? error.message : "Result not found"}
        </p>
        <Button onClick={() => navigate("/search")} variant="outline">
          Back to Search
        </Button>
      </div>
    );
  }

  const chunks: Chunk[] = result.lyrics?.chunks ?? [];

  return (
    <div className="container mx-auto px-4 py-12 lg:py-16">
      {/* Back Button */}
      <Button
        onClick={() => navigate("/search")}
        variant="ghost"
        className="mb-8 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white"
      >
        <ArrowLeft className="w-4 h-4 mr-2" />
        Back to Search
      </Button>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
        <div className="lg:col-span-2 space-y-8">
          <HeroSection
            title={result.title || "Untitled"}
            uploader={result.uploader || "Unknown artist"}
            errorMessage={result.error_message}
          />

          <LyricsPreviewSection
            vocalsSrc={vocalsUrl}
            accompanimentSrc={accompanimentUrl}
            title={result.title ?? "Karaoke"}
            chunks={chunks}
          />
        </div>

        {/* Sidebar - Processing Info */}
        <div className="lg:col-span-1">
          <div className="sticky top-20 space-y-6">
            <ResultDetailsCard resultId={result.id} createdAt={result.created_at} />

            {thumbnailUrl && (
              <ThumbnailCard
                thumbnailUrl={thumbnailUrl}
                youtubeUrl={result.youtube_url}
                title={result.title}
              />
            )}

            {chunks.length > 0 && (
              <LyricsInfoCard totalSegments={chunks.length} fullText={result.lyrics?.full_text} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
