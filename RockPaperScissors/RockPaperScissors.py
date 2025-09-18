# Rock Paper Scissors Game

import random 

# Initialize scores
user_wins = 0
computer_wins = 0

# Options for the game
options = ["rock", "paper", "scissors"]

# Main game loop
while True:
    user_input = input("Type  Rock/Paper/Scissors or Q to quit: ").lower()
    if user_input == "q":
        break
    
    if user_input not in options:
        continue
    
    random_number = random.randint(0, 2)
    #rock = 0, paper = 1, scissors = 2
    computer_pick = options[random_number]
    print("Computer picked", computer_pick + ".")
    if user_input == computer_pick:
        print("It's a tie!")
    elif (user_input == "rock" and computer_pick == "scissors") or (user_input == "paper" and computer_pick == "rock") or (user_input == "scissors" and computer_pick == "paper"):
        print("You win!")
        user_wins += 1
    else:
        print("You lose!")
        computer_wins += 1

# Display final scores
print("Game Over!")
print("Final score - You:", user_wins, ", Computer:", computer_wins)
print("Thanks for playing!")
