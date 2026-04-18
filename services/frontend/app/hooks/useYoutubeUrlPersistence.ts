const YOUTUBE_URL_STORAGE_KEY = "karaoke_youtube_url";

export function getPersistedYoutubeUrl(): string | null {
  try {
    return localStorage.getItem(YOUTUBE_URL_STORAGE_KEY);
  } catch (error) {
    console.error("Failed to get persisted youtube url:", error);
  }
  return null;
}

export function saveYoutubeUrl(youtubeUrl: string): void {
  try {
    localStorage.setItem(YOUTUBE_URL_STORAGE_KEY, youtubeUrl);
  } catch (error) {
    console.error("Failed to save youtube url:", error);
  }
}

export function clearYoutubeUrl(): void {
  localStorage.removeItem(YOUTUBE_URL_STORAGE_KEY);
}
