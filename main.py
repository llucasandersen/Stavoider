import turtle
import random
import time
import google.generativeai as genai
import pygame

# Initialization of the game and the necessary modules.
is_game_active = True
playernew = True
newtomini = True
pygame.init()
pygame.mixer.init()

# Loading sound effects for the game.
countdown_sound = pygame.mixer.Sound("audios/countdown.mp3")
gameover_sound = pygame.mixer.Sound("audios/gameover.mp3")
minigame_sound = pygame.mixer.Sound("audios/minigame.mp3")
move_sound = pygame.mixer.Sound("audios/Move.mp3")
youwin_sound = pygame.mixer.Sound("audios/youwin.mp3")
background = pygame.mixer.Sound("audios/backroundnoise.mp3")

# Configuration for the Google Gemini AI API.
# The API key can be supplied via the GEMINI_API_KEY environment variable.
import os
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    genai.configure(api_key="")

# Define the model generation configuration and safety settings.
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# Initialize the model with specified settings.
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Setup for the main game screen.
wn = turtle.Screen()
wn.bgcolor("black")
wn.setup(600, 600)
wn.title("Stavoider")

def setup_border():
    """
    Draws a border around the game screen.
    """
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
    """
    Creates and positions the player in the game.
    Returns a Turtle object representing the player.
    """
    player = turtle.Turtle()
    player.color("purple")
    player.shape("triangle")
    player.penup()
    player.speed(0)
    player.setposition(random.randint(-250, 290), random.randint(-290, 290))
    player.setheading(-90)
    return player

def setup_sprites(player, number_of_sprites, buffer=50, include_minigame_sprite=False):
    """
    Generates sprites for the game, avoiding placement too close to the player.
    Returns a list of Turtle objects representing the sprites.
    """
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
    """
    Draws a button with specified text and position.
    Returns a Turtle object that represents the button.
    """
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
    """
    Clears all turtles from the screen.
    """
    for turtle in wn.turtles():
        turtle.hideturtle()
    wn.clear()

def main_menu():
    """
    Displays the main menu of the game.
    """
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

    def tutorial():
        """
        Displays the tutorial for the game.
        """
        global playernew
        clear_screen()
        background.play()
        wn.bgcolor("black")
        tutorial_turtle = turtle.Turtle()
        tutorial_turtle.hideturtle()
        tutorial_turtle.color("white")
        tutorial_turtle.penup()
        tutorial_turtle.goto(0, 150)
        tutorial_turtle.write("Welcome to Stavoider!", align="center", font=("Arial", 24, "bold"))
        tutorial_turtle.goto(0, 100)
        tutorial_turtle.write("You are a spaceship trying to avoid asteroids.", align="center",
                              font=("Arial", 16, "normal"))
        tutorial_turtle.goto(0, 50)
        tutorial_turtle.write("Collect green asteroids to destroy other asteroids.", align="center",
                              font=("Arial", 16, "normal"))
        tutorial_turtle.goto(0, 0)
        tutorial_turtle.write("Use WASD or Arrow Keys to move:", align="center", font=("Arial", 16, "normal"))
        tutorial_turtle.goto(0, -50)
        tutorial_turtle.write("W or Up Arrow: Move Up", align="center", font=("Arial", 16, "normal"))
        tutorial_turtle.goto(0, -100)
        tutorial_turtle.write("A or Left Arrow: Move Left", align="center", font=("Arial", 16, "normal"))
        tutorial_turtle.goto(0, -150)
        tutorial_turtle.write("S or Down Arrow: Move Down", align="center", font=("Arial", 16, "normal"))
        tutorial_turtle.goto(0, -200)
        tutorial_turtle.write("D or Right Arrow: Move Right", align="center", font=("Arial", 16, "normal"))

        # Allow some time to read the tutorial
        wn.update()
        time.sleep(9)
        playernew = False
        score = 0
        slowdownscore = 0
        wn.onscreenclick(None)
        clear_screen()
        wn.tracer(0)
        setup_border()
        player = setup_player()
        setup_key_bindings(player)
        sprites = setup_sprites(player, number_of_sprites=75, include_minigame_sprite=True)
        wn.bgcolor("black")
        countdown()  # Initiate countdown before the game starts
        game_loop(player, sprites, score, slowdownscore)

    def playonenter():
        """
        Initiates the game or tutorial when the player selects the play option.
        """
        global is_game_active, playernew
        is_game_active = True
        if playernew:
            playernew = False
            tutorial()
        else:
            score = 0
            slowdownscore = 0
            wn.onscreenclick(None)
            clear_screen()
            wn.tracer(0)
            setup_border()
            player = setup_player()
            setup_key_bindings(player)
            sprites = setup_sprites(player, number_of_sprites=75, include_minigame_sprite=True)
            wn.bgcolor("black")
            countdown()  # Initiate countdown before the game starts
            game_loop(player, sprites, score, slowdownscore)

    wn.listen()
    wn.onkey(playonenter, "Return")

    def on_click(x, y):
        """
        Handles mouse clicks on the play and exit buttons.
        """
        if -50 <= x <= 50:
            if -25 <= y <= 25:
                global is_game_active, playernew
                is_game_active = True
                if playernew:
                    tutorial()
                else:
                    score = 0
                    slowdownscore = 0
                    wn.onscreenclick(None)
                    clear_screen()
                    wn.tracer(0)
                    setup_border()
                    player = setup_player()
                    setup_key_bindings(player)
                    sprites = setup_sprites(player, number_of_sprites=75, include_minigame_sprite=True)
                    wn.bgcolor("black")
                    countdown()  # Initiate countdown before the game starts
                    game_loop(player, sprites, score, slowdownscore)
            elif -100 <= y <= -50:
                close_game()

    wn.onscreenclick(on_click)

