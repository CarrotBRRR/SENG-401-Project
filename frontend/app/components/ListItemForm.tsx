import ListingDetails from "./listItemFormComponents/ListingDetails";
import ListingMedia from "./listItemFormComponents/ListingMedia";
import ListingLocation from "./listItemFormComponents/ListingLocation";
import ListingContactInformation from "./listItemFormComponents/ListingContactInformation";
import SubmitButton from "./SubmitButton";
import { createListing } from "../actions";
export default function ListItemForm() {
  return (
    <form className="flex flex-col gap-4 text-brand" action={createListing}>
      <ListingDetails />
      <ListingMedia />
      <ListingLocation />
      <ListingContactInformation />
      <SubmitButton />
    </form>
  );
}
