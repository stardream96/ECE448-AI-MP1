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
from pygame.locals import *
from agent import Agent
from maze import Maze
import time

def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)


def bfs(maze):
	startPoint = maze.getStart()
	currentLevel=[startPoint]
	goals=maze.getObjectives()
	path=[startPoint]
	steps=0
	while len(goals)!=0:
		pathtemp=[]
		finalPosition = goals.pop(0)
		print(finalPosition)
		dict_parent={} #store the positions that is not chosed
		explored=[] #record the positions explored
		for position in currentLevel:
			explored.append(position)
		#time.sleep(0.5)
		while (finalPosition not in currentLevel):#loop until the goal is in currentlevel of seach
			steps=steps+len(currentLevel)
			#time.sleep(1)
			nextLevel=[] #clear nextlevel data
			for currentLevelposition in currentLevel: #iterate the positions in current level, and explore the next level
				currentNeighbors=maze.getNeighbors(currentLevelposition[0], currentLevelposition[1])
				for nextLevelPosition in currentNeighbors:
					if nextLevelPosition not in explored: #not not the way that have been explored
						nextLevel.append(nextLevelPosition)
						dict_parent[nextLevelPosition]=currentLevelposition
						explored.append(nextLevelPosition) #def the position as explored
			currentLevel=nextLevel #update currentlevel
			#print(currentLevel)
		currentPosition=finalPosition
		#print(dict_parent,finalPosition,startPoint)
		while currentPosition != startPoint:
			pathtemp.insert(0,currentPosition)
			currentPosition=dict_parent[currentPosition]
		path.extend(pathtemp)
		currentLevel=[finalPosition]
		startPoint=finalPosition
	return path, steps

		
def dfs(maze):
	currentPosition = maze.getStart()
	goals=maze.getObjectives()
	path=[currentPosition]
	steps=0
	finalpath=[]
	while len(goals)!=0:
		finalPosition = goals.pop(0)
		dict_frontier={} #store the positions that is not chosed
		while (currentPosition != finalPosition): #loop until reach the goal
			steps=steps+1
			currentNeighbors = maze.getNeighbors(currentPosition[0], currentPosition[1])
			if currentPosition not in dict_frontier: #if not recorded in dict., record it
				neighbors=[]
				for neighbor in currentNeighbors:
					if neighbor != currentPosition and neighbor not in dict_frontier: #not the way it comes from and not the way that have been explored
						neighbors.append(neighbor)
				dict_frontier[currentPosition]=neighbors
			currentNeighbors = dict_frontier[currentPosition]
			if len(currentNeighbors) ==0: #if no more direction available, then wrong path, pop path items to retrieve, and update currentPosition
				currentPosition=path.pop(-1)
				if len(dict_frontier[currentPosition]) !=0:
					path.append(currentPosition)
			else: #if have direction available, go to the direction and pop it from the frontier dict.
				lastPosition=currentPosition
				currentPosition=currentNeighbors.pop(-1)
				dict_frontier[lastPosition]=currentNeighbors
				path.append(currentPosition) #add position to the path
			if steps>10000:
				return path, steps
		finalpath.extend(path)
	#print(finalpath)
	return finalpath, steps

def dfsa(maze): #advanced with better performance in open space with a little bit higher cost. Could able to make the cost similar to normal dfs
	currentPosition = maze.getStart()
	goals=maze.getObjectives()
	path=[currentPosition]
	steps=0
	finalpath=[]
	while len(goals) !=0:
		finalPosition = goals.pop()
		dict_frontier={} #store the positions that is not chosed
		deletedpath=[]
		path=[currentPosition]
		while (currentPosition != finalPosition):
			steps=steps+1
			currentNeighbors = maze.getNeighbors(currentPosition[0], currentPosition[1])
			#print('neighbors',currentNeighbors)
			if currentPosition not in dict_frontier: #if not recorded in dict., record it
				neighbors=[]
				for neighbor in currentNeighbors:
					if len(path)>=4:
						if neighbor == path[-4]:
							deletedpath.append(path.pop(-2))
							path.pop(-2)
					if neighbor != currentPosition and neighbor not in dict_frontier: #not the way it comes from and not the way that have been explored
						neighbors.append(neighbor)

				dict_frontier[currentPosition]=neighbors

			currentNeighbors = dict_frontier[currentPosition]
			#print('poped',currentNeighbors)
			if len(currentNeighbors) ==0: #if no more direction available, then wrong path, pop path items to retrieve, and update currentPosition
				if len(path)>=1:
					currentPosition=path.pop(-1)
					deletedpath.append(currentPosition)
				else:#retrive through deleted path until new direction available
					while len(dict_frontier[currentPosition])==0:
						currentPosition=deletedpath.pop(-1)
						path.append(currentPosition)
						steps=steps+1
				if len(dict_frontier[currentPosition]) !=0:
					path.append(currentPosition)
			else: #if have direction available, go to the direction and pop it from the frontier dict.
				lastPosition=currentPosition
				#print(currentPosition,currentNeighbors)
				currentPosition=currentNeighbors.pop(-1)
				dict_frontier[lastPosition]=currentNeighbors
				path.append(currentPosition) #add position to the path
			#print('p',path)
			# if steps>5000:
				# #print(dict_frontier)
				# return path, steps
		if steps>10000:
			#print(dict_frontier)
			return finalpath, steps
		finalpath.extend(path)
	return finalpath, steps


def greedy(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0


def astar(maze):
    # TODO: Write your code here
    # return path, num_states_explored
    return [], 0