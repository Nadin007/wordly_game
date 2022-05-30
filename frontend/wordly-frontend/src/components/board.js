import React from "react";
import {CellsRow} from './cells-row';

export const Board = (props) => {
    let words = props.words;
    return <div className="board">
        <CellsRow word={words[0] ? words[0].word : '' } status={words[0] ? words[0].status : ''}/>
        <CellsRow word={words[1] ? words[1].word : '' } status={words[1] ? words[1].status : ''}/>
        <CellsRow word={words[2] ? words[2].word : '' } status={words[2] ? words[2].status : ''}/>
        <CellsRow word={words[3] ? words[3].word : '' } status={words[3] ? words[3].status : ''}/>
        <CellsRow word={words[4] ? words[4].word : '' } status={words[4] ? words[4].status : ''}/>
        <CellsRow word={words[5] ? words[5].word : '' } status={words[5] ? words[5].status : ''}/>
        

    </div>
}