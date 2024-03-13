import PersonalDetails from "./components/PersonalDetails";
import ContactDetails from "./components/ContactDetails";
import Biography from "./components/Biography";
import RatingDetails from "./components/RatingDetails";

export default function page() {
  return (
    // TODO: responsive design
    <div className="bg-white dark:bg-black w-full p-24 rounded-xl text-brand flex flex-row justify-between">
      <PersonalDetails></PersonalDetails>
      <div className=" flex flex-col gap-8">
        <ContactDetails></ContactDetails>
        <RatingDetails></RatingDetails>
      </div>
      <Biography></Biography>
    </div>
  );
}
