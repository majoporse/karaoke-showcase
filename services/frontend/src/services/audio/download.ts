/**
 * Download an audio file from a presigned URL
 * @param url - The presigned URL to the audio file
 * @returns Promise<Blob> The downloaded audio file
 */
export async function downloadAudioFile(url: string): Promise<Blob> {
  // console.warn("Downloading audio file from:", url);
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`Failed to download audio file: ${response.statusText}`);
  }

  return await response.blob();
}

/**
 * Create an object URL for a blob (for use in audio tags)
 */
export function createAudioUrl(blob: Blob): string {
  return URL.createObjectURL(blob);
}

/**
 * Revoke an object URL to free memory
 */
export function revokeAudioUrl(url: string): void {
  URL.revokeObjectURL(url);
}

/**
 * Download audio and return an object URL
 * @param url - The presigned URL to the audio file
 * @returns Promise<string> Object URL for the audio
 */
export async function fetchAudioUrl(url: string): Promise<string> {
  const blob = await downloadAudioFile(url);
  return createAudioUrl(blob);
}
