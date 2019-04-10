import tkinter as tk
from tkinter import filedialog as fd
import math, os, re
from modules import *

root = tk.Tk()

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
max_width = math.ceil(screen_width * 0.7)
max_height = math.ceil(screen_height * 0.7)
default_cell_size = 50

array = []
canvas = None

def centre(window):
	global screen_height, screen_width
	window.update_idletasks()
	width = window.winfo_width()
	height = window.winfo_height()
	x0 = math.floor((screen_width - width) / 2)
	y0 = math.floor((screen_height - height) / 2)
	window.geometry("{}x{}+{}+{}".format(width,height,x0,y0))

def vlines(canvas,cell_size,height,width,top,left):
	for x in range(left,width + left + 1,cell_size):
		canvas.create_line(x,top,x,top + height,fill="#555555")

def hlines(canvas,cell_size,height,width,top,left):
	for y in range(top,top + height + 1,cell_size):
		canvas.create_line(left,y,left + width,y,fill="#555555")

def fill(canvas,array,cell_size,top,left):
	for x in range(len(array)):
		for y in range(len(array[0])):
			if int(array[x][y]) == 1:
				x1 = left + x*cell_size
				x2 = left + (x + 1) * cell_size
				y1 = top + y * cell_size
				y2 = top + (y + 1) * cell_size
				canvas.create_rectangle(x1,y1,x2,y2,fill="#000000")

def create_canvas():
	global canvas, max_width, max_height
	canvas = tk.Canvas(root,width=max_width,height=max_height)
	root.title("Map Creator")
	canvas.pack()

def update_grid(array):
	global canvas, max_height, max_width
	global cell_size, canvas_height, canvas_width, left_buffer, top_buffer
	canvas.delete("all")
	x_cells = len(array)
	if x_cells > 0:
		y_cells = len(array[0])
	else:
		y_cells = 0
	cell_size = default_cell_size

	enable_save(y_cells > 0)

	if cell_size*x_cells > max_width:
		cell_size = math.floor(max_width / x_cells)
	if cell_size*y_cells > max_height:
		cell_size = math.floor(max_height / y_cells)

	canvas_width = cell_size * x_cells
	canvas_height = cell_size * y_cells

	left_buffer = math.floor((max_width - canvas_width) / 2)
	top_buffer = math.floor((max_height - canvas_height) / 2)

	fill(canvas,array,cell_size,top_buffer,left_buffer)
	vlines(canvas,cell_size,canvas_height,canvas_width,top_buffer,left_buffer)
	hlines(canvas,cell_size,canvas_height,canvas_width,top_buffer,left_buffer)
	root.deiconify()

def home():
	# Create a blank screen
	global array, canvas
	#array=[]
	array=[[0,0],[0,0]]
	update_grid(array)

def new_map():
	# Create a new map with given dimensions
	global array, canvas
	dimensions = getDimensions(canvas).result
	if dimensions == None:
		return
	x_cells = dimensions[0]
	y_cells = dimensions[1]
	array = [[0 for row in range(y_cells)] for col in range(x_cells)]
	update_grid(array)

def load_map():
	global array
	filename = fd.askopenfilename(initialdir="./",title="Open Map", \
		filetypes=(("map files","*.map"),("all files","*.*")))
	f = open(filename,"r")
	f_contents = f.read()
	f.close()

	f_contents = f_contents.split("\n")

	t_array = []

	for i in f_contents:
		t_array.append(i.split(","))

	array = transpose(t_array)

	update_grid(array)

def save_map():
	global array
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
	for col in transpose(array):
		for cell in col:
			output += "{},".format(cell)
		output = output[:-1] + "\n"
	f = open(filename,"w")
	f.write(output[:-1])
	f.close()

def modify_grid(event,value):
	global cell_size, array, canvas_height, canvas_width
	global top_buffer, left_buffer
	if not( left_buffer < event.x < left_buffer + canvas_width and
			top_buffer < event.y < top_buffer + canvas_height):
		return

	x = math.floor((event.x - left_buffer) / cell_size)
	y = math.floor((event.y - top_buffer) / cell_size)
	canvas = event.widget

	array[x][y] = value
	update_grid(array)

def mark(event):
	# Add a block to the cell
	modify_grid(event,1)

def clear(event):
	# Remove a block from the cell
	modify_grid(event,0)

def key_pressed(event):
	if event.char=="\x1b":
		root.destroy()

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

class yesno(modal.message):
	def buttons(self):
		self.add_button("No",self.cancel)
		self.add_button("Yes",self.ok,"active")
	def apply(self):
		self.result = 1

def enable_save(pBool):
	global b3
	if pBool:
		b3.config(state="normal")
	else:
		b3.config(state="disabled")

def transpose(m):
	w1 = len(m)
	w2 = len(m[0])
	new_array = [[0 for i in range(w1)] for q in range(w2)]
	for i in range(w1):
		for j in range(w2):
			new_array[j][i] = m[i][j]
	return new_array

create_canvas()

b1 = tk.Button(root, text="New Map", command=new_map)
b2 = tk.Button(root, text="Load Map", command = load_map)
b3 = tk.Button(root, text="Save Map", command=save_map, state="disabled")
#b4 = tk.Button(root, text="Exit", command=quit())
b1.pack(side="left", padx=10, pady=10)
b2.pack(side="left", anchor="center", padx=10, pady=10)
#b4.pack(side="right", padx=10, pady=10)
b3.pack(side="right", padx=10, pady=10)

home()
centre(root)

canvas.focus_set()
canvas.bind("<Button-1>",mark)
canvas.bind("<B1-Motion>",mark)
canvas.bind("<Button-3>",clear)
canvas.bind("<B3-Motion>",clear)
canvas.bind("<Key>",key_pressed)
tk.mainloop()

## Bug-check the save/load functionality
## See if you can de-globalise the "array" variable
