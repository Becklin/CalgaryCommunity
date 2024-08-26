import React from "react";
import "./style.css";

function RankingList({ ranking, setPosition, setHighlightedCommunity }) {
  // eslint-disable-next-line react/prop-types
  const triggerNavigation = (centroid, id) => {
    setPosition(centroid.coordinates);
    setHighlightedCommunity(id);
  };
  const content = ranking.map((comm, index) => {
    const { name, score, income, service_count, centroid, id } = comm;
    return (
      <li
        className="ranking"
        key={index + name}
        onClick={triggerNavigation.bind(null, centroid, id)}
      >
        <span className="ranking-order">{index + 1}</span>
        <div>
          <span className="ranking-title">{name}</span>
          <div className="ranking-info">
            <span>CAD: {income}</span>
            <span>SERVICES: {service_count}</span>
            <span>SCR: {(score * 1000).toFixed()}</span>
          </div>
        </div>
      </li>
    );
  });
  return <ul>{content}</ul>;
}

export default RankingList;
