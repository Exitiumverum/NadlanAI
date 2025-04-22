import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "NadlanAI - Israeli Real Estate Aggregator",
  description: "Find and compare real estate deals from all major Israeli real estate websites in one place",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="he" dir="rtl">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
