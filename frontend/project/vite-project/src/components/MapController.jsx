import React, { useEffect } from "react";
import { useMap } from "react-leaflet";

export default function MapController({ position, zoom }) {
  const map = useMap();
  useEffect(() => {
    if (position) {
      console.log(position);
      map.setView(position, zoom);
    }
  }, [map, position, zoom]);
  return null;
}
