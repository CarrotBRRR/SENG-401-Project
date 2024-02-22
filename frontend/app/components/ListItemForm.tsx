"use client";
import React from "react";
import ListingDetails from "./listItemFormComponents/ListingDetails";
import ListingMedia from "./listItemFormComponents/ListingMedia";
import ListingLocation from "./listItemFormComponents/ListingLocation";
import ListingContactInformation from "./listItemFormComponents/ListingContactInformation";
import { toast } from "react-toastify";
import { functionThatReturnPromise } from "../utils/mockPromise";
import { Button } from "flowbite-react";

export default function ListItemForm() {
  const notify = () =>
    toast.promise(functionThatReturnPromise, {
      pending: "Listing is being uploaded...",
      success: "Listing has been posted",
      error: "Listing rejected. Please try again later.",
    });
  return (
    <form
      className="flex flex-col gap-4 text-brand"
      onSubmit={(e) => {
        e.preventDefault();
        notify();
      }}
    >
      <ListingDetails></ListingDetails>
      <ListingMedia></ListingMedia>
      <ListingLocation></ListingLocation>
      <ListingContactInformation></ListingContactInformation>
      <Button
        color={"primary"}
        type="submit"
        className="flex justify-center place-items-center items-center font-bold"
      >
        Post Listing
      </Button>
    </form>
  );
}
