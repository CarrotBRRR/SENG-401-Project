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
  const maxImageSize = 5 * 1024 * 1024; // 5 MB

  const handleAddImage = (newImage: File, index: number) => {
    if (index >= 8) return;
    if (newImage.size > maxImageSize) {
      alert("Image is too large. Please upload an image smaller than 5MB.");
      return;
    }
    setImageURLs((prevURLs) => {
      const updatedURLs = [...prevURLs];
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target?.result) {
          updatedURLs[index] = e.target.result as string;
        }
      };
      reader.readAsDataURL(newImage);
      return updatedURLs;
    });
    setImages((prevImages) => {
      const updatedImages = [...prevImages];
      updatedImages[index] = newImage;
      return updatedImages;
    });
  };
  const handleRemoveImage = (index: number) => {
    if (index >= 8) return;
    setImages((prevImages) => {
      const updatedImages = [...prevImages];
      updatedImages[index] = undefined;
      return updatedImages;
    });
    setImageURLs((prevURLs) => {
      const updatedURLs = [...prevURLs];
      // @ts-ignore
      updatedURLs[index] = null;
      return updatedURLs;
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
              if (e.target.files?.[0]) {
                handleAddImage(e.target.files[0], index);
              }
            }}
          />
        </label>
        <Button
          color={"primary"}
          className="w-full h-12 flex place-content-center justify-center items-center"
          onClick={() => handleRemoveImage(index)}
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
        name="images"
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
