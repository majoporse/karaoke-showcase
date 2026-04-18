"use client";

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Skeleton } from "../ui/skeleton";
import { ResultPreview } from "./ResultPreview";
import type ProcessingResult from "clients/orchestrator-ws/ProcessingResult";

interface ResultSidebarProps {
  result: ProcessingResult | null;
  isProcessing: boolean;
}

export function ResultSidebar({ result, isProcessing }: ResultSidebarProps) {
  return (
    <div className="sticky top-20">
      <Card>
        <CardHeader>
          <CardTitle className="text-sm font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
            Result Details
          </CardTitle>
        </CardHeader>
        <CardContent>
          {result?.success ? (
            <ResultPreview result={result} />
          ) : isProcessing ? (
            <div className="mt-6 space-y-4">
              <Skeleton className="h-32 w-full" />
            </div>
          ) : null}
        </CardContent>
      </Card>
    </div>
  );
}
