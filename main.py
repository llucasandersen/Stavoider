import turtle
import random
import time
import google.generativeai as genai

# Configure the Google Gemini AI
genai.configure(api_key="AIzaSyCJTc3g3cFaS3Vr16xfiuHnXC6XzPdwnW0")

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(600, 600)
wn.title("Stavoider")


def setup_border():
    border_pen = turtle.Turtle()
    border_pen.speed(0)
    border_pen.color("white")
    border_pen.penup()
    border_pen.setposition(-300, -290)
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
    player.setposition(random.randint(-250, 290), random.randint(-290, 290))
    player.setheading(-90)
    return player


def setup_sprites(player, number_of_sprites, buffer=50, include_minigame_sprite=False):
    sprites = []
    while len(sprites) < number_of_sprites:
        sprite = turtle.Turtle()
        sprite.color("orange")
        sprite.shape("circle")
        sprite.penup()
        sprite.setposition(290, 290)
        sprite.speed(0)
        is_too_close = True
        while is_too_close:
            x = random.randint(-290, 290)
            y = random.randint(-290, 290)
            if abs(x) > buffer or abs(y) > buffer:
                if player.distance(x, y) > 40:  # Check distance from the player
                    sprite.setposition(x, y)
                    is_too_close = False
        sprites.append(sprite)
    if include_minigame_sprite:
        minigame_sprite = turtle.Turtle()
        minigame_sprite.color("green")
        minigame_sprite.shape("circle")
        minigame_sprite.penup()
        minigame_sprite.setposition(random.randint(-240, 290), random.randint(-290, 290))
        minigame_sprite.speed(0)
        sprites.append(minigame_sprite)
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
    title_turtle.write("Stavoider", align="center", font=("Copperplate Gothic", 50, "bold"))
    title_turtle.goto(0, -150)
    title_turtle.write("Made by Lucas", align="center", font=("Copperplate Gothic", 15, "bold"))
    play_button = draw_button("Play", -50, -25)
    exit_button = draw_button("Exit", -50, -100)

    def on_click(x, y):
        if -50 <= x <= 50:
            if -25 <= y <= 25:
                score = 0
                wn.onscreenclick(None)
                clear_screen()
                wn.tracer(0)
                setup_border()
                player = setup_player()
                setup_key_bindings(player)
                sprites = setup_sprites(player, number_of_sprites=75, include_minigame_sprite=True)
                wn.bgcolor("black")
                countdown()  # Initiate countdown before the game starts
                game_loop(player, sprites, score)
            elif -100 <= y <= -50:
                close_game()

    wn.onscreenclick(on_click)


def countdown():
    countdown_turtle = turtle.Turtle()
    countdown_turtle.hideturtle()
    countdown_turtle.color("white")
    countdown_turtle.penup()
    countdown_turtle.goto(0, 0)
    for i in range(3, 0, -1):
        countdown_turtle.clear()
        countdown_turtle.write(f"{i}...", align="center", font=("Arial", 40, "bold"))
        wn.update()
        time.sleep(1)
    countdown_turtle.clear()


def game_loop(player, sprites, score):
    e = True
    minigame_sprite = sprites[-1]  # Assume the last sprite is the minigame trigger
    while e:
        wn.update()
        for sprite in sprites[:-1]:  # All sprites except the minigame trigger
            x = sprite.xcor()
            x += (1.5 + (score / 30))
            sprite.setx(x)
            if sprite.xcor() > 290:
                y = sprite.ycor()
                y = random.randint(-290, 290)
                sprite.sety(y)
                sprite.setx(-290)
            if player.distance(sprite) < 15:
                player.goto(400, 400)
                end_game(score)
                e = False
        # Check for collision with the minigame sprite
        if player.distance(minigame_sprite) < 15:
            trigger_minigame(player, score, sprites, e)
        score += 0.01

def wrap_text(text, wrap_length):
    """Wrap text to the specified length."""
    words = text.split()
    wrapped_text = ""
    line = ""
    for word in words:
        if len(line) + len(word) + 1 <= wrap_length:
            line += (word + " ")
        else:
            wrapped_text += (line.strip() + "\n")
            line = word + " "
    wrapped_text += line.strip()
    return wrapped_text


