import "./App.css";
import { React, useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Tooltip,
  Polygon,
  Popup,
  Marker,
} from "react-leaflet";

import L from "leaflet";
import "leaflet/dist/leaflet.css";

function App() {
  const [communities, setCommunities] = useState([]);
  const [services, setService] = useState([]);
  const [income, setIncome] = useState([]);
  const [serviceCommunities, setServiceCommunities] = useState([]);

  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const loadTop5Communities = async () => {
    try {
      const resp = await fetch(
        "http://localhost:8000/api/v1/community-service-counts/"
      );
      const json = await resp.json();
      setServiceCommunities(json);
      return json;
    } catch (error) {
      setError(error);
    } finally {
      setLoading(false);
    }
  };
  useEffect(() => {
    const getData = async () => {
      const urls = [
        "http://localhost:8000/api/v1/community/",
        "http://localhost:8000/api/v1/crimesReport/",
        "http://localhost:8000/api/v1/service/",
        "http://localhost:8000/api/v1/income/",
      ];
      try {
        const jsons = await Promise.all(
          urls.map(async (url) => {
            const resp = await fetch(url);
            const json = await resp.json();
            return json;
          })
        );
        const orderedIncome = jsons[3].sort(
          (a, b) =>
            a.total_household_total_income - b.total_household_total_income
        );
        const crimeReport = jsons[1].data;
        const communitiesWithCrimeReport = jsons[0].map((comm, index) => {
          const { id } = comm;
          const hasComm = crimeReport.find(
            ({ community_id }) => community_id === id
          );
          if (hasComm)
            comm["crimeReportCount"] = Number(hasComm.total_whole_year);
          return comm;
        });
        setCommunities(communitiesWithCrimeReport);
        setService(jsons[2]);
        setIncome(orderedIncome);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, []);
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  const class_colors = {
    1: "#e41a1c",
    2: "#377eb8",
    3: "#4daf4a",
    4: "#984ea3",
  };

  const displayCommunities = (communities) => {
    const results = communities.map((comm, index) => {
      const { crimeReportCount, name, sector, multipolygon } = comm;
      let isServiceCommunities;
      if (serviceCommunities) {
        for (const key in serviceCommunities) {
          if (key === name) isServiceCommunities = key === name;
        }
      }
      return (
        <Polygon
          key={index}
          weight={1}
          fillOpacity="0.4"
          pathOptions={{
            color: isServiceCommunities
              ? "yellow"
              : class_colors[comm.class_code],
            fillColor: "yellow",
          }}
          // color="yellow"
          positions={multipolygon.coordinates}
        >
          <Tooltip sticky>
            <div className="">
              <span>{name}</span>
              <br />
              <span>{sector}</span>
              <br />
              <span>crimes :{crimeReportCount}</span>
            </div>
          </Tooltip>
        </Polygon>
      );
    });
    return results;
  };
  const displayServices = (services) => {
    let customIcon = L.divIcon({
      className: "custom-marker",
      html: '<div class="custom-marker-inner"></div>',
    });
    const hospital = L.divIcon({
      className: "custom-marker-hospital",
      html: '<div class="custom-marker-inner-hospital"></div>',
    });
    const attraction = L.divIcon({
      className: "custom-marker-hospital",
      html: '<div class="custom-marker-inner-attraction"></div>',
    });
    const transform = (type, { point: { coordinates }, name, address }) => {
      let icon;
      switch (type) {
        case "Hospital":
        case "PHS Clinic":
          icon = hospital;
          break;
        case "Attraction":
          icon = attraction;
          break;
        default:
          icon = customIcon;
          break;
      }
      return (
        <Marker position={coordinates} icon={icon}>
          <Popup>
            {name} <br /> {address}
            <br /> {type}
          </Popup>
        </Marker>
      );
    };
    const result = services.reduce(function (result, { type, ...rest }) {
      if (type !== "Community Centre") {
        result.push(transform(type, rest));
      }
      return result;
    }, []);
    return result;
  };
  const displayIncome = (income) => {
    const getColor = (index, total) => {
      const startColor = [255, 165, 0];
      const endColor = [0, 0, 140];
      const ratio = index / total;
      const color = endColor.map((start, i) => {
        return Math.round(start + ratio * (startColor[i] - start));
      });
      return `rgb(${color.join(",")})`;
    };

    const polygonOptions = income.map((pos, index) => ({
      fillColor: getColor(index, income.length - 1),
      color: getColor(index, income.length - 1),
      weight: 1,
    }));
    const results = income.map((section, index) => {
      const {
        total_household_total_income,
        ward,
        polygon: { coordinates },
      } = section;

      return (
        <Polygon
          key={index}
          weight={1}
          fillOpacity="0.4"
          pathOptions={polygonOptions[index]}
          positions={coordinates}
        >
          <Tooltip sticky>
            <div className="">
              <span>{ward}</span>
              <br />
              <span>{total_household_total_income}</span>
            </div>
          </Tooltip>
        </Polygon>
      );
    });
    return results;
  };
  return (
    <>
      <div onClick={loadTop5Communities}>Top 5 community</div>
      <MapContainer
        center={[51.0447, -114.0719]}
        zoom={13}
        style={{ height: "100vh", width: "100vw" }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {displayIncome(income)}
        {displayCommunities(communities)}
        {displayServices(services)}
      </MapContainer>
    </>
  );
}

export default App;
