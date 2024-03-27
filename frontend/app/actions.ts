"use server";
import { Session, getServerSession } from "next-auth";
import { redirect } from "next/navigation";
import { authOptions } from "./utils/authOptions";
import { LocationInfo } from "./interfaces/LocationI";
import { GetItemPageAPIResponse } from "./interfaces/ListItemI";
import { revalidatePath } from "next/cache";
import { SuperSession } from "./interfaces/UserI";

const GET_USER_URL = process.env.GET_USER_URL as string;
const CREATE_USER_URL = process.env.CREATE_USER_URL as string;
const CREATE_LISTING_URL = process.env.CREATE_LISTING_URL as string;
const BORROW_ITEM_URL = process.env.BORROW_ITEM_URL as string;
const DELETE_LISTING_URL = process.env.DELETE_LISTING_URL as string;
const RETURN_ITEM_URL = process.env.RETURN_ITEM_URL as string;
const GET_ITEM_PAGE_URL = process.env.GET_ITEM_PAGE_URL as string;
const GET_LENDER_ITEMS_URL = process.env.GET_LENDER_ITEMS_URL as string;
const REQUEST_ITEM_URL = process.env.REQUEST_ITEM_URL as string;
const GET_BORROWED_ITEMS_URL = process.env.GET_BORROWED_ITEMS_URL as string;
const GET_ITEM_FROM_ID_URL = process.env.GET_ITEM_FROM_ID_URL as string;
const UPDATE_ACCOUNT_LOCATION_URL = process.env
  .UPDATE_ACCOUNT_LOCATION_URL as string;
const UPDATE_LISTING_URL = process.env.UPDATE_LISTING_URL as string;
const UPDATE_ACCOUNT_URL = process.env.UPDATE_ACCOUNT_URL as string;
const UPDATE_RATING_URL = process.env.UPDATE_RATING_URL as string;
export const createListing = async (formData: FormData) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.error("No session found. Please log in to continue.");
      return;
    }
    const rawFormData = Object.fromEntries(formData.entries());

    const images = String(rawFormData.images).split(",");
    const modifiedArray = images.map((item) => (item === "" ? null : item));
    const myBody = {
      category: rawFormData.category,
      condition: rawFormData.condition,
      listingTitle: rawFormData.listingTitle,
      description: rawFormData.description,
      tags: rawFormData.tags,
      images: modifiedArray,
      location: rawFormData.location,
      lenderID: rawFormData.lenderID,
    };
    const response = await fetch(CREATE_LISTING_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify(myBody),
    });
    if (!response.ok) {
      const errorResponse = await response.json();
      console.error("Failed to create listing:", errorResponse);
      const errorMessage = `Failed to create item. Status code: ${
        response.status
      }, Error: ${errorResponse.message || response.statusText}`;
      return Promise.reject(new Error(errorMessage));
    }
    return { status: "success" };
  } catch (error) {
    console.error("Error creating listing:", error);
    return `Error creating listing: ${error}`;
  }
};

