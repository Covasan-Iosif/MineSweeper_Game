from tkinter import Button, Label
import random
import settings
import ctypes # throw generic messages
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):
        self.is_mine = is_mine
        self.is_open = False
        self.is_mine_candidate = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        
        # Append the object tot the Cell.all list
        Cell.all.append(self)

    def create_btn_obj(self, location):
        btn = Button(
            location,
            width=12,
            height=4,           
        )
        #passing the referance of the method
        btn.bind('<Button-1>',  self.left_click_actions) # left click
        btn.bind('<Button-3>',  self.right_click_actions) # right click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg="black",
            fg="white",
            text=f"Cells Left:{Cell.cell_count}",
            width=12,
            height=4,
            font=("Times New Roman", 33)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
            
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            # If mines count is equal to cells left count show Winning message
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, 'Congratulations! You won the game', 'Game Over!', 0)

        
        # Cancel left and right click events if cell is already opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')
    
    def get_cell_by_axis(self, x,y):
        #return a cell object based on the values of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property #read only atribute
    def surrounded_cells(self):
            cells =  [
            self.get_cell_by_axis(self.x-1,self.y-1),
            self.get_cell_by_axis(self.x-1, self.y),
            self.get_cell_by_axis(self.x-1, self.y+1),
            self.get_cell_by_axis(self.x, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y-1),
            self.get_cell_by_axis(self.x+1, self.y),
            self.get_cell_by_axis(self.x+1, self.y+1),
            self.get_cell_by_axis(self.x, self.y+1),
        ]
            cells = [cell for cell in cells if cell is not None] # to eliminate Nones    
            return cells

    @property #read only atribute
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter+=1
        return counter

    def show_cell(self):
        if not self.is_open:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # If this was a mine candidate then configure the bg color to SystemButtonFace
            self.cell_btn_object.configure(bg="SystemButtonFace")
        # Mark the cell as opened; use it as the last line of this method
        self.is_open = True


    def show_mine(self):
        # Intrerupt the game and display a message for losing the game
        self.cell_btn_object.configure(bg="red")
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine', 'Game Over', 0)
        sys.exit(0)
        
        
        

    
    # To mark and unmark possible mines
    def right_click_actions(self, event):
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(bg ="orange")
            self.is_mine_candidate = True
        else: 
            self.cell_btn_object.configure(bg="SystemButtonFace") # The basic button color
            self.is_mine_candidate = False
    
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT, 
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True 
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

