from tkinter import Tk, Canvas, PhotoImage, Button, Label, Entry, Radiobutton, IntVar
from random import randint as rand
from time import sleep
import time
# Screen Resolution is 1280x720
# Controls: 'Space' to jump, 'p' to pause, 'i' for invincibility, 's' to slow game down, 'b' for boss key

##### FUNCTIONS #####
def countdown():
    global isLoaded
    canvas.itemconfig(countdown_text, state="normal")
    canvas.itemconfig(flappy_bird, state="normal")
    # if file not loaded then keep bird at starting place otherwise keep it as saved place
    if not isLoaded:
        canvas.coords(flappy_bird, 200, 320)
    countdown = 3
    while countdown > 0:
        canvas.itemconfig(countdown_text, text = str(countdown))
        window.update()
        sleep(1)
        countdown -= 1
    canvas.itemconfig(countdown_text, text = "Go!")
    window.update()
    sleep(1)
    canvas.itemconfig(countdown_text, state="hidden")

def create_pipes():
    global chosenDifficulty
    i = 0
    x1 = 1300
    x2 = 1450
    delete_pipes()
    if not isLoaded:
        chosenDifficulty = difficulty.get()
    # difficulty.get() is 1 when easy mode, 2 when normal mode
    if chosenDifficulty == 1:
        gap = 500
    else:
        gap = 250
    # loop to create three top and bottom pipes (3 pipe groups)
    while i < 3:
        # selecting random y value to place the top pipe at depending on chosen difficulty
        if gap == 250:
            y = rand(10, 450)
        else:
            y = rand(10, 210)
        # creating top and bottom pipes with gap between them defined by chosen difficulty
        tp = canvas.create_rectangle(x1, -200, x2, y, fill="#1FB533", tags="tp", width = 2, outline = "black")
        bp = canvas.create_rectangle(x1, y + gap, x2, 730, fill="#1FB533", tags="bp", width = 2, outline = "black")
        canvas.tag_lower(tp)
        canvas.tag_lower(bp)
        top_pipes.append(tp)
        bottom_pipes.append(bp)
        # increasing the x coordinates so that there is equal distance between each pipe group
        x1 = x1 + 1430/3
        x2 = x2 + 1430/3
        i = i + 1

def delete_pipes():
    canvas.delete("tp")
    canvas.delete("bp")
    top_pipes.clear()
    bottom_pipes.clear()

def move_pipes():
    global chosenDifficulty, slowedPipes
    if slowedPipes:
        pipeSpeed = -3
    else:
        pipeSpeed = -5
    if chosenDifficulty == 1:
        gap = 500
    else:
        gap = 250
    for i in range(3):
        pos_top_pipe = canvas.coords(top_pipes[i])
        pos_bottom_pipe = canvas.coords(bottom_pipes[i])
        # if the pipes haven't reached the left side of the screen then move pipes to the left
        if pos_top_pipe[2] > 0 or pos_bottom_pipe[2] > 0:
            canvas.move(bottom_pipes[i], pipeSpeed, 0)
            canvas.move(top_pipes[i], pipeSpeed, 0)
        else:
            # otherwise move the pipe to the right side of the screen updating it with random y positions again
            if gap == 250:
                y = rand(10, 450)
            else:
                y = rand(10, 210)
            canvas.coords(top_pipes[i], 1280, -100, 1430, y)
            canvas.coords(bottom_pipes[i], 1280, y + gap, 1430, 730)

def count_score():
    global score
    for i in range(3):
        pos_top_pipe = canvas.coords(top_pipes[i])
        # if right part (x2) of pipe moves past bird then score increments
        if (pos_top_pipe[2] < 198) and (pos_top_pipe[2] > 192):
            score = score + 1
            # Update score text, ensuring it fits inside orange background
            canvas.itemconfig(score_text, text = " Score: " + str(score) + " ")
            canvas.coords(score_text_background, canvas.bbox(score_text))

