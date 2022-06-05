import React from "react";
import './statisticBtn.css';


export const StatisticBtn = (props) => {
    return <button
    className="statistic-btn"
    title="Show the game statistic"
    aria-label="Show the game statistic"
    onClick={props.showStatistic}>
    </button>
}