import React from "react";
import { Bar } from "./bar";
import './graph.css'


export const Graph = (props) => {
    let maxAttempt = Math.max(...props.solved)
    return <div className="graph">
        {props.solved.map((a, ind) => {
            return <Bar number={ind+1} persent={a/maxAttempt * 100} barNumber={a}/> 
            })}
    </div>
}