def jump(event):
    global speed, slowedPipes
    if slowedPipes:
        jump_speed = -5
    else:
        jump_speed = -6
    pos_flappy_bird = canvas.coords(flappy_bird)
    # jump lasts for for 0.5 seconds
    t_end = time.time() + 0.5
    while time.time() < t_end and not isPaused:
        canvas.move(flappy_bird,0,jump_speed)
        sleep(0.00000000000001)
        jump_speed = jump_speed + 0.1 # jump speed decreases in order to simulate gravity
        move_pipes() # make sure pipes are still moving even during bird jump event
        count_score() # count score even during the bird jump event
        check_collision()
        window.update()
        if (pos_flappy_bird[1] - 50) < 0:
            break
    # reset speed so that fall restarts from 0m/s
    speed = 0

def main_game():
    global speed, gameOver, playerName, score, slowedPipes
    # if not loaded file, get entered player name otherwise keep saved player name
    if not isLoaded:
        playerName = entry.get()
    if playerName == "" or playerName[0] == " " or ":" in playerName:
        canvas.itemconfig(invalidNameText, state="normal")
    else:
        # configuring canvas items state (hidden or shown) in main game
        canvas.itemconfig(invalidNameText, state="hidden")
        canvas.itemconfig(noSavedFileText, state="hidden")
        canvas.itemconfig(easyOptionCanvas, state="hidden")
        canvas.itemconfig(normalOptionCanvas, state="hidden")
        canvas.itemconfig(playerNameText, state="hidden")
        canvas.itemconfig(entryCanvas, state="hidden")
        canvas.itemconfig(menu_screen_background, state="hidden")
        canvas.itemconfig(start_button_canvas, state="hidden")
        canvas.itemconfig(logo, state="hidden")
        canvas.itemconfig(leaderboard_button_canvas, state="hidden")
        canvas.itemconfig(home_button_canvas, state="hidden")
        canvas.itemconfig(load_button_canvas, state="hidden")
        canvas.focus_set()
        canvas.coords(score_text, 0, 0)
        canvas.coords(score_text_background, canvas.bbox(score_text))
        if not isLoaded:
            # if not loaded file then create new pipes and reset score
            create_pipes()
            score = 0
            canvas.itemconfig(score_text, text = " Score: " + str(score) + " ", state="hidden")
        countdown()
        canvas.itemconfig(score_text, state="normal")
        canvas.itemconfig(score_text_background, state="normal")
        canvas.bind('<space>', jump)
        canvas.bind('p', check_paused)
        canvas.bind('i', invincible)
        canvas.bind('s', slowPipes)
        # show if invincibility is enabled
        if cheatEnabled:
            canvas.itemconfig(cheatEnabled_text, state="normal")
            canvas.itemconfig(cheatEnabled_text_background, state="normal")
        # show if slowed pipes is enabled
        if slowedPipes:
            canvas.itemconfig(slowPipeEnabled_text, state="normal")
            canvas.itemconfig(slowPipeEnabled_text_background, state="normal")
        gameOver = False
        speed = 0
        while not gameOver and not isPaused:
            # fall speed increases in order to simulate gravity
            if slowedPipes:
                speed = speed + 0.1
            else:
                speed = speed + 0.3
            pos_flappy_bird = canvas.coords(flappy_bird)
            # if bird hits bottom of screen then game is over
            if (pos_flappy_bird[1] + 20) > 720:
                endGame()
                gameOver = True
            canvas.move(flappy_bird,0,speed)
            move_pipes()
            count_score()
            check_collision()
            sleep(0.01)
            window.update()

def check_collision():
    global gameOver, cheatEnabled
    # only check for collision if invincibility cheat is not enabled
    if not cheatEnabled:
        for i in range(3):
            pos_top_pipe = canvas.coords(top_pipes[i])
            pos_bottom_pipe = canvas.coords(bottom_pipes[i])
            # if bird overlaps pipe then game is over
            if (flappy_bird in canvas.find_overlapping(pos_top_pipe[0], pos_top_pipe[1], pos_top_pipe[2],     pos_top_pipe[3])) or (flappy_bird in canvas.find_overlapping(pos_bottom_pipe[0], pos_bottom_pipe[1], pos_bottom_pipe[2], pos_bottom_pipe[3])):
                endGame()
                gameOver = True