def trigger_minigame(player, score, sprites, e):
    if e == False:
        end_game(score)
    else:
        number_of_sprites = len(sprites)
        print(f"score: {score}")

        wn.tracer(0)  # Stop updating the screen
        clear_screen()
        setup_border()
        wn.bgcolor("black")  # Reset background color

        minigame_turtle = turtle.Turtle()
        minigame_turtle.hideturtle()
        minigame_turtle.color("white")
        minigame_turtle.penup()
        minigame_turtle.goto(0, 150)
        minigame_turtle.write("Typing Mini-Game!", align="center", font=("Arial", 24, "bold"))

        prompt = f"Generate a creative sentence about dodging that is roughly {int(score)} words long."

        try:
            prompt_parts = [{"text": prompt}]
            response = model.generate_content(prompt_parts)
            challenge_sentence = response.text.strip().lower()  # Normalize the text for comparison
        except Exception as ex:
            challenge_sentence = "dodge the hurdles swiftly!"  # Fallback sentence

        wrapped_sentence = wrap_text(challenge_sentence, 40)  # Wrap text to fit the screen
        minigame_turtle.goto(0, 50)
        minigame_turtle.write(wrapped_sentence, align="center", font=("Arial", 18, "normal"))
        wn.update()  # Update the screen to show the mini-game prompt

        user_input = wn.textinput("Mini-Game", "Type the sentence exactly as shown above:").strip().lower()
        if user_input == challenge_sentence:
            minigame_turtle.goto(0, 30)
            score += 5
            number_of_sprites -= max(6, int(0.1 * number_of_sprites))
            minigame_turtle.write(f"+5 Score. Only {number_of_sprites} asteroids remain.", align="center",
                                  font=("Arial", 18, "normal"))
            time.sleep(3)
        else:
            minigame_turtle.goto(0, 30)
            minigame_turtle.write(f"Incorrect", align="center", font=("Arial", 18, "normal"))
            time.sleep(1)
        # Clean up mini-game elements
        minigame_turtle.clear()
        minigame_turtle.hideturtle()

        # Reset the game to continue
        wn.onscreenclick(None)
        clear_screen()
        wn.tracer(0)
        setup_border()
        player = setup_player()
        setup_key_bindings(player)
        sprites = setup_sprites(player, number_of_sprites=number_of_sprites, include_minigame_sprite=True)
        wn.bgcolor("black")
        countdown()  # Initiate countdown before the game starts
        game_loop(player, sprites, score)


def setup_key_bindings(player):
    wn.listen()
    wn.onkey(lambda: move_left(player), "Left")
    wn.onkey(lambda: move_right(player), "Right")
    wn.onkey(lambda: move_up(player), "Up")
    wn.onkey(lambda: move_down(player), "Down")
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
    wn.bgcolor("black")
    score_display = turtle.Turtle()
    score_display.hideturtle()
    score_display.color("white")
    score_display.penup()
    score_display.goto(0, 100)

    # Determine score message
    if score <= 8:
        message = "You weren't even trying."
    elif score <= 11:
        message = "Okay, that's a solid score."
    elif score <= 18:
        message = "You're pretty good at this game."
    elif score <= 25:
        message = "You were made for this game."
    else:
        message = "No one is better than you. That's a crazy score."

    score_display.write(message, align="center", font=("Arial", 18, "normal"))
    score_display.goto(0, 50)
    score_display.write(f"Score: {int(score)}", align="center", font=("Arial", 24, "normal"))
    play_again_button = draw_button("Play Again", -50, -25, "grey")
    exit_button = draw_button("Exit", -50, -100)

    def on_click(x, y):
        if -50 <= x <= 50:
            if -25 <= y <= 25:
                play_again_button.clear()
                wn.onscreenclick(None)
                main_menu()
            elif -100 <= y <= -50:
                close_game()

    wn.onscreenclick(on_click)


def close_game():
    wn.bye()


def main():
    main_menu()
    wn.update()


main()
wn.mainloop()
