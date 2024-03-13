"use client";
import { Button, Label, TextInput } from "flowbite-react";
import { FaSearch } from "react-icons/fa";
import React, { useState } from "react";

export default function TagsComponent() {
  const [tags, setTags] = useState<string[]>([]);
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
  );
}
