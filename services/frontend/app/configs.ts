import { Configuration } from "clients/orchestrator";

console.warn(import.meta.env.VITE_API_URL);
export const config = new Configuration({
  basePath: import.meta.env.VITE_API_URL,
});

export const s3Config = {
  endpoint: import.meta.env.VITE_MINIO_URL,
  bucket: import.meta.env.VITE_MINIO_BUCKET,
  accessKeyId: import.meta.env.VITE_MINIO_ACCESS_KEY,
  secretAccessKey: import.meta.env.VITE_MINIO_SECRET_KEY,
  region: "us-east-1",
};
console.warn(s3Config);
