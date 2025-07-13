// 💜 MAMA BEAR'S VITE CONFIG - CONNECTING REACT TO TAURI! ⚡
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

// https://vitejs.dev/config/
export default defineConfig(async () => ({
  plugins: [react()],

  // 🚀 Tauri expects a fixed port, disable HMR host check
  server: {
    port: 1420,
    strictPort: true,
    watch: {
      // 💜 Tell Vite to ignore watching src-tauri
      ignored: ["**/src-tauri/**"],
    },
  },

  // 🎯 Path resolution for our beautiful components
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
      "@/components": resolve(__dirname, "./src/components"),
      "@/lib": resolve(__dirname, "./src/lib"),
    },
  },

  // 🌟 Build configuration
  build: {
    // 💜 Tauri uses Chromium on Windows and WebKit on macOS and Linux
    target: process.env.TAURI_ENV_PLATFORM == "windows" ? "chrome105" : "safari13",
    // 🚀 Don't minify for debug builds
    minify: !process.env.TAURI_ENV_DEBUG ? "esbuild" : false,
    // 💜 Produce sourcemaps for debug builds
    sourcemap: !!process.env.TAURI_ENV_DEBUG,
  },
}));
