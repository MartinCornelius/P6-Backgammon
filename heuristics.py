import random

def random(possible_moves, current_board):
	return random.choice(possible_moves)

def move_furthest_first(possible_moves, current_board):
	furthest_move = possible_moves[0]
	for move in possible_moves:
		if current_board.current_player == 0:
			if furthest_move[0] < move[0]:
				furthest_move = move
			elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
				furthest_move = move
		else:
			if furthest_move[0] > move[0]:
				furthest_move = move
			elif furthest_move[0] == move[0] and furthest_move[2] < move[2]:
				furthest_move = move
	return furthest_move

def move_closest_first(possible_moves, current_board):
	closest_move = possible_moves[0]
	for move in possible_moves:
		if current_board.current_player == 0:
			if closest_move[0] > move[0]:
				closest_move = move
			elif closest_move[0] == move[0] and closest_move[2] < move[2]:
				closest_move = move
		else:
			if closest_move[0] < move[0]:
				closest_move = move
			elif closest_move[0] == move[0] and closest_move[2] < move[2]:
				closest_move = move
	return closest_move

def keep_pieces_safe():
	pass

def hit_enemy_pieces():
	pass