"use client";
import { Button } from "flowbite-react";
import React from "react";
import { useFormStatus } from "react-dom";
function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <Button
      color={"primary"}
      type="submit"
      {...(pending && { isProcessing: true, disabled: true })}
      className="  relative font-bold"
      aria-disabled={pending}
    >
      {pending ? "Processing..." : "Post Listing"}
    </Button>
  );
}

export default SubmitButton;
