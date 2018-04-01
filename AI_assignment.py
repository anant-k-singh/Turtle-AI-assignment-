import Tkinter as tk
import sys
import copy
import random

sys.setrecursionlimit(1000000)


if sys.argv[1] == 'hva':
	print 'Human Agent is Player1 ( BLUE )'
	print 'AI Agent is Player2 ( GREEN )'
elif sys.argv[1] == 'hvr':
	print 'Human Agent is Player1 ( BLUE )'
	print 'Random Agent is Player2 ( GREEN )'
elif sys.argv[1] == 'ava':
	print 'AI Agent is Player1 ( BLUE )'
	print 'AI Agent is Player2 ( GREEN )'
elif sys.argv[1] == 'avr':
	print 'AI Agent is Player1 ( BLUE )'
	print 'Random Agent is Player2 ( GREEN )'
else:
	print 'Invalid Player Argument!'
	sys.exit()

ROWS = 8
COLS = 8
LAYERS = 2
col_width = 80
row_height = 80
ratio = 0.2
minMaxTurn=0
bestrow=[]
bestcol=[]
bestdir=[]
symbolA=-1
symbolB=1
symbolEmpty=0

class gameState:
	def __init__(self):
		self.matrix = [[symbolEmpty]*COLS for _ in xrange(0,ROWS)]

board = gameState()

for i in xrange(0,LAYERS):
	for j in xrange(0,COLS):
		board.matrix[i][j] = symbolA
		board.matrix[ROWS -1 -i][j] = symbolB

turn=0
countA=COLS*LAYERS
countB=COLS*LAYERS

scol=-1
srow=-1
def getScore(gamestate):
	a=0
	b=0
	for i in xrange(0,ROWS):
		for j in xrange(0,COLS):
			if gamestate.matrix[i][j]==symbolA:
				a=a+1
			elif gamestate.matrix[i][j]==symbolB:
				b=b+1
	return a,b
'''
	0 North
	1 NW
	2 West
	3 SW
	4 South
	5 SE
	6 East
	7 NE
'''
dr=[-1,-1,0,1,1,1,0,-1]
dc=[0,-1,-1,-1,0,1,1,1]

col_width=row_height
WIDTH = COLS * col_width
HEIGHT = ROWS * row_height
Padding = int(ratio*col_width)

root = tk.Tk()
var = tk.StringVar()
w=tk.Label(root, textvariable=var)
c = tk.Canvas(root, width=WIDTH, height=HEIGHT, borderwidth=5, background='black')
# c.create_text(100,200,font="Times 10 bold",text="Click the bubbles.")
c.pack()
w.pack()
# c.create_line(0,2,4,2,fill="red")
def updateboard():
	global ROWS, COLS, board, symbolA, symbolB,p
	var.set('Player 1 : '+str(getScore(board)[0])+' & Player 2 : '+str(getScore(board)[1]))
	# w=tk.Entry(root, textvariable=var)
	# w.pack()
	for i in xrange(0,ROWS):
		for j in xrange(0,COLS):
			if board.matrix[i][j] == symbolA:
				c.create_rectangle(j*col_width+Padding, i*row_height+Padding, (j+1)*col_width-Padding, (i+1)*row_height-Padding, fill="blue")
			elif board.matrix[i][j] == symbolB:
				c.create_rectangle(j*col_width+Padding, i*row_height+Padding, (j+1)*col_width-Padding, (i+1)*row_height-Padding, fill="green")
			else:
				c.create_rectangle(j*col_width+Padding, i*row_height+Padding, (j+1)*col_width-Padding, (i+1)*row_height-Padding, fill="black")
	# c.create_rectangle(0*col_width+20, 0*row_height+20, (0+1)*col_width-20, (0+1)*row_height-20, fill="white")
	for j in xrange(1,COLS):
		c.create_line(j*col_width,0,j*col_width,(ROWS)*row_height,fill= "white",width=2)
	for i in xrange(0,ROWS):
		c.create_line(0,i*row_height,(COLS)*col_width,i*row_height,fill="white",width=2)

def terminalState(currentState):
	# cState=gameState()
	# cState=copy.deepcopy(currentState)
	# print currentState.matrix
	a,b = getScore(currentState) 
	if a==0 or b==0:
		return 1
	else:
		return 0

def insideboard(r, c):
	if r>=0 and r<ROWS and c>=0 and c<COLS:
		return 1
	else:
		return 0

def validMove(r,c,dir,currentState, turn=-1):
	# print r,c,dir,turn
	mysymbol=currentState.matrix[r][c]
	othersymbol=mysymbol*(-1)
	# board.matrix=currentState.matrix
	if turn != -1:
		if turn == 0:
			mysymbol = symbolA
		elif turn == 1:
			mysymbol = symbolB
		othersymbol = mysymbol * (-1)
	if currentState.matrix[r][c] == othersymbol or currentState.matrix[r][c] == symbolEmpty:
		return False
	nextr = r+dr[dir]
	nextc = c+dc[dir]
	if insideboard(nextr,nextc):
		if currentState.matrix[nextr][nextc] == mysymbol:
			return False
		elif currentState.matrix[nextr][nextc] == othersymbol:
			nextr += dr[dir]
			nextc += dc[dir]
			if not insideboard(nextr,nextc) or currentState.matrix[nextr][nextc] != symbolEmpty:
				return False
		return True
	else:
		return False

