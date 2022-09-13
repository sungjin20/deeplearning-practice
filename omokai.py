'''
몬테카를로 트리 탐색을 이용한 틱택토 인공지능 코드를 확장시켜 오목 유사 게임으로 적용을 시킨 코드임
탐색하고 시뮬레이션 해야할 수가 많아 best move를 구하기까지 시간이 많이 걸림
'''

import copy
import time
import numpy as np
import random
from math import sqrt, log

wh = 8
leng = 5
def next_point(board):
	rst = []
	for i in range(wh):
		for j in range(wh):
			if board[i][j] == '': rst.append((i, j))
	return rst
	
def is_finish(board):
	for i in range(wh):
		for j in range(wh-leng+1):
			tg = board[i][j]
			if tg == '': continue
			else:
				is_ok = 1
				for k in range(1, leng):
					if board[i][j+k] == tg: continue
					else:
						is_ok = 0
						break
				if is_ok: return tg
				else: j += k
	for i in range(wh):
		for j in range(wh-leng+1):
			tg2 = board[j][i]
			if tg2 == '': continue
			else:
				is_ok = 1
				for k in range(1, leng):
					if board[j+k][i] == tg2: continue
					else:
						is_ok = 0
						break
				if is_ok: return tg2
				else: j += k
	for j in range(wh-leng+1):
		tg2 = board[j][j]
		if tg2 == '': continue
		else:
			is_ok = 1
			for k in range(1, leng):
				if board[j+k][j+k] == tg2: continue
				else:
					is_ok = 0
					break
			if is_ok: return tg2
			else: j += k
	for j in range(wh-leng+1):
		tg2 = board[j][wh - j - 1]
		if tg2 == '': continue
		else:
			is_ok = 1
			for k in range(1, leng):
				if board[j+k][wh - j - k - 1] == tg2: continue
				else:
					is_ok = 0
					break
			if is_ok: return tg2
			else: j += k
	return ''

def evaluate(board, turn):
	if is_finish(board) == 'O':
		if turn == 'O': return 1
		else: return -1
	if is_finish(board) == 'X':
		if turn == 'X': return 1
		else: return -1
	return 0
	
def r_playout(board, turn, num):
	if num == 0: return board
	if turn == 'O':
		movable_point = next_point(board)
		if len(movable_point) == 0:
			return board
		move = movable_point[random.randrange(0, len(movable_point))]
		bd = copy.deepcopy(board)
		bd[move[0]][move[1]] = 'O'
		if is_finish(bd) != '':
			return bd
		else:
			return r_playout(bd, 'X', num-1)
		
	if turn == 'X':
		movable_point = next_point(board)
		if len(movable_point) == 0:
			return board
		move = movable_point[random.randrange(0, len(movable_point))]
		bd = copy.deepcopy(board)
		bd[move[0]][move[1]] = 'X'
		if is_finish(bd) != '':
			return bd
		else:
			return r_playout(bd, 'O', num-1)
			
def UCB1(w, n, t):
		return w/n +  sqrt(2*log(t)/n)
		
class node:
	def __init__(self, board, turn, rootnode):
		self.board = board
		self.w = 0
		self.n = 0
		self.turn = turn
		self.child = []
		self.rootnode = rootnode
		
	def make_child(self):
		if self.turn == 'O':
			movable_point = next_point(self.board)
			for k in movable_point:
				new_board = copy.deepcopy(self.board)
				new_board[k[0]][k[1]] = 'O'
				new_child = node(new_board, 'X', self)
				self.child.append(new_child)
		if self.turn == 'X':
			movable_point = next_point(self.board)
			for k in movable_point:
				new_board = copy.deepcopy(self.board)
				new_board[k[0]][k[1]] = 'X'
				new_child = node(new_board, 'O', self)
				self.child.append(new_child)
		
	def selection(self):
		ucb = []
		for i in self.child:
			if i.n == 0: return i
			else: ucb.append(UCB1(i.w, i.n, self.n))
		return self.child[np.argmax(ucb)]

	def simulation(self, playout_num, expansion_num, real_turn):
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

board = [['' for col in range(wh)] for row in range(wh)]
board[int(wh/2)][int(wh/2)] = 'X'

for i in range(wh):
	print(board[i][0:wh])
	
while(True):
	turn = 'O'
	playout_num = wh**2
	expansion_num = 10
	N = node(board, turn, None)
	N.make_child()
	a = time.time()
	N.simulation(playout_num, expansion_num, turn)
	b = time.time()
	sim_num = int(60 / (b-a))
	sim_num = 3000
	for i in range(sim_num):
		N.simulation(playout_num, expansion_num, turn)
		print(str(i) + " / " + str(sim_num))
	lst = []
	for i in N.child:
		lst.append(i.n)
	rst = N.child[np.argmax(lst)].board
	for i in range(wh):
		print(rst[i][0:wh])
	board = rst
	a = int(input("i_x : "))
	b = int(input("i_y : "))
	board[a][b] = 'X'
