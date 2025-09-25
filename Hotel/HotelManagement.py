# Moon Roadside Hotel Management System.
# This program simulates a roadside hotel management system where the hotel owner
# interacts with guests upon arrival, asks dynamic questions, and assigns rooms. The
# system is designed to create a friendly and engaging experience for users through
# interactive conversations, including short stories, emotion detection, humorous
# responses, and follow-up questions based on guest answers.


import random
import time
import re

# Dictionary of questions with response patterns, reactions, and follow-up questions
questions = {
    "Where are you from?": {
        "patterns": {
            r"tehran|teheran": {
                "response": "Oh, Tehran? How was the traffic there?",
                "follow_up": "Did you come through the crazy city traffic or take a shortcut?"
            },
            r"shiraz": {
                "response": "Shiraz, the city of poets! Got any Hafez verses to share?",
                "follow_up": "Visited any gardens there recently?"
            },
            r"north|mazandaran|gilan": {
                "response": "The green north? Love those forests!",
                "follow_up": "Did you see the sea or stick to the mountains?"
            },
            r".*": "Cool, sounds like a great place!"
        }
    },
    "It's pretty cold outside, isn't it?": {
        "patterns": {
            r"yes|cold|freezing": {
                "response": "Brr! Want a hot tea?",
                "follow_up": {
                    r"yes|yeah|sure": [
                        "Awesome, I'll get you a hot tea right away!",
                        "Great choice! Saffron tea or regular?"
                    ],
                    r"no|nah|nope": [
                        "No worries, maybe later then!",
                        "Alright, we'll keep the tea warm for you!"
                    ],
                    r".*": ["Okay, let me know if you change your mind!"]
                }
            },
            r"no|warm|hot": "Really? Guess you're used to tougher weather!",
            r".*": "Well, you must be comfy in our warm hotel then!"
        }
    },
    "Where are you headed?": {
        "patterns": {
            r"north|mazandaran|gilan": {
                "response": "Heading to the green north? Nice choice!",
                "follow_up": "Planning to hit the beach or explore the forests?"
            },
            r"south|kish|qeshm": {
                "response": "Oh, the sunny south? Beaches and all?",
                "follow_up": "Got any plans for water sports?"
            },
            r"no idea|dunno|don't know": {
                "response": "No destination? Then this hotel is your dream stop!",
                "follow_up": "Wanna explore around here instead?"
            },
            r".*": "Sounds like an adventure! Safe travels!"
        }
    },
    "How did you end up here?": {
        "patterns": {
            r"lost|wrong turn": "Haha, got lost and found us? Lucky you!",
            r"friend|recommended": "Nice to hear we come recommended!",
            r".*": "Well, we're glad fate brought you here!"
        }
    },
    "How many days are you planning to stay?": {
        "patterns": {
            r"\d+": "Alright, we'll make sure your stay is comfy!",
            r"not sure|maybe": "No worries, stay as long as you like!",
            r".*": "Cool, we'll sort out the details later!"
        }
    },
    "Have you been here before?": {
        "patterns": {
            r"yes|yeah": "Welcome back! Missed us, huh?",
            r"no|first": "First time? You're in for a treat!",
            r".*": "Well, we're happy to have you here!"
        }
    }
}

# Dictionary for emotion detection
emotions = {
    r"tired|exhausted|worn out": [
        "Oh, you sound beat! We'll get you a comfy room to relax.",
        "Tough day, huh? Don't worry, we've got a cozy spot for you."
    ],
    r"excited|great|awesome": [
        "Love your energy! Let's make your stay just as awesome!",
        "Wow, you're pumped! We've got something special for you."
    ],
    r"stressed|anxious": [
        "Sounds like you need a break. Our rooms are super relaxing!",
        "No stress here! We'll make sure you unwind."
    ]
}

# Dictionary for personalization question responses
personalization = {
    r"calm|relax|quiet": "Got it! We'll set up a cozy, calm vibe for your room.",
    r"fun|happy|cheerful": "Awesome! We'll make your room bright and cheerful!",
    r".*": "Alright, we'll make your room super comfy, just the way you like!"
}

# List of short stories for the hotel
stories = [
    "Last night, a guest left a mysterious old key in the lobby. Think it unlocks a secret room?",
    "They say a famous poet stayed here years ago and wrote a poem on our walls! Wanna hunt for it?",
    "One of our guests swore they heard music from an empty room last week. Spooky, right?"
]

