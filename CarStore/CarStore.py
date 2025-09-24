# Import necessary modules
import sys
import json
import os
import uuid  # For generating unique VINs

# Define the Car class to represent each sports car, with more real-world attributes
class Car:
    def __init__(self, make, model, year, price, horsepower, top_speed, color="Black", mileage=0, vin=None):
        """
        Initialize a Car object with realistic attributes.
        :param make: Manufacturer (e.g., Ford, Chevrolet)
        :param model: Model name (e.g., Mustang, Corvette)
        :param year: Manufacturing year
        :param price: Price in USD
        :param horsepower: Engine horsepower
        :param top_speed: Top speed in mph
        :param color: Exterior color (default: Black)
        :param mileage: Current mileage in miles (default: 0)
        :param vin: Vehicle Identification Number (auto-generated if None)
        """
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.horsepower = horsepower
        self.top_speed = top_speed
        self.color = color
        self.mileage = mileage
        self.vin = vin if vin else str(uuid.uuid4())[:17]  # Generate a 17-char VIN-like unique ID
        self.is_sold = False  # Track if the car has been sold
        self.discount = 0.0  # Percentage discount for promotions

    def display_info(self):
        """Display detailed information about the car, including VIN and discount."""
        status = "Sold" if self.is_sold else "Available"
        discounted_price = self.price * (1 - self.discount / 100)
        return (f"{self.year} {self.make} {self.model} (VIN: {self.vin}) - Color: {self.color}, "
                f"Mileage: {self.mileage} miles, HP: {self.horsepower}, "
                f"Top Speed: {self.top_speed} mph, Original Price: ${self.price:.2f}, "
                f"Discount: {self.discount}%, Final Price: ${discounted_price:.2f} - Status: {status}")

    def update_price(self, new_price):
        """Update the base price of the car."""
        self.price = new_price
        print(f"Price updated for {self.make} {self.model} to ${new_price:.2f}")

    def apply_discount(self, discount_percent):
        """Apply a discount percentage to the car."""
        self.discount = discount_percent
        print(f"Applied {discount_percent}% discount to {self.make} {self.model}")

    def mark_as_sold(self):
        """Mark the car as sold."""
        if not self.is_sold:
            self.is_sold = True
            print(f"{self.make} {self.model} (VIN: {self.vin}) has been sold!")
        else:
            print(f"{self.make} {self.model} is already sold.")

# Define the Customer class for real-world sales tracking
class Customer:
    def __init__(self, name, email, phone):
        """
        Initialize a Customer object.
        :param name: Customer's full name
        :param email: Customer's email address
        :param phone: Customer's phone number
        """
        self.name = name
        self.email = email
        self.phone = phone
        self.purchases = []  # List of purchased car VINs

    def display_info(self):
        """Display customer information."""
        return f"Customer: {self.name}, Email: {self.email}, Phone: {self.phone}, Purchases: {len(self.purchases)} cars"

    def add_purchase(self, vin):
        """Add a purchased car VIN to the customer's record."""
        self.purchases.append(vin)

# Define the Sale class to record transactions
class Sale:
    def __init__(self, car, customer, sale_price, tax_rate=0.07):
        """
        Initialize a Sale object.
        :param car: The Car object sold
        :param customer: The Customer object
        :param sale_price: The final sale price (after discount)
        :param tax_rate: Sales tax rate (default 7%)
        """
        self.car_vin = car.vin
        self.customer_name = customer.name
        self.sale_price = sale_price
        self.tax = sale_price * tax_rate
        self.total = sale_price + self.tax
        self.date = "2023-10-01"  # Placeholder; in real-world, use datetime.now()

    def generate_receipt(self):
        """Generate a simple receipt string."""
        return (f"Receipt for {self.customer_name}:\n"
                f"Car VIN: {self.car_vin}\n"
                f"Sale Price: ${self.sale_price:.2f}\n"
                f"Tax: ${self.tax:.2f}\n"
                f"Total: ${self.total:.2f}\n"
                f"Date: {self.date}")

