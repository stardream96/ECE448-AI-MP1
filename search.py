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
	
	ex_positions=[startPoint]
	ex_positions.extend(goals)
	steps=0
	dict_cn={}
	dict_cn_len={}
	finalpath=[startPoint]
	for i in range(len(ex_positions)-1):
		for j in range(i+1,len(ex_positions)):
			#print(i,i+j+1)
			start_final=(ex_positions[i],ex_positions[j])
			currentLevel=[ex_positions[i]]
			finalPosition=ex_positions[j]
			pathtemp=[]
			dict_parent={} #store the positions that is not chosed
			explored=[] #record the positions explored
			for position in currentLevel:
				explored.append(position)
			#time.sleep(0.5)
			#print(start_final)
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
				if len(currentLevel)==0:
					time.sleep(2)
				#print(currentLevel,finalPosition not in currentLevel)
				#time.sleep(0.5)
			currentPosition=finalPosition
			#print(dict_parent,finalPosition,startPoint)
			while currentPosition != ex_positions[i]:
				pathtemp.insert(0,currentPosition)
				currentPosition=dict_parent[currentPosition]
			dict_cn[start_final]=pathtemp
			dict_cn_len[start_final]=len(pathtemp)
			#print(len(pathtemp))
	order=[startPoint]
	currentPosition=startPoint
	dict_ex_p_left={}
	left=goals
	dict_frontier={}
	dn=0
	#print(dict_cn_len)
	while len(left)!=0:
		#print(left)
		fnmin=sum(sorted(dict_cn_len.values())[-len(left):])+dn
		next=order[-1]
		for nextPosition in left:#find smallest hn+dn
			dict_cn_temp=dict_cn.copy()
			dict_cn_len_temp=dict_cn_len.copy()
			for exroute in dict_cn:
				if exroute[0] in order or exroute[1] in order or exroute[0] == currentPosition or exroute[1] == currentPosition:
					dict_cn_temp.pop(exroute)
					dict_cn_len_temp.pop(exroute)
					#print('poped')
			#print(order,currentPosition,nextPosition)
			if (currentPosition,nextPosition) in dict_cn_len:
				route=(currentPosition,nextPosition)
			else:
				route=(nextPosition,currentPosition)
			hn=sum(sorted(dict_cn_len_temp.values())[0:len(left)])
			dn_temp=dict_cn_len[route]+dn
			fn=hn+dn_temp
			#print('f:',fn,fnmin,dn,(hn,dn_temp))
			if fn<=fnmin:
				fnmin=fn
				next=nextPosition
		if (currentPosition,next) in dict_cn_len:
			dn=dict_cn_len[(currentPosition,next)]+dn
		else:
			dn=dict_cn_len[(next,currentPosition)]+dn
		order.append(next)
		currentPosition=next
		left.remove(currentPosition)
	for i in range(len(order)-1):
		if (order[i],order[i+1]) in dict_cn:
			finalpath.extend(dict_cn[order[i],order[i+1]])
		else:
			finalpath.pop(-1)
			finalpath.extend(reversed(dict_cn[order[i+1],order[i]]))
			finalpath.append(order[i+1])
	#print(finalpath)
	return finalpath, steps

		
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
			if steps>100000:
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
		if steps>100000:
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
	startPoint = maze.getStart()
	currentLevel=[startPoint]
	goals=maze.getObjectives()
	ex_positions=[startPoint]
	ex_positions.extend(goals)
	steps=0
	dict_cn={}
	dict_cn_len={}
	finalpath=[startPoint]
	removelist=[]
	x=((len(ex_positions)-1)*(len(ex_positions)))/2
	for i in range(len(ex_positions)-1):
		for j in range(i+1,len(ex_positions)):
			x=x-1
			start_final=(ex_positions[i],ex_positions[j])
			currentPosition = ex_positions[i]
			finalPosition = ex_positions[j]
			frontierSet={}
			frontierSet[currentPosition]=abs(finalPosition[0]-currentPosition[0])+abs(finalPosition[1]-currentPosition[1])
			path=[]
			dict_parent={}
			explored=[currentPosition]
			dict_pathlength={}
			dict_pathlength[currentPosition]=0
			while (currentPosition!=finalPosition):
				neighbors=[]
				neighborstemp=maze.getNeighbors(currentPosition[0], currentPosition[1])
				for neighbor in neighborstemp:
					if neighbor in frontierSet:
						pathlength=dict_pathlength[currentPosition]+1
						if frontierSet[neighbor]>abs(finalPosition[0]-neighbor[0])+abs(finalPosition[1]-neighbor[1])+pathlength:
							frontierSet[neighbor]=abs(finalPosition[0]-neighbor[0])+abs(finalPosition[1]-neighbor[1])+pathlength
							dict_parent[neighbor]=currentPosition
							dict_pathlength[neighbor]=pathlength
					if neighbor not in explored:
						neighbors.append(neighbor)
						explored.append(neighbor)
						#print('neighbor',neighbor)
						
				if len(neighbors)!=0:
					for neighbor in neighbors:
						pathlength=dict_pathlength[currentPosition]+1
						frontierSet[neighbor]=finalPosition[0]-neighbor[0]+finalPosition[1]-neighbor[1]+pathlength
						dict_parent[neighbor]=currentPosition
						dict_pathlength[neighbor]=pathlength
					frontierSet.pop(currentPosition)
					s=[(k,frontierSet[k]) for k in sorted(frontierSet,key=frontierSet.get)]
					currentPosition=s[0][0]

				else:
					frontierSet.pop(currentPosition)
					s=[(k,frontierSet[k]) for k in sorted(frontierSet,key=frontierSet.get)]
					currentPosition=s[0][0]
					#print('current',currentPosition)
				steps=steps+1
			while currentPosition != ex_positions[i]:
				path.insert(0,currentPosition)
				currentPosition=dict_parent[currentPosition]
				#print('insert', currentPosition)
			if x%1000==0:
				print('step(1/2),left:',x)
			dict_cn[start_final]=path
			dict_cn_len[start_final]=len(path)
	print('step 1 finished')
	left=goals
	order=[startPoint]
	currentPosition=startPoint
	dict_ex_p_left={}
	left=goals
	dict_frontier={}
	dn=0
	hnold=0
	#print(dict_cn_len)
	while len(left)!=0:
		#print(left)
		fnmin=sum(sorted(dict_cn_len.values())[-len(left):])+dn
		next=order[-1]
		routelist={}
		passedlist={}
		for nextPosition in left:#find smallest hn+dn
			dict_cn_temp=dict_cn.copy()
			dict_cn_len_temp=dict_cn_len.copy()
			for exroute in dict_cn:
				if (exroute[0] not in left and exroute[1] not in left) or exroute[0] == currentPosition or exroute[1] == currentPosition:
					dict_cn_temp.pop(exroute)
					dict_cn_len_temp.pop(exroute)
					#print('poped')
			#print(order,currentPosition,nextPosition)
			if (currentPosition,nextPosition) in dict_cn_len:
				route=(currentPosition,nextPosition)
			else:
				route=(nextPosition,currentPosition)
			passed=[]
			for position in left:
				if position in dict_cn[(route)]:
					passed.append(position)
			dict_cn_temp2=dict_cn_temp.copy()
			dict_cn_len_temp2=dict_cn_len_temp.copy()
			for exroute in dict_cn_temp:
				if exroute[0] in passed or exroute[1] in passed:
					dict_cn_temp2.pop(exroute)
					dict_cn_len_temp2.pop(exroute)

			steps=steps+1
			passedlist[route]=passed
			hn=sum(sorted(dict_cn_len_temp2.values())[0:len(left)-len(passed)])
			dn_temp=dict_cn_len[route]+dn
			fn=hn+dn_temp
			#print('f:',fn,fnmin,dn,(hn,dn_temp))
			routelist[route]=fn
			
		s=routelist[min(routelist,key=routelist.get)]
		sorted_routelist=[(k,routelist[k]) for k in sorted(routelist,key=routelist.get)]

		maxroute=sorted_routelist[0][0]
		#print (s,sorted_routelist,maxroute)
		for prot_route in routelist:
			if routelist[prot_route]==s:
				#print('here',routelist[prot_route])
				if dict_cn_len[prot_route]>dict_cn_len[maxroute]:
					maxroute=prot_route
		if currentPosition == maxroute[1]:
			next=maxroute[0]
		else:
			next=maxroute[1]
		#print(maxroute)
		for position in left:
			if position in dict_cn[maxroute] and position != next:
				left.remove(position)
		hnold=hn
		if (currentPosition,next) in dict_cn_len:
			dn=dict_cn_len[(currentPosition,next)]+dn
		else:
			dn=dict_cn_len[(next,currentPosition)]+dn
		order.append(next)
		print('step(2/2),left:',len(left))
		currentPosition=next
		left.remove(currentPosition)
	for i in range(len(order)-1):
		if (order[i],order[i+1]) in dict_cn:
			finalpath.extend(dict_cn[order[i],order[i+1]])
		else:
			finalpath.pop(-1)
			finalpath.extend(reversed(dict_cn[order[i+1],order[i]]))
			finalpath.append(order[i+1])
	print(order)
	return finalpath, steps