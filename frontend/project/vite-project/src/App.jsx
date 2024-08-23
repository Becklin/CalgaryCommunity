/* eslint-disable react/prop-types */
import "./App.css";
import { React, useEffect, useState } from "react";
import { Col, Row } from "antd";
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
import RankingList from "./components/RankingList/rankingList";
import MapController from "./components/MapController";
import WeightsForm from "./components/WeightsForm/WeightsForm";
import Hospital from "./assets/hospital.js";
console.log(Hospital);
function App() {
  const [ranking, setRanking] = useState([]);
  const [services, setService] = useState([]);
  const [income, setIncome] = useState([]);
  const [values, setValues] = useState({ crimes: 4, services: 4, income: 2 });

  const [serviceCommunities, setServiceCommunities] = useState([]);
  const [position, setPosition] = useState([51.0447, -114.0719]);

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
  const isNotEqualToTen = (value, type) => {
    let total = value;
    for (let val in values) {
      if (val === type) continue;
      total += values[val];
    }
    console.log("total", total);
    return total !== 10;
  };
  const onCrimesChange = (value) => {
    if (isNotEqualToTen(value, "crimes")) {
      setValues({
        ...values,
        crimes: value,
      });
    }
  };
  const onServicesChange = (value) => {
    if (isNotEqualToTen(value, "services")) {
      setValues({
        ...values,
        services: value,
      });
    }
  };
  const onIncomeChange = (value) => {
    if (isNotEqualToTen(value, "income")) {
      setValues({
        ...values,
        income: value,
      });
    }
  };
  const onFinish = async () => {
    try {
      const rankingResponse = await fetch(
        "http://localhost:8000/api/v1/community-rank/",
        {
          method: "POST",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            crimes: values.crimes,
            services: values.services,
            income: values.income,
          }),
        }
      );
      const rankingJson = await rankingResponse.json();
      setRanking(rankingJson.data);
    } catch (error) {
      throw error.message;
    }
  };
  const onFinishFailed = (errorInfo) => {
    console.log("Failed:", errorInfo);
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

        const rankingResp = await fetch(
          "http://localhost:8000/api/v1/community-rank/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              crimes: values.crimes,
              services: values.services,
              income: values.income,
            }),
          }
        );
        const rankingJson = await rankingResp.json();

        setService(jsons[2]);
        setIncome(orderedIncome);
        setRanking(rankingJson.data);
      } catch (error) {
        setError(error);
      } finally {
        setLoading(false);
      }
    };
    getData();
  }, [values.crimes, values.income, values.services]);
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  const class_colors = {
    1: "#e41a1c",
    2: "#377eb8",
    3: "#4daf4a",
    4: "#984ea3",
  };

  const displayCommunities = (ranking) => {
    const results = ranking.map((comm, index) => {
      const { name, score, income, sector, service_count, multipolygon } = comm;

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
          positions={JSON.parse(multipolygon).coordinates}
        >
          <Tooltip sticky>
            <div className="">
              <span>{name}</span>
              <br />
              <span>{sector}</span>
              <br />
              <span>crimes :{service_count}</span>
              <br />
              <span>income :{income}</span>
              <br />
              <span>score :{score}</span>
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
      html: Hospital,
    });
    const hospital = L.divIcon({
      className: "custom-marker-hospital",
      html: Hospital,
    });
    const attraction = L.divIcon({
      className: "custom-marker-attraction",
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
  const getMaxValue = (currentInput) => {
    const total =
      values.crimes + values.services + values.income - values[currentInput];
    return 10 - total;
  };

  return (
    <Row>
      <Col span={18} push={6}>
        <MapContainer
          center={[51.0447, -114.0719]}
          zoom={13}
          style={{ height: "100vh", width: "100vw", zIndex: 0 }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {displayIncome(income)}
          {displayCommunities(ranking)}
          {displayServices(services)}
          <MapController position={position} />
        </MapContainer>
      </Col>
      <Col className="sidecar" span={6} pull={18} style={{ height: "100vh" }}>
        <WeightsForm
          onFinish={onFinish}
          onFinishFailed={onFinishFailed}
          getMaxValue={getMaxValue}
          values={values}
          onCrimesChange={onCrimesChange}
          onServicesChange={onServicesChange}
          onIncomeChange={onIncomeChange}
        />
        <div className="ranking-wrapper">
          <RankingList ranking={ranking} setPosition={setPosition} />
        </div>
      </Col>
    </Row>
  );
}

export default App;
