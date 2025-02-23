import tkinter as tk
import random

class Card:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Player:
    def __init__(self, name, position):
        self.name = name
        self.hand = []
        self.position = position

    def draw_card(self, deck):
        if deck:
            self.hand.append(deck.pop(0))

    def play_card(self, index):
        if index < len(self.hand):
            return self.hand.pop(index)
        return None

    def __str__(self):
        return f'{self.name}: ' + ', '.join(str(card) for card in self.hand)

class Game:
    def __init__(self, root):
        self.deck = [Card(value) for value in range(1, 6)] * 5
        random.shuffle(self.deck)
        self.player = Player("Player", 0)
        self.cpu = Player("CPU", 22)
        self.root = root
        self.board = [' ' for _ in range(23)]
        self.player_hand_frame = None  # Initialize player_hand_frame to None
        self.game_over = False  # Add a flag to check if the game is over
        self.create_widgets()

    def deal(self):
        for _ in range(5):
            self.player.draw_card(self.deck)
            self.cpu.draw_card(self.deck)

    def create_widgets(self):
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()
        self.buttons = []
        for i in range(23):
            btn = tk.Button(self.board_frame, text=' ', width=2, height=1)
            btn.grid(row=0, column=i)
            self.buttons.append(btn)
        self.update_board()

        self.player_hand_frame = tk.Frame(self.root)
        self.player_hand_frame.pack()
        self.deal()
        self.show_hand()

    def update_board(self):
        if self.board_frame and self.buttons:
            for i in range(23):
                try:
                    if i == self.player.position:
                        self.buttons[i].configure(text='P')
                    elif i == self.cpu.position:
                        self.buttons[i].configure(text='C')
                    else:
                        self.buttons[i].configure(text=' ')
                except tk.TclError:
                    pass
            
            self.show_hand()
            
            if self.is_game_over() and not self.game_over:
                winner = "Player wins!" if self.player.position < self.cpu.position else "CPU wins!"
                self.end_game(winner)

    def show_hand(self):
        if self.is_game_over():  # Check if the game is over
            return  # If the game is over, do not show the hand

        if self.player_hand_frame:
            self.player_hand_frame.destroy()  # Destroy existing frame
        self.player_hand_frame = tk.Frame(self.root)  # Re-create the frame
        self.player_hand_frame.pack()
        for index, card in enumerate(self.player.hand):
            btn = tk.Button(self.player_hand_frame, text=str(card), command=lambda i=index: self.play_round(i))
            btn.pack(side=tk.LEFT)

    def is_game_over(self):
        # Check if either player has won
        return self.player.position == self.cpu.position

    def play_round(self, player_index):
        self.player_current_card = player_index  # Store the current card index
        player_card = self.player.play_card(player_index)
        
        self.ask_player_move(player_card.value, player_card)
        
    def ask_player_move(self, value, player_card):
        move_window = tk.Toplevel(self.root)
        move_window.title("Move Player")

        label = tk.Label(move_window, text="Do you want to move left or right?")
        label.pack()

        left_btn = tk.Button(move_window, text="Left", command=lambda: self.move_and_close(move_window, self.player, -value, player_card))
        left_btn.pack(side=tk.LEFT)

        right_btn = tk.Button(move_window, text="Right", command=lambda: self.move_and_close(move_window, self.player, value, player_card))
        right_btn.pack(side=tk.RIGHT)

    def move_and_close(self, window, player, value, player_card):
        if self.is_game_over():  # Check if the game is over
            return  # If the game is over, do nothing

        if self.can_move(player, value):
            self.move_player(player, value)
            if not self.is_game_over():  # Only draw a card if the game is not over
                self.player.draw_card(self.deck)
            window.destroy()
            if not self.is_game_over():  # Only let the CPU play if the game is not over
                self.cpu_play(player_card)
        else:
            self.player.hand.insert(self.player_current_card, player_card)
            window.destroy()
            self.show_hand()

    def can_move(self, player, value):
        new_pos = player.position + value
        if player == self.player:
            return 0 <= new_pos < 23
        else:
            return 0 <= new_pos < 23

    def cpu_play(self, player_card):
        if self.is_game_over():  # Check if the game is over
            return  # If the game is over, do nothing

        for cpu_index, cpu_card in enumerate(self.cpu.hand):
            move_left = self.cpu.position - cpu_card.value
            move_right = self.cpu.position + cpu_card.value

            if move_right == self.player.position:
                self.cpu.hand.pop(cpu_index)
                self.cpu.position = move_right
                self.update_board()
                self.end_game("CPU wins!")
                return
            elif move_left == self.player.position:
                self.cpu.hand.pop(cpu_index)
                self.cpu.position = move_left
                self.update_board()
                self.end_game("CPU wins!")
                return
        else:
            cpu_index = random.randint(0, len(self.cpu.hand)-1)
            cpu_card = self.cpu.play_card(cpu_index)
            self.cpu.draw_card(self.deck)
            self.cpu_move(cpu_card.value)

        print(f'Player plays: {player_card}')
        print(f'CPU plays: {cpu_card}')

        self.show_hand()

    def cpu_move(self, value):
        move_left = self.cpu.position - value
        move_right = self.cpu.position + value

        if move_right == self.player.position:
            self.cpu.position = move_right
            self.update_board()
            self.end_game("CPU wins!")
        elif move_left == self.player.position:
            self.cpu.position = move_left
            self.update_board()
            self.end_game("CPU wins!")
        elif 0 <= move_right < 23 and move_right < self.player.position:
            self.cpu.position = move_right
        else:
            self.cpu.position = move_left

        self.update_board()

    def move_player(self, player, value):
        new_pos = player.position + value
        if player == self.player:
            if 0 <= new_pos < 23:
                player.position = new_pos
                if player.position == self.cpu.position:
                    self.update_board()
                    self.end_game("Player wins!")
        else:
            if 0 <= new_pos < 23:
                player.position = new_pos
                if player.position == self.player.position:
                    self.update_board()
                    self.end_game("CPU wins!")

        self.update_board()

    def end_game(self, message):
        if not self.game_over:  # Check if the game has already ended
            self.game_over = True  # Set the game over flag

            # Update the board to reflect the final positions
            if "CPU wins!" in message:
                self.board[self.player.position] = ' '  # Clear player's icon
                self.board[self.cpu.position] = 'C'  # Set CPU's icon
                self.buttons[self.player.position].configure(text='C')  # Manually set the button text to 'C'
            else:
                self.board[self.cpu.position] = ' '  # Clear CPU's icon
                self.board[self.player.position] = 'P'  # Set player's icon
            
            self.update_board()  # Refresh the board

            # Destroy the player's hand frame if it exists
            if self.player_hand_frame:
                self.player_hand_frame.destroy()
                self.player_hand_frame = None  # Set to None after destroying

            # Display the end game message
            end_label = tk.Label(self.root, text=message, font=('Helvetica', 24))
            end_label.pack()

def main():
    root = tk.Tk()
    root.title("En Garde")
    game = Game(root)
    root.mainloop()

if __name__ == "__main__":
    main()