# Define the Inventory class to manage cars, customers, and sales
class Inventory:
    def __init__(self, data_file='inventory.json'):
        """Initialize inventory, loading from a JSON file for persistence."""
        self.cars = []  # List of Car objects
        self.customers = []  # List of Customer objects
        self.sales = []  # List of Sale objects
        self.data_file = data_file
        self.load_data()  # Load existing data if file exists
        if not self.cars:
            self.add_sample_cars()  # Add samples if empty

    def add_sample_cars(self):
        """Add some predefined American sports cars with realistic details."""
        self.add_car(Car("Ford", "Mustang GT", 2023, 55000, 450, 155, "Red", 5000))
        self.add_car(Car("Chevrolet", "Corvette Stingray", 2024, 65000, 495, 194, "Blue", 1000))
        self.add_car(Car("Dodge", "Challenger SRT Hellcat", 2022, 70000, 707, 199, "Black", 20000))
        self.add_car(Car("Tesla", "Roadster", 2025, 200000, 1000, 250, "Silver", 0))  # Electric sports car for variety
        print("Sample American sports cars added to inventory.")

    def add_car(self, car):
        """Add a new car to the inventory and save."""
        self.cars.append(car)
        self.save_data()
        print(f"Added {car.make} {car.model} (VIN: {car.vin}) to inventory.")

    def remove_car(self, index):
        """Remove a car from inventory by index and save."""
        if 0 <= index < len(self.cars):
            removed = self.cars.pop(index)
            self.save_data()
            print(f"Removed {removed.make} {removed.model} from inventory.")
        else:
            print("Invalid car index.")

    def add_customer(self, customer):
        """Add a new customer and save."""
        self.customers.append(customer)
        self.save_data()
        print(f"Added customer: {customer.name}")

    def record_sale(self, car, customer):
        """Record a sale, mark car as sold, add to customer purchases, and save."""
        if car.is_sold:
            print("Car is already sold.")
            return
        discounted_price = car.price * (1 - car.discount / 100)
        sale = Sale(car, customer, discounted_price)
        self.sales.append(sale)
        car.mark_as_sold()
        customer.add_purchase(car.vin)
        self.save_data()
        print(sale.generate_receipt())

    def search_cars(self, keyword, min_price=None, max_price=None, min_hp=None):
        """Advanced search for cars with filters for real-world querying."""
        results = []
        for car in self.cars:
            if (keyword.lower() in (car.make.lower() + car.model.lower() + str(car.year)) and
                (min_price is None or car.price >= min_price) and
                (max_price is None or car.price <= max_price) and
                (min_hp is None or car.horsepower >= min_hp)):
                results.append(car)
        if results:
            print("Search results:")
            for i, car in enumerate(results):
                print(f"{i}: {car.display_info()}")
        else:
            print("No cars found matching the search.")

    def display_all_cars(self):
        """Display all cars in the inventory."""
        if not self.cars:
            print("Inventory is empty.")
        else:
            print("Current Inventory:")
            for i, car in enumerate(self.cars):
                print(f"{i}: {car.display_info()}")

    def display_customers(self):
        """Display all customers."""
        if not self.customers:
            print("No customers registered.")
        else:
            print("Registered Customers:")
            for i, cust in enumerate(self.customers):
                print(f"{i}: {cust.display_info()}")

    def display_sales_report(self):
        """Display a simple sales report."""
        if not self.sales:
            print("No sales recorded.")
        else:
            total_revenue = sum(sale.total for sale in self.sales)
            print(f"Sales Report: {len(self.sales)} sales, Total Revenue: ${total_revenue:.2f}")
            for sale in self.sales:
                print(sale.generate_receipt())

    def get_car_by_index(self, index):
        """Retrieve a car by its index."""
        if 0 <= index < len(self.cars):
            return self.cars[index]
        return None

    def get_customer_by_index(self, index):
        """Retrieve a customer by its index."""
        if 0 <= index < len(self.customers):
            return self.customers[index]
        return None

    def save_data(self):
        """Save inventory, customers, and sales to JSON file with pretty printing."""
        data = {
            "cars": [vars(car) for car in self.cars],  # Convert to dict
            "customers": [vars(cust) for cust in self.customers],
            "sales": [{"car_vin": sale.car_vin, "customer_name": sale.customer_name,
                       "sale_price": sale.sale_price, "tax": sale.tax,
                       "total": sale.total, "date": sale.date} for sale in self.sales]
        }
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, sort_keys=True)  # Pretty print with 4-space indentation
        print("Data saved to file.")

    def load_data(self):
        """Load data from JSON file if exists."""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.cars = [Car(**car_data) for car_data in data.get("cars", [])]
            self.customers = [Customer(**cust_data) for cust_data in data.get("customers", [])]
            # Reconstruct sales (simplified, as Sale object reconstruction is complex)
            self.sales = [Sale(Car(vin=sale_data["car_vin"]), Customer(sale_data["customer_name"], "", ""),
                              sale_data["sale_price"], tax_rate=sale_data["tax"]/sale_data["sale_price"])
                         for sale_data in data.get("sales", [])]
            print("Data loaded from file.")