def endGame():
    global isLoaded
    canvas.itemconfig(menu_screen_background, state="normal")
    canvas.itemconfig(game_over_text, state="normal")
    if not isLoaded:
        canvas.itemconfig(restart_button_canvas, state="normal")
    canvas.itemconfig(home_button_canvas, state="normal")
    canvas.itemconfig(score_text_background, state="hidden")
    canvas.itemconfig(flappy_bird, state="hidden")
    canvas.itemconfig(cheatEnabled_text, state="hidden")
    canvas.itemconfig(cheatEnabled_text_background, state="hidden")
    canvas.itemconfig(slowPipeEnabled_text, state="hidden")
    canvas.itemconfig(slowPipeEnabled_text_background, state="hidden")
    canvas.tag_raise(score_text)
    canvas.coords(score_text, 490, 225)
    canvas.unbind('<space>')
    canvas.unbind('p')
    canvas.unbind('i')
    canvas.unbind('s')
    # saving data to leaderboard text file
    leaderboard_file = open("leaderboard.txt", "a")
    leaderboard_file.write(playerName + ":" + str(score) + "\n")
    leaderboard_file.close()
    isLoaded = False

def restart_game():
    global score
    # reset score
    score = 0
    canvas.itemconfig(score_text, text = " Score: " + str(score) + " ", state="hidden")
    canvas.coords(score_text, 0, 0)
    canvas.itemconfig(menu_screen_background, state="hidden")
    canvas.itemconfig(game_over_text, state="hidden")
    canvas.itemconfig(restart_button_canvas, state="hidden")
    main_game()

def check_paused(event):
    global speed, gameOver, isPaused
    # if game is paused then unpause it
    if isPaused:
        canvas.itemconfig(paused_text, state="hidden")
        canvas.itemconfig(paused_text_background, state="hidden")
        canvas.itemconfig(save_button_canvas, state="hidden")
        canvas.itemconfig(successfulSave, state="hidden")
        isPaused = False
        # continue game movements and animations
        while not gameOver and not isPaused:
            speed = speed + 0.3
            pos_flappy_bird = canvas.coords(flappy_bird)
            if (pos_flappy_bird[1] + 20) > 720:
                endGame()
                gameOver = True
            canvas.move(flappy_bird,0,speed)
            move_pipes()
            count_score()
            check_collision()
            sleep(0.01)
            window.update()
    # if game is not paused then pause it
    else:
        canvas.itemconfig(paused_text, state="normal")
        canvas.itemconfig(paused_text_background, state="normal")
        canvas.itemconfig(save_button_canvas, state="normal")
        isPaused = True

def invincible(event):
    global cheatEnabled
    # if invincibility is on, turn it off
    if cheatEnabled:
        canvas.itemconfig(cheatEnabled_text, state="hidden")
        canvas.itemconfig(cheatEnabled_text_background, state="hidden")
        cheatEnabled = False
    # if invincibility is off, turn it on
    else:
        canvas.itemconfig(cheatEnabled_text, state="normal")
        canvas.itemconfig(cheatEnabled_text_background, state="normal")
        cheatEnabled = True

def slowPipes(event):
    global slowedPipes
    # if slowed pipes is on, turn it off
    if slowedPipes:
        canvas.itemconfig(slowPipeEnabled_text, state="hidden")
        canvas.itemconfig(slowPipeEnabled_text_background, state="hidden")
        slowedPipes = False
    # if slowed pipes is off, turn it on
    else:
        canvas.itemconfig(slowPipeEnabled_text, state="normal")
        canvas.itemconfig(slowPipeEnabled_text_background, state="normal")
        slowedPipes = True

