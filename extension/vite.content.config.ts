/// <reference types="node" />
import { resolve } from "node:path";
import { defineConfig } from "vite";

const rootDir = __dirname;
const srcDir = resolve(rootDir, "src");
const distDir = resolve(rootDir, "dist");

export default defineConfig({
  build: {
    outDir: distDir,
    emptyOutDir: false,
    sourcemap: false,
    lib: {
      entry: resolve(srcDir, "content/index.ts"),
      name: "WebShieldContent",
      formats: ["iife"],
      fileName: () => "content.js"
    },
    rollupOptions: {
      output: {
        inlineDynamicImports: true
      }
    }
  }
});