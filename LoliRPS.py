import tkinter as tk
import random
import os
from PIL import Image, ImageTk  # You need to install Pillow library
import pygame  # Import the pygame library

# Track if intense music has started
intense_music_started = False

class Character:
    def __init__(self, name, hp, img_prefix):
        self.name = name
        self.hp = hp
        self.img_prefix = img_prefix
        self.image_label = None
        self.wins = 0
        self.last_image_path = None  # Store the last selected image path

    def get_image(self):
        try:
            folder_path = f"images/{self.img_prefix}_{self.hp}"
            images = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".png")]
            if self.last_image_path:
                images = [img for img in images if img != self.last_image_path]  # Exclude the last selected image
            if images:
                image_path = random.choice(images)
                self.last_image_path = image_path  # Store the new selected image path
                image = Image.open(image_path)
                max_size = (200, 200)  # Increase the maximum size to 200x200 pixels
                image.thumbnail(max_size, Image.LANCZOS)
                return ImageTk.PhotoImage(image)
            else:
                print(f"No images found in {folder_path}")
                return None
        except FileNotFoundError:
            print(f"Folder {folder_path} not found")
            return None

def init_characters(reset_wins=False):
    global loli1, loli2
    if reset_wins or loli1 is None or loli2 is None:
        loli1 = Character("Loli 1", 4, "loli1")
        loli2 = Character("Loli 2", 4, "loli2")
    else:
        loli1.hp = 4
        loli2.hp = 4
    update_gui(reset=True)
    play_background_music()  # Play the background music when characters are initialized

def get_random_move():
    moves = ["rock", "paper", "scissors"]
    return random.choice(moves)

def determine_winner(move1, move2):
    if move1 == move2:
        return None
    elif (move1 == "rock" and move2 == "scissors") or (move1 == "scissors" and move2 == "paper") or (move1 == "paper" and move2 == "rock"):
        return 1
    else:
        return 2

def update_gui(reset=False):
    # Get a new random image for each character
    loli1_image = loli1.get_image()
    loli2_image = loli2.get_image()

    # Update hit point labels
    loli1_hp_label.config(text=f"{loli1.name} HP: {loli1.hp}")
    loli2_hp_label.config(text=f"{loli2.name} HP: {loli2.hp}")

    # Update the image labels
    if loli1_image:
        loli1_image_label.config(image=loli1_image)
        loli1_image_label.image = loli1_image  # Keep a reference
    if loli2_image:
        loli2_image_label.config(image=loli2_image)
        loli2_image_label.image = loli2_image  # Keep a reference

    # Update win count labels
    loli1_win_label.config(text=f"Wins: {loli1.wins}")
    loli2_win_label.config(text=f"Wins: {loli2.wins}")

    # Reset the result label and canvas if reset is True
    if reset:
        result_label.config(text="Make your move!")
        canvas.delete("all")
        enable_buttons()

def animate_icons(player_move, opponent_move, callback):
    # Display the chosen icons over each character
    player_icon = move_icons[player_move]
    opponent_icon = move_icons[opponent_move]

    # Adjust the initial y-coordinate to move the icons higher up
    player_icon_item = canvas.create_image(150, 70, image=player_icon)
    opponent_icon_item = canvas.create_image(450, 70, image=opponent_icon)

    winner = determine_winner(player_move, opponent_move)

    def move_winner():
        if winner == 1:
            canvas.tag_raise(player_icon_item, opponent_icon_item)  # Bring the winner icon to the front
            for _ in range(30):
                canvas.move(player_icon_item, 10, 0)
                canvas.update()
                canvas.after(15)
            canvas.after(500, callback)
        elif winner == 2:
            canvas.tag_raise(opponent_icon_item, player_icon_item)  # Bring the winner icon to the front
            for _ in range(30):
                canvas.move(opponent_icon_item, -10, 0)
                canvas.update()
                canvas.after(15)
            canvas.after(500, callback)
        else:
            # Move closer to each other
            for _ in range(17):  # Adjust this value to get them closer without crossing
                canvas.move(player_icon_item, 7, 0)
                canvas.move(opponent_icon_item, -7, 0)
                canvas.update()
                canvas.after(15)
            # Bounce back
            for _ in range(15):
                canvas.move(player_icon_item, -5, 0)
                canvas.move(opponent_icon_item, 5, 0)
                canvas.update()
                canvas.after(15)
            canvas.after(500, callback)

    canvas.after(500, move_winner)
    canvas.after(1500, lambda: canvas.delete("all"))  # Remove icons after the animation

def disable_buttons():
    rock_button.config(state=tk.DISABLED)
    paper_button.config(state=tk.DISABLED)
    scissors_button.config(state=tk.DISABLED)
    play_again_button.pack()  # Show the "Play Again" button

def enable_buttons():
    rock_button.config(state=tk.NORMAL)
    paper_button.config(state=tk.NORMAL)
    scissors_button.config(state=tk.NORMAL)
    play_again_button.pack_forget()  # Hide the "Play Again" button initially

def play_background_music():
    pygame.mixer.music.load("music/background.mp3")  # Load the background music file
    pygame.mixer.music.play(-1)  # Play the background music in a loop

