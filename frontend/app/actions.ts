"use server";
import { Session } from "next-auth";
import { redirect } from "next/navigation";

const CREATE_USER_URL =
  "https://gporbws4heru7rlgqtgbfegx4a0svrhp.lambda-url.ca-central-1.on.aws/";

const GET_USER_URL =
  "https://v5ezikbdjg4hadx5mqmundbaxq0zjdnj.lambda-url.ca-central-1.on.aws/";

export const createListing = async (formData: FormData) => {
  const rawFormData = Object.fromEntries(formData.entries());
  //   parse and Send to API endpoint
  console.log(rawFormData);
  redirect("/");
};

export const createUser = async (name: string, email: string) => {
  const body = {
    name: name,
    email: email,
    rating: null,
    bio: null,
    location: null,
  };
  const response = await fetch(CREATE_USER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return response.json();
};

export const getUser = async (email: string) => {
  const body = {
    email: email,
  };
  console.log(body);
  const response = await fetch(GET_USER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  console.log(response.json());
  return response.json();
};

export const authenticateUser = async (session: Session) => {
  const user = await getUser(session.user?.email || "");
  if (user) {
    return user;
  } else {
    if (session.user?.name && session.user?.email) {
      return createUser(session.user.name, session.user.email);
    }
  }
};
