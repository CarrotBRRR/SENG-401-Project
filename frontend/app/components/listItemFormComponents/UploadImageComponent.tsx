"use client";
import React, { useState } from "react";
import Image from "next/image";
import { Button } from "flowbite-react";
import { FaTimes, FaUpload } from "react-icons/fa";

export default function UploadImageComponent() {
  const [images, setImages] = useState<(File | undefined)[]>(
    Array.from({ length: 8 })
  );
  const handleAddTag = (newImage: File, index: number) => {
    if (index >= 8) return;
    setImages((prevImages) => {
      const updatedImages = [...prevImages];
      updatedImages[index] = newImage;
      return updatedImages;
    });
  };
  const handleRemoveTag = (index: number) => {
    if (index >= 8) return;
    setImages((prevImages) => {
      const updatedImages = [...prevImages];
      updatedImages[index] = undefined;
      return updatedImages;
    });
  };
  const MediaImage = ({
    index,
    file = "/missingImage.jpg",
  }: {
    index: number;
    file: string;
  }) => {
    console.log(index, file);
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
                handleAddTag(e.target.files[0], index);
              }
            }}
          />
        </label>
        <Button className="w-full h-12" onClick={() => handleRemoveTag(index)}>
          {file === "/missingImage.jpg" ? "" : <FaTimes />}
        </Button>
      </div>
    );
  };
  return (
    <div className="flex flex-row flex-wrap gap-2">
      {images.map((image, index) => {
        console.log(image);
        return (
          <MediaImage
            key={index}
            index={index}
            file={image ? URL.createObjectURL(image) : "/missingImage.jpg"}
          />
        );
      })}
    </div>
  );
}
