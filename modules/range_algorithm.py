# A script that will take an input grid with walls, start and end, and return a
# path if a valid one exists. Otherwise, will return None.

directions = ((0,1),(0,-1),(1,0),(-1,0))

def astar_range(arr,start,max_distance):
    array = [ [i if i >= 0 else 1 for i in row] for row in arr ]
    grid_width = len(array)
    grid_height = len(array[0])
    reachable = astar(array, start, max_distance, grid_width, grid_height)
    return reachable

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

def astar(terrain,start,max_distance,grid_width,grid_height):
    start_cell = [start,0,0]
    open_list = []
    accepted_list = []
    open_list.append(start_cell)
    while True:
        # Check to see if any cells remain to be checked
        if len(open_list) == 0:
            # No possible cells remaining, return list
            return accepted_list
        # Some cells left, take the one with the lowest current path
        current_lowest_path = open_list[0][1]
        index = 0
        for i in range(1,len(open_list)):
            if current_lowest_path > open_list[i][1]:
                current_lowest_path = open_list[i][1]
                index = i
        current_cell = open_list.pop(index)
        accepted_list.append(current_cell)
        if current_cell[1] < max_distance:
            # Get list of all cells reachable from here, add them to the open_list
            cell_list = [[current_cell[0][0]+d[0], current_cell[0][1]+d[1]] for
                d in directions]
            # Filter cells out based on criteria:
            for c in cell_list:
                # Reject cells outside the grid
                if (c[0] < 0) or (c[0] >= grid_width) or (c[1] < 0) or \
                    (c[1] >= grid_height):
                    continue
                # Reject impassable cells
                if terrain[c[0]][c[1]] == 0:
                    continue
                # Reject cells outside the movement range
                movement_cost = current_cell[1] + terrain[c[0]][c[1]]
                if movement_cost > max_distance:
                    continue
                # Reject cells already investigated (unless having a valid path)
                found = False
                for cl in accepted_list:
                    if cl[0] == c:
                        found = True
                        break
                if found:
                    continue

                for ol in open_list:
                    if ol[0] == c:
                        if ol[1] > movement_cost:
                            ol[1] = movement_cost
                            ol[2] = current_cell[0]
                        found = True
                        break
                if not found:
                    open_list.append( [c,movement_cost,current_cell[0]] )

def print_grid(terrain):
    grid_height = len(terrain)
    grid_width = len(terrain[0])
    for row in terrain:
        terrain_row = "[ "
        for i in row:
            terrain_row += str(i)+" "
        terrain_row += "]"
        print(terrain_row)

if __name__ == "__main__":
    print("Okay")
    ter = [ [1 for r in range(10)] for c in range(10) ]
    for a in ter:
        print(a)
    results = astar_range(ter,[0,0],3,10,10)
    print(results)
    print()
    display = [ [" " for r in range(10)] for c in range(10) ]
    for r in results:
        x = r[0][0]
        y = r[0][1]
        s = r[1]
        display[x][y] = s
    print_grid(display)
