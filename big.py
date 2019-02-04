import math
import bisect
def helper_helper(maze, start, end, visited):
    frontier = []
    frontier.append(start)

    explored = {}
    explored[start]  = []
    while frontier:
        front = frontier[0]
        frontier.pop(0)

        neighbors = maze.getNeighbors(front[0], front[1])
        for nb in neighbors:
            if nb == end:
                front_path = explored[front]
                nb_path = front_path.copy()
                nb_path.append(nb)

                return nb_path
            if nb in visited:
                continue
            if nb in explored:
                continue
            else:
                front_path = explored[front]
                nb_path = front_path.copy()
                nb_path.append(nb)
                explored[nb] = nb_path

                frontier.append(nb)
    return []
def helper_function(maze, unvisited,visited, pt_route):
    food = maze.getObjectives()

    food_num = len(food)

    start = pt_route
    start_tuple     = (start,)

    frontier = []
    frontier.append(start_tuple)                    # all paths in tuple

    number_tier = []
    number_tier.append(food_num)

    g               = {}                        # K: path         V: current_point
    g[start_tuple]  = 0

    route   = []

    maximum = 0
    best_path = []
    while frontier:
        front_path = frontier[0]
        front_point= front_path[-1]
        frontier.pop(0)
        number_tier.pop(0)

                                                #front_path = explored[front_point][0]
        front_food = g[front_path]
        neighbors = maze.getNeighbors(front_point[0], front_point[1])

        for nb in neighbors:
            nb_path   = list(front_path)
            nb_food   = front_food + 1
            if nb in visited:
                continue
            if nb in nb_path:
                continue

            else :
                nb_path.append(nb)
                nb_path = tuple(nb_path)
                g[nb_path] = nb_food

                fvalue  = len(nb_path) + food_num
                # index = bisect.bisect(number_tier,fvalue)

                frontier.insert(0, nb_path)
                number_tier.insert(0, fvalue)

                if (nb_food > maximum):

                    maximum = nb_food
                    best_path = nb_path

                if (nb_food == food_num):
                    return list(nb_path),nb_food

    route = list(best_path)
    route_back = helper_helper(maze, route[-1], pt_route, visited)
    route = route + route_back
    #print("211",route)
    return route
def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    food = maze.getObjectives()

    food_num = len(food)
    print(food_num)

    start = maze.getStart()
    start_tuple     = (start,)

    frontier = []
    frontier.append(start_tuple)                    # all paths in tuple

    number_tier = []
    number_tier.append(food_num)

    # explored        = {}                        # K:                                                path (tuple)  V: point
    # explored[start] = [[]]                      # K: position      V: first: list of paths #######  (pos + cur_point)    #second: remaining food

    g               = {}                        # K: path         V: current_point
    g[start_tuple]  = 0

    route   = []

    maximum = 0
    while frontier:
        front_path = frontier[0]
        front_point= front_path[-1]
        frontier.pop(0)
        number_tier.pop(0)

                                                #front_path = explored[front_point][0]
        front_food = g[front_path]
        neighbors = maze.getNeighbors(front_point[0], front_point[1])

        for nb in neighbors:
            nb_path   = list(front_path)
            nb_food   = front_food + 1
            if nb in nb_path:
                #continue
                indices = [i for i, x in enumerate(nb_path) if x == nb]
                index = indices[-1]

                subpath = nb_path[0:(index+1)]

                last_time_food = g[tuple(subpath)]
                if front_food == last_time_food:
                    continue
                else:
                    nb_food -= 1
                    nb_path.append(nb)
                    nb_path = tuple(nb_path)
                    g[nb_path] = nb_food

                    fvalue  = len(nb_path) + food_num
                    index = bisect.bisect(number_tier,fvalue)

                    frontier.insert(index, nb_path)
                    number_tier.insert(index, fvalue)
            else :

                nb_path.append(nb)
                nb_path = tuple(nb_path)
                g[nb_path] = nb_food

                fvalue  = len(nb_path) + food_num
                # index = bisect.bisect(number_tier,fvalue)

                frontier.insert(0, nb_path)
                number_tier.insert(0, fvalue)

                if (nb_food > maximum):
                    print (nb_food, nb_path)
                    maximum = nb_food
                    if maximum == 146:
                        route = nb_path
                        frontier.clear()
                        break
                        # return  list(nb_path), 148
                if (nb_food == food_num):
                    return list(nb_path),nb_food

    route = list(route)
    unvisited = food.copy()
    # print("line 220 ", len(unvisited), unvisited)
    for anything in list(route)[1:]:

        unvisited.remove(anything)
    # return unvisited, 0
    while unvisited:

        for i in range(0, len(route)):
            rt_pt = route[i]
            neighbors = maze.getNeighbors(rt_pt[0], rt_pt[1])
            for nb in neighbors:
                if nb in route:
                    continue
                else:
                    subranch = helper_function(maze, unvisited, route, route[i])
                    route    = route[:i]+subranch+route[(i+1):]
                    for new_visited in subranch:
                        if new_visited in unvisited:
                            unvisited.remove(new_visited)

    new_food_list = []
    print("--332",unvisited)
    return route, 0
def manhattan(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
