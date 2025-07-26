import turtle

screen = turtle.Screen()
screen.title("🎨 Turtle Drawing App")
screen.bgcolor("black")

pen = turtle.Turtle()
pen.speed(0)
pen.pensize(3)
pen.color("white")

colors = ["red", "green", "blue", "yellow", "purple", "white"]
color_index = 0

def move_forward():
    pen.forward(20)

def move_backward():
    pen.backward(20)

def turn_left():
    pen.left(15)

def turn_right():
    pen.right(15)

def clear():
    pen.clear()

def change_color():
    global color_index
    color_index = (color_index + 1) % len(colors)
    pen.color(colors[color_index])

def toggle_pen():
    if pen.isdown():
        pen.penup()
    else:
        pen.pendown()

# Key bindings
screen.listen()
screen.onkey(move_forward, "Up")
screen.onkey(move_backward, "Down")
screen.onkey(turn_left, "Left")
screen.onkey(turn_right, "Right")
screen.onkey(clear, "c")
screen.onkey(change_color, "space")
screen.onkey(toggle_pen, "p")

print("🖱️ Controls:")
print("Arrow keys to move")
print("Space to change color")
print("'p' to toggle pen")
print("'c' to clear screen")

screen.mainloop()
