"use client";
import React, { useState, useEffect } from "react";

interface Location {
  latitude: number;
  longitude: number;
}

export default function MyComponent() {
  const [location, setLocation] = useState<Location | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        (error) => {
          setError(error.message);
        }
      );
    } else {
      setError("Geolocation is not supported by your browser.");
    }
  }, []);

  // Use location or error state in your component logic
  return (
    <div>
      {location ? (
        <p>
          Your latitude: {location.latitude}, longitude: {location.longitude}
        </p>
      ) : (
        <p>{error || "Loading location..."}</p>
      )}
    </div>
  );
}
