import type { Route } from "./+types/create";
import { useState, useEffect } from "react";
import { Button } from "../components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { Input } from "../components/ui/input";
import { AudioResult } from "../components/karaoke/AudioResult";
import { ResultSidebar } from "../components/karaoke/ResultSidebar";
import { AlertCircle, Loader2, Youtube, CheckCircle2, XCircle, Clock } from "lucide-react";
import { ProcessingApi } from "clients/orchestrator";
import { config } from "~/configs";
import { useProcessingWebSocket } from "../hooks/useProcessingWebSocket";
import { useQueuePosition } from "../hooks/useQueuePosition";
import ProcessingOutputPayload from "clients/orchestrator-ws/ProcessingOutputPayload";
import ProcessingResult from "clients/orchestrator-ws/ProcessingResult";
import Chunk from "clients/orchestrator-ws/Chunk";
import {
  getPersistedJobId,
  savePersistedJobId,
  clearPersistedJobId,
} from "../hooks/useJobPersistence";
import {
  getPersistedYoutubeUrl,
  saveYoutubeUrl,
  clearYoutubeUrl,
} from "../hooks/useYoutubeUrlPersistence";

export function meta(_: Route.MetaArgs) {
  return [
    { title: "SingSync - Create Karaoke" },
    { name: "description", content: "Extract vocals and accompaniment from any YouTube video" },
  ];
}

function unmarshalChunks(chunks: any[] | undefined): Chunk[] | undefined {
  if (!Array.isArray(chunks)) return chunks;

  return chunks.map((chunk: any) => (chunk instanceof Chunk ? chunk : Chunk.unmarshal(chunk)));
}

