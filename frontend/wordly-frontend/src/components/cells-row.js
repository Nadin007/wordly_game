import React from "react";
import {BordCell} from './cell.js';
import './cells-row.css'

export const CellsRow = (props) => {
    let word = props.word || ''
    let status = props.status || []
    return <div className="cells-row">
        < BordCell letter={word[0]} status={status[0]}/>
        < BordCell letter={word[1]} status={status[1]}/>
        < BordCell letter={word[2]} status={status[2]}/>
        < BordCell letter={word[3]} status={status[3]}/>
        < BordCell letter={word[4]} status={status[4]}/>
        
    </div>
}