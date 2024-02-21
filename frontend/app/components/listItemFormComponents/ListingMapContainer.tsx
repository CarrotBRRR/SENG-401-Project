import React from "react";
import Image from "next/image";
export default function ListingMapContainer() {
  return (
    <div>
      ListingMapContainer
      <Image
        src={"https://via.placeholder.com/407x188"}
        alt="Map of Calgary, AB T3A 7V4"
        width={384}
        height={192}
      />
    </div>
  );
}
