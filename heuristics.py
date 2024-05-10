import random

def random(possible_moves, current_board):
	return random.choice(possible_moves)

def move_furthest_first(possible_moves, current_board):
	furthest_move = possible_moves[0]
	for move in possible_moves:
		if current_board.current_player == 0:
			furthest_move = move if furthest_move[0] > move[0] else furthest_move
		else:
			furthest_move = move if furthest_move[0] < move[0] else furthest_move
	print(possible_moves)
	print(furthest_move)
	return furthest_move

def move_closest_first(possible_moves, current_board):
	closest_move = possible_moves[0]
	for move in possible_moves:
		if current_board.current_player == 0:
			closest_move = move if closest_move[0] < move[0] else closest_move
	return closest_move

def keep_pieces_safe():
	pass

def hit_enemy_pieces():
	pass