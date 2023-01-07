/*
    This file houses a node guessing game
 */
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
})

let number = Math.floor(100 * Math.random())
let guess = ""


/* Quit the game */
function answer_quit () {
    console.log("Thanks for playing")
    readline.close()
    process.exit()
}

/* Get User input */
function get_input(prompt) {
    readline.question(prompt,
        (answer) => {
            guess = answer
            if (guess === 'q') {
                answer_quit()
            } else {
                if (guess < number) {
                    guess = get_input("Your guess is to low. Try again.")
                } else if (guess > number) {
                    guess = get_input("Your guess is to high. Try again.")
                } else {
                    guess = get_input("Correct! I've guessed another. try again or enter q to quit.")
                    number = Math.floor(100 * Math.random())
                }
            }
        }
    )
}


get_input('Okay, I have chosen a number. Guess what it is....')
