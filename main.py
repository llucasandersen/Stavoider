import turtle
import random

wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(600, 600)
wn.title("Stavoider")


def setup_border():
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-290, 290)
    border_pen.pendown()
    border_pen.pensize(3)
    for side in range(4):
        border_pen.fd(600)
        border_pen.lt(90)
    border_pen.hideturtle()


def setup_player():
    player = turtle.Turtle()
    player.color("purple")
    player.shape("triangle")
    player.penup()
    player.speed(0)
    player.setposition(0, 0)
    player.setheading(-90)
    return player


def setup_sprites(number_of_sprites, buffer=50):
    sprites = []
    while len(sprites) < number_of_sprites:
        sprite = turtle.Turtle()
        sprite.color("orange")
        sprite.shape("circle")
        sprite.penup()
        sprite.setposition(290, 290)
        sprite.speed(0)
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        if abs(x) > buffer or abs(y) > buffer:
            sprite.setposition(x, y)
            sprites.append(sprite)
    return sprites


def draw_button(text, x, y, color="grey"):
    button = turtle.Turtle()
    button.hideturtle()
    button.speed(0)
    button.penup()
    button.goto(x, y)
    button.fillcolor(color)
    button.begin_fill()
    for _ in range(2):
        button.forward(100)
        button.left(90)
        button.forward(50)
        button.left(90)
    button.end_fill()
    button.goto(x + 50, y + 10)
    button.color("white")
    button.write(text, align="center", font=("Arial", 16, "normal"))
    return button

def clear_screen():
    for turtle in wn.turtles():
        turtle.hideturtle()
    wn.clear()


def main_menu():
    clear_screen()
    wn.bgcolor("black")
    title_turtle = turtle.Turtle()
    title_turtle.hideturtle()
    title_turtle.color("white")
    title_turtle.penup()
    title_turtle.goto(0, 100)
    title_turtle.write("Stavoider", align="center", font=("Arial", 30, "bold"))
    play_button = draw_button("Play", -50, -25)

    def on_click(x, y):
        if -50 <= x <= 50 and -25 <= y <= 25:
            wn.onscreenclick(None)
            clear_screen()
            wn.tracer(0)
            setup_border()
            player = setup_player()
            setup_key_bindings(player)
            sprites = setup_sprites(number_of_sprites=70)
            wn.bgcolor("black")
            game_loop(player, sprites)

    wn.onscreenclick(on_click)


def game_loop(player, sprites):
    score = 0
    e = True
    while e:
        wn.update()
        for sprite in sprites:
            x = sprite.xcor()
            x += 2
            sprite.setx(x)
            if sprite.xcor() > 290:
                y = sprite.ycor()
                y = random.randint(-290, 290)
                sprite.sety(y)
                sprite.setx(-290)
            if player.distance(sprite) < 20:
                end_game(score)
                e = False
        score += 0.01

def setup_key_bindings(player):
    wn.listen()
    wn.onkey(lambda: move_left(player), "a")
    wn.onkey(lambda: move_right(player), "d")
    wn.onkey(lambda: move_up(player), "w")
    wn.onkey(lambda: move_down(player), "s")

def move_left(player):
    x = player.xcor()
    x -= 15
    if x < -280:
        x = -280
    player.setx(x)

def move_right(player):
    x = player.xcor()
    x += 15
    if x > 280:
        x = 280
    player.setx(x)

def move_up(player):
    y = player.ycor()
    y += 15
    if y > 280:
        y = 280
    player.sety(y)

def move_down(player):
    y = player.ycor()
    y -= 15
    if y < -280:
        y = -280
    player.sety(y)


def end_game(score):
    clear_screen()
    setup_border()
    wn.bgcolor("black")  # Ensure the background is black
    score_display = turtle.Turtle()
    score_display.hideturtle()
    score_display.color("white")
    score_display.penup()
    score_display.goto(0, 100)
    score_display.write(f"Score: {int(score)}", align="center", font=("Arial", 24, "normal"))
    play_again_button = draw_button("Play Again", -50, -25, "grey")
    wn.onscreenclick(lambda x, y: restart_game(x, y, play_again_button))

def restart_game(x, y, play_again_button):
    if -50 <= x <= 50 and -25 <= y <= 25:
        play_again_button.clear()
        wn.onscreenclick(None)
        main_menu()

def main():
    main_menu()
    wn.update()

main()
wn.mainloop()
