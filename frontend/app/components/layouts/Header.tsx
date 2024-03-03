import {
  Button,
  Dropdown,
  DropdownDivider,
  DropdownHeader,
  DropdownItem,
  Navbar,
} from "flowbite-react";
import { TextInput } from "flowbite-react";
import { FaLocationDot } from "react-icons/fa6";
import { FaSearch } from "react-icons/fa";
import Image from "next/image";
import Link from "next/link";
import { getServerSession } from "next-auth/next";
import { authOptions } from "@/app/utils/authOptions";

function Logo() {
  return (
    <Link href="/" className="flex flex-row">
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
    </Link>
  );
}

function UserProfile({
  sessionUser,
}: {
  sessionUser:
    | {
        name?: string | null | undefined;
        email?: string | null | undefined;
        image?: string | null | undefined;
      }
    | null
    | undefined;
}) {
  const imageSrc = sessionUser?.image || "";
  return (
    <Dropdown
      inline
      label={
        <Image
          src={imageSrc}
          width={45}
          height={45}
          alt="profile image"
          className="rounded-full"
        />
      }
    >
      <DropdownHeader>
        <span className="block text-sm">{sessionUser?.name}</span>
        <span className="block truncate text-sm font-medium">
          {sessionUser?.email}
        </span>
      </DropdownHeader>
      <DropdownItem>My Profile</DropdownItem>
      <DropdownItem>Requested Tools</DropdownItem>
      <DropdownItem>Active Listings</DropdownItem>
      <DropdownItem>Disputes</DropdownItem>
      <DropdownDivider />
      <DropdownItem as="a" href="/api/auth/signout">
        Sign out
      </DropdownItem>
    </Dropdown>
  );
}

export default async function Header() {
  const session = await getServerSession(authOptions);
  const sessionUser = session && session.user;
  const dropdownOptions = [
    "Hand Tools",
    "Power Tools",
    "Outdoor & Garden",
    "Hammers",
    "Sports",
  ];
  return (
    <Navbar fluid rounded>
      <Logo />

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
      <div className="flex flex-row gap-4 place-items-center place-content-center">
        {session ? (
          <UserProfile sessionUser={sessionUser} />
        ) : (
          <Link href="/api/auth/signin">
            <Button
              className="transition duration-300 ease-in-out transform hover:scale-105"
              gradientDuoTone="purpleToBlue"
            >
              {"Sign in"}
            </Button>
          </Link>
        )}
        <Link href="/upload">
          <Button
            color="primary"
            className="transition duration-300 ease-in-out transform hover:scale-105"
          >
            List Items
          </Button>
        </Link>
      </div>
    </Navbar>
  );
}