export const updateAccountLocation = async (newLocation: LocationInfo) => {
  const session: SuperSession | null = await getServerSession(authOptions);
  if (!session) {
    console.log("No session found");
    return;
  }
  console.log("updateAccountLocation");
  const locationString = `${newLocation.city}, ${newLocation.province}, ${newLocation.country}`;
  const body = { location: locationString, userID: session.userData.userID };
  console.log(body);
  const response = await fetch(UPDATE_ACCOUNT_LOCATION_URL, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      accessToken: JSON.stringify(session.token.accessToken),
    },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const errorMessage =
      "Failed to update account location. Status code: " + response.status;
    console.error(errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
  return response.json();
};

export const createUser = async (session: Session) => {
  try {
    const body = {
      name: session.user?.name,
      email: session.user?.email,
      profilePicture: session.user?.image,
      rating: null,
      bio: null,
      location: null,
      phoneNumber: null,
    };
    const response = await fetch(CREATE_USER_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      const errorMessage =
        "Failed to update account location. Status code: " + response.status;
      console.error(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }
    return response;
  } catch (error) {
    console.error("Error creating user:", error);
    return null;
  }
};

export const getUser = async (email: string) => {
  const response = await fetch(GET_USER_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      email: email,
    },
  });
  return response;
};
export const getUserByID = async (userID: string) => {
  try {
    const session = await getServerSession(authOptions);
    if (!session) {
      console.error("No session found. Please log in to continue.");
      return null; // Or throw new Error("No session found");
    }

    const response = await fetch(GET_USER_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        userID: userID,
      },
    });

    const data = await response.json(); // Parse JSON response once

    if (!response.ok) {
      console.error(
        `Failed to get user. Status code: ${response.status}`,
        data
      );
      return null; // Or throw new Error(`Failed to get lender items. Status code: ${response.status}`);
    }

    return data; // Successfully return the parsed data
  } catch (error) {
    console.error("Error getting user:", error);
    return null; // Or throw error; depending on how you want to handle errors
  }
};
export const authenticateUser = async (session: Session) => {
  if (!session.user?.email) {
    return;
  }
  const res = await getUser(session.user?.email);
  if (res.ok) {
    return res;
  } else {
    if (session.user?.name && session.user?.email) {
      const newRes = await createUser(session);
      return newRes;
    }
  }
};

export const requestItem = async (formData: FormData) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.error("No session found. Please log in.");
      return;
    }

    const rawFormData = Object.fromEntries(formData.entries());

    const newBody = {
      itemID: rawFormData.itemID,
      borrowerID: rawFormData.borrowerID,
      startDate: Math.floor(
        new Date(rawFormData.borrowDate as string).getTime() / 1000
      ),
      endDate: Math.floor(
        new Date(rawFormData.returnDate as string).getTime() / 1000
      ),
    };

    const response = await fetch(REQUEST_ITEM_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify(newBody),
    });

    if (!response.ok) {
      const errorResponse = await response.text(); // It's better to await here for consistency
      const errorMessage = `Failed to request item. Status code: ${response.status}, Error: ${errorResponse}`;
      console.error(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }

    return { status: "success", response: await response.json() }; // Assuming JSON response, adjust as needed
  } catch (error) {
    console.error("An error occurred:", error);
    return `An error occurred: ${error || "Unknown error"}`;
  }
};

export const getBorrowedItems = async (borrowerID: string) => {
  const session: SuperSession | null = await getServerSession(authOptions);
  if (!session) {
    console.log("No session found");
    return;
  }
  const response = await fetch(GET_BORROWED_ITEMS_URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      accessToken: JSON.stringify(session.token.accessToken),
      borrowerID: borrowerID,
    },
  });

  if (response.status !== 200) {
    const errorMessage =
      "Failed to get Borrowed items. Status code: " + response.status;
    console.error(errorMessage);
    return errorMessage;
  }
  const borrowedItems = await response.json();
  return borrowedItems;
};

export const getLenderItems = async () => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.error("No session found. Please log in to continue.");
      return null; // Or throw new Error("No session found");
    }

    const lenderID = session.userData.userID;
    const response = await fetch(GET_LENDER_ITEMS_URL, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
        lenderID: lenderID, // Ensure headers are correctly named and valued
      },
    });

    const data = await response.json(); // Parse JSON response once

    if (response.status !== 200) {
      console.error(
        `Failed to get lender items. Status code: ${response.status}`,
        data
      );
      return null; // Or throw new Error(`Failed to get lender items. Status code: ${response.status}`);
    }

    return data; // Successfully return the parsed data
  } catch (error) {
    console.error("Error fetching lender items:", error);
    return null; // Or throw error; depending on how you want to handle errors
  }
};

export const deleteItem = async (itemID: string) => {
  const session: SuperSession | null = await getServerSession(authOptions);
  if (!session) {
    console.log("No session found");
    return;
  }
  const response = await fetch(DELETE_LISTING_URL, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
      accessToken: JSON.stringify(session.token.accessToken),
      itemID: itemID,
    },
  });

  if (!response.ok) {
    const errorMessage = `Failed to delete item. Status code: ${response.status}`;
    console.error(errorMessage);
    return errorMessage;
  }
  revalidatePath(`/listings/item`);
  revalidatePath(`/listings/item/[itemID]`, "page");

  return { message: "Item deleted successfully" };
};

