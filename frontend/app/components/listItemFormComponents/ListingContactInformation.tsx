"use client";
import { Label, TextInput } from "flowbite-react";
import React, { useState } from "react";
import { FaPhone, FaInbox } from "react-icons/fa";

export default function ListingContactInformation() {
  const [phoneNum, setPhoneNum] = useState<string>("");
  const [email, setEmail] = useState<string>("");

  return (
    <div className="flex flex-col gap-4 border p-4 rounded shadow justify-between">
      <div className=" flex flex-row place-items-center gap-4">
        <div className=" rounded-lg bg-gray-200 p-2 size-8 justify-center items-center flex">
          4
        </div>
        <div className=" text-xl font-medium text-black ">
          Contact Information
        </div>
      </div>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="phoneNumber" value="Phone Number: (optional)" />
        </div>
        <div className=" mb-2 block">
          <TextInput
            onChange={(e) => setPhoneNum(e.target.value)}
            value={phoneNum}
            id="phoneNumber"
            icon={FaPhone}
            placeholder="123 456 7890"
            maxLength={11}
            helperText="Your phone number will show up on your listing"
          />
        </div>
      </div>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="email" value="Email: " />
        </div>
        <div className=" mb-2 block">
          <TextInput
            type="email"
            onChange={(e) => setEmail(e.target.value)}
            value={email}
            id="email"
            icon={FaInbox}
            placeholder="john.doe@email.com"
            minLength={8}
            maxLength={30}
            helperText="Your email will show up on your listing"
          />
        </div>
      </div>
    </div>
  );
}
