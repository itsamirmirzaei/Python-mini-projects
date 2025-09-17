import random

def get_valid_input(prompt, min_value=None):
    """Prompt the user for input and validate it as an integer.

    Args:
        prompt (str): The message to display to the user.
        min_value (int, optional): The minimum acceptable value. Defaults to None.

    Returns:
        int: The validated integer input provided by the user.
    """
    while True:
        user_input = input(prompt)
        if user_input.isdigit():
            number = int(user_input)
            if min_value is not None and number <= min_value:
                print(f"Please enter a number greater than {min_value}.")
                continue
            return number
        print("Please enter a valid number.")

def play_game():
    """Run a single round of the number guessing game.

    Returns:
        int: The number of guesses taken to guess the correct number.
    """
    print("Welcome to the Number Guessing Game!")
    top_of_range = get_valid_input("Enter a number to set the range (0 to your number): ", 0)
    
    random_number = random.randint(0, top_of_range)
    guesses = 0

    while True:
        guesses += 1
        user_guess = get_valid_input("Make a guess: ")
        
        if user_guess == random_number:
            print(f"Congratulations! You got it in {guesses} guesses!")
            break
        elif user_guess > random_number:
            print("Too high! Try a lower number.")
        else:
            print("Too low! Try a higher number.")

    return guesses

def main():
    """Main function to control the game flow and allow replay.

    The function repeatedly runs the game until the user chooses to exit.
    """
    while True:
        play_game()
        replay = input("Would you like to play again? (yes/no): ").lower()
        if replay != 'yes':
            print("Thanks for playing! Goodbye!")
            break

if __name__ == "__main__":
    """Entry point of the program."""
    main()