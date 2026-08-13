import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig(({ mode }) => ({
  build: {
    minify: mode === "unminified" ? false : true,
    cssMinify: mode === "unminified" ? false : true,
  },
  plugins: [react()],
  resolve: {
    tsconfigPaths: true,
  },
}));
