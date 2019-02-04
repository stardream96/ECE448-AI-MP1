# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Michael Abir (abir2@illinois.edu) on 08/28/2018
# Modified by Rahul Kunji (rahulsk2@illinois.edu) on 01/16/2019

"""
This is the main entry point for MP1. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (row, col) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)


from collections import deque
import heapq
def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)

#uses deque for stack & queue in dfs/bfs
def bfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    num_states_explored = 0
    queue = deque()
    visited = []
    previous_node = {}
    start = maze.getStart()     #(row, col)
    queue.append(start)
    visited.append(start)
    while len(queue) != 0:
        current = queue.popleft()
        num_states_explored += 1
        if maze.isObjective(current[0], current[1]):
            break
        neighbors = maze.getNeighbors(current[0], current[1])
        for n in neighbors:
            if n not in visited:
                queue.append(n)
                visited.append(n)
                previous_node[n] = current
    path = []
    path.append(current)
    while current != maze.getStart():
        path.append(previous_node[current])
        current = previous_node[current]

    return path, num_states_explored


def dfs(maze):
    # TODO: Write your code here
    # return path, num_states_explored

    num_states_explored = 0
    queue = deque()
    visited = []
    previous_node = {}
    start = maze.getStart()  # (row, col)
    queue.append(start)
    visited.append(start)
    while len(queue) != 0:
        current = queue.pop()   #only part different from bfs
        num_states_explored += 1
        if maze.isObjective(current[0], current[1]):
            break
        neighbors = maze.getNeighbors(current[0], current[1])
        for n in neighbors:
            if n not in visited:
                queue.append(n)
                visited.append(n)
                previous_node[n] = current
    path = []
    path.append(current)
    while current != maze.getStart():
        path.append(previous_node[current])
        current = previous_node[current]

    return path, num_states_explored

#priority queue needs "import heapq"
def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    heap = []
    visited = []
    previous_node = {}
    start = maze.getStart()  # (row, col)
    end = maze.getObjectives()
    m_distance = abs(end[0][0] - start[0]) + abs(end[0][1] - start[0])
    heapq.heappush(heap, (m_distance, start))
    visited.append(start)
    while len(heap) != 0:
        current = heapq.heappop(heap)[1]
        num_states_explored += 1
        if maze.isObjective(current[0], current[1]):
            break
        neighbors = maze.getNeighbors(current[0], current[1])
        for n in neighbors:
            if n not in visited:
                m_distance = abs(end[0][0] - n[0]) + abs(end[0][1] - n[1])
                heapq.heappush(heap, (m_distance, n))
                visited.append(n)
                previous_node[n] = current
    path = []
    path.append(current)
    while current != maze.getStart():
        path.append(previous_node[current])
        current = previous_node[current]

    return path, num_states_explored

#uses heapq
def astar(maze):       #handles both single and multi dots (suboptimal)
    # TODO: Write your code here
    # return path, num_states_explored
    num_states_explored = 0
    path = []
    round = 1       #check round number to print correct path
    start = maze.getStart()  # (row, col)
    ends = maze.getObjectives()
    while len(ends) > 0:
        objectives = {}  # dictionary of end : distance
        for e in ends:
            objectives[e] = abs(e[0] - start[0]) + abs(e[1] - start[1])
        min_end = min(objectives.keys(), key=(lambda k: objectives[k]))  # find the closest dot
        ends.remove(min_end)

        heap = []
        visited = []
        previous_node = {}

        m_distance = abs(min_end[0] - start[0]) + abs(min_end[1] - start[1])
        heapq.heappush(heap, (m_distance, start, 0))  # distance from start is 0 here
        visited.append(start)

        while len(heap) != 0:
            temp = heapq.heappop(heap)  # contains a tuple (3 elements)
            current = temp[1]
            distance_from_start = temp[2]
            num_states_explored += 1
            if current == min_end:
                break
            neighbors = maze.getNeighbors(current[0], current[1])
            for n in neighbors:
                if n not in visited:
                    m_distance = abs(min_end[0] - n[0]) + abs(min_end[1] - n[1])
                    heapq.heappush(heap, (distance_from_start + m_distance, n, distance_from_start + 1))
                    visited.append(n)
                    previous_node[n] = current
        temp_path = []
        temp_path.append(current)
        while current != start:
            temp_path.append(previous_node[current])
            current = previous_node[current]
        temp_path.reverse()
        if round > 1:
            temp_path.pop(0)    #the dots will appear twice w/o this line
        print(temp_path)
        path += temp_path
        start = min_end     #update start and search for new destination
        round += 1
    return path, num_states_explored


#below is a copy of the single destination version written before
'''
num_states_explored = 0
    heap = []
    visited = []
    previous_node = {}
    start = maze.getStart()  # (row, col)
    end = maze.getObjectives()
    m_distance = abs(end[0][0] - start[0]) + abs(end[0][1] - start[1])
    heapq.heappush(heap, (m_distance, start, 0))    #distance from start is 0 here
    visited.append(start)
    while len(heap) != 0:
        temp = heapq.heappop(heap)      #contains a tuple (3 elements)
        current = temp[1]
        distance_from_start = temp[2]
        num_states_explored += 1
        if maze.isObjective(current[0], current[1]):
            break
        neighbors = maze.getNeighbors(current[0], current[1])
        for n in neighbors:
            if n not in visited:
                m_distance = abs(end[0][0] - n[0]) + abs(end[0][1] - n[1])
                heapq.heappush(heap, (distance_from_start + m_distance, n, distance_from_start + 1))
                visited.append(n)
                previous_node[n] = current
    path = []
    path.append(current)
    while current != maze.getStart():
        path.append(previous_node[current])
        current = previous_node[current]

    return path, num_states_explored
'''
