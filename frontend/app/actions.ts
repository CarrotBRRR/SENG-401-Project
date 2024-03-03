"use server";
import { redirect } from "next/navigation";

export const createListing = async (formData: FormData) => {
  const rawFormData = Object.fromEntries(formData.entries());
  //   parse and Send to API endpoint
  console.log(rawFormData);
  redirect("/");
};

export const signOut = () => {};
