/// <reference types="node" />
import { resolve } from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const rootDir = __dirname;
const srcDir = resolve(rootDir, "src");
const distDir = resolve(rootDir, "dist");
const publicDir = resolve(rootDir, "public");

export default defineConfig({
  root: srcDir,
  publicDir,
  plugins: [react()],
  base: "./",
  build: {
    outDir: distDir,
    emptyOutDir: true,
    cssCodeSplit: false,
    rollupOptions: {
      input: {
        popup: resolve(srcDir, "popup/index.html"),
        options: resolve(srcDir, "options/index.html"),
        history: resolve(srcDir, "history/index.html")
      },
      output: {
        entryFileNames: "assets/[name].js",
        chunkFileNames: "assets/[name].js",
        assetFileNames: (assetInfo: { name?: string }) => {
          if (assetInfo.name?.endsWith(".css")) {
            return "assets/[name]";
          }
          return "assets/[name].[ext]";
        }
      }
    }
  }
});