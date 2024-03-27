"use client";
import { toast } from "react-toastify";
import { borrowItem } from "../actions";

export default function AcceptRequestButton({
  itemID,
  borrowerID,
}: {
  itemID: string;
  borrowerID: string;
}) {
  const notify = () =>
    toast.promise(borrowItem(itemID, borrowerID), {
      pending: "Request is being accepted...",
      success: {
        render() {
          return "Request has been accepted";
        },
      },
      error: {
        render({ data }) {
          return `${data}`;
        },
      },
    });

  return (
    <button
      className="px-3 py-2 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-md"
      onClick={notify}
    >
      Accept
    </button>
  );
}
