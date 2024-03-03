export const functionThatReturnPromise = () =>
  new Promise((resolve) => setTimeout(resolve, 3000));

export const functionThatReturnPromiseFail = () =>
  new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Promise failed")), 3000)
  );
