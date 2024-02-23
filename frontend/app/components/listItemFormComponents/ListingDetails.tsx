"use client";
import React, { useState } from "react";
import { Button, Select, Label, TextInput, Textarea } from "flowbite-react";
import { FaSearch } from "react-icons/fa";
import { useListItem } from "@/app/context/ListItemContext";
import { Condition } from "@/app/interfaces/ListItemI";
export default function ListingDetails() {
  const { tags, setTags } = useListItem();
  const [newTag, setNewTag] = useState<string>("");
  const handleAddTag = () => {
    if (newTag.length < 2) return;
    if (tags.length >= 5) return;
    if (tags.includes(newTag)) return;
    setTags((prevTags) => [...prevTags, newTag]); // Add your new tag logic here
    setNewTag("");
  };
  const removeTag = (indexToRemove: number) => {
    setTags((prevTags) =>
      prevTags.filter((_, index) => index !== indexToRemove)
    );
  };

  return (
    <div className="flex flex-col gap-4 border p-4 rounded shadow justify-between">
      <div className=" flex flex-row place-items-center gap-4">
        <div className=" rounded-lg bg-gray-200 p-2 size-8 justify-center items-center flex">
          1
        </div>
        <div className=" text-xl font-medium text-black ">Listing Details</div>
      </div>
      <div className=" inline-flex flex-row justify-start items-center gap-2.5 whitespace-nowrap text-sm cursor-pointer">
        <p className="text-brand font-medium">Select Category:</p>
        <p className="text-brand font-bold ">
          Buy and Sell {">"} Sporting Goods & Exercise {">"} Ski
        </p>
        <p className="text-blue-500 font-bold ">Change category</p>
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
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="tags" value="Tags (optional)" />
          <div className=" font-normal text-sm">
            Increase your item exposure. Enter up to 5 keywords someone could
            search to find your listing.
          </div>
        </div>
        <div className=" mb-2 block">
          <TextInput
            onChange={(e) => setNewTag(e.target.value)}
            value={newTag}
            id="tags"
            icon={FaSearch}
            placeholder="Enter a tag"
            minLength={2}
            maxLength={20}
            helperText="Tag must be between 2-20 characters"
          />
        </div>
        <input
          className="hidden"
          name="tags"
          value={JSON.stringify(tags)}
          readOnly
        />

        <div className="flex flex-row gap-4">
          <Button
            color={"primary"}
            onClick={handleAddTag}
            className="flex-nowrap text-nowrap"
          >
            Add tag
          </Button>
          <ul className="flex flex-wrap gap-2 w-full p-2 bg-slate-500 rounded-lg">
            {tags.map((tag, index) => (
              <Button
                color={"primary"}
                key={index}
                size="xs"
                onClick={() => removeTag(index)}
              >
                {tag}
              </Button>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
