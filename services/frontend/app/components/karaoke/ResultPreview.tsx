import { CheckCircle2, AlertCircle } from "lucide-react";
import { Badge } from "../ui/badge";
import type ProcessingResult from "clients/orchestrator-ws/ProcessingResult";

interface ResultPreviewProps {
  result: ProcessingResult | null;
}

export function ResultPreview({ result }: ResultPreviewProps) {
  return (
    <div className="space-y-5">
      {/* Status */}
      <div>
        <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-2">
          Status
        </div>
        <div className="flex items-center gap-2">
          {result ? (
            result.success ? (
              <Badge variant="success" className="gap-1.5">
                <CheckCircle2 className="h-3.5 w-3.5" />
                Success
              </Badge>
            ) : (
              <Badge variant="destructive" className="gap-1.5">
                <AlertCircle className="h-3.5 w-3.5" />
                Failed
              </Badge>
            )
          ) : (
            <Badge variant="outline">No results yet</Badge>
          )}
        </div>
      </div>

      {/* Error */}
      {result?.error && (
        <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-900 rounded-lg p-3">
          <div className="text-xs font-semibold text-red-600 dark:text-red-400 uppercase tracking-wide mb-1">
            Error
          </div>
          <p className="text-xs text-red-700 dark:text-red-300">{result.error}</p>
        </div>
      )}

      {/* Lyrics */}
      {result?.lyrics && typeof result.lyrics === "string" && result.lyrics.length > 0 && (
        <div>
          <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-2">
            Lyrics
          </div>
          <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3 border border-slate-200 dark:border-slate-700 max-h-48 overflow-auto">
            <pre className="text-xs text-slate-700 dark:text-slate-300 font-mono whitespace-pre-wrap break-words leading-relaxed">
              {result.lyrics}
            </pre>
          </div>
        </div>
      )}

      {/* JSON Response */}
      {result && (
        <div>
          <div className="text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide mb-2">
            Raw Response
          </div>
          <details className="group">
            <summary className="cursor-pointer text-xs font-medium text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-300 transition flex items-center gap-1">
              <span className="group-open:rotate-90 transition inline-block">▶</span>
              View JSON
            </summary>
            <div className="bg-slate-50 dark:bg-slate-800 rounded-lg p-3 border border-slate-200 dark:border-slate-700 mt-2 max-h-64 overflow-auto">
              <pre className="text-xs text-slate-700 dark:text-slate-300 font-mono whitespace-pre-wrap break-words leading-relaxed">
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
