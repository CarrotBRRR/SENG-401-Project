import React from "react";
import { DetailField } from "./DetailField";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/utils/authOptions";

export default async function ContactDetails() {
  const session = await getServerSession(authOptions);
  const phoneNum = "123-456-7890";
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-xl font-medium">Contact Details</h1>
      <div className="flex flex-col gap-4 text-black dark:text-white">
        <DetailField title={"phoneNum"} value={phoneNum} />
        <DetailField title={"email"} value={session?.user?.email} />
      </div>
    </div>
  );
}
