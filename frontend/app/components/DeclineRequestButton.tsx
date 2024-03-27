"use client";
import { toast } from "react-toastify";
import { cancelRequest } from "../actions";

export default function DeclineRequestButton({
  itemID,
  borrowerID,
}: {
  itemID: string;
  borrowerID: string;
}) {
  const notify = () =>
    toast.promise(cancelRequest(itemID, borrowerID), {
      pending: "Request is being declined...",
      success: {
        render() {
          return "Request has been declined!";
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
      className="px-3 py-2 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-md mr-2"
      onClick={notify}
    >
      Decline
    </button>
  );
}