def countdown():
    """
    Plays a countdown sound and displays countdown from 3 to 1.
    """
    countdown_sound.play()
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

def tutorialmini(player, score, sprites, slowdownscore):
    """
    Displays the tutorial for the mini-game.
    """
    global newtomini
    newtomini = False
    clear_screen()
    background.play()
    wn.bgcolor("black")
    tutorial_turtle = turtle.Turtle()
    tutorial_turtle.hideturtle()
    tutorial_turtle.color("white")
    tutorial_turtle.penup()
    tutorial_turtle.goto(0, 150)
    tutorial_turtle.write("You have reached the Typing Mini Game", align="center", font=("Arial", 22, "bold"))
    tutorial_turtle.goto(0, 100)
    tutorial_turtle.write("There will be a prompt that you will write out in the text box.", align="center",
                          font=("Arial", 16, "normal"))
    tutorial_turtle.goto(0, 50)
    tutorial_turtle.write('When you are done press "Enter".', align="center",
                          font=("Arial", 16, "normal"))
    tutorial_turtle.goto(0, 0)
    tutorial_turtle.write("Tips:", align="center", font=("Arial", 16, "normal"))
    tutorial_turtle.goto(0, -50)
    tutorial_turtle.write("You are timed.", align="center", font=("Arial", 16, "normal"))
    tutorial_turtle.goto(0, -100)
    tutorial_turtle.write("Don't forget the period.", align="center", font=("Arial", 16, "normal"))
    tutorial_turtle.goto(0, -150)
    tutorial_turtle.write("Don't forget commas.", align="center", font=("Arial", 16, "normal"))
    tutorial_turtle.goto(0, -200)
    tutorial_turtle.write("You can move the Entry box if needed.", align="center", font=("Arial", 16, "normal"))
    wn.update()
    time.sleep(9)
    trigger_minigame(player, score, sprites, slowdownscore)

def game_loop(player, sprites, score, slowdownscore):
    """
    Main game loop that continuously updates and checks for game events.
    """
    global is_game_active, newtomini
    minigame_sprite = sprites[-1]  # Assume the last sprite is the minigame trigger
    minigame_move_timer = time.time()  # To track when to move the minigame_sprite

    while is_game_active:
        wn.update()
        # Move minigame_sprite every second

        if minigame_sprite.xcor() > 290:  # Check if it's beyond the right boundary
            minigame_sprite.setx(-290)  # Teleport to the left side
        x = minigame_sprite.xcor()
        x += 1
        minigame_sprite.setx(x)

        for sprite in sprites[:-1]:  # All sprites except the minigame trigger
            x = sprite.xcor()
            x += 1.5 + (score / 30) - slowdownscore
            sprite.setx(x)
            if sprite.xcor() > 290:
                y = sprite.ycor()
                y = random.randint(-290, 290)
                sprite.sety(y)
                sprite.setx(-290)
            if player.distance(sprite) < 15:
                gameover_sound.play()
                player.goto(400, 400)
                minigame_sprite.goto(-400, -400)
                if is_game_active:  # Ensure the game didn't exit during the delay
                    wn.clear()
                    end_game(score, sprites)
                running = False
        # Check for collision with the minigame sprite
        if player.distance(minigame_sprite) < 20 and is_game_active:  # Ensure game is still running
            minigame_sound.play()
            if newtomini:
                newtomini = False
                tutorialmini(player, score, sprites, slowdownscore)
            else:
                trigger_minigame(player, score, sprites, slowdownscore)
        score += 0.01

def wrap_text(text, wrap_length):
    """
    Wraps text to the specified length.
    """
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

