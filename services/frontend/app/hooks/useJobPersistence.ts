const STORAGE_KEY = "karaoke_job_id";

export function getPersistedJobId(): string | null {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch (error) {
    console.error("Failed to retrieve persisted job id:", error);
  }
  return null;
}

export function savePersistedJobId(jobId: string): void {
  try {
    localStorage.setItem(STORAGE_KEY, jobId);
  } catch (error) {
    console.error("Failed to save job id:", error);
  }
}

export function clearPersistedJobId(): void {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error("Failed to clear job id:", error);
  }
}
