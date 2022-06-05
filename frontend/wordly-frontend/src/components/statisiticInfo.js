import React from "react";
import './statisiticInfo.css'


export const Info = (props) => {
    return <div className="statistic-info">
        <div className="info-value">{props.value}</div>
        <div className="info-title">{props.title}</div>
    </div>
}