export const borrowItem = async (itemID: string, borrowerID: string) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.log("No session found");
      return;
    }
    const response = await fetch(BORROW_ITEM_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify({
        itemID: itemID,
        borrowerID: borrowerID,
      }),
    });

    if (response.status !== 200) {
      const errorMessage =
        "Failed to borrow item. Status code: " + response.status;
      console.error(errorMessage);
      return errorMessage;
    }
    revalidatePath(`/requested`);
    return "Item borrowed successfully";
  } catch (error) {
    console.error("Error borrowing item:", error);
    return `Error borrowing item: ${error}`;
  }
};
export const cancelRequest = async (itemID: string, borrowerID: string) => {
  try{
  const session: SuperSession | null = await getServerSession(authOptions);
  if (!session) {
    console.log("No session found");
    return;
  }
  const response = await fetch(
    "https://kwvu2ae5lllfz77k5znkrvnrii0brzuf.lambda-url.ca-central-1.on.aws/",
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify({
        itemID: itemID,
        borrowerID: borrowerID,
      }),
    }
  );

  if (!response.ok) {
    const errorMessage =
      "Failed to decline request. Status code: " + response.status;
    console.error(errorMessage);
    return errorMessage;
  }
  revalidatePath(`/requested`);
  return "Request declined successfully";
} catch (error) {
  console.error("Error declining request:", error);
  return `Error declining request: ${error}`;
};}

export const getItemPage = async ({
  location = "Calgary, Alberta, Canada",
  pageCount = "10",
  category = "",
  lastItem = "",
  search = "",
}: {
  location?: string;
  pageCount?: string;
  category?: string;
  lastItem?: string;
  search?: string;
}) => {
  const session: SuperSession | null = await getServerSession(authOptions);
  if (!session) {
    console.log("No session found");
    return;
  }
  const userLocation = session.userData.location || location;
  const response = await fetch(GET_ITEM_PAGE_URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      location: userLocation,
      pageCount: pageCount,
      category: category,
      lastItem: lastItem,
      search: search,
    },
  });

  if (response.status !== 200) {
    const errorMessage =
      "Failed to get item page. Status code: " + response.status;
    console.error(errorMessage);
    return errorMessage;
  }

  const itemPage: GetItemPageAPIResponse = await response.json();
  return itemPage;
};

export const getAddress = async (latitude: number, longitude: number) => {
  const response = await fetch(
    `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=${process.env.GOOGLE_MAPS_API_KEY}`
  );
  const data = await response.json();
  return data;
};

export const getItemFromID = async (itemID: string) => {
  const response = await fetch(GET_ITEM_FROM_ID_URL, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      itemID: itemID,
    },
  });

  if (response.status !== 200) {
    const errorMessage =
      "Failed to get item from id. Status code: " + response.status;
    console.error(errorMessage);
    return errorMessage;
  }

  const item = await response.json();
  return item;
};

export const searchItemsRedirect = async (formData: FormData) => {
  const rawFormData = Object.fromEntries(formData.entries());
  const searchValue = rawFormData.searchValue;
  const category = rawFormData.category;
  const location = rawFormData.location;
  let searchQuery = "?";
  if (searchValue) {
    searchQuery += `search=${searchValue}&`;
  }
  if (category) {
    searchQuery += `category=${category}&`;
  }
  if (location) {
    searchQuery += `location=${location}&`;
  }
  redirect(`/listings${searchQuery}`);
};

