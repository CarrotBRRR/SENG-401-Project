"use client";
import React, { createContext, useContext, useState, ReactNode } from "react";
import { ListItemI, Condition, Category } from "../interfaces/ListItemI";

// Create the context with a default value
const listItemContextDefaultValues: ListItemI = {
  category: Category.Other,
  title: "",
  condition: Condition.New,
  description: "",
  tags: [],
  images: Array.from({ length: 8 }),
  city: "",
  postalCode: "",
  phoneNum: "",
  email: "",
  setTitle: () => {},
  setCondition: () => {},
  setDescription: () => {},
  setTags: () => {},
  setImages: () => {},
  setCity: () => {},
  setPostalCode: () => {},
  setPhoneNum: () => {},
  setEmail: () => {},
};

const ListItemContext = createContext<ListItemI>(listItemContextDefaultValues);

export function useListItem() {
  return useContext(ListItemContext);
}

// Provider component
export function ListItemProvider({ children }: { children: ReactNode }) {
  const [category, setCategory] = useState<Category>(Category.Other); // Default value is "Other" [0]
  const [title, setTitle] = useState<string>("");
  const [condition, setCondition] = useState<Condition>(Condition.UsedLikeNew);
  const [description, setDescription] = useState<string>("");
  const [tags, setTags] = useState<string[]>([]);
  const [images, setImages] = useState<(File | undefined)[]>(
    Array.from({ length: 8 })
  );
  const [city, setCity] = useState<string>("");
  const [postalCode, setPostalCode] = useState<string>("");
  const [phoneNum, setPhoneNum] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const value: ListItemI = {
    category,
    title,
    condition,
    description,
    tags,
    images,
    city,
    postalCode,
    phoneNum,
    email,
    setTitle,
    setCondition,
    setDescription,
    setTags,
    setImages,
    setCity,
    setPostalCode,
    setPhoneNum,
    setEmail,
  };
  return (
    <ListItemContext.Provider value={value}>
      {children}
    </ListItemContext.Provider>
  );
}
