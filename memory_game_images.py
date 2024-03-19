import os
import random
from tkinter import *
from tkinter import font

class MemoryGame:
    def __init__(self, root, board_size=4):
        self.root = root
        self.root.title("Memory Game")
        self.board_size = board_size
        self.half_elements = (self.board_size * self.board_size) // 2
        self.moves = 0
        self.pairs = 0
        
        # Ustalanie ścieżki do katalogu "images"
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.images_directory = os.path.join(current_directory, 'images')
        
        # Sprawdzenie czy katalog "images" istnieje
        if not os.path.exists(self.images_directory):
            raise FileNotFoundError("Katalog 'images' nie istnieje.")
        
        # Tworzenie listy plików obrazków
        self.image_files = os.listdir(self.images_directory)
        self.image_files *= 2  # Każdy obrazek powinien pojawić się dwa razy
        random.shuffle(self.image_files)
        
        # Inicjalizacja przycisków i kliknięć
        self.buttons = []
        self.clicked = []
        self.counter = 0
        
        # Tworzenie planszy
        self.board = [self.image_files[i: i + self.board_size] for i in range(0, len(self.image_files), self.board_size)]   
        
        # Tworzenie przycisków i przypisywanie im obrazków
        for i in range(self.board_size):
            for j in range(self.board_size):
                button = Button(self.root, text="✥", padx=83, pady=83, 
                                font=font.Font(family='Helvetica', size=16, weight='bold'),
                                command=lambda row=i, column=j: self.button_click(row, column))
                button.grid(row=i, column=j)
                self.buttons.append(button)
    
    def button_click(self, row, column):        
        if (row * self.board_size + column) not in self.clicked: 
            self.moves += 1
            self.clicked.append(row * self.board_size + column)
            self.counter += 1
            
            # Ustawienie obrazka na przycisku
            image_path = os.path.join(self.images_directory, self.board[row][column])
            photo = PhotoImage(file=image_path)
            self.buttons[row * self.board_size + column].config(image=photo, text="")
            self.buttons[row * self.board_size + column].image = photo
            
            
            
            if self.counter == 2 and self.board[self.clicked[0] // self.board_size][self.clicked[0] % self.board_size] == self.board[self.clicked[1] // self.board_size][self.clicked[1] % self.board_size]:
                self.pairs += 1
                for idx in self.clicked:
                    self.buttons[idx].grid_forget()
                    label = Label(self.root, padx=100, pady=91) 
                    label.grid(row=idx // self.board_size, column=idx % self.board_size)
                
                self.clicked = []  # Czyszczenie listy po znalezieniu pary
                self.counter = 0  # Resetowanie licznika
                self.check_game_over()
                
            elif self.counter == 3:
                for idx in self.clicked[:-1]:  # Ukrycie poprzednich obrazków
                    self.buttons[idx].config(image="", text="✥")
                self.clicked = [self.clicked[-1]]  # Zostawienie ostatniego kliknięcia na liście
                self.counter = 1  # Resetowanie licznika
        # self.pairs = 8
        # self.check_game_over()    
    def check_game_over(self):
        if self.pairs == self.half_elements:
            # Dodanie napisu
            label = Label(self.root, text="Gratulacje! Znalazłeś wszystkie pary.", font=("Helvetica", 16))
            # label.grid(row=self.board_size // 2, column=self.board_size // 2, columnspan=self.board_size, rowspan=self.board_size)
            label.grid(row=0, column=0, columnspan=self.board_size, rowspan=self.board_size)

    
            

root = Tk()
game = MemoryGame(root)
root.mainloop()


