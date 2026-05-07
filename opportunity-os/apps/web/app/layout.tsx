import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "OPPORTUNITY OS",
  description: "Autonomous business-opportunity detection & launch platform.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen font-sans antialiased">{children}</body>
    </html>
  );
}