def play_intense_music():
    global intense_music_started
    if not intense_music_started:
        pygame.mixer.music.load("music/intense.mp3")  # Load the intense music file
        pygame.mixer.music.play(-1)  # Play the intense music in a loop
        intense_music_started = True

def player_move(player_choice):
    global intense_music_started
    move1 = player_choice
    move2 = get_random_move()

    round_result = f"{loli1.name} chooses {move1}, {loli2.name} chooses {move2}"

    winner = determine_winner(move1, move2)
    if winner == 1:
        loli2.hp -= 1
        round_result += f"\n{loli2.name} loses 1 HP! Remaining HP: {loli2.hp}"
    elif winner == 2:
        loli1.hp -= 1
        round_result += f"\n{loli1.name} loses 1 HP! Remaining HP: {loli1.hp}"
    else:
        round_result += "\nIt's a tie! No HP lost."

    def show_results():
        result_label.config(text=round_result)
        if (loli1.hp == 1 or loli2.hp == 1) and not intense_music_started:
            play_intense_music()  # Play intense music if either character is down to 1 hit point

        if loli1.hp == 0:
            play_background_music()  # Play background music when Loli 1's HP is 0
            loli2.wins += 1  # Increment Loli 2's win count
            update_gui()  # Update GUI to show the new win count
            result_label.config(text=round_result + f"\n{loli1.name} has been defeated! {loli2.name} wins the game!")
            disable_buttons()
        elif loli2.hp == 0:
            play_background_music()  # Play background music when Loli 2's HP is 0
            loli1.wins += 1  # Increment Loli 1's win count
            update_gui()  # Update GUI to show the new win count
            result_label.config(text=round_result + f"\n{loli2.name} has been defeated! {loli1.name} wins the game!")
            disable_buttons()
        update_gui()  # Always update the GUI at the end of a round

    animate_icons(move1, move2, show_results)

# Initialize pygame
pygame.init()

# Create the main window
root = tk.Tk()
root.title("Rock, Paper, Scissors - Battle")
root.geometry("600x600")  # Reduced the window height to 550 pixels

# Create and place widgets for the characters and their hit points
frame = tk.Frame(root)
frame.pack(pady=0)  # Remove padding

loli1_win_label = tk.Label(frame, text="Wins: 0", font=("Helvetica", 14))
loli1_win_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)  # Adjust position of Loli 1's win label

loli1_image_label = tk.Label(frame, image=None)
loli1_image_label.grid(row=0, column=1, padx=5, pady=5)  # Use grid layout and reduce padding

loli1_hp_label = tk.Label(frame, text="", font=("Helvetica", 14))
loli1_hp_label.grid(row=1, column=1, padx=5, pady=0)  # Use grid layout and reduce padding

loli2_image_label = tk.Label(frame, image=None)
loli2_image_label.grid(row=0, column=2, padx=5, pady=5)  # Use grid layout and reduce padding

loli2_hp_label = tk.Label(frame, text="", font=("Helvetica", 14))
loli2_hp_label.grid(row=1, column=2, padx=5, pady=0)  # Use grid layout and reduce padding

loli2_win_label = tk.Label(frame, text="Wins: 0", font=("Helvetica", 14))
loli2_win_label.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)  # Adjust position of Loli 2's win label

# Create a canvas for animations
canvas = tk.Canvas(root, width=600, height=150)
canvas.pack()

# Create and place widgets for the result
result_label = tk.Label(root, text="Make your move!", font=("Helvetica", 14))
result_label.pack(pady=0)  # Remove padding

# Create and place buttons for player choices using images
button_frame = tk.Frame(root)
button_frame.pack(pady=0)  # Remove padding

# Load images for rock, paper, scissors
rock_image = ImageTk.PhotoImage(Image.open("images/rock.png").resize((80, 80), Image.LANCZOS))
paper_image = ImageTk.PhotoImage(Image.open("images/paper.png").resize((80, 80), Image.LANCZOS))
scissors_image = ImageTk.PhotoImage(Image.open("images/scissors.png").resize((80, 80), Image.LANCZOS))

# Store icons in a dictionary for easy access
move_icons = {
    "rock": rock_image,
    "paper": paper_image,
    "scissors": scissors_image
}

rock_button = tk.Button(button_frame, image=rock_image, command=lambda: player_move("rock"))
rock_button.grid(row=0, column=0, padx=5)  # Use grid layout and reduce padding

paper_button = tk.Button(button_frame, image=paper_image, command=lambda: player_move("paper"))
paper_button.grid(row=0, column=1, padx=5)  # Use grid layout and reduce padding

scissors_button = tk.Button(button_frame, image=scissors_image, command=lambda: player_move("scissors"))
scissors_button.grid(row=0, column=2, padx=5)  # Use grid layout and reduce padding

# Create and place the "Play Again" button
play_again_button = tk.Button(root, text="Play Again", command=lambda: init_characters(reset_wins=False), font=("Helvetica", 14))
play_again_button.pack(pady=5)  # Remove padding
play_again_button.pack_forget()  # Hide the "Play Again" button initially

# Initialize characters and update GUI
loli1 = None
loli2 = None
init_characters()

# Start the Tkinter event loop
root.mainloop()
