import React from "react";
import './cell.css'

export const BordCell = (props) => {
    let newClass = `letter-cell ${getLetterState(props.status)}`
    return <div className={newClass}>
        {props.letter}
    </div>
}

const getLetterState = (status) => {
    switch (status) {
        case 1:
            return 'letter-cell-success';
        case 0:
            return 'letter-cell-exist';
        case -1:
            return 'letter-cell-fail';
        default:
            return '';
    }
}