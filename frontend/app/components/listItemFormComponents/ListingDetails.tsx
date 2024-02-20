"use client";
import React from "react";
import { Button, Select, Checkbox, Label, TextInput } from "flowbite-react";
export default function ListingDetails() {
  return (
    <>
      <div className=" flex flex-row place-items-center gap-4">
        <div className=" rounded-lg bg-gray-200 p-2 size-8 justify-center items-center flex">
          1
        </div>
        <div className=" text-xl font-medium text-black ">Listing Details</div>
      </div>
      <div className=" inline-flex flex-row justify-start items-center gap-2.5 whitespace-nowrap text-sm">
        <button className="text-brand font-medium ">Select Category:</button>
        <button className="text-brand font-bold ">
          Buy and Sell {">"} Sporting Goods & Exercise {">"} Ski
        </button>
        <button className="text-blue-500 font-bold ">Change category</button>
      </div>

      <form
        className="flex max-w-md flex-col gap-4"
        onSubmit={(e) => e.preventDefault()}
      >
        <div>
          <div className="mb-2 block font-bold">
            <Label htmlFor="condition" value="Condition: (optional)" />
          </div>
          <Select id="condition">
            <option>-Select-</option>
            <option>New</option>
            <option>Used - Like new</option>
            <option>Used - Good</option>
            <option>Used - Fair</option>
          </Select>
        </div>
        <div>
          <div className="mb-2 block">
            <Label htmlFor="listingTitle" value="Listing title" />
          </div>
          <TextInput id="listingTitle" type="text" required />
        </div>
        <Button type="submit">Submit</Button>
      </form>
    </>
  );
}
