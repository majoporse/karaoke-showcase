import { useQuery } from "@tanstack/react-query";
import { ProcessingApi } from "clients/orchestrator";
import { config } from "~/configs";

export interface QueuePositionData {
  task_id: string;
  position: number;
  total_in_queue: number;
}

/**
 * Hook to fetch and poll the queue position for a task
 * Automatically refetches every minute (60000ms) when enabled
 * Disables polling when task_id is null or undefined
 */
export function useQueuePosition(taskId: string | null) {
  return useQuery<QueuePositionData>({
    queryKey: ["queuePosition", taskId],
    queryFn: async () => {
      if (!taskId) {
        throw new Error("Task ID is required");
      }

      const api = new ProcessingApi(config);
      const response = await api.getQueuePositionProcessQueuePositionTaskIdGet(taskId);
      return response.data;
    },
    // Only run the query if taskId is provided
    enabled: !!taskId,
    // Refetch every 1 minute (60000ms)
    refetchInterval: 60000,
    // Keep the data while refetching
    staleTime: 30000, // Consider data stale after 30 seconds
    // Retry on failure with exponential backoff
    retry: 2,
    // Don't retry on 404 (task not in queue anymore)
    retryOnMount: true,
  });
}
