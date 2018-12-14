import tkinter as tk
from tkinter import filedialog, messagebox

b_width = 12
b_text_size = 10

class Window(tk.Frame):
    def __init__(self,master=None,side="top"):
        super().__init__(master)
        self.pack(side=side)
        self.buttonList = []
        self.labelList = []
        #self.counter_text = tk.StringVar()
        #self.counter_text.set(self.count)

class Grid(tk.Frame):
    def __init__(self,master=None, rows=2, columns=2,side="top",padx=0,pady=0):
        super().__init__(master)
        self.pack(side=side,padx=padx,pady=pady)
        self.buttonList=[]
        self.terrain = []
        for i in range(rows):
            self.buttonList.append([])
            self.terrain.append([])
            for j in range(columns):
                newButton = tk.Button(self, image=None, width=1, height=1, bg="white", activebackground="#ddd")
                newButton.i = i
                newButton.j = j
                newButton.configure(command = lambda bi = newButton.i , bj = newButton.j: grid_click(self,bi,bj))
                #newButton.bind("<Button-3>",something)
                self.buttonList[i].append(newButton)
                self.buttonList[i][j].grid(row=i,column=j)
                self.terrain[i].append(0)

class Grid2(tk.Frame):
    def __init__(self,master=None,rows=2,columns=2,side="top"):
        super().__init__(master)
        self.pack(side=side)
        self.buttonList = []
        self.terrain = []
        for i in range(rows):
            self.buttonList.append([])
            self.terrain.append([])
            for j in range(columns):
                nB = tk.Button(self,bg="white",width=1,height=1, activebackground="#ddd")
                nB.i = i
                nB.j = j
                nB.configure(command = lambda nBi=nB.i, nBj=nB.j: grid_click(self,nBi,nBj))
                L = self.buttonList
                L[i].append(nB)
                L[i][j].place(anchor="c")
                self.terrain[i].append(0)

def grid_click(grid,i,j):
    if grid.terrain[i][j] == 0:
        grid.terrain[i][j] = 1
        grid.buttonList[i][j].configure(bg = "black", activebackground="#555")
    else:
        grid.terrain[i][j] = 0
        grid.buttonList[i][j].configure(bg = "white", activebackground="#ddd")

def add_button(p_parent, p_text, p_command, p_side="top", p_fg="black", width=b_width, font="Helvetica "+str(b_text_size)):
    rclick = lambda: print("Hi")
    newButton = tk.Button(p_parent)
    newButton["text"] = p_text
    newButton["command"] = p_command
    newButton["width"] = b_width
    newButton["font"] = "Helvetica "+str(b_text_size)
    newButton["fg"] = p_fg
    newButton.bind("<Button-3>",something)
    p_parent.buttonList.append(newButton)
    p_parent.buttonList[len(p_parent.buttonList) - 1].pack(side=p_side)

def add_label(p_parent,p_text,p_font="Helvetica 12", width=-1):
    newLabel = tk.Label(p_parent, text=p_text, font=p_font)
    if width != -1:
        newLabel["width"] = width
    L = p_parent.labelList
    L.append(newLabel)
    L[len(L) - 1].pack()

def save_map():
    savename = filedialog.asksaveasfile(mode="w", defaultextension=".fmap", initialdir="./maps")
    savename.write("Hello ")
    savename.write("There\n")
    savename.write("General Kenobi...")
    savename.close()

def something(event):
    print(event)

def new_map():
    width = messagebox.askquestion("Set Width","Set the width:")
    while width > 20 or width < 3:
        messagebox.showerror("Error","Width must be between 3 and 20.")
        width = filedialog.askquestion("Set Width","Set the width:")

def import_map():
    open_file = filedialog.askopenfilename(initialdir="./maps")
    if open_file in [(),""]:
        pass
    else:
        open_file = open_file.split('.')
        file_type = open_file.pop()
        if file_type == 'fmap':
            b_num = 0
            w_map()
        else:
            messagebox.showerror("Error", "Filename incompatible.\nPlease select a .fmap file.")

def test_openfile():
    open_file = filedialog.askdirectory()
    print(open_file)

def blank():
    pass

root = tk.Tk()
root.geometry("800x700")
title = Window(root)
add_label(title," A* Pathing Map Editor \n", "Helvetica 20 underline")
grid = Grid(root,rows=20, columns=20)
controls = Window(root,side="bottom")
add_button(controls,"New",new_map,"left")
add_button(controls,"Clear",blank,"left")
add_button(controls,"Load",blank,"left")
add_button(controls,"Save",save_map,"left","green")
add_button(controls,"Quit",root.destroy,"right","red")
root.mainloop()