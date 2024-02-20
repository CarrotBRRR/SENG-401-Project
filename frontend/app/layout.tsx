import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "./theme-provider";
import "./globals.css";
import { ThemeSwitcher } from "./components/ThemeSwitcher";
import Header from "./components/layouts/Header";
import Footer from "./components/layouts/Footer";
import { CustomFlowbiteTheme, Flowbite } from "flowbite-react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "ToolShed",
  description: "The tool lending platform",
};
const customTheme: CustomFlowbiteTheme = {
  button: {
    color: {
      primary: " bg-brand hover:bg-red-600",
    },
  },
  datepicker: {
    popup: {
      footer: {
        button: {
          today: "bg-brand text-white hover:opacity-90",
        },
      },
    },
    views: {
      days: {
        items: {
          item: {
            selected:
              "dark:text-white dark:hover:bg-gray-600 bg-brand text-white hover:bg-brand-lighter",
          },
        },
      },
    },
  },
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
            {children}
            <Footer></Footer>
          </ThemeProvider>
        </Flowbite>
      </body>
    </html>
  );
}
