import React from "react";
import DatepickerRentalForm from "./DatepickerRentalForm";
import { requestItem } from "../actions";
import { getServerSession } from "next-auth";
import SubmitButton from "./SubmitButton";
export default async function RequestRentalForm() {
  const session = await getServerSession();
  const itemID = "1";
  return (
    <>
      <form
        action={requestItem}
        className=" mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg"
      >
        <div className="flex flex-col gap-8">
          <input className="hidden" name="itemID" value={itemID} readOnly />
          <input
            className="hidden"
            name="userID"
            value={session?.user?.email || ""}
            readOnly
          />
          <h1 className=" font-bold text-2xl">Request Item Rental</h1>
          <div className=" w-full ">
            <label
              htmlFor="return-date"
              className="block text-sm font-medium text-gray-900 dark:text-white"
            >
              Return Date *
            </label>
            <DatepickerRentalForm />
          </div>
          <div className="w-full">
            <label
              htmlFor="message"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Custom Message
            </label>
            <textarea
              id="message"
              name="message"
              rows={5}
              className="block p-2.5 w-full text-sm text-gray-900 bg-stone-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              placeholder="Leave a comment..."
            />
          </div>
          <SubmitButton
            pending="Requesting item..."
            success="Request has been made successfully!"
            error="Error requesting item. Please try again later."
          />
        </div>
      </form>
    </>
  );
}
