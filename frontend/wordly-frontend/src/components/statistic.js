import React, { useEffect, useState } from "react";
import { Graph } from "./graph";
import { Info } from "./statisiticInfo";
import './statistic.css';
import { Url } from "../const.js";


export const Stat = (props) => {
    const [solved, setSolved] = useState([0, 0, 0, 0, 0, 0]);
    const [attempt, setAttempt] = useState(0);

    useEffect(() => {
        if (!props.isOpen){
            return;
        }
        fetch(`${Url}/stat/`, {
            method: 'GET',
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include",
        })
        .then(r => r.ok ? r.json() : Promise.reject('Could not get statistic!'))
        .then(result => {
            setSolved(result.solved);
            setAttempt(result.attempt);
        })
    }, [props.isOpen]);
    if (!props.isOpen){
        return '';
    }
    let wonValue = solved.reduce(
        (ind, nexInd) => ind + nexInd, 0
    )

    return <div className="statistic">
        <div className="statistic-title">statistic</div>
        <div className="statistic-info-table">
            <Info title='Played' value={attempt}/>
            <Info title='Won' value={wonValue}/>
        </div>
        <div className="statistic-title">attempts statistic</div>
        <Graph solved={solved} />
        <div className="button-wrapper">
            {props.isSolved ? <button onClick={props.updateChallenge} className="next-button">Next</button> : ''}
        </div>
    </div>
}