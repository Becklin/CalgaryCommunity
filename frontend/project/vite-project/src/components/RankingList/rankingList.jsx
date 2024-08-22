import React from "react";
import "./style.css";

function RankingList({ ranking, setPosition }) {
  // eslint-disable-next-line react/prop-types
  const content = ranking.map((comm, index) => {
    const { name, score, income, service_count, centroid } = comm;
    return (
      <li className="ranking" key={index}>
        <i className="ranking-score">{(score * 1000).toFixed()}</i>
        {name}
        <div className="ranking-info">
          <span>CAD: {income}</span>
          <span>services: {service_count}</span>
          <button onClick={setPosition.bind(null, centroid.coordinates)} />
        </div>
      </li>
    );
  });
  return <ul>{content}</ul>;
}

export default RankingList;
