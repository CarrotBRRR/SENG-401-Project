import React from "react";
import ListingDetails from "./listItemFormComponents/ListingDetails";
import ListingMedia from "./listItemFormComponents/ListingMedia";

export default function ListItemForm() {
  return (
    <div className="text-brand gap-2 flex flex-col">
      <ListingDetails></ListingDetails>
      <ListingMedia></ListingMedia>
    </div>
  );
}
