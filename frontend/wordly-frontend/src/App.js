
import { useEffect, useState } from 'react';
import './App.css';
import { Board } from './components/board';
import { Header } from './components/header';

function App() {
    let [words, setWords] = useState([
        {word: '', status: []}
    ]);
    let key_handler = (e) => {
        let letter = e.key;
        if (words.length < 7) {
            let current_word = words[words.length - 1];
            if (current_word.word.length < 5 && letter.length === 1 && letter.match(/[a-zA-Z]/)) {
                let new_words = [
                    ...words.slice(0, words.length - 1),
                    {word: current_word.word + letter, status: []}
                ]
                setWords(new_words)
                return;
            }

            if (letter === 'Backspace' && current_word.status.length === 0) {
                let new_words = [
                    ...words.slice(0, words.length - 1),
                    {word: current_word.word.slice(0, current_word.word.length - 1), status: []}
                ]
                setWords(new_words)
                return;
            }
        }
    };

    useEffect(() => {
        window.addEventListener('keyup', key_handler);

        return () => {
            window.removeEventListener('keyup', key_handler);
        };
    }, [words]);

    return <>
        <Header />
        <div className='game-app'>
            <Board words = {words} />
        </div>
    </>
}

export default App;
