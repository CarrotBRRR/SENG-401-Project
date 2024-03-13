import { Label, Textarea } from "flowbite-react";
import EditButton from "./EditButton";

export default function Biography() {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-row justify-between">
        <h1 className="text-xl font-medium">Biography</h1>
        <EditButton></EditButton>
      </div>
      <div className="flex flex-col gap-4 text-black dark:text-white">
        <div className="max-w-md">
          <Textarea
            id="comment"
            placeholder="Enter a description..."
            rows={12}
            className=" bg-purple-200 text-brand shadow "
          />
        </div>
      </div>
    </div>
  );
}
