# A script that will take an input grid with walls, start and end, and return a
# path if a valid one exists. Otherwise, will return None.
import random

def dirs():
    directions = [[0,1],[0,-1],[1,0],[-1,0]]
    output = random.shuffle(directions)
    return directions

def astar_path(arr,start,end):
    array = [ [i if i >= 0 else 1 for i in row] for row in arr ]
    grid_width = len(array)
    grid_height = len(array[0])
    path = astar(array, start, end, grid_width, grid_height)
    return path

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

def astar(terrain, start, end, grid_width, grid_height):
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
        cell_list = [[current[0][0]+d[0],current[0][1]+d[1]] for d in dirs()]
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