def goHome():
    delete_pipes()
    # configuring canvas items state to go back to home menu
    canvas.itemconfig(start_button_canvas, state="normal")
    canvas.itemconfig(leaderboard_button_canvas, state="normal")
    canvas.itemconfig(logo, state="normal")
    canvas.itemconfig(playerNameText, state="normal")
    canvas.itemconfig(entryCanvas, state="normal")
    canvas.itemconfig(easyOptionCanvas, state="normal")
    canvas.itemconfig(normalOptionCanvas, state="normal")
    canvas.itemconfig(load_button_canvas, state="normal")
    canvas.itemconfig(leaderboard_title, state="hidden")
    canvas.itemconfig(Leaderboard_text, state="hidden")
    canvas.itemconfig(game_over_text, state="hidden")
    canvas.itemconfig(score_text, state="hidden")
    canvas.itemconfig(restart_button_canvas, state="hidden")
    canvas.itemconfig(home_button_canvas, state="hidden")
    canvas.focus_set()
    canvas.tag_raise(entryCanvas)
    canvas.tag_raise(start_button_canvas)
    canvas.tag_raise(leaderboard_button_canvas)

def updateLeaderboard():
    # configuring canvas items state to show leaderboard
    canvas.itemconfig(leaderboard_title, state="normal")
    canvas.itemconfig(Leaderboard_text, state="normal")
    canvas.itemconfig(home_button_canvas, state="normal")
    canvas.itemconfig(playerNameText, state="hidden")
    canvas.itemconfig(entryCanvas, state="hidden")
    canvas.itemconfig(start_button_canvas, state="hidden")
    canvas.itemconfig(logo, state="hidden")
    canvas.itemconfig(leaderboard_button_canvas, state="hidden")
    canvas.itemconfig(invalidNameText, state="hidden")
    canvas.itemconfig(noSavedFileText, state="hidden")
    canvas.itemconfig(easyOptionCanvas, state="hidden")
    canvas.itemconfig(normalOptionCanvas, state="hidden")
    canvas.itemconfig(load_button_canvas, state="hidden")
    leaderboard_file = open("leaderboard.txt", "r")
    leaderboard_names = []
    leaderboard_scores = []
    # adding each leaderboard name and score to lists
    for line in leaderboard_file:
        line = line.rstrip()
        leaderboard_names.append(line.split(':')[0])
        leaderboard_scores.append(line.split(':')[1])
    # if there is at least one player in leaderboard then update it
    if len(leaderboard_names) > 0:
        # zipping leaderboard names and scores so that sorting scores will sort names too
        leaderboard_scores = list(map(int, leaderboard_scores))
        zipped_lists = zip(leaderboard_scores, leaderboard_names)
        leaderboard_scores, leaderboard_names = zip(*sorted(zipped_lists, reverse=True))
        updated_leaderboard = ""
        position = 1
        # only show top 5 players in leaderboard screen
        if len(leaderboard_names) >= 5:
            numpositions = 5
        else:
            numpositions = len(leaderboard_names)
        for i in range(numpositions):
            updated_leaderboard = updated_leaderboard + str(position) + ". " + leaderboard_names[i] + " - " + str(leaderboard_scores[i]) + "\n"
            position += 1
        canvas.itemconfig(Leaderboard_text, text = updated_leaderboard)
    leaderboard_file.close()

def showBossKey(event):
    global isBossKey
    # if boss key is shown, hide it
    if isBossKey:
        isBossKey = False
        canvas.itemconfig(bossKeyCanvas, state="hidden")
    # if boss key is hidden, show it
    else:
        isBossKey = True
        canvas.itemconfig(bossKeyCanvas, state="normal")

def saveFile():
    # saving data to text file
    canvas.itemconfig(successfulSave, state="normal")
    canvas.tag_raise(successfulSave, 'all')
    saveFileText = open("saveFile.txt", "w")
    saveFileText.write(str(canvas.coords(flappy_bird)) + "\n")
    saveFileText.write(str(score) + "\n")
    for i in range(3):
        saveFileText.write(str(canvas.coords(top_pipes[i])) + "\n")
        saveFileText.write(str(canvas.coords(bottom_pipes[i])) + "\n")
    saveFileText.write(str(playerName) + "\n")
    saveFileText.write(str(difficulty.get()) + "\n")
    saveFileText.close()

