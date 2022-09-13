'''
�� �ڵ�� ����ī���� Ʈ�� Ž���� �̿��� ȿ������ �⹰�̵��� ���ϴ� ������
�Ѱ���:
	random playout�� ���� ���迡 �����ϹǷ� ���� best move�� ��ġ���� ����������
	�ð��� �����ɸ�
'''

from gimul import gimul_coordinate as mp
from math import sqrt, log
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
	if is_finish(board) == 'n': return 0
	if is_finish(board) == 'h':
		if turn == 'han': return 1
		else: return -1
	if is_finish(board) == 'c':
		if turn == 'cho': return 1
		else: return -1

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

def UCB1(w, n, t): # ����ī���� Ʈ�� Ž������ selection�� ���̵尡 ��. �� �Լ� ���� ū ��� ���� ����
		return w/n +  sqrt(2*log(t)/n)
		
class node: # Ʈ���� ��� ����
	def __init__(self, board, turn, rootnode):
		self.board = board
		self.w = 0
		self.n = 0
		self.turn = turn
		self.child = []
		self.rootnode = rootnode
		
	def make_child(self): # �ڽ� ��带 ����
		if self.turn == 'han':
			for i in range(1, 10):
				for j in range(1, 11):
					if board[i][j] > 0 and board[i][j] < 10:
						movable_point = mp(i, j, board)
						for k in movable_point:
							new_board = piece_move(board, i, j, k[0], k[1])
							new_child = node(new_board, 'cho', self)
							self.child.append(new_child)
		if self.turn == 'cho':
			for i in range(1, 10):
				for j in range(1, 11):
					if board[i][j] > 10:
						movable_point = mp(i, j, board)
						for k in movable_point:
							new_board = piece_move(board, i, j, k[0], k[1])
							new_child = node(new_board, 'han', self)
							self.child.append(new_child)
		
	def selection(self): # ����
		ucb = []
		for i in self.child:
			if i.n == 0: return i
			else: ucb.append(UCB1(i.w, i.n, self.n))
		return self.child[np.argmax(ucb)]

	def simulation(self, playout_num, expansion_num, real_turn): # ����ī���� Ʈ�� Ž������ �� ���� �ùķ��̼��� ����
		t_node = self
		while(len(t_node.child) != 0):
			t_node = t_node.selection()
		bd = r_playout(t_node.board, t_node.turn, playout_num)
		add_w = evaluate(bd, real_turn)
		t_node.w += add_w
		t_node.n += 1
		if t_node.n == expansion_num:
			t_node.make_child()
		t_node = t_node.rootnode
		while(t_node != None):
			t_node.w += add_w
			t_node.n += 1
			t_node = t_node.rootnode
		
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
	turn = 'cho'
	playout_num = 80
	expansion_num = 5
	N = node(board, turn, None)
	N.make_child()
	a = time.time()
	N.simulation(playout_num, expansion_num, turn)
	b = time.time()
	sim_num = int(60 / (b-a))
	sim_num = 2000
	for i in range(sim_num):
		N.simulation(playout_num, expansion_num, turn)
		print(str(i) + " / " + str(sim_num))
	lst = []
	for i in N.child:
		lst.append(i.n)
	rst = N.child[np.argmax(lst)].board
	for i in range(1, 10):
		print(rst[i][1:11])
	board = rst
	a = int(input("i_x : "))
	b = int(input("i_y : "))
	c = int(input("f_x : "))
	d = int(input("f_y : "))
	ttt = board[a][b]
	board[a][b] = 0
	board[c][d] = ttt

