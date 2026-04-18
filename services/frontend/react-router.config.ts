import type { Config } from "@react-router/dev/config";

export default {
  // Configure as SPA (Single Page Application)
  ssr: false,
  // Output the built client files to build directory
  buildDirectory: "build",
} satisfies Config;
