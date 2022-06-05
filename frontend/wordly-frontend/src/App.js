
import { useCallback, useEffect, useState } from 'react';
import './App.css';
import { Board } from './components/board';
import { Header } from './components/header';
import { Url } from './const';

const reqquestCurrentChallenge = () => {
    return fetch(`${Url}/word/`, { credentials: "include" })
}

function App() {
    let [words, setWords] = useState([]);

    useEffect(() => {
        fetch(`${Url}/v1/auth/`, { method: 'POST', credentials: "include" })
            .then(reqquestCurrentChallenge)
            .then(r => {
                if (r.ok) {
                    return r.json();
                }

                return fetch(`${Url}/challenge/`, { method: "POST", credentials: "include" })
                    .then(reqquestCurrentChallenge)
                    .then(r => r.json())
            })
            .then(w => {
                let words = w.words.word;
                let results = w.results;
                setWords(words.map((w, index) => ({ word: w.word, status: results[index] || [] })));
            });
    }, []);
    
    let createNewWord = useCallback(word => {
        setWords([ ...words, word ]);
    });

    return <>
        <Header />
        <div className='game-app'>
            <Board words = {words} createNewWord={ createNewWord } />
        </div>
    </>
}

export default App;
