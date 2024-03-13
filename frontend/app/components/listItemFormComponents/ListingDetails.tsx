import { Select, Label, TextInput, Textarea } from "flowbite-react";
import { Category, Condition } from "@/app/interfaces/ListItemI";
import ListItemFormTemplate from "./ListItemFormTemplate";
import TagsComponent from "./TagsComponent";
export default function ListingDetails() {
  return (
    <ListItemFormTemplate formNumber={1} formHeader={"ListingDetails"}>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="category" value="Category: " />
        </div>
        <Select id="category" name="category">
          {Object.values(Category).map((cond) => (
            <option key={cond} value={cond}>
              {cond}
            </option>
          ))}
        </Select>
      </div>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="condition" value="Condition: (optional)" />
        </div>
        <Select id="condition" name="condition">
          {Object.values(Condition).map((cond) => (
            <option key={cond} value={cond}>
              {cond}
            </option>
          ))}
        </Select>
      </div>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="listingTitle" value="Listing title" />
        </div>
        <TextInput id="listingTitle" type="text" required name="listingTitle" />
      </div>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="description" value="Description" />
        </div>
        <Textarea
          id="description"
          placeholder="Enter a description"
          rows={4}
          name="description"
        />
      </div>
      <TagsComponent></TagsComponent>
    </ListItemFormTemplate>
  );
}
