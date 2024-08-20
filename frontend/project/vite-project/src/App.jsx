import "./App.css";
import { React, useEffect, useState } from "react";
import { Button, InputNumber, Slider, Form } from "antd";
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
  const onFinish = (values) => {
    console.log("Success:", values);
    fetch("http://localhost:8000/api/v1/rank/", {
      method: "POST",
      body: values,
    }).then((data) => {
      console.log("成功", data);
    });
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
        style={{ height: "100vh", width: "100vw", zIndex: 0 }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {displayCommunities(communities)}
        {displayIncome(income)}
        {/* {displayServices(services)} */}
      </MapContainer>
      <Form
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 16,
        }}
        style={{
          maxWidth: 600,
          position: "fixed",
          top: "120px",
          left: "30px",
          zIndex: 1,
          background: "white",
          padding: "10px",
        }}
        initialValues={{
          remember: true,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item label="Services">
          <Form.Item name="input-number" noStyle>
            <InputNumber min={1} max={10} />
          </Form.Item>
          <span
            className="ant-form-text"
            style={{
              marginInlineStart: 8,
            }}
          >
            Kilometers
          </span>
        </Form.Item>
        <Form.Item name="income" label="Income">
          <Slider
            marks={{
              0: "A",
              20: "B",
              40: "C",
              60: "D",
              80: "E",
              100: "F",
            }}
          />
        </Form.Item>
        <Form.Item name="crimesReport" label="Crimes Report">
          <Slider
            marks={{
              0: "A",
              20: "B",
              40: "C",
              60: "D",
              80: "E",
              100: "F",
            }}
          />
        </Form.Item>
        <Form.Item
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
    </>
  );
}

export default App;
