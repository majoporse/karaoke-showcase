import { useQuery } from "@tanstack/react-query";
import { StorageApi } from "clients/orchestrator/api";
import { config } from "~/configs";

interface PresignedUrls {
  vocalsUrl?: string;
  accompanimentUrl?: string;
}

export function usePresignedUrls(vocalsPath?: string | null, accompanimentPath?: string | null) {
  const storageApi = new StorageApi(config);

  return useQuery({
    queryKey: ["presignedUrls", vocalsPath, accompanimentPath],
    queryFn: async (): Promise<PresignedUrls> => {
      if (!vocalsPath || !accompanimentPath) {
        throw new Error("Missing audio paths");
      }

      const [vocalsResponse, accompanimentResponse] = await Promise.all([
        storageApi.presignUrlPresignGet(vocalsPath),
        storageApi.presignUrlPresignGet(accompanimentPath),
      ]);

      return {
        vocalsUrl: vocalsResponse.data.url,
        accompanimentUrl: accompanimentResponse.data.url,
      };
    },
    enabled: !!(vocalsPath && accompanimentPath),
  });
}
