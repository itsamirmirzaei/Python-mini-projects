# A simple slot machine game implemented in Python.
# The game allows users to spin a slot machine, check for wins, and buy additional attempts
import random
import sys
import time

class SlotMachine:
    def __init__(self, reels=3, symbols=None):
        # Initialize the slot machine with specified number of reels and symbols
        self.reels = reels
        self.symbols = symbols if symbols else ['🍒', '🍋', '🔔', '⭐', '7️⃣']
        self.current_spin = []
        self.wins = 0
        self.losses = 0
        self.score = 0
        self.attempts = 3  # User starts with 3 attempts
        self.symbol_values = {'🍒': 10, '🍋': 15, '🔔': 20, '⭐': 30, '7️⃣': 50}
        self.attempt_cost = 50  # Cost to buy one additional attempt

    def spin(self):
        # Generate a random spin result
        self.current_spin = [random.choice(self.symbols) for _ in range(self.reels)]
        return self.current_spin

    def display_spin(self):
        # Display spinning animation with 3 frames
        for _ in range(3):
            print("Spinning" + "." * (_ % 3 + 1), end="\r")
            time.sleep(0.5)
        print(" | ".join(self.current_spin))

    def check_win(self):
        # Check for a full match: all symbols are the same
        if len(set(self.current_spin)) == 1:
            return "full_match", self.symbol_values[self.current_spin[0]] * 3
        # Check for a partial match: at least two symbols are the same
        elif any(self.current_spin.count(symbol) >= 2 for symbol in self.current_spin):
            winning_symbol = max(set(self.current_spin), key=self.current_spin.count)
            return "partial_match", self.symbol_values[winning_symbol] * 2
        return None, 0

    def buy_attempt(self):
        # Allow user to buy an additional attempt if they have enough score
        if self.score >= self.attempt_cost:
            self.score -= self.attempt_cost
            self.attempts += 1
            print(f"You bought one attempt for {self.attempt_cost} points! Remaining score: {self.score}, Attempts left: {self.attempts}")
            return True
        else:
            print(f"Not enough points to buy an attempt! You need {self.attempt_cost} points, but you have {self.score}.")
            return False

    def play(self):
        # Welcome message and game initialization
        print(f"Welcome to the Slot Machine! Score starts at 0. You have {self.attempts} attempts.")
        while self.attempts > 0:
            input("Press Enter to spin the slot machine...")
            # Decrease attempt count
            self.attempts -= 1
            self.spin()
            self.display_spin()
            win_type, points = self.check_win()

            if win_type:
                self.wins += 1
                self.score += points
                if win_type == "full_match":
                    print(f"Jackpot! All symbols match! +{points} points (Wins: {self.wins}, Losses: {self.losses}, Score: {self.score}, Attempts left: {self.attempts})")
                else:
                    print(f"Partial win! Two or more symbols match! +{points} points (Wins: {self.wins}, Losses: {self.losses}, Score: {self.score}, Attempts left: {self.attempts})")
            else:
                self.losses += 1
                print(f"Better luck next time! (Wins: {self.wins}, Losses: {self.losses}, Score: {self.score}, Attempts left: {self.attempts})")

            # Offer to buy an attempt if score is sufficient
            if self.attempts == 0 and self.score >= self.attempt_cost:
                while True:
                    buy = input(f"You have {self.score} points. Buy another attempt for {self.attempt_cost} points? (yes/no): ").strip().lower()
                    if buy in ['yes', 'y']:
                        if self.buy_attempt():
                            break
                    elif buy in ['no', 'n']:
                        print(f"\nGame Over! Final Stats: Wins: {self.wins}, Losses: {self.losses}, Total Score: {self.score}")
                        print("Thank you for playing!")
                        time.sleep(2)
                        sys.exit()
                    else:
                        print("Please enter 'yes' or 'no'.")
            elif self.attempts == 0:
                print(f"\nGame Over! You've used all your attempts. Final Stats: Wins: {self.wins}, Losses: {self.losses}, Total Score: {self.score}")
                print("Thank you for playing!")
                time.sleep(2)
                sys.exit()

            while True:
                play_again = input("Would you like to play again? (yes/no): ").strip().lower()
                if play_again in ['yes', 'y']:
                    break
                elif play_again in ['no', 'n']:
                    print(f"\nGame Over! Final Stats: Wins: {self.wins}, Losses: {self.losses}, Total Score: {self.score}")
                    print("Thank you for playing!")
                    time.sleep(2)
                    sys.exit()
                else:
                    print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    # Create and start the slot machine game
    slot_machine = SlotMachine()
    slot_machine.play()