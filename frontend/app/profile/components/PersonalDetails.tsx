import React from "react";
import Image from "next/image";
import { DetailField } from "./DetailField";
import { getServerSession } from "next-auth";
import { authOptions } from "@/app/utils/authOptions";
import UserLocation from "./UserLocation";
export default async function PersonalDetails() {
  const session = await getServerSession(authOptions);
  const name = session?.user?.name;
  // const city = "Calgary";
  // const city =
  //   navigator.geolocation.getCurrentPosition((position) => {
  //     return position.coords.latitude;
  //   }) || "Calgary";
  const state = "Alberta";

  return (
    <div className="flex flex-col gap-4 ">
      <h1 className="text-xl font-medium">Personal Details</h1>
      <div className="flex flex-row gap-4">
        <Image
          src="/missingImage.jpg"
          alt="profileImage"
          width={180}
          height={200}
          className="rounded-xl object-fill shadow-lg"
        />
        <div className="flex flex-col gap-4 text-black dark:text-white">
          <DetailField title={"Name"} value={name} />
          <UserLocation></UserLocation>
          <DetailField title={"State"} value={state} />
        </div>
      </div>
    </div>
  );
}
