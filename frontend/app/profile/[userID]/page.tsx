import { getUserByID } from "@/app/actions";
import PersonalDetails from "../components/PersonalDetails";
import ContactDetails from "../components/ContactDetails";
import RatingDetails from "../components/RatingDetails";
import Biography from "../components/Biography";
import { UserI } from "@/app/interfaces/UserI";
import Link from "next/link";

export default async function page({ params }: { params: { userID: string } }) {
  const res: UserI = await getUserByID(params.userID);
  const location = res?.location;
  const name = res?.name;
  const rating = res.rating;
  const bio = res.bio;
  const email = res.email;
  const phoneNum = res.phoneNum;

  return (
    // TODO: responsive design
    <>
      <div className="flex flex-col items-center justify-around w-full">
        <div className="bg-white dark:bg-black w-full px-24 pt-24 rounded-xl text-brand flex flex-row justify-between">
          <PersonalDetails location={location} name={name} />
          <div className=" flex flex-col gap-8">
            <ContactDetails email={email} phoneNum={phoneNum} />
            <RatingDetails rating={rating} />
          </div>
          <Biography bio={bio} />
        </div>
        <div className="flex flex-row justify-center items-center w-full text-center pt-20">
          <Link href={`/profile/edit/${params.userID}`} className="flex justify-center items-center bg-brand font-bold rounded-lg w-fit h-full text-center hover:underline text-4xl px-3 py-3">Edit Profile</Link>
        </div>
      </div>
    </>
  );
}