def loadFile():
    global playerName, isLoaded, score, chosenDifficulty
    # loading data from saved file
    saveFileText = open("saveFile.txt", "r")
    first_char = saveFileText.read(1)
    # only load file if there is a saved file (if text file not empty)
    if first_char != "":
        isLoaded = True
        # configuring canvas items state to load file and start game
        canvas.itemconfig(invalidNameText, state="hidden")
        canvas.itemconfig(easyOptionCanvas, state="hidden")
        canvas.itemconfig(normalOptionCanvas, state="hidden")
        canvas.itemconfig(playerNameText, state="hidden")
        canvas.itemconfig(entryCanvas, state="hidden")
        canvas.itemconfig(menu_screen_background, state="hidden")
        canvas.itemconfig(start_button_canvas, state="hidden")
        canvas.itemconfig(logo, state="hidden")
        canvas.itemconfig(leaderboard_button_canvas, state="hidden")
        canvas.itemconfig(home_button_canvas, state="hidden")
        canvas.itemconfig(load_button_canvas, state="hidden")
        canvas.itemconfig(score_text, state="normal")
        canvas.itemconfig(score_text_background, state="normal")
        canvas.focus_set()
        # Loading scores, chosen difficulty, player name, and position of the bird
        all_lines = saveFileText.readlines()
        score = int(all_lines[1].rstrip())
        canvas.itemconfig(score_text, text = " Score: " + str(score) + " ")
        canvas.coords(score_text_background, canvas.bbox(score_text))
        pos_flappy_bird = all_lines[0].rstrip()[1:len(all_lines[0].rstrip()) - 1]
        y1 = float(pos_flappy_bird.split(', ')[1])
        canvas.coords(flappy_bird, 200, y1)
        playerName = all_lines[8].rstrip()
        chosenDifficulty = int(all_lines[9].rstrip())
        # Creating new pipes and moving them to the saved locations
        create_pipes()
        for i in range(3):
            if i == 0:
                pos_top_pipe = all_lines[2].rstrip()[1:len(all_lines[2].rstrip()) - 1]
                x1 = float(pos_top_pipe.split(', ')[0])
                y1 = float(pos_top_pipe.split(', ')[1])
                x2 = float(pos_top_pipe.split(', ')[2])
                y2 = float(pos_top_pipe.split(', ')[3])
                canvas.coords(top_pipes[i], x1, y1, x2, y2)
                pos_bottom_pipe = all_lines[3].rstrip()[1:len(all_lines[3].rstrip()) - 1]
                x1 = float(pos_bottom_pipe.split(', ')[0])
                y1 = float(pos_bottom_pipe.split(', ')[1])
                x2 = float(pos_bottom_pipe.split(', ')[2])
                y2 = float(pos_bottom_pipe.split(', ')[3])
                canvas.coords(bottom_pipes[i], x1, y1, x2, y2)
            elif i == 1:
                pos_top_pipe = all_lines[4].rstrip()[1:len(all_lines[4].rstrip()) - 1]
                x1 = float(pos_top_pipe.split(', ')[0])
                y1 = float(pos_top_pipe.split(', ')[1])
                x2 = float(pos_top_pipe.split(', ')[2])
                y2 = float(pos_top_pipe.split(', ')[3])
                canvas.coords(top_pipes[i], x1, y1, x2, y2)
                pos_bottom_pipe = all_lines[5].rstrip()[1:len(all_lines[5].rstrip()) - 1]
                x1 = float(pos_bottom_pipe.split(', ')[0])
                y1 = float(pos_bottom_pipe.split(', ')[1])
                x2 = float(pos_bottom_pipe.split(', ')[2])
                y2 = float(pos_bottom_pipe.split(', ')[3])
                canvas.coords(bottom_pipes[i], x1, y1, x2, y2)
            else:
                pos_top_pipe = all_lines[6].rstrip()[1:len(all_lines[6].rstrip()) - 1]
                x1 = float(pos_top_pipe.split(', ')[0])
                y1 = float(pos_top_pipe.split(', ')[1])
                x2 = float(pos_top_pipe.split(', ')[2])
                y2 = float(pos_top_pipe.split(', ')[3])
                canvas.coords(top_pipes[i], x1, y1, x2, y2)
                pos_bottom_pipe = all_lines[7].rstrip()[1:len(all_lines[7].rstrip()) - 1]
                x1 = float(pos_bottom_pipe.split(', ')[0])
                y1 = float(pos_bottom_pipe.split(', ')[1])
                x2 = float(pos_bottom_pipe.split(', ')[2])
                y2 = float(pos_bottom_pipe.split(', ')[3])
                canvas.coords(bottom_pipes[i], x1, y1, x2, y2)
        # running the game
        main_game()
    else:
        canvas.itemconfig(noSavedFileText, state="normal")
    saveFileText.close()

