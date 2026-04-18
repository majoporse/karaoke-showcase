import { Card, CardContent, CardHeader, CardTitle } from "../ui/card";
import { Separator } from "../ui/separator";

interface LyricsInfoCardProps {
  totalSegments: number;
  fullText?: string;
}

export function LyricsInfoCard({ totalSegments, fullText }: LyricsInfoCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-semibold text-slate-600 dark:text-slate-400 uppercase tracking-wide">
          Lyrics Info
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-xs text-slate-500 dark:text-slate-500 uppercase tracking-wide mb-1">
            Total Segments
          </p>
          <p className="text-slate-900 dark:text-white font-medium">{totalSegments}</p>
        </div>
        {fullText && (
          <>
            <Separator />
            <div>
              <p className="text-xs text-slate-500 dark:text-slate-500 uppercase tracking-wide mb-2">
                Full Text
              </p>
              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed line-clamp-4 overflow-hidden">
                {fullText}
              </p>
            </div>
          </>
        )}
      </CardContent>
    </Card>
  );
}
