import React from "react";
import { Avatar, Dropdown, DropdownItem } from "flowbite-react";

export default function Notification() {
  return (
    <div className="flex bg-brand p-4 w-full mx-auto relative">
      <div className="flex">
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
          <DropdownItem>View Profile</DropdownItem>
        </Dropdown>
      </div>
      <div className="flex-col flex-grow ml-4">
        <p className="text-white text-lg mb-4">
          Joseph has Requested your Hammer!
        </p>
        <div className="flex">
          <button className="px-3 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-md mr-2">
            Decline
          </button>
          <button className="px-3 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-md">
            Accept
          </button>
        </div>
      </div>
      <div className="absolute top-0 right-0 text-gray-300 text-sm mt-5 mr-3">
        Calgary | 1 hour ago
      </div>
    </div>
  );
}
