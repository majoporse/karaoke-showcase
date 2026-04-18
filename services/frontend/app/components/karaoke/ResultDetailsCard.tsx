import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";

interface ResultDetailsProps {
  resultId?: string;
  createdAt?: string | null;
}

export function ResultDetailsCard({ resultId, createdAt }: ResultDetailsProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
          Result Details
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-xs text-slate-500 dark:text-slate-500 uppercase tracking-wide mb-1">
            ID
          </p>
          <p className="text-sm font-mono text-slate-900 dark:text-white break-all">
            {resultId}
          </p>
        </div>
        <div>
          <p className="text-xs text-slate-500 dark:text-slate-500 uppercase tracking-wide mb-1">
            Created
          </p>
          <p className="text-sm text-slate-900 dark:text-white">
            {createdAt ? new Date(createdAt).toLocaleDateString() : "Unknown"}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