# List of funny responses for unclear answers
funny_responses = [
    "Wait, did I hear that right? Are you from the moon or what?",
    "Haha, that's a new one! Are you a secret adventurer?",
    "You sound like you've got a wild story—spill the beans next time!"
]

# List of available rooms
rooms = {
    101: {"status": "available", "type": "Single", "price": 100000},
    102: {"status": "available", "type": "Single", "price": 100000},
    201: {"status": "available", "type": "Double", "price": 150000},
    202: {"status": "available", "type": "Double", "price": 150000},
    301: {"status": "available", "type": "Family", "price": 200000}
}

# Function to welcome the guest and handle dynamic conversation
def welcome_guest():
    print("Welcome to Moon Roadside Hotel! 🌙")
    time.sleep(1)
    name = input("What's your name? ")
    print(f"Alright {name}, let's have a chat!")
    time.sleep(1)
    
    # Track asked questions to avoid repetition
    asked_questions = []
    question_count = 0
    
    while question_count < 3:
        # Select a random unasked question
        available_questions = [q for q in questions.keys() if q not in asked_questions]
        if not available_questions:
            break
        question = random.choice(available_questions)
        asked_questions.append(question)
        
        print(question)
        answer = input("What's your answer? ").lower()
        time.sleep(1)
        
        # Check for emotions in the answer
        emotion_detected = False
        for pattern, responses in emotions.items():
            if re.search(pattern, answer):
                print(random.choice(responses))
                time.sleep(1)
                emotion_detected = True
                break
        
        # Find a matching response for the question
        response_found = False
        for pattern, response in questions[question]["patterns"].items():
            if re.search(pattern, answer):
                if isinstance(response, dict):
                    # Handle special cases (tea offer or follow-up questions)
                    print(response["response"])
                    time.sleep(1)
                    if "follow_up" in response:
                        if isinstance(response["follow_up"], dict):
                            # Tea offer case
                            tea_answer = input("So, what do you say? ").lower()
                            time.sleep(1)
                            for tea_pattern, tea_responses in response["follow_up"].items():
                                if re.search(tea_pattern, tea_answer):
                                    print(random.choice(tea_responses))
                                    break
                            else:
                                print(random.choice(response["follow_up"][r".*"]))
                        else:
                            # Regular follow-up question
                            print(response["follow_up"])
                            follow_up_answer = input("Tell me more: ").lower()
                            time.sleep(1)
                            # Check for emotions in follow-up answer
                            for pattern, responses in emotions.items():
                                if re.search(pattern, follow_up_answer):
                                    print(random.choice(responses))
                                    break
                            else:
                                print("Nice to know!")
                else:
                    print(response)
                response_found = True
                break
        
        if not response_found and not emotion_detected:
            print(random.choice(funny_responses))
        
        question_count += 1
        time.sleep(1)
    
    # Tell a short story
    story = random.choice(stories)
    print(f"By the way, {name}, here's a little something about our hotel: {story}")
    story_answer = input("What do you think? ").lower()
    time.sleep(1)
    for pattern, responses in emotions.items():
        if re.search(pattern, story_answer):
            print(random.choice(responses))
            break
    else:
        print("Haha, we'll see if you spot anything interesting during your stay!")
    
    # Ask a personalization question
    print("What kind of vibe do you want for your room? (e.g., calm, fun)")
    vibe = input("Your choice: ").lower()
    time.sleep(1)
    for pattern, response in personalization.items():
        if re.search(pattern, vibe):
            print(response)
            break
    
    print(f"Well then, welcome to our hotel, {name}!")
    time.sleep(1)
    return name

# Function to assign a room
def assign_room():
    available_rooms = [room for room, info in rooms.items() if info["status"] == "available"]
    
    if not available_rooms:
        print("Sorry, no rooms are available!")
        return None, None, None
    
    room_number = random.choice(available_rooms)
    room_type = rooms[room_number]["type"]
    room_price = rooms[room_number]["price"]
    rooms[room_number]["status"] = "occupied"
    
    return room_number, room_type, room_price

# Main function for hotel management
def main():
    print("*** Moon Roadside Hotel Management System ***")
    guest_name = welcome_guest()
    
    room_number, room_type, room_price = assign_room()
    
    if room_number:
        print(f"\nDear {guest_name}, your room is ready!")
        print(f"Room number: {room_number}")
        print(f"Room type: {room_type}")
        print(f"Cost per night: {room_price:,} IRR")
    else:
        print("Please try again later.")

# Run the program
if __name__ == "__main__":
    main()
    