################################## Initializing canvas items and variables ##################################

##### Initializing window and canvas #####
window = Tk()
window.title("Flappy Bird")
canvas = Canvas(window, width=1280, height=720, bg="#54C3FF")
gameOver = False
isPaused = False
cheatEnabled = False
slowedPipes = False
isBossKey = False
isLoaded = False
chosenDifficulty = 2
playerName = ""

##### Creating the flappy bird #####
bird_img = PhotoImage(file = "flappy_bird.png") # image source: https://www.hiclipart.com/free-transparent-background-png-clipart-slgkr
flappy_bird = canvas.create_image(200, 320, image = bird_img)
speed = 0

##### Initializing pipe lists #####
bottom_pipes = []
top_pipes = []

##### Countdown #####
countdown_text = canvas.create_text(600, 300, text = "", fill="black", font=("Comic Sans MS Bold", 200))
canvas.itemconfig(countdown_text, state="hidden")

##### Creating score canvas items #####
score = 0
score_text = canvas.create_text(0, 0, text = " Score: 0 ", fill="white", font=("Comic Sans MS Bold", 50), anchor="nw")
score_text_background = canvas.create_rectangle(canvas.bbox(score_text), fill="orange")
canvas.itemconfig(score_text, state="hidden")
canvas.itemconfig(score_text_background, state="hidden")
canvas.tag_lower(score_text_background, score_text)

##### Start screen canvas items #####
logo_img = PhotoImage(file = "logo.png") # image source: https://www.pngegg.com/en/png-twbto
menu_screen_background = canvas.create_rectangle(40, 40, 1240, 680, fill="orange")
logo = canvas.create_image(630, 150, image = logo_img)
start_button = Button(window, text = "Start", font=("Comic Sans MS Bold", 40), command = main_game)
start_button_canvas = canvas.create_window(620, 420, window = start_button)
leaderboard_button = Button(window, text = "Leaderboard", font=("Comic Sans MS Bold", 30), command = updateLeaderboard)
leaderboard_button_canvas = canvas.create_window(620, 635, window = leaderboard_button)
playerNameText = canvas.create_text(450, 250, text="Player name:", font=("Comic Sans MS Bold", 40))
entry = Entry(window, font=("Comic Sans MS Bold", 30))
entryCanvas = canvas.create_window(800, 250, window=entry)
invalidNameText = canvas.create_text(650, 300, text="Invalid player name (should not be empty and have no ':')", font=("Comic Sans MS Bold", 20), fill = "red")
canvas.itemconfig(invalidNameText, state="hidden")
difficulty = IntVar()
easyOption = Radiobutton(window, text="Beginner", bg = "orange", font=("Comic Sans MS Bold", 30), variable=difficulty, value=1)
normalOption = Radiobutton(window, text="Expert", bg = "orange", font=("Comic Sans MS Bold", 30), variable=difficulty, value=2)
normalOption.select()
easyOptionCanvas = canvas.create_window(490, 350, window=easyOption)
normalOptionCanvas = canvas.create_window(740, 350, window=normalOption)
load_button = Button(window, text = "Load file", font=("Comic Sans MS Bold", 30), command = loadFile)
load_button_canvas = canvas.create_window(620, 560, window = load_button)
noSavedFileText = canvas.create_text(620, 500, text="No save file to load", font=("Comic Sans MS Bold", 20), fill = "red")
canvas.itemconfig(noSavedFileText, state="hidden")

