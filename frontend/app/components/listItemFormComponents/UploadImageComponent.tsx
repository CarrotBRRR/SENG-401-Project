"use client";
import React, { useState } from "react";
import Image from "next/image";
import { Button } from "flowbite-react";
import { FaTimes } from "react-icons/fa";

export default function UploadImageComponent() {
  const [images, setImages] = useState<(File | undefined)[]>(
    Array.from({ length: 8 })
  );
  const [imageURLs, setImageURLs] = useState<string[]>(
    Array.from({ length: 8 })
  );
  const handleAddTag = (newImage: File, index: number) => {
    if (index >= 8) return;
    // upload to cloudinary...
    setImageURLs((prevURLs) => {
      const updatedURLs = [...prevURLs];
      updatedURLs[index] = URL.createObjectURL(newImage);
      return updatedURLs;
    });
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
        <Button
          color={"primary"}
          className="w-full h-12 flex place-content-center justify-center items-center"
          onClick={() => handleRemoveTag(index)}
        >
          {file === "/missingImage.jpg" ? "" : <FaTimes />}
        </Button>
      </div>
    );
  };
  return (
    <div className="flex flex-row flex-wrap gap-2">
      <input
        className="hidden"
        name="imageURLs"
        readOnly
        value={JSON.stringify(imageURLs)}
      />
      {images.map((image, index) => {
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
