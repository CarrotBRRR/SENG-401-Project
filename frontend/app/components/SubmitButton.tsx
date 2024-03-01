"use client";
import { Button } from "flowbite-react";
import React from "react";
import { useFormStatus } from "react-dom";
import { toast } from "react-toastify";
import { functionThatReturnPromise } from "../utils/mockPromise";
function SubmitButton() {
  const { pending } = useFormStatus();
  const notify = () =>
    toast.promise(functionThatReturnPromise, {
      pending: "Listing is being uploaded...",
      success: "Listing has been posted",
      error: "Listing rejected. Please try again later.",
    });
  return (
    <Button
      color={"primary"}
      type="submit"
      {...(pending && { isProcessing: true, disabled: true })}
      className="  relative font-bold"
      aria-disabled={pending}
      onClick={notify}
    >
      {pending ? "Processing..." : "Post Listing"}
    </Button>
  );
}

export default SubmitButton;
