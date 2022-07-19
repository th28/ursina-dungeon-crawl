
import random
import heapq
from itertools import combinations
from webbrowser import get





class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return not self.elements
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def get_neighbors(mp, node):
    x = node[0]
    y = node[1]
    all_nodes = []
    neighbors = []
    dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    
    for i in range(len(mp)):
        for j in range(len(mp[0])):
            all_nodes.append((i,j))

    for d in dirs:
        neighbor = (x + d[0], y + d[1])
        if neighbor in all_nodes:
            neighbors.append(neighbor)

    return neighbors

def get_cost(mp,node):
    x = node[0]
    y = node[1]
    costs = {'x': 10, '.': 5, 'w': 10}
    return costs[mp[y][x]]

def get_path(mp, start, goal):
    #basically ripped from the amazing https://www.redblobgames.com/pathfinding/a-star/introduction.html
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        for neighbor in get_neighbors(mp, current):
            new_cost = cost_so_far[current] + get_cost(mp, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                frontier.put(neighbor, new_cost)
                came_from[neighbor] = current

    current = goal
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse

    return path


class Room:
    def __init__(self, x, y, w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.center = (self.x + self.w//2, self.y + self.h//2)


def gen_map(map_w, map_h, room_max_w, room_max_h, room_cnt):
    room_lst = []

    #generate rooms
    for i in range(room_cnt):
        room_w = random.randint(2, room_max_w)
        room_h = random.randint(2, room_max_h)

        room_x = random.randint(0,map_w - (room_w+1))
        room_y = random.randint(0,map_h - (room_h+1))

        room = Room(room_x, room_y, room_w, room_h)
        room_lst.append(room)

    #render map
    mp = [list(range(map_w)) for i in range(map_h) ]
    for row in range(map_h):
        for col in range(map_w):
            if row == 0 or row == map_h-1:
                mp[row] = ['x']*map_w
            else:
                mp[row] = ['x']*map_w
                mp[row][0] = 'x'
                mp[row][map_w-1] = 'x'

    for cnt, room in enumerate(room_lst):
        for i in range(room.h):
            for j in range(room.w):
                if i == 0 or i == room.h - 1:
                    mp[room.y+i][room.x+j] = 'w'
                elif j == 0 or j == room.w - 1:
                    mp[room.y+i][room.x+j] = 'w'
                else:
                    mp[room.y+i][room.x+j] ='.'

    #connect rooms
    room_pairs = combinations(room_lst, 2)
    #print(list(room_pairs))
    for pair in room_pairs:
        start = pair[0].center
        end = pair[1].center
        path = get_path(mp, start, end)

        #dig some paths
        for t in path:
            mp[t[1]][t[0]] = '.'
            neighbors = get_neighbors(mp, t)
            for neighbor in neighbors:
                if mp[neighbor[1]][neighbor[0]] == 'x':
                    mp[neighbor[1]][neighbor[0]] = 'w'
        
    quit_flag = False
    for i in range(map_h):
        if quit_flag == False:
            for j in range(map_w):
                if mp[i][j] == '.':                        
                    mp[i][j] = 'p'
                    quit_flag = True
                    break
        else:
            break  
                        

    return mp
            

#z = gen_map(100,100, 10, 10, 5)
#for i in z:
#    print(i)


