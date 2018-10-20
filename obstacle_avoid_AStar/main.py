import numpy as np
import heapq
import sys

## function to check for intersection with obstacle
def checkIntersection(start,end,rects):
	if start == end:
		return True
	p1 = np.array(start)
	p2 = np.array(end)
	pathnorm = np.linalg.norm(p2-p1)
	intersects = []
	for rect in rects:
		tempsigns = []
		tempdists = []
		for p3 in rect:
			if p3 == start or p3 == end:
				continue
			# use orthogonal projection to check if all points of
			# obstacle lie on same side of the line joining current start and neighbour end point
			orthprojsign = np.sign(np.cross(p2-p1,p3-p1)/pathnorm)
			tempsigns.append(orthprojsign)
			# use projection of obstcle on the line joining current start and neighbour end point
			# to check if obstacle lies in between the points
			p3dist = np.dot(p2-p1,p3-p1)/pathnorm
			if p3dist > 0 and p3dist < pathnorm:
				tempdists.append(1)
        	else:
				tempdists.append(0)
		tempsigns = np.unique(tempsigns)
		tempsigns = tempsigns[tempsigns!=0]
		# multiple signs indicate obstacle points lie on either side of the line
		if len(tempsigns) > 1:
			# if atleast one point of obstacle in between the start and end point, we have an intersection
			if np.sum(tempdists) > 0:
				intersects.append(1)
	# return true if intersection occurs
	if np.sum(np.array(intersects)):
		return True
	else:
		return False

## class which defines the state of a point in the graph
class node(object):
	def __init__(self,coord,gScore,hScore,parent):
		self.gScore = gScore # g-value cost
		self.hScore = hScore # h-value cost
		self.parent = parent # parent node
		self.coord = coord	# coordinates of the point
		self.fScore = gScore + hScore # f-value
		self.successors = [] # valid children states

	# equals operator defination to evaluate equality of two states
	def __eq__(self, other) :
		return self.gScore == other.gScore and self.fScore == other.fScore and self.hScore == other.hScore and self.coord == other.coord and self.parent.coord == other.parent.coord

	# get valid neighbours of current point based on whether they intersect the obstacle or not
	def getvalidSuccessors(self,end,successorPoints,obstacles):
		validSuccessors = []
		for x in successorPoints:
			# if no intersection check further
			if not checkIntersection(self.coord,x,obstacles):
				parent = self
				gScore = self.gScore + dist(self.coord,x)
				hScore = dist(x,end)
				# include only those successors which move toward the solution
				# this avoids looping
				if hScore >= self.hScore:
					continue
				tmpnode = node(x,gScore,hScore,parent)
				validSuccessors.append(tmpnode)
		return validSuccessors

## calculate distance between two points
## used in calculating g-value and h-value
def dist(coord1,coord2):
	p1 = np.array(coord1)
	p2 = np.array(coord2)
	return np.linalg.norm(p2 - p1)

## aStar function
def aStarSearch(startNode, endcoord, Successorcoords, obstacles):
	openList = []
	pqueue = [] # priority queue for open list
	closedList = []
	# push start state to priority queue
	heapq.heappush(pqueue,(startNode.fScore,startNode))
	openList.append(startNode)
	# stack which stores solution states
	solutionNodes = []
	while pqueue != []:
		# pop highest priority state from heap
		(_,curNode) = heapq.heappop(pqueue)
		# remove current state from openlist
		openList.remove(curNode)
		if curNode.coord == endcoord:
			# if end state reached, add to solution stack
			solutionNodes.append(curNode)
			closedList.append(curNode)
			# extracting only top 3 solutions (because complex problem takes too long for extracting all sols.)
			if len(solutionNodes) >=3:
				break
			# use continue to avoid expanding end state
			continue
		# append curent state to closed list
		closedList.append(curNode)
		# get valid next states
		nextNodes = curNode.getvalidSuccessors(endcoord,Successorcoords,obstacles)
		children = []
		for nextNode in nextNodes:
			if nextNode in closedList:
				continue
			if nextNode not in openList:
				children.append(nextNode)
				# push all valid successor states to priority queue
				# fscore is used for determining the priority
				heapq.heappush(pqueue,(nextNode.fScore,nextNode))
				openList.append(nextNode)
		# add valid successor states to current state class dictionary	
		curNode.successors = children
	return solutionNodes

## initialize all possible successors
def initializeSuccessorList(start, end, allRects):
	successors = []
	dists = []
	p1 = np.array(start)
	# extract successors from vertices of obstacles
	for rect in allRects:
		for x in rect:
			p2 = np.array(x)
			dist = np.linalg.norm(p2-p1)
			successors.append(x)
			dists.append(dist)
	# sort successors based on how far they are from the start point
	args = np.argsort(dists)
	suc = []
	# actual sorting performed
	for x in args:
		suc.append(successors[x])
	# return sorted successor list
	return suc

## main
def main(filename):
	# open problem file
	f = open(filename) #f = open(str(sys.argv[1]))
	data = f.read().split('\n')
	print("start point - " + data[0])
	print("end point - " + data[1])
	# read start and end points, convert to float
	start = data[0].split(' ')
	start = [float(x) for x in start]
	end = data[1].split(' ')
	end = [float(x) for x in end]
	numrects = data[2]
	print("number of obstacles - "+ data[2])
	rects = []
	print("obstacle locations: ")
	# read all obstacles
	for x in data[3:-1]:
		print(x)
		temp = x.split(' ')
		temp = [float(y) for y in temp]
		temp = [temp[i:i+2] for i in xrange(0, len(temp), 2)]
		rects.append(temp)
	# initialize all possible successors
	sucs = initializeSuccessorList(start, end, rects)
	sucs.remove(start)
    # initialize start state
	parent = None
	startNode = node(start, 0, dist(start,end), parent)
	# run Astar search
	solutions = aStarSearch(startNode, end, sucs, rects)
	top3Sol = []
	# backtrack solution path from solution state
	for sol in solutions:
		tempsol = []
		while sol.parent is not None:
			tempsol.append((sol.coord,sol.gScore))
			sol = sol.parent
		tempsol.append((start,0))
		tempsol.reverse()
		top3Sol.append(tempsol)
	print("\nprinting top solution")
	print("Point           Cumulive Cost")
	for x in top3Sol[0]:
		print(str(x[0]) + "      " + "{0:.6g}".format(x[1]))
	
if __name__ == "__main__":
	fList = ['f1.txt','f2.txt','f3.txt']
	types = ['simple dataset','difficult dataset', 'customized dataset']
	for x,y in zip(fList,types):
		print("running " + y)
		main(x)
		print('\n')