def getLegalActions(r, c,currentState):
	directions = []
	for i in range(0,len(dr)):
		if validMove(r,c,i,currentState):
			directions.append(i)
	# return valid directions
	return directions

def successor(currentState,r,c,dir):
	nr = r+dr[dir]
	nc = c+dc[dir]
	nextState = copy.deepcopy(currentState)
	if nextState.matrix[nr][nc]*nextState.matrix[r][c] == -1:
		nextState.matrix[nr][nc]=nextState.matrix[r][c]
		nr = nr+dr[dir]
		nc = nc+dc[dir]		
	nextState.matrix[nr][nc]=nextState.matrix[r][c]
	nextState.matrix[r][c]=0
	return nextState

def applyMove(r, c, dir):
	global countA, countB
	nextr = r+dr[dir]
	nextc = c+dc[dir]
	if board.matrix[nextr][nextc] != symbolEmpty:
		if turn == 0:
			board.matrix[nextr][nextc] = symbolA
			countA+=1
			countB-=1
		else:
			board.matrix[nextr][nextc] = symbolB
			countA-=1
			countB+=1
		nextr += dr[dir]
		nextc += dc[dir]
	board.matrix[r][c], board.matrix[nextr][nextc] = board.matrix[nextr][nextc], board.matrix[r][c]
	updateboard()


def getDir(srow, scol, frow, fcol):
	for i in xrange(0,len(dr)):
		if srow+dr[i] == frow and scol+dc[i] == fcol:
			return i
	else:
		return -1

def evaluationFunction(gameState,symbol=symbolA):
	score = 0
	if symbol==symbolA:
		score = getScore(gameState)[0]
	else:
		score = getScore(gameState)[1]
	scoreA = 0
	scoreB = 0
	# for i in xrange(0,ROWS):
	# 	for j in xrange(0,COLS):
	# 		if gameState.matrix[i][j] == symbolA:
	# 			for dir in xrange(0,len(dr)):
	# 				nextr, nextc = i+dr[dir], j+dc[dir]
	# 				if insideboard(nextr+dr[dir],nextc+dc[dir]) and gameState.matrix[i][j] == symbolB and gameState.matrix[nextr+dr[dir]][nextc+dc[dir]] == symbolEmpty:
	# 					scoreA += 1
	# 		elif gameState.matrix[i][j] == symbolB:
	# 			for dir in xrange(0,len(dr)):
	# 				nextr, nextc = i+dr[dir], j+dc[dir]
	# 				if insideboard(nextr+dr[dir],nextc+dc[dir]) and gameState.matrix[i][j] == symbolA and gameState.matrix[nextr+dr[dir]][nextc+dc[dir]] == symbolEmpty:
	# 					scoreB += 1
	# if scoreB > 0:
	# 	scoreB = 999999
	return score + scoreA - scoreB

def randomAgent():
	global turn
	validPiece = []
	for i in xrange(0,ROWS):
		for j in xrange(0,COLS):
			if board.matrix[i][j] == symbolB:
				actions = getLegalActions(i,j,board)
				if len(actions) > 0:
					validPiece.append([i,j,actions])
	index = random.randint(0,len(validPiece)-1)
	# print(validPiece[index])
	action_index = random.randint(0,len(validPiece[index][2])-1)
	# print("idx",action_index)
	action = validPiece[index][2][action_index]
	applyMove(validPiece[index][0],validPiece[index][1],action)

def AlphaBetaAction(currentState,curDepth,A,B,Depth,symbol=symbolA):
	global minMaxTurn
	# print 'mturn',minMaxTurn
	# minCount=0
	# maxCount=0
	# maxList=[]
	# minList=[]
	bestScore = [-999999]
	for i in xrange(0,ROWS):
		for j in xrange(0,COLS):
			if currentState.matrix[i][j]==symbol:
				# maxCount=maxCount+1
				# maxList.append([i,j])
				s = Max(currentState,curDepth,A,B,i,j,Depth,bestScore,symbol)
				# print "score for ",i,',',j,' = ',s
	# for i in xrange(0,maxCount):
		# minMaxTurn=1-minMaxTurn
		# print currentState.matrix
		# Max(currentState,curDepth,A,B,maxList[i][0],maxList[i][1])
	# else:
	# 	print 'else'
	# 	for i in xrange(0,minCount):
	# 		minMaxTurn=1-minMaxTurn
	# 		print 'min'
	# 		return Min(currentState,curDepth,A,B,minList[i][0],minList[i][1],Depth)
flag = 0

