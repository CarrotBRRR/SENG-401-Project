import { authOptions } from "@/app/utils/authOptions";
import { Label, TextInput } from "flowbite-react";
import { getServerSession } from "next-auth/next";
import { FaPhone, FaInbox } from "react-icons/fa";
import ListItemFormTemplate from "./ListItemFormTemplate";

export default async function ListingContactInformation() {
  const session = await getServerSession(authOptions);
  return (
    <ListItemFormTemplate formNumber={4} formHeader={"Contact information"}>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="phoneNumber" value="Phone Number: (optional)" />
        </div>
        <div className=" mb-2 block">
          {/* TODO: Phone number needs to appear here */}
          <TextInput
            id="phoneNumber"
            icon={FaPhone}
            placeholder="123 456 7890"
            maxLength={11}
            helperText="Your phone number will show up on your listing"
          />
        </div>
      </div>
      <div>
        <div className="mb-2 block font-bold">
          <Label htmlFor="email" value="Email: " />
        </div>
        <div className=" mb-2 block">
          <TextInput
            type="email"
            id="email"
            name="email"
            icon={FaInbox}
            placeholder="john.doe@email.com"
            minLength={8}
            maxLength={50}
            helperText="Your email will show up on your listing"
            disabled
            value={session?.user?.email || ""}
          />
        </div>
        <input
          className="hidden"
          name="lenderID"
          // @ts-ignore
          value={session?.userData[0]?.userID || session?.user?.email}
          readOnly
        />
      </div>
    </ListItemFormTemplate>
  );
}
