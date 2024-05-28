import random

def rand_choice(possible_moves, current_board):
	return random.choice(possible_moves)

def move_furthest_first(possible_moves, current_board):
	furthest_move = possible_moves[0]
	if current_board.current_player == 0:
		for move in possible_moves:
			if furthest_move[0] < move[0]:
				furthest_move = move
			elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
				furthest_move = move
	else:
		for move in possible_moves:
			if furthest_move[0] > move[0]:
				furthest_move = move
			elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
				furthest_move = move
	return furthest_move

def move_closest_first(possible_moves, current_board):
	closest_move = possible_moves[0]
	if current_board.current_player == 0:
		for move in possible_moves:
			if closest_move[0] > move[0]:
				closest_move = move
			elif closest_move[0] == move[0] and closest_move[2] < move[2]:
				closest_move = move
	else:
		for move in possible_moves:
			if closest_move[0] < move[0]:
				closest_move = move
			elif closest_move[0] == move[0] and closest_move[2] < move[2]:
				closest_move = move
	return closest_move

def keep_pieces_safe(possible_moves, current_board):
	for move in possible_moves:
		if current_board.points[current_board.current_player][move[1]] > 0:
			return move
	return rand_choice(possible_moves, None)

def hit_enemy_pieces(possible_moves, current_board):
	if current_board.current_player == 0:
		for move in possible_moves:
			if move[1] >= 0 and move[1] <= 23 and current_board.points[1][move[1]] == 1:
				return move
	else:
		for move in possible_moves:
			if move[1] >= 0 and move[1] <= 23 and current_board.points[0][move[1]] == 1:
				return move
	return rand_choice(possible_moves, None)

def bear_off_first(possible_moves, current_board):
	if current_board.current_player == 0:
		for move in possible_moves:
			if move[1] < 0:
				return move
	else:
		for move in possible_moves:
			if move[1] > 23:
				return move
	return rand_choice(possible_moves, current_board)

def near_edge_first(possible_moves, current_board):
	for move in possible_moves:
		if move[1] >= 0 and move[1] <=23:
			return move
	return rand_choice(possible_moves, current_board)

def dan_heuristic(possible_moves, current_board):
	unchanged_move = None
	furthest_move = None
	#Check if hit move is possible.
	if current_board.current_player == 0:
		for move in possible_moves:
			if current_board.points[1 - current_board.current_player][move[1]] == 1:
				if furthest_move == None:
					furthest_move = move
				elif furthest_move[0] < move[0]:
					furthest_move = move
				elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
					furthest_move = move
	else:
		for move in possible_moves:
			if current_board.points[1 - current_board.current_player][move[1]] == 1:
				if furthest_move == None:
					furthest_move = move
				elif furthest_move[0] > move[0]:
					furthest_move = move
				elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
					furthest_move = move

	if current_board.current_player == 0:
		if furthest_move == unchanged_move:
			#Check if safe move is possible.
			for move in possible_moves:
				if current_board.points[current_board.current_player][move[1]] > 0:
					if furthest_move == None:
						furthest_move = move
					elif furthest_move[0] < move[0]:
						furthest_move = move
					elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
						furthest_move = move
	else:
		if furthest_move == unchanged_move:
			#Check if safe move is possible.
			for move in possible_moves:
				if current_board.points[current_board.current_player][move[1]] > 0:
					if furthest_move == None:
						furthest_move = move
					if furthest_move[0] > move[0]:
						furthest_move = move
					elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
						furthest_move = move

	if furthest_move == unchanged_move:
		#Find furthest move.
		furthest_move = possible_moves[0]
		if current_board.current_player == 0:
			for move in possible_moves:
				if furthest_move == None:
					furthest_move = move
				elif furthest_move[0] < move[0]:
					furthest_move = move
				elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
					furthest_move = move
		else:
			for move in possible_moves:
				if furthest_move == None:
					furthest_move = move
				elif furthest_move[0] > move[0]:
					furthest_move = move
				elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
					furthest_move = move

	return furthest_move

#Check if there is any pieces that can hit each other on the board
def pre_running_game_check(current_board):
	if current_board.bar[0] > 0 or current_board.bar[1] > 0:
		return False
	player1_counter = current_board.borne_off[0]
	player2_counter = current_board.borne_off[1]
	biggest = 0
	smallest = 23
	i = 0
	while player1_counter < 15 and i < 24:
		player1_counter += current_board.points[0][i]
		i += 1
	biggest = i - 1
	i = 23
	while player2_counter < 15 and i > -1:
		player2_counter += current_board.points[1][i]
		i -= 1
	smallest = i + 1
	if biggest < smallest:
		return True
	return False

def home_game_check(current_board):
	if current_board.bar[0] != 0 or current_board.bar[1] != 0:
		return False
	if current_board.current_player == 0 and (current_board.borne_off[0] + sum(current_board.points[0][0:6])) != 15:
		return False
	if current_board.current_player == 1 and (current_board.borne_off[1] + sum(current_board.points[1][18:24])) != 15:
		return False
	return True
	


def first_strat(possible_moves, current_board):
	#Hit
	if pre_running_game_check(current_board): 
		if current_board.current_player == 0:
			for move in possible_moves:
				if move[1] >= 0 and move[1] <= 23 and current_board.points[1][move[1]] == 1:
					return move
		else:
			for move in possible_moves:
				if move[1] >= 0 and move[1] <= 23 and current_board.points[0][move[1]] == 1:
					return move
		#move furthest
		return move_furthest_first(possible_moves, current_board)
	
	elif home_game_check(current_board) == False:
		return move_furthest_first(possible_moves, current_board)
	
	else:
		return bear_off_first(possible_moves, current_board)

def second_strat(possible_moves, current_board):
	if home_game_check(current_board) == False:
		return move_furthest_first(possible_moves, current_board)
	else:
		return bear_off_first(possible_moves, current_board)
	