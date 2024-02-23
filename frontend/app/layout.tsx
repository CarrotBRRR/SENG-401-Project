import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "./theme-provider";
import "./globals.css";
import { ThemeSwitcher } from "./components/ThemeSwitcher";
import Header from "./components/layouts/Header";
import Footer from "./components/layouts/Footer";
import { Flowbite } from "flowbite-react";
import customTheme from "./flowBiteTheme";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useTheme } from "next-themes";
import ToastComponent from "./components/ToastComponent";

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
        <Flowbite theme={{ theme: customTheme }}>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <Header></Header>
            <ThemeSwitcher />
            <div className="flex min-h-screen flex-col items-center justify-between p-24">
              {children}
            </div>
            <ToastComponent></ToastComponent>
            <Footer></Footer>
          </ThemeProvider>
        </Flowbite>
      </body>
    </html>
  );
}
