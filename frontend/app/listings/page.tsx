import React from "react";
import Image from "next/image";
import { FaRegHeart, FaHeart } from "react-icons/fa";
import Link from "next/link";
import { Dropdown, DropdownItem } from "flowbite-react";

const CategoryOptions = () => {
  const categories = [
    "Hand Tools",
    "Power Tools",
    "Outdoor & Garden",
    "Hammers",
  ];
  return (
    <ul className="flex flex-col gap-1">
      {categories.map((category) => (
        <li
          key={category}
          className="rounded-sm p-2 pr-8 bg-[#E9E6F2] shadow cursor-pointer hover:opacity-80"
        >
          <h2 className="text-2xl ">{category}</h2>
        </li>
      ))}
    </ul>
  );
};

const SortListingsButton = () => {
  const dropDownOptions = ["Dashboard", "Settings", "Earnings", "Sign out"];
  return (
    <Dropdown label="Sort by" color="primary">
      {dropDownOptions.map((option) => (
        <DropdownItem key={option}>{option}</DropdownItem>
      ))}
    </Dropdown>
  );
};
const ListingsContainer = () => {
  const listings = [
    {
      itemID: 1,
      title: "Great Value Rising Crust Frozen Pizza, Supreme",
      location: "Calgary | 6 minutes ago",
      description:
        "Vivamus adipiscing nisl ut dolor dignissim semper. Nullaluctus malesuada tincidunt. Class aptent taciti sociosqu ad litora torquent Vivamus adipiscing nisl ut dolor dignissim semper.",
      image: "https://via.placeholder.com/120x120",
    },
    {
      itemID: 2,
      title: "Great Value Rising Crust Frozen Pizza, Supreme",
      location: "Calgary | 6 minutes ago",
      description:
        "Vivamus adipiscing nisl ut dolor dignissim semper. Nullaluctus malesuada tincidunt. Class aptent taciti sociosqu ad litora torquent Vivamus adipiscing nisl ut dolor dignissim semper.",
      image: "https://via.placeholder.com/120x120",
    },
    {
      itemID: 3,
      title: "Great Value Rising Crust Frozen Pizza, Supreme",
      location: "Calgary | 6 minutes ago",
      description:
        "Vivamus adipiscing nisl ut dolor dignissim semper. Nullaluctus malesuada tincidunt. Class aptent taciti sociosqu ad litora torquent Vivamus adipiscing nisl ut dolor dignissim semper.",
      image: "https://via.placeholder.com/120x120",
    },
    {
      itemID: 4,
      title: "Great Value Rising Crust Frozen Pizza, Supreme",
      location: "Calgary | 6 minutes ago",
      description:
        "Vivamus adipiscing nisl ut dolor dignissim semper. Nullaluctus malesuada tincidunt. Class aptent taciti sociosqu ad litora torquent Vivamus adipiscing nisl ut dolor dignissim semper.",
      image: "https://via.placeholder.com/120x120",
    },
  ];
  return (
    <ul className="flex flex-col gap-3 ">
      <div className="flex flex-row justify-between items-center">
        <div className="text-black text-2xl">
          Results 1-{listings.length} of {listings.length}
        </div>
        <SortListingsButton />
        {/* <div className="p-2.5 rounded-xl border border-black flex-col justify-start items-start gap-px inline-flex">
          <div className="text-black text-base">Sort by</div>
          <div className="justify-center items-center inline-flex">
            <div className="text-xl">Posted: newest first</div>
          </div>
        </div> */}
      </div>
      <ul className="flex flex-col gap-1 ">
        {listings.map((listing) => (
          <li
            key={listing.title}
            className=" shadow rounded-lg border border-brand flex flex-row gap-4 p-4"
          >
            <Link href={`listings/${listing.itemID}`}>
              <Image
                width={120}
                height={120}
                src={listing.image}
                alt="listing Image"
                className="rounded"
              />
            </Link>

            <div className=" flex flex-col gap-2">
              <Link href={`listings/${listing.itemID}`}>
                <h1 className="text-gray-950 text-xl font-semibold">
                  {listing.title}
                </h1>
              </Link>

              <h2 className=" text-sm font-bold">{listing.location}</h2>
              <h3 className=" text-gray-600 text-xs font-normal">
                {listing.description}
              </h3>
            </div>
            <FaRegHeart className=" size-8 hover:scale-110 transition duration-300 ease-in-out cursor-pointer" />
          </li>
        ))}
      </ul>
    </ul>
  );
};

export default function page() {
  return (
    <div className="flex flex-row gap-4 text-brand">
      <div className="flex-col gap-4 inline-flex">
        <h1 className="text-2xl font-bold ">Category</h1>
        <CategoryOptions />
      </div>
      <ListingsContainer />
    </div>
  );
}
