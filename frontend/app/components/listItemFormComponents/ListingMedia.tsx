"use client";
import React, { useState } from "react";
import {
  Button,
  Select,
  Label,
  TextInput,
  Textarea,
  FileInput,
} from "flowbite-react";
import { toast } from "react-toastify";
import { FaSearch } from "react-icons/fa";
import {
  functionThatReturnPromiseFail,
  functionThatReturnPromise,
} from "@/app/utils/mockPromise";
import Image from "next/image";

export default function ListingMedia() {
  const [images, setImages] = useState<File[]>([]);
  const handleAddTag = (newImage: File) => {
    if (images.length >= 8) return;
    if (images.includes(newImage)) return;
    setImages((prevImages) => [...prevImages, newImage]); // Add your new tag logic here
  };
  const notify = () =>
    toast.promise(functionThatReturnPromise, {
      pending: "Listing is being uploaded...",
      success: "Listing has been posted",
      error: "Listing rejected. Please try again later.",
    });
  const MediaImage = ({
    index,
    file = "/missingImage.jpg",
  }: {
    index: number;
    file?: string;
  }) => {
    console.log(file);
    return (
      <div className="w-44 border rounded hover:opacity-90 cursor-pointer">
        <label
          className="h-44 flex place-content-center"
          htmlFor={`file-upload-${index}`}
        >
          <Image
            alt="upload image"
            className=" object-contain"
            src={file}
            width={176}
            height={176}
          />
          <input
            id={`file-upload-${index}`}
            type="file"
            className="hidden"
            accept="image/*"
            onChange={(e) => {
              if (e.target.files && e.target.files[0]) {
                handleAddTag(e.target.files[0]);
              }
            }}
          />
        </label>
        <div className="w-full h-12 bg-green-300"></div>
      </div>
    );
  };
  return (
    <form
      className="flex flex-col gap-4 border p-4 rounded shadow"
      onSubmit={(e) => {
        e.preventDefault();
        notify();
      }}
    >
      <div className=" flex flex-row place-items-center gap-4">
        <div className=" rounded-lg bg-gray-200 p-2 size-8 justify-center items-center flex">
          2
        </div>
        <div className=" text-xl font-medium text-black ">Media</div>
      </div>
      <div className=" flex flex-col gap-2.5 text-sm">
        <h2 className="text-brand font-bold ">
          Add photos to attract interest to your item
        </h2>
        <h3 className="text-brand font-medium ">
          Include pictures with different angles and details.
        </h3>
        <h3 className="text-brand font-medium ">
          You can upload a maximum of 8 photos that are at least 300px wide or
          tall (we recommend at least 1000px.)
        </h3>{" "}
        <h3 className="text-brand font-medium ">
          Drag and drop to change the order of your pictures.
        </h3>
      </div>
      <div className="flex flex-row flex-wrap gap-2">
        {images.map((image, index) => {
          return (
            <MediaImage
              key={index}
              index={index}
              file={URL.createObjectURL(image)}
            />
          );
        })}
      </div>
      <div className="flex flex-row gap-2 flex-wrap">
        {Array.from({ length: 8 - images.length }, (_, i) => (
          <MediaImage key={i} index={i}></MediaImage>
        ))}
      </div>
      <Button type="submit">Submit</Button>
    </form>
  );
}
