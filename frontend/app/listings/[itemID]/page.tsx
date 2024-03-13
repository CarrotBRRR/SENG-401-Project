import RequestRentalForm from "@/app/components/RequestRentalForm";
import React from "react";

export default function page({ params }: { params: { itemID: string } }) {
  return (
    <div>
      Listing page for {params.itemID}
      <RequestRentalForm></RequestRentalForm>
    </div>
  );
}
