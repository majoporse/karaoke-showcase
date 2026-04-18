import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Skeleton } from "../ui/skeleton";
import { KaraokeSync } from "./KaraokeSync";
import type ProcessingResult from "clients/orchestrator-ws/ProcessingResult";
import { useQuery } from "@tanstack/react-query";
import { config } from "~/configs";
import { StorageApi } from "clients/orchestrator/api";

interface AudioResultProps {
  result: ProcessingResult | null;
  isLoading: boolean;
}

export function AudioResult({ result, isLoading }: AudioResultProps) {
  const storageApi = new StorageApi(config);

  const { isPending: presignLoading, data: presignedUrls } = useQuery({
    queryKey: ["presignedUrls", result?.vocalsPath, result?.accompanimentPath],
    queryFn: async () => {
      if (!result?.vocalsPath || !result?.accompanimentPath) {
        throw new Error("Missing audio paths");
      }

      const [vocalsResponse, accompanimentResponse] = await Promise.all([
        storageApi.presignUrlPresignGet(result.vocalsPath),
        storageApi.presignUrlPresignGet(result.accompanimentPath),
      ]);
      console.log("Vocals URL:", vocalsResponse.data.url);
      console.log("Accompaniment URL:", accompanimentResponse.data.url);

      return {
        vocalsUrl: vocalsResponse.data.url,
        accompanimentUrl: accompanimentResponse.data.url,
      };
    },
    enabled: !!(result?.vocalsPath && result?.accompanimentPath),
  });

  const vocalsUrl = presignedUrls?.vocalsUrl ?? null;
  const accompanimentUrl = presignedUrls?.accompanimentUrl ?? null;

  if (isLoading) {
    return (
      <Card>
        <CardContent className="pt-6 space-y-6">
          <div className="space-y-4">
            <Skeleton className="h-5 w-48" />
            <Skeleton className="h-32 w-full" />
          </div>
          <div className="space-y-4">
            <Skeleton className="h-5 w-32" />
            <div className="space-y-2">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-[90%]" />
              <Skeleton className="h-4 w-[80%]" />
              <Skeleton className="h-4 w-[95%]" />
              <Skeleton className="h-4 w-[85%]" />
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (!vocalsUrl || !accompanimentUrl || presignLoading) {
    return (
      <Card>
        <CardContent className="pt-6">
          <Skeleton className="h-32 w-full" />
        </CardContent>
      </Card>
    );
  }

  // Convert WS chunks to API chunks format
  const convertChunksToApiFormat = (wsChunks: any[] | null | undefined) => {
    if (!wsChunks || !Array.isArray(wsChunks)) return [];
    return wsChunks.map((chunk) => ({
      start: chunk.start,
      end: chunk.end,
      text: chunk.reservedText || chunk.text || "",
    }));
  };

  const chunks = convertChunksToApiFormat(result?.chunks);
  const title = result?.ytMetadata?.title || "Karaoke";

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide">
          Your Karaoke
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <KaraokeSync
          vocalsSrc={vocalsUrl}
          accompanimentSrc={accompanimentUrl}
          title={title}
          chunks={chunks}
        />
      </CardContent>
    </Card>
  );
}
