# Bank account management project using object-oriented programming in Python
# This project includes BankAccount (base class for bank accounts),
# SavingsAccount (inherits from BankAccount with interest functionality),
# and Bank class to manage multiple accounts.
# Uses encapsulation (private variables), inheritance, and polymorphism.
# Updated to allow user-driven deposit and withdrawal operations via terminal input.
# Currency changed to USD.

import random  # For generating random account numbers

class BankAccount:
    def __init__(self, owner_name, initial_balance=0):
        self.owner_name = owner_name
        self._account_number = self._generate_account_number()  # Private variable
        self._balance = initial_balance  # Private variable for encapsulation

    def _generate_account_number(self):
        """Private method to generate a random account number"""
        return random.randint(1000000000, 9999999999)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            print(f"{amount} USD deposited to account {self._account_number}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self._balance >= amount:
                self._balance -= amount
                print(f"{amount} USD withdrawn from account {self._account_number}.")
            else:
                print("Insufficient balance.")
        else:
            print("Withdrawal amount must be positive.")

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        return f"Bank account {self._account_number} owned by {self.owner_name} with balance {self._balance} USD"

class SavingsAccount(BankAccount):
    def __init__(self, owner_name, initial_balance=0, interest_rate=0.05):
        super().__init__(owner_name, initial_balance)
        self.interest_rate = interest_rate  # Interest rate (e.g., 5%)

    def apply_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"Interest of {interest} USD applied to account {self.get_account_number()}.")

    # Polymorphism: override withdraw method to add restriction
    def withdraw(self, amount):
        if amount > self._balance * 0.9:  # Cannot withdraw more than 90% of balance
            print("Cannot withdraw more than 90% of balance in a savings account.")
        else:
            super().withdraw(amount)

class Bank:
    def __init__(self):
        self.accounts = {}  # Dictionary to store accounts with account number as key

    def add_account(self, account):
        self.accounts[account.get_account_number()] = account
        print(f"Account {account.get_account_number()} added to the bank.")

    def find_account(self, account_number):
        return self.accounts.get(account_number, None)

    def transfer(self, from_account_number, to_account_number, amount):
        from_acc = self.find_account(from_account_number)
        to_acc = self.find_account(to_account_number)
        if from_acc and to_acc and amount > 0:
            if from_acc.get_balance() >= amount:
                from_acc.withdraw(amount)
                to_acc.deposit(amount)
                print(f"Transferred {amount} USD from {from_account_number} to {to_account_number}.")
            else:
                print("Insufficient balance in source account.")
        else:
            print("Invalid accounts or amount.")

def main():
    # Create bank
    my_bank = Bank()

    # Create initial accounts
    acc1 = BankAccount("Ali Rezaei", 1000)
    acc2 = SavingsAccount("Maryam Ahmadi", 500, interest_rate=0.07)
    my_bank.add_account(acc1)
    my_bank.add_account(acc2)

    while True:
        print("\n=== Bank Management System ===")
        print("1. Deposit to an account")
        print("2. Withdraw from an account")
        print("3. Apply interest (Savings Account only)")
        print("4. Transfer between accounts")
        print("5. Show account details")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            acc_num = int(input("Enter account number: "))
            amount = float(input("Enter amount to deposit (USD): "))
            account = my_bank.find_account(acc_num)
            if account:
                account.deposit(amount)
            else:
                print("Account not found.")

        elif choice == "2":
            acc_num = int(input("Enter account number: "))
            amount = float(input("Enter amount to withdraw (USD): "))
            account = my_bank.find_account(acc_num)
            if account:
                account.withdraw(amount)
            else:
                print("Account not found.")

        elif choice == "3":
            acc_num = int(input("Enter savings account number: "))
            account = my_bank.find_account(acc_num)
            if isinstance(account, SavingsAccount):
                account.apply_interest()
            elif account:
                print("This is not a savings account.")
            else:
                print("Account not found.")

        elif choice == "4":
            from_acc_num = int(input("Enter source account number: "))
            to_acc_num = int(input("Enter destination account number: "))
            amount = float(input("Enter amount to transfer (USD): "))
            my_bank.transfer(from_acc_num, to_acc_num, amount)

        elif choice == "5":
            acc_num = int(input("Enter account number: "))
            account = my_bank.find_account(acc_num)
            if account:
                print(account)
            else:
                print("Account not found.")

        elif choice == "6":
            print("Exiting the system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main()