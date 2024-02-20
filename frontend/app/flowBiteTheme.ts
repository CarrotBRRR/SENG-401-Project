import { CustomFlowbiteTheme } from "flowbite-react";

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
  label: {
    root: {
      base: "",
      disabled: "",
      colors: {
        default: "",
        disabled: "",
        error: "",
        success: "",
      },
    },
  },
};

export default customTheme;
