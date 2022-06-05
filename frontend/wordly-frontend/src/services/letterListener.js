const AllowedLetters = ['Backspace', 'Enter']

export class LetterListener {
    constructor (window) {
        this.window = window;
        this.fns = [];

        window.addEventListener('keyup', (e) => {
            let letter = e.key;
            if (letter.length === 1 && letter.match(/[a-zA-Z]/)) {
                this.fire(letter);
                return;
            } 
            if (AllowedLetters.includes(letter)) {
                this.fire(letter);
                return;
            }
        });
    }
    
    subscribe (fn) {
        this.fns.push(fn);
    }

    unsubscribe (fn) {
        this.fns = this.fns.filter(f => f !== fn);
    }

    fire (letter) {
        this.fns.forEach(fn => {
            fn(letter);
        });
    }
}

export default new LetterListener(window);