def trigger_minigame(player, score, sprites, slowdownscore):
    """
    Trigger the typing mini-game when the player collides with the minigame sprite.
    """
    global is_game_active
    if not is_game_active:
        end_game(score, sprites)
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
        minigame_turtle.goto(0, 190)
        minigame_turtle.write("Typing Mini-Game!", align="center", font=("Arial", 24, "bold"))

        prompt = (f"Generate a sentence about dodging that is roughly {int(score)} words long. If the score is 0 then "
                  f"make a 1 word long sentence.")

        try:
            prompt_parts = [{"text": prompt}]
            response = model.generate_content(prompt_parts)
            challenge_sentence = response.text.strip().lower()  # Normalize the text for comparison
            challenge_sentenceshow = response.text
        except Exception as ex:
            challenge_sentenceshow = "dodge the hurdles swiftly!"  # Fallback sentence
            challenge_sentence = "dodge the hurdles swiftly!"

        word_count = len(challenge_sentence.split()) * 2.25  # Count the words
        minigame_turtle.goto(0, 50)
        wrapped_sentence = wrap_text(challenge_sentenceshow, 40)
        minigame_turtle.write(wrapped_sentence, align="center", font=("Arial", 12, "normal"))
        wn.update()  # Update the screen to show the mini-game prompt

        start_time = time.time()  # Record the time at which input starts
        user_input = wn.textinput("Mini-Game",
                                  f"Type the sentence exactly as shown above (Time: {int(word_count)} seconds):").strip().lower()
        elapsed_time = time.time() - start_time

        if user_input == challenge_sentence and elapsed_time <= word_count:
            minigame_turtle.goto(0, 20)
            score += 5
            slowdownscore += score / 50
            number_of_sprites -= 5 + word_count - elapsed_time
            number_of_spritesrounded = int(number_of_sprites)
            minigame_turtle.write(f"+5 Score. Only {number_of_spritesrounded} asteroids remain. Good timing!", align="center",
                                  font=("Arial", 18, "normal"))
            minigame_turtle.goto(0, -1)
            minigame_turtle.write(f"Took {elapsed_time:.2f} seconds.", align="center",
                                  font=("Arial", 18, "normal"))
            time.sleep(2)
        else:
            print(elapsed_time)
            minigame_turtle.goto(0, 20)
            if user_input != challenge_sentence:
                minigame_turtle.write(f"Incorrect.", align="center", font=("Arial", 18, "normal"))
            else:
                minigame_turtle.write(f"Too slow.", align="center", font=("Arial", 18, "normal"))
                minigame_turtle.goto(0, 0)
                minigame_turtle.write(f"Took {elapsed_time:.2f} seconds and had {word_count} seconds.", align="center", font=("Arial", 18, "normal"))


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
        game_loop(player, sprites, score, slowdownscore)

def setup_key_bindings(player):
    """
    Sets up the key bindings for player movement.
    """
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
    """
    Moves the player left when the corresponding key is pressed.
    """
    x = player.xcor()
    x -= 15
    if x < -280:
        x = -280
    move_sound.play()
    player.setx(x)

def move_right(player):
    """
    Moves the player right when the corresponding key is pressed.
    """
    x = player.xcor()
    x += 15
    if x > 280:
        x = 280
    move_sound.play()
    player.setx(x)

def move_up(player):
    """
    Moves the player up when the corresponding key is pressed.
    """
    y = player.ycor()
    y += 15
    if y > 280:
        y = 280
    move_sound.play()
    player.sety(y)

def move_down(player):
    """
    Moves the player down when the corresponding key is pressed.
    """
    y = player.ycor()
    y -= 15
    if y < -280:
        y = -280
    move_sound.play()
    player.sety(y)

def end_game(score, sprites):
    """
    Handles game termination and displays the final score.
    """
    global is_game_active
    is_game_active = False
    sprites = len(sprites)
    clear_screen()
    setup_border()
    wn.bgcolor("black")
    score_display = turtle.Turtle()
    score_display.hideturtle()
    score_display.color("white")
    score_display.penup()
    score_display.goto(0, 100)
    if sprites == 0:
        youwin_sound.play()
        score_display.goto(0, 130)
        score_display.write("You Won", align="center", font=("Arial", 30, "normal"))
    else:
        # Determine score message
        if score <= 9:
            message = "You weren't even trying."
        elif score <= 19:
            message = "Okay, that's a solid score."
        elif score <= 25:
            message = "You're pretty good at this game."
        elif score <= 47:
            message = "You were made for this game."
        else:
            message = "No one is better than you. That's a crazy score."
        score_display.write(message, align="center", font=("Arial", 18, "normal"))

    score_display.goto(0, 50)
    score_display.write(f"Score: {int(score)}", align="center", font=("Arial", 24, "normal"))
    play_again_button = draw_button("Play Again", -50, -25, "grey")
    exit_button = draw_button("Exit", -50, -100)

    def tryagain():
        """
        Resets the game when the play again button is clicked.
        """
        play_again_button.clear()
        wn.onscreenclick(None)
        main_menu()

    wn.listen()
    wn.onkey(tryagain, "Return")

    def on_click(x, y):
        """
        Handles clicks on the play again or exit buttons.
        """
        if -50 <= x <= 50:
            if -25 <= y <= 25:
                play_again_button.clear()
                wn.onscreenclick(None)
                main_menu()
            elif -100 <= y <= -50:
                close_game()

    wn.onscreenclick(on_click)

def close_game():
    """
    Closes the game window.
    """
    wn.bye()

def main():
    """
    Main entry point of the program. Calls the main menu.
    """
    main_menu()
    wn.update()

main()
wn.mainloop()