def Max(currentState,curDepth,A,B,r,c,Depth,bestScore,symbol):
	global bestrow,bestcol,bestdir
	if terminalState(currentState):
		return evaluationFunction(currentState,symbol)
	
	legalMoves = getLegalActions(r,c,currentState)
	for move in legalMoves:
		nextState = successor(currentState,r,c,move)
		if terminalState(nextState):
			del bestrow[:]
			del bestcol[:]
			del bestdir[:]

			bestrow.append(r)
			bestcol.append(c)
			bestdir.append(move)
			bestScore[0]=evaluationFunction(nextState,symbol)
			return bestScore[0]
		minBestScore = [999999]
		flag = 0
		for i in xrange(0,ROWS):
			for j in xrange(0,COLS):
				if currentState.matrix[i][j] == -symbol:
					p=Min(nextState,curDepth+1,A,B,i,j,Depth,minBestScore,symbol)
			# 		minMaxTurn=1-minMaxTu
					if p>bestScore[0]:
						if curDepth==0:
							del bestrow[:]
							del bestcol[:]
							del bestdir[:]

							bestrow.append(r)
							bestcol.append(c)
							bestdir.append(move)
						bestScore[0]=p
					elif p == bestScore[0]:
						if curDepth==0:
							bestrow.append(r)
							bestcol.append(c)
							bestdir.append(move)
		if bestScore[0] > B:
			return bestScore[0]
		A = max(A,bestScore[0])
	# print score,"score for Max @",curDepth
	return bestScore[0]

def Min(currentState, curDepth,A,B,r,c,Depth,minBestScore, symbol):
	global flag
	# print 'minDepth',curDepth
	if curDepth == Depth or terminalState(currentState):
		# print 'dc'
		return evaluationFunction(currentState,symbol)
	legalMoves = getLegalActions(r,c,currentState)
	# Max's turn
	# if Min_idx == 1:
	# flag = 0
	if len(legalMoves) == 0:
		flag = flag +1
	if flag==getScore(currentState)[1]:
		print 'Draw!'
		sys.exit()
	for move in legalMoves:
		nextState = successor(currentState,r,c,move)
		if terminalState(nextState):
			# return evaluationFunction(nextState)
			return -999999,flag
		# score.append( Max(nextState,curDepth+1) )
		bestScore = [-999999]
		for i in xrange(0,ROWS):
			for j in xrange(0,COLS):
				if currentState.matrix[i][j]==symbol:
					p=Max(nextState,curDepth,A,B,i,j,Depth,bestScore,symbol)
				   	if(p<minBestScore[0]):
						minBestScore[0]=p
		# score = min(score,AlphaBetaAction(nextState,curDepth,A,B,Depth))
		if minBestScore[0] < A:
			return minBestScore[0],flag
		B = min(B,minBestScore[0])
	return minBestScore[0],flag

def g():
	if countA == 0 or countB == 0:
		return 1

def AI_Agent(symbol=symbolA):
	A=-float('inf')
	B=float('inf')
	Depth=1
	currentState=copy.deepcopy(board)
	AlphaBetaAction(currentState,0,A,B,Depth,symbol)

	randomIndex = random.randint(0,len(bestrow)-1)
	# print(bestrow)
	# print(bestcol)
	# print(bestdir)
	applyMove(bestrow[randomIndex],bestcol[randomIndex],bestdir[randomIndex])

def AIvRandom():
	global turn
	if g():
		if countB == 0:
			print 'Blue Team Wins'
		else:
			print 'Green Team Wins'
		sys.exit()
	if turn == 0:
		AI_Agent()
	else:
		randomAgent()
	turn = 1-turn

def AIvAI():
	global turn
	if g():
		if countB == 0:
			print 'Blue Team Wins'
		else:
			print 'Green Team Wins'
		sys.exit()
	if turn == 0:
		AI_Agent(symbolA)
	else:
		AI_Agent(symbolB)
	turn = 1-turn

def f(frow, fcol):
	global scol,srow,turn
	# print(srow, scol, frow, fcol)
	dir = getDir(srow, scol, frow, fcol)
	if dir != -1 and validMove(srow,scol,dir,board,turn):
		applyMove(srow,scol,dir)
		scol=-1
		srow=-1
		turn = 1-turn
		if sys.argv[1] == 'hva':
			AI_Agent(symbolB)
		elif sys.argv[1] == 'hvr':
			randomAgent()
		turn = 1-turn
	else:
		scol=-1
		srow=-1
		print("Illegal Move")

def callback(event):
	global scol,srow
	if len(sys.argv) > 1:
		if sys.argv[1] == 'ava':
			AIvAI()
		elif sys.argv[1] == 'avr':
			AIvRandom()
		elif sys.argv[1] == 'hva' or sys.argv[1] == 'hvr':
			# Calculate column and row number
			if scol == -1:
				srow = event.y//row_height
				scol = event.x//col_width
			else:
				f(event.y//row_height, event.x//col_width)

def reset(event):
	global scol,srow
	scol = -1
	srow = -1

c.bind("<Button-1>", callback)
c.bind("<Button-3>", reset)
updateboard()
root.mainloop()