function unmarshalProcessingResult(resultData: any): ProcessingResult {
  if (!resultData) return resultData;

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

export default function Create() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [processingError, setProcessingError] = useState<string | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isInQueue, setIsInQueue] = useState(false);

  // Hook to poll queue position every 1 minute
  const { data: queuePosition, isLoading: isLoadingQueue } = useQueuePosition(
    isInQueue ? jobId : null
  );

  // Load persisted jobId and youtubeUrl on mount
  useEffect(() => {
    const persistedJobId = getPersistedJobId();
    if (persistedJobId) {
      const checkJobValidity = async () => {
        try {
          const api = new ProcessingApi(config);
          const response =
            await api.getLatestJobMessageProcessJobJobIdLatestMessageGet(persistedJobId);

          const queuePositionResponse =
            await api.getQueuePositionProcessQueuePositionTaskIdGet(persistedJobId);

          let isInQueue = false;
          if (queuePositionResponse.data && queuePositionResponse.data.position !== undefined) {
            isInQueue = queuePositionResponse.data.position !== null;
            setIsInQueue(isInQueue);
          }

          if (!isInQueue) {
            if (response.data && response.data.message && response.data.message.payload) {
              const payload = unmarshalWebSocketMessage({ payload: response.data.message.payload });

              if (payload.result?.success !== null && payload.result?.success !== undefined) {
                clearYoutubeUrl();
                return;
              }
            } else {
              clearPersistedJobId();
              return;
            }
          }

          setJobId(persistedJobId);
        } catch (err) {
          clearPersistedJobId();
        }
      };

      checkJobValidity();
    }

    const persistedYoutubeUrl = getPersistedYoutubeUrl();
    if (persistedYoutubeUrl) {
      setYoutubeUrl(persistedYoutubeUrl);
    }
  }, []);

  // Connect to WebSocket for real-time updates
  const {
    isConnected,
    state: processingState,
    connect,
    disconnect,
  } = useProcessingWebSocket({
    jobId: jobId,
    onError: (error) => {
      setProcessingError(error);
      setIsInQueue(false);
      disconnect();
    },
    onComplete: (payload: ProcessingOutputPayload) => {
      setIsInQueue(false);
      if (payload.result?.success === true && !payload.result?.error) {
        clearYoutubeUrl();
        clearPersistedJobId();
      } else if (payload.result?.success === false || payload.result?.error) {
        setProcessingError(payload.result?.error || "Processing failed");
      }
      disconnect();
    },
  });

  // Auto-connect to WebSocket when we have a job
  useEffect(() => {
    if (jobId && !isConnected) {
      connect();
    }
  }, [jobId, isConnected, connect]);

  // Update queue status when processing starts (currentStep > 0)
  useEffect(() => {
    if (processingState && processingState.currentStep > 0) {
      setIsInQueue(false);
    }
  }, [processingState?.currentStep]);

  const handleProcess = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (youtubeUrl.trim()) {
      setProcessingError(null);
      setJobId(null);
      setIsSubmitting(true);

      if (isConnected) {
        disconnect();
      }

      try {
        const api = new ProcessingApi(config);
        console.log("Submitting job for:", youtubeUrl.trim());
        const response = await api.queueAudioProcessingProcessQueuePost(youtubeUrl.trim());

        const jobResponse = response.data;

        if (jobResponse.job_id) {
          const newJobId = jobResponse.job_id;
          console.log("Job ID:", newJobId);
          setJobId(newJobId);
          setIsInQueue(true);
          savePersistedJobId(newJobId);
        } else {
          setProcessingError("Failed to get job ID from server");
        }
      } catch (error) {
        const errorMsg = error instanceof Error ? error.message : "Failed to submit job";
        setProcessingError(errorMsg);
      } finally {
        setIsSubmitting(false);
      }
    }
  };

  return (
    <div className="flex flex-1 flex-col">
      <div className="container mx-auto px-4 py-12 lg:py-16">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 lg:gap-12">
          {/* Main content */}
          <div className="lg:col-span-2 space-y-8">
            {/* Hero section */}
            <Card>
              <CardHeader>
                <CardTitle className="text-5xl lg:text-6xl font-light tracking-tight text-slate-900 dark:text-white">
                  Create Your <span className="font-semibold">Karaoke</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-lg text-slate-600 dark:text-slate-400 font-light">
                  Paste a YouTube link and let AI remove the vocals. You'll get the perfect backing
                  track to sing along to.
                </p>
              </CardContent>
            </Card>

            {/* Input section */}
            <Card>
              <CardContent className="pt-6">
                <form onSubmit={handleProcess} className="space-y-4">
                  <div className="relative">
                    <Youtube className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 dark:text-slate-500" />
                    <Input
                      id="url"
                      type="text"
                      placeholder="Paste YouTube song link..."
                      value={youtubeUrl}
                      onChange={(e) => {
                        setYoutubeUrl(e.target.value);
                        saveYoutubeUrl(e.target.value);
                      }}
                      disabled={isSubmitting || !!jobId}
                      className="pl-10"
                      required
                    />
                  </div>

                  {processingError && (
                    <div className="flex gap-3 bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-900 rounded-lg p-4 mt-4">
                      <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm font-medium text-red-900 dark:text-red-200">Error</p>
                        <p className="text-sm text-red-700 dark:text-red-300">{processingError}</p>
                      </div>
                    </div>
                  )}

                  <Button
                    type="submit"
                    disabled={isSubmitting || !!jobId || !youtubeUrl.trim()}
                    className="w-full"
                    size="lg"
                  >
                    {isSubmitting ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Submitting job...
                      </>
                    ) : jobId &&
                      processingState &&
                      processingState.currentStep > 0 &&
                      !processingState.result ? (
                      <>
                        <Loader2 className="mr-2 h-5 w-5 animate-spin" />
                        Creating your karaoke...
                      </>
                    ) : (
                      "Remove Vocals"
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Queue position section - shows when job is queued but not yet processing */}
            {jobId && isInQueue && queuePosition && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide">
                    Queue Status
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex items-start gap-3 p-3 bg-amber-50 dark:bg-amber-950/30 rounded-lg border border-amber-200 dark:border-amber-900">
                    <Clock className="h-5 w-5 text-amber-600 dark:text-amber-400 flex-shrink-0 mt-0.5 animate-pulse" />
                    <div className="flex-1">
                      <p className="text-sm font-medium text-slate-900 dark:text-white">
                        Position in queue:{" "}
                        <span className="font-bold">{queuePosition.position + 1}</span> of{" "}
                        <span className="font-bold">{queuePosition.total_in_queue}</span>
                      </p>
                      <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                        {queuePosition.position === 0
                          ? "Your job is next! Processing will start shortly."
                          : `Waiting for ${queuePosition.position} job${queuePosition.position === 1 ? "" : "s"} ahead to complete.`}
                      </p>
                      {isLoadingQueue && (
                        <p className="text-xs text-slate-500 dark:text-slate-500 mt-1">
                          Updating position...
                        </p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Progress tracking section */}
            {jobId && processingState && processingState.currentStep > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle className="text-sm font-semibold text-slate-900 dark:text-white uppercase tracking-wide">
                    Processing Progress
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Progress bar */}
                  {!processingState.result && (
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-slate-600 dark:text-slate-400">
                          Step {processingState.currentStep} of {processingState.totalSteps}
                        </span>
                        <span className="text-sm font-medium text-slate-900 dark:text-white">
                          {Math.round(
                            (processingState.currentStep / (processingState.totalSteps || 0)) * 100
                          )}
                          %
                        </span>
                      </div>
                      <div className="h-2 bg-slate-200 dark:bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-500 ease-out"
                          style={{
                            width: `${
                              (processingState.currentStep / (processingState.totalSteps || 0)) *
                              100
                            }%`,
                          }}
                        />
                      </div>
                    </div>
                  )}

                  {/* Status message */}
                  {processingState && (
                    <div className="flex items-start gap-3 p-3 bg-blue-50 dark:bg-blue-950/30 rounded-lg border border-blue-200 dark:border-blue-900">
                      {!processingState?.result ? (
                        <Loader2 className="h-5 w-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5 animate-spin" />
                      ) : processingState.result.success === true ? (
                        <CheckCircle2 className="h-5 w-5 text-green-600 dark:text-green-400 flex-shrink-0 mt-0.5" />
                      ) : (
                        <XCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1">
                        <p className="text-sm font-medium text-slate-900 dark:text-white">
                          {processingState.desc}
                        </p>
                        {processingState.result?.error && (
                          <p className="text-sm text-red-600 dark:text-red-400 mt-1">
                            {processingState.result.error}
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Audio result section - delegated to AudioResult component */}
            {processingState && processingState.currentStep > 0 && (
              <AudioResult
                result={processingState.result || null}
                isLoading={!processingState.result}
              />
            )}
          </div>

          {/* Sidebar - Result preview */}
          <div className="lg:col-span-1">
            <ResultSidebar
              result={processingState?.result || null}
              isProcessing={processingState ? processingState.currentStep > 0 : false}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
