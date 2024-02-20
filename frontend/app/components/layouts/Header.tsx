import {
  Avatar,
  Button,
  Dropdown,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  Navbar,
  NavbarBrand,
  NavbarCollapse,
  NavbarLink,
  NavbarToggle,
} from "flowbite-react";
import { Label, TextInput } from "flowbite-react";
import { FaLocationDot } from "react-icons/fa6";

import { FaSearch } from "react-icons/fa";
import Image from "next/image";
export default function Header() {
  return (
    <Navbar fluid rounded>
      <NavbarBrand href="/">
        <Image
          height={36}
          width={36}
          src="/favicon.svg"
          className="mr-3 h-6 sm:h-9"
          alt="ToolShed Logo"
        />
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">
          ToolShed
        </span>
      </NavbarBrand>
      <div className="flex md:order-2 gap-4">
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
        <Button className=" bg-brand">List Items</Button>

        <NavbarToggle />
      </div>
      <div className="flex gap-4 place-items-center">
        <TextInput
          type="text"
          icon={FaSearch}
          placeholder="What are you looking for?"
        />

        <Dropdown inline label="All categories">
          <DropdownItem>Hand Tools</DropdownItem>{" "}
          <DropdownItem>Power Tools</DropdownItem>{" "}
          <DropdownItem>Outdoor & Garden</DropdownItem>{" "}
          <DropdownItem>Hammers</DropdownItem>
          <DropdownItem>Sports</DropdownItem>
        </Dropdown>
        <div className=" flex flex-row place-items-center gap-2">
          <div className="rounded-full opacity-80 p-2 bg-brand">
            <FaLocationDot></FaLocationDot>
          </div>

          <div className=" text-sm">Calgary, Alberta</div>
        </div>
      </div>
    </Navbar>
  );
}
