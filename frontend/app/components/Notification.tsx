import { Avatar, Dropdown, DropdownItem } from "flowbite-react";
import { getUserByID } from "../actions";
import Image from "next/image";
import Link from "next/link";
import { BorrowRequest, ItemsGetListI } from "../interfaces/ListItemI";
import DeclineRequestButton from "./DeclineRequestButton";
import AcceptRequestButton from "./AcceptRequestButton";

export default async function Notification({
  request,
  item,
}: {
  request: BorrowRequest;
  item: ItemsGetListI;
}) {
  const images = item.images;
  const timestamp = request.timestamp;
  const borrowerID = request.borrowerID;
  const itemName = item.itemName;
  const itemID = item.itemID;
  const borrowerDetails = await getUserByID(borrowerID);

  const currentTimestamp = Math.floor(Date.now() / 1000);
  const timeDifference = currentTimestamp - parseInt(timestamp, 10);

  let formattedTimeAgo;
  if (timeDifference < 60) {
    formattedTimeAgo = `${Math.floor(timeDifference)} seconds ago`;
  } else if (timeDifference < 3600) {
    formattedTimeAgo = `${Math.floor(timeDifference / 60)} minutes ago`;
  } else if (timeDifference < 86400) {
    formattedTimeAgo = `${Math.floor(timeDifference / 3600)} hours ago`;
  } else {
    formattedTimeAgo = `${Math.floor(timeDifference / 86400)} days ago`;
  }

  const startDateObj = new Date(Number(request.startDate) * 1000);
  const endDateObj = new Date(Number(request.endDate) * 1000);
  const formattedStartDate = startDateObj.toISOString().split("T")[0];
  const formattedEndDate = endDateObj.toISOString().split("T")[0];

  const imageSrc = images.length > 0 ? images[0] : "/missingImage.jpg";

  return (
    <>
      <div className="flex bg-brand p-4 border border-gray-700 w-full mx-auto relative">
        <div className="flex p-2">
          {borrowerDetails && (
            <Dropdown
              inline
              label={
                <Avatar
                  alt="User settings"
                  img={borrowerDetails.profilePicture}
                  rounded
                />
              }
            >
              <Link href={`/profile/${borrowerID}`}>
                <DropdownItem>View Profile</DropdownItem>
              </Link>
            </Dropdown>
          )}
        </div>
        <div className="flex-col flex-grow pl-4 pr-4">
          {borrowerDetails && (
            <p className="text-white text-lg mb-4 pr-4">
              {borrowerDetails.name} has Requested your {itemName}!
            </p>
          )}
          <div className="flex flex-row">
            <div className="pr-8">
              <Link href={`listings/item/${itemID}`}>
                <Image
                  height={80}
                  width={80}
                  src={imageSrc}
                  className="mr-3 rounded"
                  alt="Item Image"
                />
              </Link>
            </div>
            <div>
              <p className="text-sm">
                {formattedStartDate} - {formattedEndDate}
              </p>
              <div className="flex pt-2">
                <DeclineRequestButton itemID={itemID} borrowerID={borrowerID} />
                <AcceptRequestButton itemID={itemID} borrowerID={borrowerID} />
              </div>
            </div>
          </div>
        </div>
        {borrowerDetails && (
          <div className="top-0 right-0 text-gray-300 text-sm pl-10 pt-1">
            {borrowerDetails.location} | {formattedTimeAgo}
          </div>
        )}
      </div>
    </>
  );
}
