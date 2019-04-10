import tkinter as tk
from tkinter import filedialog as fd
from math import floor, ceil
import os, re
from modules.pathing_algorithm import astar_path
from modules.range_algorithm import astar_range
import modules.modal as modal

class grid_canvas(tk.Canvas):
    def __init__(self,master,width,height):
        self.frame = master
        tk.Canvas.__init__(self,master,width=width,height=height)
        self.width = width
        self.height = height
        self.reset_grid(10,10)
        self.markers = []

    def reset_grid(self, xcells, ycells):
        self.cell_array = [[1 for y in range(ycells)] for x in range(xcells)]
        self.markers = []
        self.draw_grid()

    def draw_grid(self,path=[]):
        # Clear canvas
        self.delete("all")

        # Ensure there are a valid number of cells
        array = [ [i if i >= 0 else 1 for i in row] for row in self.cell_array ]
        x_cells = len(array)
        if x_cells > 0:
            y_cells = len(array[0])
        else:
            y_cells = 0

        # Resize cells if necessary
        min_buffers = 20
        cell_size = 50
        if cell_size*x_cells > (self.width-min_buffers):
            cell_size = floor((self.width-min_buffers) / x_cells)
        if cell_size*y_cells > (self.height-min_buffers):
            cell_size = floor((self.height-min_buffers) / y_cells)

        grid_width = cell_size * x_cells
        grid_height = cell_size * y_cells

        left_buffer = floor( (self.width - grid_width) / 2 )
        top_buffer = floor( (self.height - grid_height) / 2 )

        # # Add paths and markers
        # for c in path:
        #     array[c[0]][c[1]] = -2
        # for m in self.markers:
        #     array[m[0]][m[1]] = -1
        def cell_pos(x,y):
            x1 = left_buffer + x*cell_size
            x2 = left_buffer + (x+1)*cell_size
            y1 = top_buffer + y*cell_size
            y2 = top_buffer + (y+1)*cell_size
            return [x1,y1,x2,y2]

        # Fill in terrain blocks
        for x in range(len(array)):
            for y in range(len(array[0])):
                if array[x][y] == 0:
                    self.create_rectangle(*cell_pos(x,y),fill="#000000")

        # fill in path (if present)
        for cell in path:
            x = cell[0][0]
            y = cell [0][1]
            colour = cell[1]
            self.create_rectangle(cell_pos(x,y),fill=colour)

        # fill in markers (if no path)
        if len(path) == 0:
            for cell in self.markers:
                x = cell[0]
                y = cell[1]
                self.create_rectangle(cell_pos(x,y),fill="#ff0000")

        # Draw vertical lines
        for x in range(left_buffer, grid_width + left_buffer + 1, cell_size):
            x1 = x
            y1 = top_buffer
            x2 = x
            y2 = top_buffer + grid_height
            self.create_line(x1,y1,x2,y2, fill="#555555")

        # Draw horizontal lines
        for y in range(top_buffer, grid_height + top_buffer + 1, cell_size):
            x1 = left_buffer
            y1 = y
            x2 = left_buffer + grid_width
            y2 = y
            self.create_line(x1,y1,x2,y2, fill="#555555")

        # Update drawing
        self.frame.master.update_idletasks()

        # Save values
        self.left_buffer = left_buffer
        self.top_buffer = top_buffer
        self.cell_size = cell_size
        self.grid_width = grid_width
        self.grid_height = grid_height

        # Disable or Enable path/range buttons based on how many markers exist
        if len(self.markers) == 2:
            self.frame.b_path.config(state="normal")
        else:
            self.frame.b_path.config(state="disabled")

        if len(self.markers) >= 1:
            self.frame.b_range.config(state="normal")
        else:
            self.frame.b_range.config(state="disabled")

    ##### Cell modification ####################################################

    def cell_code(self,code):
        if isinstance(code,int):
            return self.set_value
        elif code == "m":
            return self.set_marker

    def find_click(self,event):
        if (self.left_buffer >= event.x) or \
            (self.left_buffer + self.grid_width <= event.x) or \
            (self.top_buffer >= event.y) or \
            (self.top_buffer + self.grid_height <= event.y):
            return
        x = floor( (event.x - self.left_buffer) / self.cell_size)
        y = floor( (event.y - self.top_buffer) / self.cell_size)
        return [x,y]

    def modify_grid(self,event,value):
        coords = self.find_click(event)
        if coords == None:
            return
        function = self.cell_code(value)
        self.remove_marker(coords)
        function(value,coords)
        self.draw_grid()

    def set_value(self,value,coords):
        self.cell_array[coords[0]][coords[1]] = value

    def set_marker(self,value,coords):
        if self.cell_array[coords[0]][coords[1]] == 0:
            return
        self.markers.append(coords)
        if len(self.markers) > 2:
            outdated = self.markers.pop(0)

    def remove_marker(self,coords):
        try:
            i = self.markers.index(coords)
            self.markers.pop(i)
        except:
            # Marker does not exist, do nothing
            pass

