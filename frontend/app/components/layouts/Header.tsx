import {
  Avatar,
  Button,
  Dropdown,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  Navbar,
  NavbarBrand,
} from "flowbite-react";
import { TextInput } from "flowbite-react";
import { FaLocationDot } from "react-icons/fa6";

import { FaSearch } from "react-icons/fa";
import Image from "next/image";
export default function Header() {
  const dropdownOptions = [
    "Hand Tools",
    "Power Tools",
    "Outdoor & Garden",
    "Hammers",
    "Sports",
  ];
  return (
    <Navbar fluid rounded>
      <NavbarBrand href="/">
        <Image
          height={36}
          width={36}
          src="/favicon.png"
          className="mr-3 rounded"
          alt="ToolShed Logo"
        />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
          ToolShed
        </span>
      </NavbarBrand>

      <div className="flex order-2 md:order-none gap-4 place-items-center justify-center items-center">
        <TextInput
          type="text"
          icon={FaSearch}
          placeholder="What are you looking for?"
        />

        <Dropdown inline label="All categories">
          {dropdownOptions.map((option) => (
            <DropdownItem key={option}>{option}</DropdownItem>
          ))}
        </Dropdown>
        <div className="hidden sm:flex flex-row place-items-center gap-2 ">
          <div className="rounded-full opacity-80 p-2 bg-brand">
            <FaLocationDot></FaLocationDot>
          </div>
          <div className=" text-sm">Calgary, Alberta</div>
        </div>
      </div>
      <div className="flex  gap-4">
        <Dropdown
          inline
          label={
            <Avatar
              alt="User settings"
              img="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
              rounded
            />
          }
        >
          <DropdownHeader>
            <span className="block text-sm">Bonnie Green</span>
            <span className="block truncate text-sm font-medium">
              name@flowbite.com
            </span>
          </DropdownHeader>
          <DropdownItem>My Profile</DropdownItem>
          <DropdownItem>Requested Tools</DropdownItem>
          <DropdownItem>Active Listings</DropdownItem>
          <DropdownItem>Disputes</DropdownItem>
          <DropdownDivider />
          <DropdownItem>Sign out</DropdownItem>
        </Dropdown>
        <Button color="primary">List Items</Button>
      </div>
    </Navbar>
  );
}
