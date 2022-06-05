
import { useCallback, useEffect, useState } from 'react';
import './App.css';
import { Board } from './components/board';
import { Header } from './components/header';
import { Stat } from './components/statistic';
import { Url } from './const';

const reqquestCurrentChallenge = () => {
    return fetch(`${Url}/word/`, { credentials: "include" })
}

function App() {
    let [words, setWords] = useState([]);
    let [isOpen, setIsOpen] = useState(false)
    let [isSolved, setIsSolved] = useState(false)

    const createNewChallenge = () => {
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
    };

    useEffect(() => {
        createNewChallenge();
    }, []);
    
    let createNewWord = useCallback(word => {
        setWords([ ...words, word ]);

        if (word.status.length > 0 && word.status.every(n => n === 1) || words.length === 5) {
            setTimeout(() => {
                setIsOpen(true);
                setIsSolved(true);
            }, 3000) 
        }
    });

    let updateChallenge = useCallback(
        () => {
            createNewChallenge();
            setIsOpen(false);
            setIsSolved(false);
        }
    );

    return <>
        <Header showStatistic={() => {setIsOpen(!isOpen)}} />
        <div className='game-app'>
            <Board words = {words} createNewWord={ createNewWord } />
        </div>
        <Stat isOpen={isOpen} isSolved={isSolved} updateChallenge={updateChallenge} />
    </>
}

export default App;
