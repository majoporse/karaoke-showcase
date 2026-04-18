import { Link } from "react-router";
import type { ProcessingResponse } from "clients/orchestrator";
import { Card } from "../ui/card";
import { Music, Calendar } from "lucide-react";

interface SearchResultItemProps {
  result: ProcessingResponse;
}

export function SearchResultItem({ result }: SearchResultItemProps) {
  return (
    <Link to={`/song-details/${result.id}`} className="block transition-all hover:scale-105 hover:shadow-lg">
      <Card className="p-5">
        <div className="flex items-start gap-4">
          {/* Icon */}
          <div
            className="flex-shrink-0 w-12 h-12 rounded-lg flex items-center justify-center"
            style={{
              background: "linear-gradient(to bottom right, var(--brand-primary), var(--brand-secondary))",
              boxShadow: "0 4px 12px -2px color-mix(in srgb, var(--brand-primary) 30%, transparent)",
            }}
          >
            <Music className="w-6 h-6 text-white" strokeWidth={2} />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-semibold text-slate-900 dark:text-white line-clamp-2 mb-1">
              {result.title}
            </h3>
            <p className="text-sm text-slate-600 dark:text-slate-400 line-clamp-1">{result.uploader}</p>
            <div className="flex items-center gap-1 text-xs text-slate-500 dark:text-slate-500 mt-2">
              <Calendar className="w-3 h-3" />
              {result.created_at ? new Date(result.created_at).toLocaleDateString() : "Unknown date"}
            </div>
          </div>
        </div>
      </Card>
    </Link>
  );
}