class getDimensions(modal.base):
    def body(self,master):
        tk.Label(master,text="Rows:").grid(row=0,sticky="W")
        tk.Label(master,text="Columns:").grid(row=1,sticky="W")

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)

        return self.e1

    def buttons(self):
        self.add_button("Accept",self.ok,"active")
        self.add_button("Cancel",self.cancel)

    def validate(self):
        try:
            numRows = int(self.e1.get())
            numCols = int(self.e2.get())
            assert numRows >= 1
            assert numCols >= 1
            self.result = (numCols,numRows)
            return 1
        except ValueError:
            d = modal.error(self,"Please input an integer greater than 0 for both rows and columns.")
            return 0
        except AssertionError:
            d = modal.error(self,"Both entries must be greater than 0.")
            return 0

def transpose(m):
    w1 = len(m)
    w2 = len(m[0])
    new_array = [[0 for i in range(w1)] for q in range(w2)]
    for i in range(w1):
        for j in range(w2):
            new_array[j][i] = m[i][j]
    return new_array

class yesno(modal.message):
    def buttons(self):
        self.add_button("No",self.cancel)
        self.add_button("Yes",self.ok,"active")
    def apply(self):
        self.result = 1

class grid_creator(tk.Frame):

    def __init__(self,master):
        tk.Frame.__init__(self, master)
        s = self
        s.master = master
        s.rows = 10
        s.columns = 10
        #s.screen_width = master.winfo_screenwidth()
        #s.screen_height = master.winfo_screenheight()
        s.screen_width = 800
        s.screen_height = 800 # Window size manually set
        s.max_width = ceil(s.screen_width * 1)
        s.max_height = ceil(s.screen_height * 1)
        s.cell_size = 50
        s.reset_cell_array(10,10)
        master.title("Map Creator")
        s.path_range = 3

        self.position()
        self.centre()
        #self.canvas.update_grid()

    def quit(self):
        self.master.destroy()

    def set_range(self,val):
        self.path_range += val
        self.path_range = max(1,self.path_range)
        self.b_range.configure(text="Range({})".format(self.path_range))

    def range_up(self):
        self.set_range(1)

    def range_down(self):
        self.set_range(-1)

    def position(self):
        self.f2 = tk.Frame(self)

        self.b_new = tk.Button(self.f2, text="New Map", command=self.new_map)
        self.b_save = tk.Button(self.f2, text="Save Map", command=self.save_map)
        self.b_load = tk.Button(self.f2, text="Load Map", command=self.load_map)
        self.b_path = tk.Button(self.f2, text="Path", command=self.find_path, state="disabled")
        self.b_range = tk.Button(self.f2, text="Range(3)", command=self.find_range, state="disabled")
        self.b_range_down = tk.Button(self.f2, text="<", command=self.range_down)
        self.b_range_up = tk.Button(self.f2, text=">", command=self.range_up)
        self.b_quit = tk.Button(self.f2, text="Quit", command=self.quit)

        self.b_new.pack(side="left", padx=10, pady=10)
        self.b_save.pack(side="left", anchor="center", padx=10, pady=10)
        self.b_load.pack(side="left", padx=10, pady=10)
        self.b_path.pack(side="left", padx=10, pady=10)
        self.b_range.pack(side="left", padx=10, pady=10)
        self.b_range_down.pack(side="left", padx=10, pady=10)
        self.b_range_up.pack(side="left", padx=10, pady=10)
        self.b_quit.pack(side="left", padx=10, pady=10)

        self.canvas = grid_canvas(self, width=self.screen_width*0.8, height=self.screen_height*0.8)
        self.canvas.grid(row=1, sticky=tk.N+tk.E+tk.S+tk.W)

        self.canvas.pack(fill="both", expand="yes")
        self.f2.pack()
        self.pack()

        self.canvas.bind("<Button-1>",lambda x: self.canvas.modify_grid(x,0))
        self.canvas.bind("<B1-Motion>",lambda x: self.canvas.modify_grid(x,0))
        self.canvas.bind("<Button-3>",lambda x: self.canvas.modify_grid(x,1))
        self.canvas.bind("<B3-Motion>",lambda x: self.canvas.modify_grid(x,1))
        self.canvas.bind("<Button-2>",lambda x: self.canvas.modify_grid(x,"m"))

    def reset_cell_array(self, xcells, ycells):
        self.cell_array = [[0 for x in range(xcells)] for y in range(ycells)]

    def centre(self):
        m = self.master
        m.update_idletasks()
        width = m.winfo_width()
        height = m.winfo_height()
        x0 = floor((self.screen_width - width) / 2)
        y0 = floor((self.screen_height - height) / 2)
        m.geometry("{}x{}+{}+{}".format(width,height,x0,y0))

    def draw_vlines(canvas,cell_size,height,width,top,left):
        for x in range(left,width + left + 1,cell_size):
            canvas.create_line(x,top,x,top + height,fill="#555555")

    def ph(self):
        pass

    def new_map(self):
        # Create a new map with given dimensions
        dimensions = getDimensions(self).result
        if dimensions == None:
            return
        xcells = dimensions[0]
        ycells = dimensions[1]
        self.canvas.reset_grid(xcells,ycells)

    def save_map(self):
        # Save a map to a file
        filename = None
        while filename == None:
            filename = fd.asksaveasfilename(initialdir="./", title="Save as...", \
                filetypes=(("map files","*.map"),("all files","*.*")), \
                confirmoverwrite=False)
            if len(filename) == 0:
                return
            # Check that a .map file was selected
            if re.search("\.map$",filename) == None:
                d = modal.message(root,"Please selecte a .map file")
                filename = None
                continue
            # Check whether the file exists
            yesno_text = "The following file already exists:\n{}\n\n".format(filename)
            yesno_text += "Do you want to overwrite it?"
            if os.path.isfile(filename):
                if not yesno(root,yesno_text).result:
                    filename = None

        # The file has been successfully selected
        output = ""
        for col in transpose(self.canvas.cell_array):
            for cell in col:
                output += "{},".format(cell)
            output = output[:-1] + "\n"
        f = open(filename,"w")
        f.write(output[:-1])
        f.close()

    def load_map(self):
        filename = fd.askopenfilename(initialdir="./",title="Open Map", \
            filetypes=(("map files","*.map"),("all files","*.*")))
        f = open(filename,"r")
        f_contents = f.read()
        f.close()

        f_contents = f_contents.split("\n")

        t_array = []

        for row in f_contents:
            t_array.append([int(i) for i in row.split(",")])

        self.canvas.cell_array = transpose(t_array)

        self.canvas.draw_grid()

    def find_path(self):
        start = self.canvas.markers[0]
        end = self.canvas.markers[1]
        a_path = astar_path(self.canvas.cell_array,start,end)
        if isinstance(a_path, str):
            modal.message(self,"No path could be found.","Failure")
            return
        # Remove the start and end cells
        if a_path[0] == start:
            a_path.pop(0)
        if a_path[-1] == end:
            a_path.pop(-1)
        # Set the colour of each tile in the path
        path_cells = [ [coords,"#00ffff"] for coords in a_path ]
        path_cells.append( [start,"#ff0000"] )
        path_cells.append( [end,"#ff0000"] )
        self.canvas.draw_grid(path_cells)

    def find_range(self):
        start = self.canvas.markers[-1]
        if len(self.canvas.markers) > 1:
            unused = self.canvas.markers[0]
        else:
            unused = None
        a_range = astar_range(self.canvas.cell_array,start,self.path_range)
        # Set the colouring of the cells
        #   This can be based on range in future
        reachable_cells = [ [c[0],"#00ffff"] for c in a_range ]
        reachable_cells.append( [start,"#ff0000"] )
        if unused != None:
            print("HERE1")
            print(len(reachable_cells))
            colour = "#ff9a9a"
            for cell in reachable_cells:
                if cell[0] == unused:
                    colour = "#ffaaff"
                    break
            reachable_cells.append( [unused,colour] )
        print("HERE2")
        self.canvas.draw_grid(reachable_cells)

root = tk.Tk()
c = grid_creator(root)
root.mainloop()
