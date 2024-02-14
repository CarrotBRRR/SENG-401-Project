import React from "react";

export default function RequestRentalForm() {
  return (
    <>
      <form className=" mx-auto bg-white dark:bg-slate-800 p-8 rounded-lg">
        <div className="flex flex-col gap-8">
          <h1 className=" font-bold text-2xl">Request Item Rental</h1>
          <div className=" w-full ">
            <label
              htmlFor="return-date"
              className="block text-sm font-medium text-gray-900 dark:text-white"
            >
              Return Date *
            </label>
            <div className="w-full p-2 bg-stone-50 rounded border border-zinc-300 justify-start items-center">
              <input
                type="date"
                id="return-date"
                className="block w-full text-sm text-neutral-500 bg-transparent border-gray-300 dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600"
                required
              />
            </div>
          </div>
          <div className="w-full">
            <label
              htmlFor="message"
              className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
            >
              Custom Message
            </label>
            <textarea
              id="message"
              rows={5}
              className="block p-2.5 w-full text-sm text-gray-900 bg-stone-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              placeholder="Leave a comment..."
            ></textarea>
          </div>

          <button
            type="submit"
            className="text-white bg-brand hover:opacity-90 focus:ring-4 focus:outline-none focus:ring-brand-light rounded-lg w-full px-5 py-2.5 text-center"
          >
            Rent Item
          </button>
        </div>
      </form>
    </>
  );
}
