'''
�� �ڵ�� ���� ����ī���� Ʈ�� Ž���� �̿��� ȿ������ �⹰�̵��� ���ϴ� ������
�Ѱ���:
	random playout�� ���� ���迡 �����ϹǷ� ���� best move�� ��ġ���� ����������
    �ܼ��� �¸�, �й�, ���ºο� ���� ���Լ��� ����� ��� random playout�� �̿��� best move�� ���ϴ� �������� ȿ���� ���� ������ ����Ǿ� �⹰ ���� ������
    �δ� ����� �����. �̷� ���� �⹰ ���� ����ȭ �Ǿ� �ִٰ� ������ ���� �Ѱ���
    random ����� ����ϴ� ���� best move�� �������� �ð��� �ʹ� ���� �ɸ�
'''

from gimul import gimul_coordinate as mp
import copy
import random
import numpy as np
import time

def is_finish(board): # ���� �Ѵ� ��������� n, �ʰ� ��������� c, ���� ��������� h   ������ �������� Ȯ���ϴ� �Լ�
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

def evaluate(board, turn): # ���� �� ���¿� ���� �� �Լ�
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

def piece_move(board, i_x, i_y, f_x, f_y): # ���� �ű�� �Լ�
	result = copy.deepcopy(board)
	piece = result[i_x][i_y]
	result[i_x][i_y] = 0
	result[f_x][f_y] = piece
	return result
		
def r_playout(board, turn, num): # �������� numȸ��ŭ ���� �θ鼭 ������ ������
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

# ó�� ���¿� �°� ���� �����ϱ�

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
	max_playout = 30 #�ִ� ����ձ��� Ž��
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
	a = int(input("i_x : ")) # ����� AI�� ����, ����� ������ �Է�
	b = int(input("i_y : "))
	c = int(input("f_x : "))
	d = int(input("f_y : "))
	ttt = board[a][b]
	board[a][b] = 0
	board[c][d] = ttt