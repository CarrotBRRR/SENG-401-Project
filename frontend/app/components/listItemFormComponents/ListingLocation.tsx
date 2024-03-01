import React from "react";
import { FaLocationDot } from "react-icons/fa6";
import ListingMapContainer from "./ListingMapContainer";
import { Tooltip } from "flowbite-react";
import ListItemFormTemplate from "./ListItemFormTemplate";

export default function ListingLocation() {
  const city = "Calgary";
  const postalCode = "T3A 7V4";
  const province = "AB";
  const location = "Calgary, AB T3A 7V4";

  return (
    <ListItemFormTemplate formNumber={3} formHeader={"Location"}>
      <div className="flex flex-row justify-between items-center place-items-center place-content-center ">
        <div className=" flex flex-col gap-4 text-sm">
          <h2 className="text-brand font-bold ">
            {city}, {postalCode}
          </h2>
          <div className="w-56 h-14 p-2.5 bg-stone-50 rounded border border-zinc-300 justify-start items-center gap-2.5 inline-flex">
            <div className="size-10 flex justify-center items-center place-items-center bg-neutral-200 rounded-full">
              <FaLocationDot className="text-black dark:text-white" />
            </div>
            <div>
              <span className="text-neutral-500 text-xs font-normal">
                Your ad will be posted in
                <br />
              </span>
              <span className="text-neutral-500 text-sm font-bold">{city}</span>
            </div>
          </div>
          <div className="flex flex-row place-items-center gap-2">
            <h3 className="text-brand font-medium ">
              Not the city you want to post in?
            </h3>
            <Tooltip content="You can change your default location in the 'Settings' tab">
              <div className="size-8 flex justify-center items-center place-items-center bg-neutral-200  rounded-full">
                <p className="text-black dark:text-white"> ?</p>
              </div>
            </Tooltip>
          </div>
        </div>
        <ListingMapContainer />
      </div>
      <input className="hidden" name="location" value={location} readOnly />
    </ListItemFormTemplate>
  );
}
