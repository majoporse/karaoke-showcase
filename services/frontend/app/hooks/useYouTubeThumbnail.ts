export function useYouTubeThumbnail(youtubeUrl?: string | null, customThumbnail?: string | null) {
  const getYouTubeVideoId = (url: string): string | null => {
    const patterns = [
      /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/v\/)([^&\n?#]+)/,
      /^([a-zA-Z0-9_-]{11})$/,
    ];
    for (const pattern of patterns) {
      const match = url.match(pattern);
      if (match) return match[1];
    }
    return null;
  };

  const videoId = youtubeUrl ? getYouTubeVideoId(youtubeUrl) : null;
  const fallbackThumbnail = videoId ? `https://img.youtube.com/vi/${videoId}/hqdefault.jpg` : null;
  const thumbnailUrl = customThumbnail || fallbackThumbnail;

  return {
    videoId,
    thumbnailUrl,
  };
}
