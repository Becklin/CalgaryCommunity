import React, { useEffect } from "react";
import { useMap } from "react-leaflet";
import L from "leaflet";
import "./style.css";

const Legend = () => {
  const map = useMap();

  useEffect(() => {
    const legend = L.control({ position: "bottomright" });

    legend.onAdd = function () {
      const div = L.DomUtil.create("div", "info legend");
      div.innerHTML = `
        <h4>Legend</h4>
        <div><i class="attraction"></i>Attractions</div>
        <div><i class="library"></i> Library</div>
        <div><i class="hospital"></i>Hospital</div>
        <div><i class="custom"></i>Others</div>
      `;
      return div;
    };

    legend.addTo(map);

    return () => {
      legend.remove();
    };
  }, [map]);

  return null;
};

export default Legend;
