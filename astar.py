#TODO:
#Enable manipulation of terrain
#Add travel weights based on terrain
#Enable diagonal movement and add in a corresponding travel weight
#Create a program that will allow you to create maps and export them to a document
#Import the exported maps into this program
#Swap between adding and removing walls at will?
#Create a graphical user interface that will allow map creation and target selection with the mouse
#   and will also allow visual representation of map and path

def input_int(question):
  while True:
    num = input(question)
    try:
      num = int(num)
    except ValueError:
      print("ERROR: Not an integer")
      continue
    return num

def input_coords(question,length):
  while True:
    num = input(question)
    if len(num) != length:
      print("ERROR: Not correct length")
      continue
    try:
      assert int(num) == int(num)
    except ValueError:
      print("ERROR: Not an integer")
      continue
    break
  output = [int(char) for char in num]
  return output

def set_dimensions():
  global grid_width
  global grid_height
  grid_width = input_int("Grid Width: ")
  grid_height = input_int("Grid Height: ")

def in_grid(c):
  if 0 <= c[0] < grid_width and 0 <= c[1] < grid_height:
    return True
  else:
    return False

def set_terrain(w,h):
  global terrain
  terrain = [[base_terrain]*h for i in range(w)]

def print_grid():
  for y in range(grid_height-1,-1,-1):
    print(str(y)+" [",end="")
    for x in range(grid_width):
      if terrain[x][y]==0:
        print(" X ",end="")
      elif terrain[x][y]==1:
        print("   ",end="")
      else:
        print(" "+str(terrain[x][y])+" ",end="")
    print("]")
  print("   ",end="")
  for n in range(grid_width):
    print(" "+str(n)+" ",end="")
  print("")

def add_walls():
  global terrain
  while True:
    print()
    print_grid()
    num = input("Set wall at: ")
    if num == "n":
      break
    if len(num) != 2:
      print("ERROR: Not correct length")
      continue
    try:
      assert int(num) == int(num)
    except ValueError:
      print("ERROR: Not an integer")
      continue
    coords = [int(char) for char in num]
    if not in_grid(coords):
      print("ERROR: Cell outside grid")
      continue
    terrain[coords[0]][coords[1]] = 0

def remove_walls():
  global terrain
  while True:
    print()
    print_grid()
    num = input("Remove wall at: ")
    if num == "n":
      break
    if len(num) != 2:
      print("ERROR: Not correct length")
      continue
    try:
      assert int(num) == int(num)
    except ValueError:
      print("ERROR: Not an integer")
      continue
    coords = [int(char) for char in num]
    if not in_grid(coords):
      print("ERROR: Cell outside grid")
      continue
    terrain[coords[0]][coords[1]] = 1

def set_blocks(b):
  for c in b:
    terrain[c[0]][c[1]]=0

def set_start_end():
  global start
  global end
  while True:
    start = input_coords("Start: ",2)
    if not in_grid(start):
      print("ERROR: Cell outside grid")
      continue
    if terrain[start[0]][start[1]] == 0:
      print("ERROR: Cell not available")
      continue
    break
  while True:
    end = input_coords("End: ",2)
    if not in_grid(end):
      print("ERROR: Cell outside grid")
      continue
    if terrain[end[0]][end[1]] == 0:
      print("ERROR: Cell not available")
      continue
    break
  
def find_h(current,end):
  x1 = current[0]
  y1 = current[1]
  x2 = end[0]
  y2 = end[1]
  return abs(x1-x2) + abs(y1-y2)

def final_list(start,final,closed_list):
  flist = []
  current = final
  while current[0] != start:
    flist.insert(0,current[0])
    parent = current[3]
    for cell in closed_list:
      if parent == cell[0]:
        current = closed_list.pop(closed_list.index(cell))
        break
    else:
        return "ERROR: Parent cell not found in Open List"
  flist.insert(0,start)
  return flist

def astar(start,end):
  if start == end:
    return "ERROR: Start = End"
  open_list = []
  closed_list = []
  #cell format: [[x,y],b,f,parent]
  start_cell = [start,0,find_h(start,end),0]
  open_list.append(start_cell)
  while True:
    #Check for a dead end
    if len(open_list) == 0:
      return "ERROR: No Path Found"
    #Pop cell from Open_List with the lowest F
    f = open_list[0][2]
    index = 0
    for cell in open_list:
      if f > cell[2]:
        f = cell[2]
        index = open_list.index(cell)
    current = open_list.pop(index)
    closed_list.append(current)
    #Check if chosen cell is End
    if current[0] == end:
      return final_list(start,current,closed_list)
    #Create list of examinable cells
    cell_list = [[current[0][0]+d[0],current[0][1]+d[1]] for d in directions]
    #Eliminate cells outside of grid
    cell_list[:] = [c for c in cell_list if(0 <= c[0] < grid_width and 0 <= c[1] < grid_height)]
    #Eliminate impassable cells
    cell_list[:] = [c for c in cell_list if(terrain[c[0]][c[1]] != 0)]
    #Generate information for valid cells
    for cell in cell_list:
      b = current[1] + terrain[cell[0]][cell[1]]
      f = b + find_h(cell,end)
      found = False
      #Search closed_list for cell coordinates
      for c in closed_list:
        if c[0] == cell:
          found = True
          break
      if found:
        continue
      #Search open_list for cell coordinates
      for c in open_list:
        if c[0] == cell:
          #If cell in open_list has higher F, replace with new path to cell
          if c[2] > f:
            c[1] = b
            c[2] = f
            c[3] = current[0]
          found = True
          break
      if not found:
        open_list.append([cell,b,f,current[0]])
    
def highlight_path(p):
  for c in p:
    terrain[c[0]][c[1]] = "."
  c = p[0]
  terrain[c[0]][c[1]] = "s"
  c = p[len(p)-1]
  terrain[c[0]][c[1]] = "f"

def remove_path(p):
  for c in p:
    terrain[c[0]][c[1]] = 1

directions = ((0,1),(0,-1),(1,0),(-1,0))
#Diagonal directions
#Maybe include a travel weight to diagonal movements (1.2?)
#directions = ((0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,-1),(-1,1))
base_terrain = 1
blocks = [[0,3],[1,1],[1,5],[2,0],[2,3],[2,4],[3,0],[3,3],[3,4],[4,2],[4,3],[4,5],[5,3],[6,1],[6,5],[6,6],[4,1]]

set_dimensions()
set_terrain(grid_width,grid_height)
while True:
  set_blocks(blocks)
  print_grid()
  print("\n\n\n")
  set_start_end()
  path = astar(start,end)
  print("Path: ",path)
  if not isinstance(path, str):
    highlight_path(path)
    print_grid()
  yn = input("\n\nAgain? ")
  if yn != 'y':
    break
  if not isinstance(path, str):
    remove_path(path)
  remove_walls()
