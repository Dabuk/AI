## define state for the game
## each state has attributes : number of missionaries and cannibals on the left bank, boat position
## in other comments, subjects mean both missionaries and cannibals
class State(object):
   def __init__(self,M,C,B):
       self.M = M
       self.C = C
       self.B = B
   ## define equals operator on the class (useful for checking repeated states)
   def __eq__(self, other) : 
        return self.__dict__ == other.__dict__
   
   ## define illegal states 
   def isvalid(self):
       if self.M < 0 or self.C < 0 or self.B < 0 : # general check to limit numbers greater than minimum
          return False
       if self.M > 3 or self.C > 3 or self.B > 1 : # general check to limit numbers greater than maximum
          return False
       if self.M < self.C and self.M > 0: # trivial invalid according to definition
          return False
       if self.M > self.C and self.M < 3: # M < C on the other shore
          return False
       return True     

class Node(object):
   def __init__(self,state,parent):
       self.state = state
       self.parent = parent # parent node to keep track of states, and avoid repetition
       self.children = None # can be used to extract different paths from root
       self.actions = {(2,0),(0,2),(1,0),(0,1),(1,1)} # all possible combinations to cross the river
       self.stack = [] # stack of states leading to current node
 
   def genValidChildren(self): 
       parent = self
       validChildren = [] # vaid childern node list
       state = self.state
       ## if boat on left shore, subtract subjects on left shore else add subjects to left shore
       add = -1
       B = 1
       invalid = 0
       repeated = 0
       if state.B == 1:
          add = 1
          B = 0
       ## perform actions to generate set of possible children
       for action in self.actions:
           M = self.state.M + add*action[0]
           C = self.state.C + add*action[1]
           tempstate = State(M,C,B)
           if tempstate.isvalid(): # check if generated state satisfies validity conditions
              if tempstate in parent.stack:
                 repeated +=1 
                 continue  # continue if child same as parent
              cn = Node(tempstate,parent)
              cn.stack = [cn.state] + parent.stack
              validChildren.append(cn)
           else:
              invalid +=1 # invalid state generated
       self.children = validChildren
       return validChildren, invalid, repeated

## recursive depth first search
## takes in aruguments - current node, total nodes visited, repeated nodes tracked, invalid nodes tracked, solutions list
## returns total nodes visited, repeated nodes tracked, invalid nodes tracked, solutions list
def dfs(node, total, repeated, invalid, solutions):
   ## check if goal state reached, add stack to solutions list
   if node.state.M == 0 and node.state.C == 0 and node.state.B == 1:
      solutions.append(node.stack)
      return total, repeated, invalid, solutions
   ## generate valid children nodes
   children, invalidChildno, repeatchild = node.genValidChildren()
   invalid += invalidChildno
   repeated += repeatchild
   total +=len(children)
   ## if no valid children, return
   if len (children) == 0:
      return total, repeated, invalid, solutions
   for child in children:
       total, repeated, invalid, solutions = dfs(child, total, repeated, invalid, solutions)
   ## return number of total states, repeated states, invalid states and solutions stack
   return total, repeated, invalid, solutions
   
def main():
   ## state ordering - Missionary, Cannibal, L=0 / R=1
   ## define start state
   startState = State(3,3,0)
   ## define start node
   startNode = Node(startState, None)
   startNode.stack = [startNode.state]
   repeated = 0
   invalid = 0
   total = 0
   solutions = []
   ## call dfs recursively
   total, repeated, invalid, solutions = dfs(startNode, total, repeated, invalid, solutions)
   print "number of solutions ", len(solutions)
   for x in solutions:
       print("solution") 
       sols = []
       ## reverse stack to print as start - > end
       x = x[::-1]
       for y in x:
           if y.B == 0:
              print "(",y.M,",",y.C,",","L )"
           else:
              print "(",y.M,",",y.C,",","R )"
   print "total " , total , " illegals " , invalid , " repeated " , repeated

if __name__ == "__main__":
   main()
