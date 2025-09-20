import turtle
import random  # Import random module for random steps

WIDTH, HEIGHT = 500, 500
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title('Turtle Racing!')

def get_number_of_racers():
    """Prompt user for the number of racers (2-10)."""
    while True:
        racers = input("Enter the number of racers (2 - 10): ")
        if not racers.isdigit():
            print("Input is not numeric... Try again!")
            continue
        
        racers = int(racers)
        if 2 <= racers <= 10:
            return racers
        print("Input is out of range... Try again!")

num_of_racers = get_number_of_racers()
colors = ['red', 'blue', 'green', 'orange', 'purple', 'yellow', 'pink', 'brown', 'cyan', 'magenta']
# Check if there are enough colors for the number of racers
if num_of_racers > len(colors):
    print(f"Error: Maximum {len(colors)} racers are supported due to color limitations.")
    exit()

racers = [] 
start_x = -WIDTH // 2 + 20
start_y = -(num_of_racers - 1) * 20 // 2
finish_line = WIDTH // 2 - 20

# Draw the finish line
finish = turtle.Turtle()
finish.penup()
finish.goto(finish_line, HEIGHT // 2)
finish.pendown()
finish.goto(finish_line, -HEIGHT // 2)
finish.hideturtle()

# Create the racers
for i in range(num_of_racers):
    racer = turtle.Turtle()
    racer.color(colors[i])
    racer.shape('turtle')
    racer.penup()
    racer.goto(start_x, start_y + i * 20)
    racers.append(racer)

print("The race is about to begin!")
# Main race loop
while True:
    for racer in racers:
        step = random.randint(1, 10)  # Random step between 1 and 10
        racer.forward(step)
        if racer.xcor() >= finish_line:
            winner_color = racer.color()[0]
            print(f"The winner is the {winner_color} turtle!")
            screen.bye()  # Close the window
            exit()