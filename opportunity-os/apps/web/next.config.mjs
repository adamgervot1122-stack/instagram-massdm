/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  experimental: { typedRoutes: true },
  env: {
    AGENTS_API_URL: process.env.AGENTS_API_URL || "http://localhost:8000",
  },
};

export default nextConfig;
