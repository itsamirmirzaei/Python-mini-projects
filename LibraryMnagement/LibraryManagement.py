# Library Management System with persistent storage and book addition
# This program allows users to search for books by topic, add new books, and save data to a file.

import json

# Initialize the library as a dictionary with topics and an expanded list of famous books
library = {
    "programming": [
        {"title": "Python Made Simple", "author": "John Smith", "description": "A comprehensive guide to learning Python from beginner to advanced."},
        {"title": "Algorithms and Data Structures", "author": "Jane Doe", "description": "Fundamental concepts of algorithms and data structures with practical examples."},
        {"title": "Clean Code", "author": "Robert C. Martin", "description": "A handbook of agile software craftsmanship for writing clean and maintainable code."},
        {"title": "The Pragmatic Programmer", "author": "Andrew Hunt and David Thomas", "description": "A guide to becoming a better programmer with practical advice and best practices."},
        {"title": "Introduction to Algorithms", "author": "Thomas H. Cormen et al.", "description": "A comprehensive textbook on algorithms, widely used in computer science education."}
    ],
    "novel": [
        {"title": "The Little Prince", "author": "Antoine de Saint-Exupéry", "description": "A philosophical and touching story about friendship and meaning."},
        {"title": "One Hundred Years of Solitude", "author": "Gabriel García Márquez", "description": "A magical realist novel about the history of a family."},
        {"title": "1984", "author": "George Orwell", "description": "A dystopian novel exploring themes of totalitarianism and surveillance."},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "description": "A classic romance novel about love, class, and societal expectations."},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "description": "A powerful story about racial injustice and moral growth in the American South."}
    ],
    "science": [
        {"title": "A Short History of Nearly Everything", "author": "Bill Bryson", "description": "An engaging overview of the history of science and the universe."},
        {"title": "On the Origin of Species", "author": "Charles Darwin", "description": "A classic book on the theory of evolution."},
        {"title": "Cosmos", "author": "Carl Sagan", "description": "An inspiring exploration of the universe and humanity's place in it."},
        {"title": "The Selfish Gene", "author": "Richard Dawkins", "description": "A groundbreaking book on evolutionary biology and gene-centered evolution."},
        {"title": "A Brief History of Time", "author": "Stephen Hawking", "description": "A popular science book explaining complex concepts like black holes and the Big Bang."}
    ]
}

# Load library data from a JSON file
def load_library():
    global library
    try:
        with open("library.json", "r") as file:
            library = json.load(file)
        print("Library data loaded successfully.")
    except FileNotFoundError:
        print("No previous library data found. Starting with default library.")

# Save library data to a JSON file
def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file, indent=4)
    print("Library data saved successfully.")

# Function to add a new book to the library
def add_book():
    topic = input("Enter the topic for the book: ").strip().lower()
    if not topic:
        print("Error: Topic cannot be empty.")
        return
    title = input("Enter the book title: ").strip()
    if not title:
        print("Error: Title cannot be empty.")
        return
    author = input("Enter the author name: ").strip()
    description = input("Enter a brief description: ").strip()
    if topic not in library:
        library[topic] = []
    library[topic].append({"title": title, "author": author, "description": description})
    save_library()
    print(f"Book '{title}' added successfully to topic '{topic}'!")

# Function to search for books by topic
def search_books(topic):
    topic = topic.strip().lower()
    for key in library.keys():
        if topic in key.lower():
            return library[key]
    return None

# Main function to handle user interaction
def main():
    # Load library data at startup
    load_library()
    print("Welcome to the Library Management System!")
    while True:
        # Display available topics
        print("\nAvailable topics:", ", ".join(library.keys()))
        print("Enter a topic (e.g., programming, novel, science), 'add' to add a book, or 'exit' to quit:")
        user_input = input("> ").strip().lower()
        
        # Handle user commands
        if user_input == "exit":
            save_library()
            print("Thank you for using the system!")
            break
        elif user_input == "add":
            add_book()
        elif not user_input:
            print("Error: Please enter a valid topic or command.")
        else:
            books = search_books(user_input)
            if books:
                print(f"\nRecommended books for the topic '{user_input}':")
                for book in books:
                    print(f"\nTitle: {book['title']}")
                    print(f"Author: {book['author']}")
                    print(f"Description: {book['description']}")
            else:
                print(f"\nSorry, no books found for the topic '{user_input}'.")

# Entry point of the program
if __name__ == "__main__":
    main()