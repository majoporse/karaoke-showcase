import { Card, CardContent } from "../ui/card";

interface ThumbnailCardProps {
  thumbnailUrl?: string | null;
  youtubeUrl?: string | null;
  title?: string | null;
}

export function ThumbnailCard({ thumbnailUrl, youtubeUrl, title }: ThumbnailCardProps) {
  if (!thumbnailUrl) {
    return null;
  }

  return (
    <Card>
      <CardContent className="pt-6">
        <a
          href={youtubeUrl || "#"}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block group"
        >
          <div className="relative overflow-hidden rounded-lg">
            <img
              src={thumbnailUrl}
              alt={`Thumbnail for ${title || "YouTube video"}`}
              className="w-full h-auto"
            />
            <div className="absolute inset-0 flex items-center justify-center group-hover:bg-black/10 transition-all">
              <svg
                className="w-16 h-16 text-white opacity-0 group-hover:opacity-80 transition-opacity"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M8 5v14l11-7z" />
              </svg>
            </div>
          </div>
        </a>
      </CardContent>
    </Card>
  );
}
