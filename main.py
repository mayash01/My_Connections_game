import tkinter as tk
from tkmacosx import Button
from tkinter import ttk
from tkinter import PhotoImage
import random
import pandas as pd

class Connections(tk.Tk):
    def __init__(self,connections_read) :
        super().__init__()
        self.title('game')
        self.geometry('480x400+400+200')
        self.connections_read = connections_read
        self.submitted = set()
        self.curr = []  
        self.words = []
        self.all_groups = {}
        self.groups = {}
        self.group_count = {}
        self.result_text = []

    def read_to_df(self):
        for sheet_name, dataframe in connections_read.items():
            self.all_groups[sheet_name] = dataframe.to_dict()
        
        return self.all_groups
    
    def select_words(self):
        for key in self.all_groups:
            color = key
            name = next(iter(self.all_groups[key]))
            group = []

            for val in self.all_groups[color][name].values():
                val_clean = str(val).replace(" ", "").upper()
                group.append(val_clean)
                self.groups[(name,color)] = group
                self.group_count[(name,color)] = 0

            del self.all_groups[color][name]
        
        self.words = [w for word in self.groups.values() for w in word]
        print(self.words)
        return self.words, self.group, self.group_count
    
    def start_click(self,start_button):
        self.read_to_df()
        self.select_words()
        start_button.destroy()
        self.label1.config(image="")
        self.label.destroy()
        
        self.circles = self.create_circles()
        self.buttons = self.create_buttons(self.words)

    def Start_Screen(self):
        self.image = tk.PhotoImage(file="connections.png")
        self.image = self.image.subsample(2, 2)
        self.label1 = tk.Label(self, image=self.image)
        self.label1.grid(row = 0, columnspan = 5,  sticky = 'nsew')
        self.label1.place(x=230, y=100, anchor=tk.CENTER)

        self.label = tk.Label(self, text='Connections', font=('Times New Roman', 32, "bold"),fg="black")
        self.label.grid(row = 1, columnspan = 5, sticky = 'nsew')
        self.label.place(x=230, y=180, anchor=tk.CENTER)
        
        start_btn = Button(self, text='Play', bg='black',fg = 'white', activebackground = 'white', focusthickness = 0, width=100, height=45)
        start_btn.configure(command=lambda b=start_btn: self.start_click(b))
        start_btn.grid(row = 2, column=2,  sticky = 'nsew', padx = 6, pady = 6)
        start_btn.place(x=230, y=240, anchor=tk.CENTER)

        return start_btn, self.label1, self.label
    
    def click(self, btn, word):
        if sum(self.group_count.values()) == 4: 
            if btn['bg'] == "#5a594e":
                for g in self.groups:
                    if word in self.groups[g]:
                        self.group_count[g] -= 1
                        self.curr.remove(word)
                btn.configure(bg="#efefe6")
        
        else:
            if btn['bg'] == "#efefe6":
                for g in self.groups:
                    if word in self.groups[g]:
                        self.curr.append(word)
                        self.group_count[g] += 1
                btn.configure(bg="#5a594e")

            elif btn['bg'] == "#5a594e":
                for g in self.groups:
                    if word in self.groups[g]:
                        self.curr.remove(word)
                        self.group_count[g] -= 1
                btn.configure(bg="#efefe6")

    def submission(self):
        flag = False
        name = ''
        group_lst = []
        for g in self.group_count:
            if self.group_count[g] == 4:
                if tuple(self.groups[g]) not in self.submitted:
                    name = g
                    group_lst = self.groups[g]
                    flag = True
                    for w in self.groups[g]: 
                        for b in self.Buttons:
                            if b['text'] == w:
                                b.destroy() 
                                self.Buttons.remove(b)
                    break
            
        if flag:
            col = 0
            row = 4
            for bt in self.Buttons:
                bt.configure(command=lambda word = bt['text'], b=bt: self.click(b, word))
                if col<3:       
                    bt.grid(row = row,column = col, sticky = 'nsew', padx = 10, pady = 6)
                    col += 1
                else: 
                    bt.grid(row = row,column = col, sticky = 'nsew', padx = 10 , pady = 6)
                    col = 0
                    row -= 1

            print('correct!') 
            count = 5-len(self.groups)    
            text = f"{g[0]} \n {', '.join(group_lst)}"
            result_btn = Button(self, text=text , bg=g[1] ,activebackground = '#efefe6', focusthickness = 0,height=60)
            result_btn.grid(row = count, columnspan=4, sticky = 'nsew', padx = 6, pady = 6)
            self.result_text.append(result_btn)
            
            del self.groups[name]
            del self.group_count[name]
            if not self.groups:
                self.clean_board()
                print('end')

        else: 
            if sum(self.group_count.values()) == 4:
                if tuple(self.curr) not in self.submitted: 
                    self.submitted.add(tuple(self.curr))
                    self.mistake()
                    self.curr = []

                else: 
                    guessed = tk.Label(self, text='Already guessed...',bg='white', fg="black")
                    guessed.grid(row = 0, columnspan = 5,  sticky = 'nsew')
                    window.after(1000 ,guessed.destroy)
                    self.Deselect_all()


    def Shuffle(self):
        random.shuffle(self.Buttons)
        col = 0
        row = 5
        for bt in self.Buttons:
            bt.configure(command=lambda word = bt['text'], b=bt: self.click(b, word))
            if col<3:       
                bt.grid(row = row,column = col, sticky = 'nsew', padx = 10, pady = 6)
                col += 1
            else: 
                bt.grid(row = row,column = col, sticky = 'nsew', padx = 10 , pady = 6)
                col = 0
                row -= 1

    def Deselect_all(self): 
        for b in self.Buttons: 
            if b['bg'] == "#5a594e":
                b.configure(bg="#efefe6", command=lambda word = b['text'], b=b: self.click(b, word))

            for g in self.group_count:
                self.group_count[g] = 0

    def mistake(self):
        if len(self.circles) > 1:
            self.Deselect_all()
        else:
            self.results()            
            self.clean_board()
            print('lost the game')

        self.canvas.delete(self.circles.pop())
        
    def clean_board(self):
        print('new game')
        self.mistakes.destroy()
        self.Deselect_btn.destroy()
        self.Shuffle_btn.destroy()
        self.submit_btn.destroy()
        self.tried.destroy()

        new_game_btn = Button(self, text='Start new game', bg='black',fg = 'white', activebackground = 'white', focusthickness = 0, width=100, height=45)
        new_game_btn.configure(command=lambda b=new_game_btn: self.new_game_click(b))
        new_game_btn.grid(row = 5, columnspan=2, sticky = 'nsew', padx = 6, pady = 6)

    def results(self):
        r = 1
        for n in self.groups:
            text = f"{n[0]} \n {', '.join(self.groups[n])}"
            result_btn = Button(self, text=text, bg=n[1], activebackground = '#efefe6', focusthickness = 0)
            result_btn.grid(row = r, columnspan=4, sticky = 'nsew', padx = 6, pady = 6)
            self.result_text.append(result_btn)
            r += 1 

    def new_game_click(self,new_game_btn):
        print('begin')
        new_game_btn.destroy()
        for bt in self.result_text:
            bt.destroy()
        for b in self.Buttons:
            b.destroy()

        self.submitted = set()
        self.curr = []  
        self.words = []
        self.groups = {}
        self.group_count = {}
        self.result_text = []
        
        self.select_words()
        self.circles = self.create_circles()
        self.buttons = self.create_buttons(self.words)

    def create_buttons(self, words):
        self.tried = tk.Label(self, text='Create four groups of four!',fg="white")
        self.tried.grid(row = 0, columnspan = 5,  sticky = 'nsew')
        random.shuffle(self.words)
        r,c = 1,0
        self.Buttons = []
        for w in self.words:
            btn = Button(self, text=w, bg='#efefe6',activebackground = '#efefe6', focusthickness = 0, width=100, height=60)
            btn.configure(command=lambda word = w, b=btn: self.click(b, word))
            if c<3:        
                btn.grid(row = r, column = c, sticky = 'nsew', padx = 6, pady = 6)
                c += 1
            else: 
                btn.grid(row = r, column = c, sticky = 'nsew', padx = 6, pady = 6)
                c = 0
                r += 1
            self.Buttons.append(btn)

        self.mistakes = tk.Label(self, text="Mistakes Remaining:", fg="#5a594e")
        self.mistakes.place(x=95, y=310)

        self.submit_btn = Button(self, text='Submit', bg='#ffffff',activebackground = '#ffffff',fg = 'black', focusthickness = 0, command=self.submission)
        self.submit_btn.place(x=300, y=350)

        self.Deselect_btn = Button(self, text='Deselect All', bg='#ffffff',activebackground = '#ffffff',fg = 'black', focusthickness = 0, command=self.Deselect_all)
        self.Deselect_btn.place(x=175, y=350)

        self.Shuffle_btn = Button(self, text='Shuffle', bg='#ffffff',activebackground = '#ffffff',fg = 'black', focusthickness = 0, command=self.Shuffle)
        self.Shuffle_btn.place(x=78, y=350)

        return self.Buttons

    def create_circles(self):
        self.circles = []
        self.canvas = tk.Canvas(self, width=100, height=25, highlightthickness=0)
        self.circles.append(self.canvas.create_oval(5, 5, 20, 20, outline="#5a594e", fill="#5a594e"))
        self.circles.append(self.canvas.create_oval(25, 5, 40, 20, outline="#5a594e", fill="#5a594e"))
        self.circles.append(self.canvas.create_oval(45, 5, 60, 20, outline="#5a594e", fill="#5a594e"))
        self.circles.append(self.canvas.create_oval(65, 5, 80, 20, outline="#5a594e", fill="#5a594e"))
        self.canvas.grid(row=6, column=2, sticky="w")
        return self.circles

if __name__ == "__main__":
    connections_read = pd.read_excel('connections_groups.xlsx', sheet_name=None)
    window = Connections(connections_read)
    start_button = window.Start_Screen()
    window.mainloop()
