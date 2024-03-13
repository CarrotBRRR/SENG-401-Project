import { Rating, RatingStar } from "flowbite-react";
import React from "react";

export default function RatingDetails() {
  const rating = 4.1;
  return (
    <div className="flex flex-col gap-4">
      <h1 className="text-xl font-medium">Contact Details</h1>
      <div className="flex flex-col gap-4 text-black dark:text-white">
        <Rating>
          <RatingStar className="text-brand" />
          <RatingStar className="text-brand" />
          <RatingStar className="text-brand" />
          <RatingStar className="text-brand" />
          <RatingStar filled={false} />
          <p className="ml-2 text-sm font-medium text-gray-500 dark:text-gray-400">
            {rating}
          </p>
        </Rating>
      </div>
    </div>
  );
}
