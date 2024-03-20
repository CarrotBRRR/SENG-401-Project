"use client";
import React from "react";
import { useState, useEffect } from "react";
import { getSession } from "next-auth/react";
import Notification from "../components/Notification";
interface Item {
  location: string;
  lenderID: string;
  timestamp: number;
  condition: string;
  category: string;
  images: [];
  itemID: string;
  description: string;
  imageHashes: [];
  borrowRequests: BorrowRequest[];
  itemName: string;
}

interface BorrowRequest {
  borrowerID: string;
  endDate: string;
  startDate: string;
  timestamp: number;
}

export default function ItemRequests() {
  const [requestedItems, setRequestedItems] = useState<Item[]>([]);
  const [numRequests, setNumRequests] = useState<Number>(0);

  const handleAcceptRequest = (itemID: string, borrowerID: string) => {
    setRequestedItems((prevItems) =>
      prevItems.filter((item) => {
        if (item.itemID === itemID) {
          const index = item.borrowRequests.findIndex(
            (request) => request.borrowerID === borrowerID
          );
          if (index !== -1) {
            if (item.borrowRequests.length === 1) {
              // Remove the entire item if it only has one borrow request
              return false;
            } else {
              // Remove the specific borrow request from the borrowRequests array
              const updatedBorrowRequests = [...item.borrowRequests];
              updatedBorrowRequests.splice(index, 1);
              return {
                ...item,
                borrowRequests: updatedBorrowRequests,
              };
            }
          }
        }
        return true; // Keep the item unchanged if it doesn't match the condition
      })
    );
  };

  async function fetchUserDetails(email: string) {
    const response = await fetch(
      "https://v5ezikbdjg4hadx5mqmundbaxq0zjdnj.lambda-url.ca-central-1.on.aws/",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          email: email,
        },
      }
    );
    const userData = await response.json();
    return userData;
  }

  async function getLenderItems(userID: string) {
    const res = await fetch(
      "https://iat6gyr54ckeyk532ukyqqqx6m0blqpr.lambda-url.ca-central-1.on.aws/",
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          lenderID: userID,
        },
      }
    );
    if (res.status == 200) {
      const itemObject = await res.json();
      const items = itemObject["items"];
      let totalRequests = 0;
      const filteredItems = items.filter((item: Item) => {
        if (item.borrowRequests && item.borrowRequests.length > 0) {
          totalRequests += item.borrowRequests.length;
          return true;
        }
        return false;
      });
      setRequestedItems(filteredItems);
      setNumRequests(totalRequests);
    }
  }

  useEffect(() => {
    const fetchSession = async () => {
      const session = await getSession();
      if (session && session.user) {
        if (typeof session.user.email === "string") {
          const userData = await fetchUserDetails(session.user.email);
          getLenderItems(userData.userID);
        }
      }
    };
    fetchSession();
  }, []);

  return (
    <div>
      {requestedItems.length === 0 ? (
        <p>Loading...</p>
      ) : (
        <div>
          {requestedItems.map((item, index) =>
            item.borrowRequests.map((request, requestIndex) => (
              <Notification
                key={`${index}-${requestIndex}`}
                itemName={item.itemName}
                itemID={item.itemID}
                borrowerID={request.borrowerID}
                startDate={request.startDate}
                endDate={request.endDate}
                timestamp={request.timestamp}
                handleAccept={handleAcceptRequest}
              ></Notification>
            ))
          )}
        </div>
      )}
    </div>
  );
}
