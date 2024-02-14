import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "./theme-provider";
import "./globals.css";
import { ThemeSwitcher } from "./components/ThemeSwitcher";
import Header from "./components/layouts/Header";
import Footer from "./components/layouts/Footer";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ToolShed",
  description: "The tool lending platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-slate-50 dark:bg-[#0d1117]`}>
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <Header></Header>
          <ThemeSwitcher />
          {children}
          <Footer></Footer>
        </ThemeProvider>
      </body>
    </html>
  );
}