// Waiting for backend to update.
export const updateListing = async (formData: FormData) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.error("No session found. Please log in to continue.");
      return;
    }
    const rawFormData = Object.fromEntries(formData.entries());
    const images = String(rawFormData.images).split(",");
    const modifiedArray = images.map((item) => (item === "" ? null : item));
    const myBody = {
      itemID: rawFormData.itemID,
      category: rawFormData.category,
      condition: rawFormData.condition,
      listingTitle: rawFormData.listingTitle,
      description: rawFormData.description,
      tags: rawFormData.tags,
      images: modifiedArray,
      location: session.userData.location,
      lenderID: session.userData.userID,
    };
    console.log(JSON.stringify(myBody));
    const response = await fetch(UPDATE_LISTING_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(myBody),
    });
    if (!response.ok) {
      const errorResponse = await response.json();
      const errorMessage = `Failed to update listing. Status code: ${
        response.status
      }, Error: ${errorResponse.message || response.statusText}`;
      console.log(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }
    return { status: "success" };
  } catch (error) {
    console.error("Error updating listing:", error);
    return `Error updating listing: ${error}`;
  }
};

export const updateAccount = async (formData: FormData) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.error("No session found. Please log in to continue.");
      return;
    }
    const rawFormData = Object.fromEntries(formData.entries());
    const myBody = {
      name: session.user?.name,
      email: session.user?.email,
      bio: rawFormData.bio,
      location: session.userData.location,
      userID: session.userData.userID,
    };
    console.log(myBody);
    const response = await fetch(UPDATE_ACCOUNT_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify(myBody),
    });
    if (!response.ok) {
      const errorResponse = await response.json();
      const errorMessage = `Failed to update account. Status code: ${
        response.status
      }, Error: ${errorResponse.message || response.statusText}`;
      console.error(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }
    revalidatePath(`/profile/${session.userData.userID}`);
    return { status: "success" };
  } catch (error) {
    const errorMessage = `Error updating account: ${error}`;
    console.error(errorMessage);
    return errorMessage;
  }
};
export const updateRating = async (newRating: number, userID: string) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      const noSessionError = "No session found. Please log in to continue.";
      console.error(noSessionError);
      return Promise.reject(new Error(noSessionError));
    }
    const myBody = {
      newRating: newRating,
      userID: userID,
    };
    console.log(myBody);
    const response = await fetch(UPDATE_RATING_URL, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify(myBody),
    });
    if (!response.ok) {
      const errorResponse = await response.json();
      const errorMessage = `Failed to update rating. Status code: ${
        response.status
      }, Error: ${errorResponse.message || response.statusText}`;
      console.error(errorMessage);
      return Promise.reject(new Error(errorMessage));
    }
    return { status: "success" };
  } catch (error) {
    const errorMessage = `Error updating rating: ${error}`;
    console.error(errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
};
export const returnItem = async (itemID: string) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.log("No session found");
      return;
    }
    const response = await fetch(RETURN_ITEM_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accessToken: JSON.stringify(session.token.accessToken),
      },
      body: JSON.stringify({
        itemID: itemID,
      }),
    });

    if (response.status !== 200) {
      const errorMessage =
        "Failed to return item. Status code: " + response.status;
      console.error(errorMessage);
      return errorMessage;
    }

    revalidatePath(`/profile/activeListings`);
    return { status: "success" };
  } catch (error) {
    const errorMessage = `Error returning item: ${error}`;
    console.error(errorMessage);
    return errorMessage;
  }
};

export const sendBorrowedItemEmail = async (itemID: string) => {
  try {
    const session: SuperSession | null = await getServerSession(authOptions);
    if (!session) {
      console.log("No session found");
      return;
    }
    const response = await fetch(
      "https://4ig6rd4axaer54xv3auyvgajq40edups.lambda-url.ca-central-1.on.aws/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          accessToken: JSON.stringify(session.token.accessToken),
        },
        body: JSON.stringify({
          itemID: itemID,
        }),
      }
    );

    if (response.status !== 200) {
      const errorMessage =
        "Failed to send email confirmation. Status code: " + response.status;
      console.error(errorMessage);
      return errorMessage;
    }
    return { status: "success" };
  } catch (error) {
    const errorMessage = `Error sending email confirmation: ${error}`;
    console.error(errorMessage);
    return errorMessage;
  }
};
