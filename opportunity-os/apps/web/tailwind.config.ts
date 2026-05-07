import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0B0B12",
        panel: "#11111B",
        border: "#1F1F2E",
        accent: "#A6F0C6",
        accent2: "#7C5CFA",
        text: { DEFAULT: "#E7E7EE", muted: "#8A8AA0" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};

export default config;
