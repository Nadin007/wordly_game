import React from "react";
import {CellsRow} from './cells-row';

const rows = 6;
const fillWords = (words) => {
    let left = rows - words.length;
    let allWords = [ ...words ];
    for (let i = 0; i < left; i++) {
        allWords.push({ word: "", status: [] });
    }

    return allWords;
}

export const Board = (props) => {
    let words = fillWords(props.words);
    let isSolved = words.some(w => w.status.every(n => n === 1));
    let activeWord = isSolved ? undefined : words.find(word => word.status.length === 0);

    return <div className="board">
        { words.map((w, index) => {
            return <CellsRow
                createNewWord={ props.createNewWord }
                key={ w.word + index }
                word={ w.word }
                status={w.status}
                isActive={w === activeWord}
            />
        }) }
    </div>
}