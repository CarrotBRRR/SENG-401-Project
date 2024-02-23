"use client";
import React, { useRef } from "react";
import ListingDetails from "./listItemFormComponents/ListingDetails";
import ListingMedia from "./listItemFormComponents/ListingMedia";
import ListingLocation from "./listItemFormComponents/ListingLocation";
import ListingContactInformation from "./listItemFormComponents/ListingContactInformation";
import { toast } from "react-toastify";
import { functionThatReturnPromise } from "../utils/mockPromise";
import SubmitButton from "./SubmitButton";
import { createListing } from "../actions";
import { ListItemProvider } from "../context/ListItemContext";
export default function ListItemForm() {
  const notify = () =>
    toast.promise(functionThatReturnPromise, {
      pending: "Listing is being uploaded...",
      success: "Listing has been posted",
      error: "Listing rejected. Please try again later.",
    });

  const ref = useRef<HTMLFormElement>(null);
  return (
    <form
      ref={ref}
      className="flex flex-col gap-4 text-brand"
      action={async (formData) => {
        await createListing(formData);
        ref.current?.reset();
        notify();
      }}
    >
      <ListItemProvider>
        <ListingDetails></ListingDetails>
        <ListingMedia></ListingMedia>
        <ListingLocation></ListingLocation>
        <ListingContactInformation></ListingContactInformation>
        <SubmitButton></SubmitButton>
      </ListItemProvider>
    </form>
  );
}
