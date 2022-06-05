import React, { useEffect, useState } from "react";
import {BordCell} from './cell.js';
import './cells-row.css';
import LetterService from '../services/letterListener';
import { Url } from "../const.js";

export const CellsRow = (props) => {
    let [word, setWord] = useState(props.word || '');
    let [status, setStatus] = useState(props.status || []);

    let keyHandler = (letter) => {
        if (letter === 'Backspace') {
            let new_word = word.slice(0, word.length - 1);
            setWord(new_word);
            return;
        }
        if (letter === 'Enter') {
            if (word.length !== 5) {
                return;
            }
            fetch(`${Url}/word/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({
                    word: word
                })
            })
            .then((res) => res.ok ? res.json() : Promise.reject(new Error("Word doesn't exist")))
            .then(status => {
                setStatus(status.response);
                props.createNewWord({ word, status: status.response });
            })
        }
        if (word.length < 5) {
            let new_word = word + letter;
            setWord(new_word)
            return;
        }
    };

    useEffect(() => {
        if (!props.isActive) {
            return;
        }

        LetterService.subscribe(keyHandler);

        return () => {
            LetterService.unsubscribe(keyHandler);
        };  
    }, [word, status, props.isActive, props.createNewWord]);

    return <div className="cells-row">
        < BordCell letter={word[0]} status={status[0]}/>
        < BordCell letter={word[1]} status={status[1]}/>
        < BordCell letter={word[2]} status={status[2]}/>
        < BordCell letter={word[3]} status={status[3]}/>
        < BordCell letter={word[4]} status={status[4]}/>
    </div>
}