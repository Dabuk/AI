import time
import random 
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        self.time = 0
        pass

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately 
    #def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        ## current state
        #curstate = self.state(a,b,a_fin,b_fin)
        ## list accompanyinig state which are usedfor evaluating the state
        ## at the beginning, consider state itself to be its parent
        #curstate = [curstate, curstate, False, False, 0]
        ## considering ai as maximizing player
        #isMaximizingPlayer = True

        # To test the execution time, use time and file modules
        # In your experiments, you can try different depth, for example:
        #f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # Make sure to clean the file before each of/ your experiment
        #move = 0
        #for d in [6]: #You should try more
            #f.write('depth = '+str(d)+'\n')
            #t_start = time.time()
        #    self.time = t_start
            ## call minimax with starting alpha = -9999, beta = 9999, maxdepth = 7, startdepth = 0, currentstate
            ## returns heuristic value of move and the move
        #    heur, move = self.minimax(curstate,0,True,-9999,9999,d)
        #    print("ai move ", heur, move)
            #f.write(str(time.time()-t_start)+'\n')
        #f.close()
        
        #return move
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code. 
        
        #Comment all the code above and start your code here

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin

        ## swap - taken from main.py
        def swap(self):
            c=self.a[:]
            self.a=self.b[:]
            self.b=c[:]
            c = self.a_fin
            self.a_fin = self.b_fin
            self.b_fin = c

    ## move function
    def move(self, a, b, a_fin, b_fin, t):
        curstate = self.state(a,b,a_fin,b_fin)
        ## list accompanyinig state which are usedfor evaluating the state
        ## at the beginning, consider state itself to be its parent
        curstate = [curstate, curstate, False, False, 0]
        ## considering ai as maximizing player
        isMaximizingPlayer = True

        move = 0
        for d in [8]:
            self.time = time.time()
            ## call minimax with starting alpha = -9999, beta = 9999, maxdepth = 7, startdepth = 0, currentstate
            ## returns heuristic value of move and the move
            heur, move = self.minimax(curstate,0,True,-9999,9999,d)
            #print("ai move ", heur, move)
 
        return move
        

    # calling minimax function
    def minimax(self, state, depth, isMaximizingPlayer, alpha, beta, maxdepth):
        ## if time exceeds 0.99 seconds, return current state value and move 
        if (time.time() - self.time) >= .95:
            #print(time.time() - self.time)
            return self.heuristicval(state,depth)

        ## if max depth reached, return heuristic value of that state
        if depth == maxdepth:
            return self.heuristicval(state,depth)

        ## if no further moves, return 
        if sum(state[0].a) == 0: #checksum all values in a list, check if its a terminal node
           return self.heuristicval(state,depth)

        ## get all possible child states
        childstates = self.getChildstates(state[0])
        
        ## maximizer
        if isMaximizingPlayer:

            ## initialize best heuristic
            bestheur = -9999

            ## no children, return
            if len(childstates) == 0:
                return bestheur, 0

            ## initialize bestmove
            bestmove = childstates[0][4]

            ## go through each child state
            for child in childstates:
                # swap so that any current player is always "a"
                child[0].swap()
                child[1].swap()

                # check for remaining legal moves
                if sum(child[0].a) == 0:
                    continue

                # minimax search on minimizer
                heur, _ = self.minimax(child, depth + 1, False, alpha, beta, maxdepth)

                # choose move based on returned heuristic
                if heur >= bestheur:
                    bestmove = child[4]

                # reassign best heuristic - maximize
                bestheur = max(bestheur,heur)

                # alpha pruning
                alpha = max(alpha,bestheur)
                if beta <= alpha:
                    break
            return bestheur, bestmove

        ## minimizer
        else:
            ## initialize bestheuristic
            bestheur = +9999
            
            ## no children, return
            if len(childstates) == 0:
                return bestheur, 0

            ## initialize bestmove
            bestmove = childstates[0][4]

            ## go through each child state
            for child in childstates:
                # swap so that any current player is always "a"                
                child[0].swap()
                child[1].swap()
                
                # check for remaining legal moves
                if sum(child[0].a) == 0:
                    continue

                # minimax search on minimizer
                heur, _ = self.minimax(child, depth + 1, True, alpha, beta, maxdepth)

                # choose move based on returned heuristic
                if heur <= bestheur:
                    bestmove = child[4]

                # reassign best heuristic - minimize
                bestheur = min(bestheur, heur)

                # beta pruning
                beta = min(beta, bestheur)
                if beta <= alpha:
                    break

            return bestheur, bestmove

    ## get child states of current state
    def getChildstates(self,state):
        cura = state.a
        curb = state.b
        curafin = state.a_fin
        curbfin = state.b_fin

        parentstate = state 

        states = []

        ## using updatestate code from main.py to get child states
        for move in range(0,6):
            captured = 0
            a = cura
            b = curb
            a_fin = curafin
            b_fin = curbfin

            ## don't include child state if no legal move
            if a[move] == 0:
                continue

            ao = a[:]
            all = a[move:] + [a_fin] + b + a[:move]
            count = a[move]
            all[0] = 0
            p = 1
            while count > 0:
                all[p] += 1
                p = (p + 1) % 13
                count -= 1
            a_fin = all[6 - move]
            b = all[7 - move:13 - move]
            a = all[13 - move:] + all[:6-move]
            cagain = bool()
            ceat = False
            p = (p - 1) % 13
            if p == 6 - move:
                cagain = True
            if p <= 5 - move and ao[move] < 14:
                id = p + move
                if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                    ceat = True
            elif p >= 14 - move and ao[move] < 14:
                id = p + move - 13
                if (ao[id] == 0 or p % 13 == 0) and b[5 - id] > 0:
                    ceat = True
            if ceat:
                a_fin += a[id] + b[5-id]
                captured = b[5-id]
                b[5-id] = 0
                a[id] = 0
            if sum(a)==0:
                b_fin += sum(b)
            if sum(b)==0:
                a_fin += sum(a)

            ## don't include child if no state change - prevent looping
            if a == cura and b == curb and curafin == a_fin and curbfin == b_fin:
                continue

            tempstate = self.state(a, b, a_fin, b_fin)

            states.append([tempstate,parentstate,cagain,ceat,move,captured])
        return states

    ## calculate heuristic value of a state at a given depth
    def heuristicval(self,fullstate,depth):
        state = fullstate[0]
        parentstate = fullstate[1]
        cagain = fullstate[2]
        ceat = fullstate[3]
        move = fullstate[4]
        captured = fullstate[5]

        a = state.a
        b = state.b
        a_fin = state.a_fin
        b_fin = state.b_fin

        ## positive reward for increased difference between ai and opponents stones in home bin
        ## negative reward if lot of beans in ai bin and very less in opponent bin - prevent large captures
        h1 = 25.0 * (state.a_fin - state.b_fin)  - 1.0 * (sum(a) - sum(b)) / 18.0
        ## positive reward for playing again
        h2 = cagain * 20.0
        ## positive reward for capturing opponent stones
        h3 = ceat * captured * 10
        ## negative reward for staying away from win condition
        h4 = - 10 * (37 - a_fin)
        ## high positive reward for winning
        hwin = 50 * (state.a_fin > 37)
        ## High negative reward for having no remaining moves but opponent has a lot of stones to play and ends up winning.
        hlose = - 150 * (not sum(a)) * ((sum(b) + b_fin)) * ((sum(b) + b_fin) > 37)
        ## sum all heuristics
        heur = h1 + h3 + h2 + hwin + hlose + h4

        ## change sign based on heuristic calculated during minimizer / maximizer - this is because a keeps swapping between ai and opponent between plays
        if depth %2 !=0:
            heur = -1* heur

        return heur, move
