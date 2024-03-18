export enum Condition {
  New = "New",
  UsedLikeNew = "Used - Like new",
  UsedGood = "Used - Good",
  UsedFair = "Used - Fair",
}
export enum Category {
  Other = "Other",
  Sports = "Sports",
  Electronics = "Electronics",
  Furniture = "Furniture",
  Tools = "Tools",
  Outdoors = "Outdoors",
}
export interface ListItemI {
  title: string;
  condition: Condition;
  description: string;
  category: Category;
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
export interface BorrowRequest {
  borrowerID: string;
  endDate: string;
  startDate: string;
  // Need to resolve inconsistency in timestamp type
  timestamp: string;
}
export interface ItemsGetListI {
  location: string;
  lenderID: string;
  timestamp: number;
  condition: Condition;
  category: Category;
  images: string[];
  itemID: string;
  description: string;
  imageHashes?: string[];
  borrowRequests?: BorrowRequest[];
  itemName: string;
}

export interface GetItemPageAPIResponse {
  items: ItemsGetListI[];
  last_evaluated_key: string;
}
