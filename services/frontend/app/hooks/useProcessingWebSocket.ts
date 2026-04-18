import { useEffect, useRef, useCallback, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { WebSocket } from "partysocket";
import { ProcessingApi } from "clients/orchestrator";
import ProcessingOutputPayload from "clients/orchestrator-ws/ProcessingOutputPayload";
import ProcessingResult from "clients/orchestrator-ws/ProcessingResult";
import Chunk from "clients/orchestrator-ws/Chunk";
import JobProgressSubscriptionMessage from "clients/orchestrator-ws/JobProgressSubscriptionMessage";
import { config } from "~/configs";

interface UseProcessingWebSocketOptions {
  jobId: string | null;
  onMessage?: (payload: ProcessingOutputPayload) => void;
  onError?: (error: string) => void;
  onComplete?: (payload: ProcessingOutputPayload) => void;
}

function unmarshalChunks(chunks: any[] | undefined): Chunk[] | undefined {
  if (!Array.isArray(chunks)) return chunks;

  return chunks.map((chunk: any) => (chunk instanceof Chunk ? chunk : Chunk.unmarshal(chunk)));
}

function unmarshalProcessingResult(resultData: any): ProcessingResult {
  if (!resultData) return resultData;

  // Ensure chunks are properly unmarshalled
  if (resultData.chunks) {
    resultData.chunks = unmarshalChunks(resultData.chunks);
  }

  return ProcessingResult.unmarshal(resultData);
}

function unmarshalWebSocketMessage(rawMessage: any): ProcessingOutputPayload {
  const message = ProcessingOutputPayload.unmarshal(rawMessage.payload);

  if (message.result && typeof message.result === "object") {
    message.result = unmarshalProcessingResult(message.result);
  }

  return message;
}

export function useProcessingWebSocket(options: UseProcessingWebSocketOptions) {
  const wsRef = useRef<InstanceType<typeof WebSocket> | null>(null);
  const [isConnecting, setIsConnecting] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const [state, setState] = useState<ProcessingOutputPayload | null>(null);

  // Store callbacks in refs to avoid dependency issues
  const onMessageRef = useRef(options.onMessage);
  const onErrorRef = useRef(options.onError);
  const onCompleteRef = useRef(options.onComplete);

  useEffect(() => {
    onMessageRef.current = options.onMessage;
    onErrorRef.current = options.onError;
    onCompleteRef.current = options.onComplete;
  }, [options.onMessage, options.onError, options.onComplete]);

  const fetchInitialState = useCallback(async () => {
    if (!options.jobId || state) {
      return;
    }

    try {
      const api = new ProcessingApi(config);
      const response = await api.getLatestJobMessageProcessJobJobIdLatestMessageGet(options.jobId);

      if (response.data && response.data.message && response.data.message.payload) {
        const payload = unmarshalWebSocketMessage({ payload: response.data.message.payload });
        setState(payload);
        onMessageRef.current?.(payload);

        if (payload.result?.success !== null && payload.result?.success !== undefined) {
          onCompleteRef.current?.(payload);
        }
      }
    } catch (err) {
      console.error(err);
    }
  }, [options.jobId, state]);

  useEffect(() => {
    fetchInitialState();
  }, [options.jobId, state]);

  const connect = useCallback(() => {
    if (!options.jobId) {
      return;
    }

    if (wsRef.current?.readyState === WebSocket.OPEN) {
      return;
    }

    setIsConnecting(true);

    const apiUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
    const wsUrl =
      apiUrl.replace("http://", "ws://").replace("https://", "wss://").replace(/\/$/, "") +
      `/ws/job-progress/${options.jobId}`;

    try {
      wsRef.current = new WebSocket(wsUrl, [], {
        maxRetries: 5,
        minReconnectionDelay: 1000,
        maxReconnectionDelay: 30000,
      });

      wsRef.current.onopen = () => {
        try {
          const subscriptionMessage = new JobProgressSubscriptionMessage({
            payload: null,
          });
          wsRef.current?.send(subscriptionMessage.marshal());
        } catch (err) {
          console.error("Failed to send subscription message:", err);
        }

        setIsConnected(true);
        setIsConnecting(false);
      };

      wsRef.current.onmessage = (event: MessageEvent) => {
        try {
          const rawMessage = JSON.parse(event.data);
          const message = unmarshalWebSocketMessage(rawMessage);

          setState(message);
          onMessageRef.current?.(message);

          if (message.result?.success !== null && message.result?.success !== undefined) {
            onCompleteRef.current?.(message);
          }
        } catch (err) {
          const errorMsg = `Failed to parse message: ${err}`;
          console.error(errorMsg);
          onErrorRef.current?.(errorMsg);
        }
      };

      wsRef.current.onerror = (_event: Event) => {
        const errorMsg = "WebSocket connection error";
        console.error(errorMsg);
        onErrorRef.current?.(errorMsg);
        setIsConnected(false);
        setIsConnecting(false);
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        setIsConnecting(false);
      };
    } catch (err) {
      const errorMsg = `Failed to connect: ${err}`;
      console.error(errorMsg);
      onErrorRef.current?.(errorMsg);
      setIsConnecting(false);
    }
  }, [options.jobId]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
      setIsConnected(false);
    }
  }, []);

  useEffect(() => {
    return () => {
      disconnect();
    };
  }, [options.jobId, disconnect]);

  return {
    isConnecting,
    isConnected,
    state,
    connect,
    disconnect,
  };
}
