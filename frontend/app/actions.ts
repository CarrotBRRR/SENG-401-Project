"use server";
import { Session } from "next-auth";
import { redirect } from "next/navigation";

const CREATE_USER_URL =
  "https://gporbws4heru7rlgqtgbfegx4a0svrhp.lambda-url.ca-central-1.on.aws/";

const GET_USER_URL =
  "https://v5ezikbdjg4hadx5mqmundbaxq0zjdnj.lambda-url.ca-central-1.on.aws/";

const CREATE_LISTING_URL =
  "https://evieebr3t3elnuixwsaa32lp7m0fbfre.lambda-url.ca-central-1.on.aws/";
export const createListing = async (formData: FormData) => {
  const rawFormData = Object.fromEntries(formData.entries());
  // const rawFormData = {
  //   category: "Other",
  //   condition: "New",
  //   listingTitle: "test",
  //   description: "asd",
  //   tags: "[]",
  //   images: "",
  //   location: "Calgary, AB T3A 7V4",
  //   lenderID: "536b23e7-6546-4c53-8b0b-6a48ea3ad6b6",
  // };
  //   parse and Send to API endpoint
  console.log(rawFormData);
  const response = await fetch(CREATE_LISTING_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(rawFormData),
  });
  console.log(await response.json());
  // return response.json();
  // redirect("/");
};

export const createUser = async (name: string, email: string) => {
  const body = {
    name: name,
    email: email,
    rating: null,
    bio: null,
    location: null,
    phoneNumber: null,
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
  const response = await fetch(GET_USER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return response;
};

export const authenticateUser = async (session: Session) => {
  const res = await getUser(session.user?.email || "");
  if (res.ok) {
    return res;
  } else {
    if (session.user?.name && session.user?.email) {
      const newRes = await createUser(session.user.name, session.user.email);
      return newRes;
    }
  }
};
export const requestItem = async (formData: FormData) => {
  const rawFormData = Object.fromEntries(formData.entries());
  console.log(rawFormData);
  // send to API endpoint
  redirect("/");
};
