import UploadImageComponent from "./UploadImageComponent";
export default function ListingMedia() {
  return (
    <div className="flex flex-col gap-4 border p-4 rounded shadow">
      <div className=" flex flex-row place-items-center gap-4">
        <div className=" rounded-lg bg-gray-200 p-2 size-8 justify-center items-center flex">
          2
        </div>
        <div className=" text-xl font-medium text-black ">Media</div>
      </div>
      <div className=" flex flex-col gap-2.5 text-sm">
        <h2 className="text-brand font-bold ">
          Add photos to attract interest to your item
        </h2>
        <h3 className="text-brand font-medium ">
          Include pictures with different angles and details.
        </h3>
        <h3 className="text-brand font-medium ">
          You can upload a maximum of 8 photos that are at least 300px wide or
          tall (we recommend at least 1000px.)
        </h3>
        <h3 className="text-brand font-medium ">
          Click on a frame to upload an image.
        </h3>
      </div>
      <UploadImageComponent></UploadImageComponent>
    </div>
  );
}
