export enum Condition {
  New = "New",
  UsedLikeNew = "Used - Like new",
  UsedGood = "Used - Good",
  UsedFair = "Used - Fair",
}
export interface ListItemI {
  title: string;
  condition: Condition;
  description: string;
  tags: string[];
  images: (File | undefined)[];
  city: string;
  postalCode: string;
  phoneNum: string;
  email: string;
  setTitle: React.Dispatch<React.SetStateAction<string>>;
  setCondition: React.Dispatch<React.SetStateAction<Condition>>;
  setDescription: React.Dispatch<React.SetStateAction<string>>;
  setTags: React.Dispatch<React.SetStateAction<string[]>>;
  setImages: React.Dispatch<React.SetStateAction<(File | undefined)[]>>;
  setCity: React.Dispatch<React.SetStateAction<string>>;
  setPostalCode: React.Dispatch<React.SetStateAction<string>>;
  setPhoneNum: React.Dispatch<React.SetStateAction<string>>;
  setEmail: React.Dispatch<React.SetStateAction<string>>;
}
