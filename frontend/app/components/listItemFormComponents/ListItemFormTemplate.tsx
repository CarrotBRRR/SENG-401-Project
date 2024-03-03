import React, { ReactNode } from "react";

export default function ListItemFormTemplate({
  formNumber,
  formHeader,
  children,
}: {
  formNumber: number;
  formHeader: string;
  children?: ReactNode;
}) {
  return (
    <div className="flex flex-col gap-4 border p-4 rounded shadow justify-between">
      <div className=" flex flex-row place-items-center gap-4">
        <div className=" rounded-lg bg-gray-200 p-2 size-8 justify-center items-center flex">
          {formNumber}
        </div>
        <div className=" text-xl font-medium text-black ">{formHeader}</div>
      </div>
      {children}
    </div>
  );
}
