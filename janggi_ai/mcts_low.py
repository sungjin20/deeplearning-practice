'''
이 코드는 원시 몬테카를로 트리 탐색을 이용한 효율적인 기물이동을 구하는 과정임
한계점:
	random playout에 의한 경험에 의존하므로 실제 best move와 일치하지 않을수있음
    단순한 승리, 패배, 무승부에 대한 평가함수를 사용할 경우 random playout을 이용한 best move를 구하는 과정에서 효율이 낮을 것으로 예상되어 기물 별로 점수를
    두는 방식을 사용함. 이로 인해 기물 별로 점수화 되어 있다고 가정한 것이 한계임
    random 방식을 사용하다 보니 best move를 얻기까지의 시간이 너무 오래 걸림
'''

from gimul import gimul_coordinate as mp
import copy
import random
import numpy as np
import time

def is_finish(board): # 궁이 둘다 살아있으면 n, 초가 살아있으면 c, 한이 살아있으면 h   게임이 끝났는지 확인하는 함수
	cho_gung = 0
	han_gung = 0
	for i in range(4, 7):
		for j in range(1, 4):
			if board[i][j] == 5:
				han_gung = 1
				break
		for j in range(8, 11):
			if board[i][j] == 15:
				cho_gung = 1
				break
	if cho_gung and han_gung: return 'n'
	elif not cho_gung: return 'h'
	else: return 'c'

def evaluate(board, turn): # 현재 판 상태에 대한 평가 함수
	cha = 13
	po = 7
	ma = 5
	sang  = 3
	sa = 3
	jjol = 2
	gung = 200
	point_cho = 0
	point_han = 0
	for i in range(1, 10):
		for j in range(1, 11):
			if board[i][j] == 0: continue
			elif board[i][j] == 1: point_han += cha
			elif board[i][j] == 2: point_han += ma
			elif board[i][j] == 3: point_han += sang
			elif board[i][j] == 4: point_han += sa
			elif board[i][j] == 5: point_han += gung
			elif board[i][j] == 6: point_han += po
			elif board[i][j] == 7: point_han += jjol
			
			elif board[i][j] == 11: point_cho += cha
			elif board[i][j] == 12: point_cho += ma
			elif board[i][j] == 13: point_cho += sang
			elif board[i][j] == 14: point_cho += sa
			elif board[i][j] == 15: point_cho += gung
			elif board[i][j] == 16: point_cho += po
			elif board[i][j] == 17: point_cho += jjol
	if turn == 'han': return point_han - point_cho
	else: return point_cho - point_han

def piece_move(board, i_x, i_y, f_x, f_y): # 말을 옮기는 함수
	result = copy.deepcopy(board)
	piece = result[i_x][i_y]
	result[i_x][i_y] = 0
	result[f_x][f_y] = piece
	return result
		
def r_playout(board, turn, num): # 랜덤으로 num회만큼 말을 두면서 게임을 진행함
	if num == 0: return board
	if turn == 'han':
		movable_point = []
		bd = copy.deepcopy(board)
		for i in range(1, 10):
			for j in range(1, 11):
				if bd[i][j] == 0: continue
				elif bd[i][j] < 10:
					mvp = mp(i, j, bd)
					for k in mvp:
						movable_point += [(i, j, k[0], k[1])]
		if len(movable_point) == 0:
			return bd
		move = movable_point[random.randrange(0, len(movable_point))]
		bd = piece_move(bd, move[0], move[1], move[2], move[3])
		if is_finish(bd) != 'n':
			return bd
		else:
			return r_playout(bd, 'cho', num-1)
		
	if turn == 'cho':
		movable_point = []
		bd = copy.deepcopy(board)
		for i in range(1, 10):
			for j in range(1, 11):
				if bd[i][j] == 0: continue
				elif bd[i][j] > 10:
					mvp = mp(i, j, bd)
					for k in mvp:
						movable_point += [(i, j, k[0], k[1])]
		if len(movable_point) == 0:
			return bd
		move = movable_point[random.randrange(0, len(movable_point))]
		bd = piece_move(bd, move[0], move[1], move[2], move[3])
		if is_finish(bd) != 'n':
			return bd
		else:
			return r_playout(bd, 'han', num-1)
   
board = [[0 for col in range(11)] for row in range(10)]

# 처음 상태에 맞게 보드 수정하기

board[1][1] = 1
board[9][1] = 1
board[2][1] = 2
board[3][1] = 3
board[7][1] = 2
board[8][1] = 3
board[4][1] = 4
board[6][1] = 4
board[5][2] = 5
board[2][3] = 6
board[8][3] = 6
board[1][4] = 7
board[3][4] = 7
board[5][4] = 7
board[7][4] = 7
board[9][4] = 7

board[1][10] = 11
board[9][10] = 11
board[2][10] = 12
board[3][10] = 13
board[7][10] = 12
board[8][10] = 13
board[4][10] = 14
board[6][10] = 14
board[5][9] = 15
board[2][8] = 16
board[8][8] = 16
board[1][7] = 17
board[3][7] = 17
board[5][7] = 17
board[7][7] = 17
board[9][7] = 17

for i in range(1, 10):
	print(board[i][1:11])
 
 while(True):
	turn = 'cho' # han or cho
	max_playout = 30 #최대 몇수앞까지 탐색
	reapeat_num = 50 # playout repeat num
	choice = []
	if turn == 'han':
		kk = 0
		for i in range(1, 10):
			for j in range(1, 11):
				if board[i][j] == 0: continue
				elif board[i][j] < 10:
					movable_point = mp(i, j, board)
					for k in movable_point:
						choice += [(i, j, k[0], k[1])]
		score = []
		for i in choice:
			kk += 1
			bd = piece_move(board, i[0], i[1], i[2], i[3])
			sum = 0
			for j in range(reapeat_num):
				bd2 = r_playout(bd, 'cho', max_playout)
				sum += evaluate(bd2, 'han')
			print(str(kk) + " / " + str(len(choice)))
			score.append(sum)
	if turn == 'cho':
		kk = 0
		for i in range(1, 10):
			for j in range(1, 11):
				if board[i][j] == 0: continue
				elif board[i][j] > 10:
					movable_point = mp(i, j, board)
					for k in movable_point:
						choice += [(i, j, k[0], k[1])]
		score = []
		for i in choice:
			kk += 1
			bd = piece_move(board, i[0], i[1], i[2], i[3])
			sum = 0
			for j in range(reapeat_num):
				bd2 = r_playout(bd, 'han', max_playout)
				sum += evaluate(bd2, 'cho')
			print(str(kk) + " / " + str(len(choice)))
			score.append(sum)
			
	rst = choice[np.argmax(score)]
	print(rst)
	ttt = board[rst[0]][rst[1]]
	board[rst[0]][rst[1]] = 0
	board[rst[2]][rst[3]] = ttt
	for i in range(1, 10):
		print(board[i][1:11])
	a = int(input("i_x : ")) # 사람과 AI의 대전, 사람의 선택을 입력
	b = int(input("i_y : "))
	c = int(input("f_x : "))
	d = int(input("f_y : "))
	ttt = board[a][b]
	board[a][b] = 0
	board[c][d] = ttt