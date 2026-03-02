import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Logo } from "./components/ui/logo";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Banner } from "./components/banner";


const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Ethan's Job Finder",
  description: "Finding the right job for you",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <header className="p-4 border border-b-3 flex items-center justify-between px-6">
          <Logo />

          <div className="flex items-center gap-3">
            <Link href="/auth">
              <Button type="button">Sign in</Button>
            </Link>

            <Link href="/auth">
              <Button type="button">Get Started</Button>
            </Link>
          </div>
        </header>

        <Banner storageKey="dashboard-welcome" chip="Hey There!" className="mt-4">
          JobFinder is in Alpha. Users may experience bugs or unexpected behavior
        </Banner>

        {children}
      </body>
    </html>
  );
}
