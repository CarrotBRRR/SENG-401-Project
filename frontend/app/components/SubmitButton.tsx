"use client";
import { Button } from "flowbite-react";
import React from "react";
import { useFormStatus } from "react-dom";
import { toast } from "react-toastify";
import { functionThatReturnPromise } from "../utils/mockPromise";
function SubmitButton({ ...props }) {
  const pendingMessage = props.pending;
  const successMessage = props.success;
  const errorMessage = props.error;
  const { pending } = useFormStatus();
  const notify = () =>
    toast.promise(functionThatReturnPromise, {
      pending: pendingMessage || "Listing is being uploaded...",
      success: successMessage || "Listing has been posted",
      error: errorMessage || "Listing rejected. Please try again later.",
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
