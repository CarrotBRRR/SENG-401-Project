import ListItemFormTemplate from "./ListItemFormTemplate";
import UploadImageComponent from "./UploadImageComponent";
export default function ListingMedia() {
  return (
    <ListItemFormTemplate formNumber={2} formHeader={"Media"}>
      <div className=" flex flex-col gap-2.5 text-sm text-brand font-medium">
        <h2 className="font-bold ">
          Add photos to attract interest to your item
        </h2>
        <h3>Include pictures with different angles and details.</h3>
        <h3>
          You can upload a maximum of 8 photos that are at least 300px wide or
          tall (we recommend at least 1000px.)
        </h3>
        <h3>Max image size is: 5 MB </h3>
        <h3>Click on a frame to upload an image.</h3>
      </div>
      <UploadImageComponent />
    </ListItemFormTemplate>
  );
}