# Main function to run the store management program with more options
def main():
    inventory = Inventory()  # Create inventory instance with persistence

    while True:
        print("\n--- American Sports Car Dealership Management System ---")
        print("1. Display all cars")
        print("2. Add a new car")
        print("3. Search for cars (advanced)")
        print("4. Update car price")
        print("5. Apply discount to car")
        print("6. Sell a car (record sale)")
        print("7. Remove a car")
        print("8. Add a customer")
        print("9. Display customers")
        print("10. Display sales report")
        print("11. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            inventory.display_all_cars()
        elif choice == "2":
            make = input("Enter make (e.g., Ford): ")
            model = input("Enter model (e.g., Mustang): ")
            year = int(input("Enter year: "))
            price = float(input("Enter price: "))
            horsepower = int(input("Enter horsepower: "))
            top_speed = int(input("Enter top speed (mph): "))
            color = input("Enter color: ")
            mileage = int(input("Enter mileage: "))
            new_car = Car(make, model, year, price, horsepower, top_speed, color, mileage)
            inventory.add_car(new_car)
        elif choice == "3":
            keyword = input("Enter search keyword (make, model, or year): ")
            min_price = input("Min price (optional, press enter to skip): ")
            min_price = float(min_price) if min_price else None
            max_price = input("Max price (optional, press enter to skip): ")
            max_price = float(max_price) if max_price else None
            min_hp = input("Min horsepower (optional, press enter to skip): ")
            min_hp = int(min_hp) if min_hp else None
            inventory.search_cars(keyword, min_price, max_price, min_hp)
        elif choice == "4":
            inventory.display_all_cars()
            index = int(input("Enter car index to update price: "))
            car = inventory.get_car_by_index(index)
            if car:
                new_price = float(input("Enter new price: "))
                car.update_price(new_price)
                inventory.save_data()
            else:
                print("Invalid index.")
        elif choice == "5":
            inventory.display_all_cars()
            index = int(input("Enter car index to apply discount: "))
            car = inventory.get_car_by_index(index)
            if car:
                discount = float(input("Enter discount percentage: "))
                car.apply_discount(discount)
                inventory.save_data()
            else:
                print("Invalid index.")
        elif choice == "6":
            inventory.display_all_cars()
            car_index = int(input("Enter car index to sell: "))
            car = inventory.get_car_by_index(car_index)
            if car:
                inventory.display_customers()
                cust_index = int(input("Enter customer index: "))
                customer = inventory.get_customer_by_index(cust_index)
                if customer:
                    inventory.record_sale(car, customer)
                else:
                    print("Invalid customer index.")
            else:
                print("Invalid car index.")
        elif choice == "7":
            inventory.display_all_cars()
            index = int(input("Enter car index to remove: "))
            inventory.remove_car(index)
        elif choice == "8":
            name = input("Enter customer name: ")
            email = input("Enter email: ")
            phone = input("Enter phone: ")
            new_customer = Customer(name, email, phone)
            inventory.add_customer(new_customer)
        elif choice == "9":
            inventory.display_customers()
        elif choice == "10":
            inventory.display_sales_report()
        elif choice == "11":
            print("Exiting the program. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()