##### Game Over screen canvas items #####
game_over_text = canvas.create_text(625, 150, text = " Game Over! ", fill="white", font=("Comic Sans MS Bold", 100))
restart_button = Button(window, text = "Restart", font=("Comic Sans MS Bold", 40), command = restart_game)
restart_button_canvas = canvas.create_window(620, 420, window = restart_button)
canvas.itemconfig(game_over_text, state="hidden")
canvas.itemconfig(restart_button_canvas, state="hidden")

##### Pause canvas items #####
paused_text = canvas.create_text(1100, 200, text = " Paused ", fill="white", font=("Comic Sans MS Bold", 40))
paused_text_background = canvas.create_rectangle(canvas.bbox(paused_text), fill="orange")
canvas.tag_lower(paused_text_background, paused_text)
save_button = Button(window, text = "Save", font=("Comic Sans MS Bold", 40), command = saveFile)
save_button_canvas = canvas.create_window(1100, 275, window = save_button)
successfulSave = canvas.create_text(1100, 325, text="Game saved!", font=("Comic Sans MS Bold", 20), fill = "red")
canvas.itemconfig(paused_text, state="hidden")
canvas.itemconfig(paused_text_background, state="hidden")
canvas.itemconfig(save_button_canvas, state="hidden")
canvas.itemconfig(successfulSave, state="hidden")

##### Invincibility canvas items #####
cheatEnabled_text = canvas.create_text(1100, 50, text = " Invincible ", fill="white", font=("Comic Sans MS Bold", 40))
cheatEnabled_text_background = canvas.create_rectangle(canvas.bbox(cheatEnabled_text), fill="orange")
canvas.tag_lower(cheatEnabled_text_background, cheatEnabled_text)
canvas.itemconfig(cheatEnabled_text, state="hidden")
canvas.itemconfig(cheatEnabled_text_background, state="hidden")

##### Slowed pipes canvas items #####
slowPipeEnabled_text = canvas.create_text(1100, 125, text = " Slow ", fill="white", font=("Comic Sans MS Bold", 40))
slowPipeEnabled_text_background = canvas.create_rectangle(canvas.bbox(slowPipeEnabled_text), fill="orange")
canvas.tag_lower(slowPipeEnabled_text_background, slowPipeEnabled_text)
canvas.itemconfig(slowPipeEnabled_text, state="hidden")
canvas.itemconfig(slowPipeEnabled_text_background, state="hidden")

##### Leaderboard canvas items #####
leaderboard_title = canvas.create_text(625, 150, text = " Leaderboard ", fill="white", font=("Comic Sans MS Bold", 100))
Leaderboard_text = canvas.create_text(125, 220, text = "No scores yet", fill="white", font=("Comic Sans MS Bold", 50), anchor="nw")
canvas.itemconfig(leaderboard_title, state="hidden")
canvas.itemconfig(Leaderboard_text, state="hidden")

##### Home button canvas items #####
home_button = Button(window, text = "Home", font=("Comic Sans MS Bold", 30), command = goHome)
home_button_canvas = canvas.create_window(620, 635, window = home_button)
canvas.itemconfig(home_button_canvas, state="hidden")

##### Leaderboard canvas items #####
bossKeyImage = PhotoImage(file = "bosskey.png")
bossKeyLabel = Label(image = bossKeyImage)
bossKeyCanvas = canvas.create_window(640, 360, window = bossKeyLabel)
canvas.focus_set()
canvas.bind('<b>', showBossKey)
canvas.itemconfig(bossKeyCanvas, state="hidden")

##### Running the game #####
canvas.pack()
window.mainloop()
