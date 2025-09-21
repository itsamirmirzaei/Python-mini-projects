import random
from collections import defaultdict
from typing import List, Dict, Tuple


class RouletteGame:
    def __init__(self):
        self.players: Dict[str, float] = {}
        self.bets: List[Tuple[str, str, float, str]] = []  # (player_name, bet_type, amount, bet_value)
        self.wheel_numbers = [str(i) for i in range(37)] + ['00']  # All as strings
        self.payouts = {
            'straight': 35,
            'split': 17,
            'street': 11,
            'corner': 8,
            'line': 5,
            'dozen': 2,
            'column': 2,
            'red': 1,
            'black': 1,
            'even': 1,
            'odd': 1,
            'low': 1,
            'high': 1
        }
        self.red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.black_numbers = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
    
    def add_player(self, player_name: str):
        """Add a new player with an initial balance of 1000."""
        if not isinstance(player_name, str):
            raise TypeError("Player name must be a string.")
        if player_name not in self.players:
            self.players[player_name] = 1000.0
        else:
            raise ValueError("Player already exists.")
    
    def place_bet(self, player_name: str, bet_type: str, amount: float, bet_value: str = None):
        """Place a bet for the player."""
        if not isinstance(player_name, str) or not isinstance(bet_type, str):
            raise TypeError("Player name and bet type must be strings.")
        if not isinstance(amount, (int, float)):
            raise TypeError("Bet amount must be a number.")
        if amount <= 0:
            raise ValueError("Bet amount must be positive.")
        if player_name not in self.players:
            raise ValueError("Player does not exist.")
        if amount > self.players[player_name]:
            raise ValueError("Insufficient balance.")
        if bet_type not in self.payouts:
            raise ValueError("Invalid bet type.")
        if bet_type in ['straight', 'split', 'street', 'corner', 'line', 'dozen', 'column'] and bet_value is None:
            raise ValueError("Bet value required for this bet type.")
        
        self.bets.append((player_name, bet_type, amount, bet_value))
        self.players[player_name] -= amount
    
    def spin_wheel(self) -> str:
        """Spin the roulette wheel and return the winning number."""
        if not self.wheel_numbers:
            raise ValueError("Wheel numbers are not defined.")
        return random.choice(self.wheel_numbers)
    
    def evaluate_bets(self, winning_number: str):
        """Evaluate bets and calculate winnings."""
        results = defaultdict(float)
        
        for player_name, bet_type, amount, bet_value in self.bets:
            win = False
            
            if winning_number == '00':
                win = (bet_type == 'straight' and bet_value == '00')
            else:
                try:
                    num = int(winning_number)
                except ValueError:
                    continue  # For '00', only straight bet is checked
                if bet_type == 'straight' and bet_value == winning_number:
                    win = True
                elif bet_type == 'red' and num in self.red_numbers:
                    win = True
                elif bet_type == 'black' and num in self.black_numbers:
                    win = True
                elif bet_type == 'even' and num != 0 and num % 2 == 0:
                    win = True
                elif bet_type == 'odd' and num != 0 and num % 2 != 0:
                    win = True
                elif bet_type == 'low' and num != 0 and 1 <= num <= 18:
                    win = True
                elif bet_type == 'high' and num != 0 and 19 <= num <= 36:
                    win = True
                # TODO: Implement other bet types like dozen, split, etc.
                
                if win:
                    payout = amount * self.payouts[bet_type]
                    results[player_name] += payout + amount
                    self.players[player_name] += payout + amount
        
        self.bets.clear()
        return results
    
    def get_game_status(self, player_name: str) -> str:
        """Display the game status for the player."""
        status = f"\nGame Status:\n"
        status += f"{player_name}'s Balance: {self.players.get(player_name, 0):.2f}\n"
        status += "Open Bets:\n"
        for bet in self.bets:
            if bet[0] == player_name:
                status += f"Bet Type: {bet[1]}, Amount: {bet[2]}, Bet Value: {bet[3] or 'N/A'}\n"
        return status


def play_interactive_game():
    game = RouletteGame()
    
    # Get player name
    player_name = input("Enter your name: ").strip()
    game.add_player(player_name)
    
    while True:
        print(game.get_game_status(player_name))
        print("\nBet Types: straight, red, black, even, odd, low, high")
        bet_type = input("Enter bet type (or 'exit' to quit): ").strip().lower()
        
        if bet_type == 'exit':
            print(f"Game ended. {player_name}'s final balance: {game.players[player_name]:.2f}")
            break
        
        if bet_type not in game.payouts:
            print("Invalid bet type! Please choose a valid bet type.")
            continue
        
        # Get bet amount
        try:
            amount = float(input("Enter bet amount: "))
        except ValueError:
            print("Bet amount must be a number!")
            continue
        
        # Get bet value (for straight, etc.)
        bet_value = None
        if bet_type in ['straight']:
            bet_value = input("Enter bet number (0-36 or 00): ").strip()
            if bet_value not in game.wheel_numbers:
                print("Invalid number! Must be between 0-36 or 00.")
                continue
        
        # Place bet
        try:
            game.place_bet(player_name, bet_type, amount, bet_value)
        except ValueError as e:
            print(f"Error: {e}")
            continue
        
        # Spin wheel and show result
        winning_number = game.spin_wheel()
        print(f"\nWinning number: {winning_number}")
        
        results = game.evaluate_bets(winning_number)
        if player_name in results:
            print(f"{player_name} won: {results[player_name]:.2f}")
        else:
            print(f"{player_name} did not win.")
        
        # Check balance
        if game.players[player_name] <= 0:
            print(f"{player_name} has no balance left! Game over.")
            break


if __name__ == "__main__":
    print("Welcome to the Roulette Game!")
    play_interactive_game()