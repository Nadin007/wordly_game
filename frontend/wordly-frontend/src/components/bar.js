import React from "react";
import './bar.css'


export const Bar = (props) => {
    let barClassNane = props.persent ? "bar-line full-bar" : "bar-line";
    return <div className="bar">
        <span className="order-number">{props.number}</span>
        <div className={barClassNane} style={{width: props.persent + '%'}}>
            {props.barNumber}
        </div>
    </div>
}