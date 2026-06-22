class Hole:
	def __init__(self, stones: int | None, player, index: int):
		self.stones = stones # None represents kettle
		self.player = player
		self.index = index

	def copy(self):
		return Hole(self.stones, self.player, self.index)

class Counter:
	def __init__(self, count: int = 0):
		self.count = count

	def copy(self):
		return Counter(self.count)

class State:
	SIZE = 9
	STARTING_STONES_PER_HOLE = 9
	MINIMUM_STONES_TO_PLAY = 1

	def hole_iterator(self, turn, hole_index):
		"""When given row and index of the starting position, will yield each position where the player puts the stone"""
		current_row = turn
		while True:
			row = self.row_of(current_row)
			yield row[hole_index]
			hole_index += 1
			if hole_index >= self.SIZE: # if we overflow the board size, continue iterating on the opposite side
				hole_index = 0
				current_row = not current_row 

	@classmethod
	def new_starting_position(cls):
		"""Create starting position state"""
		row1 = tuple(Hole(cls.STARTING_STONES_PER_HOLE, True, i) for i in range(cls.SIZE))
		row2 = tuple(Hole(cls.STARTING_STONES_PER_HOLE, False, i) for i in range(cls.SIZE))
		point_counter1 = Counter()
		point_counter2 = Counter()
		starting_player = True
		return State(row1, row2, point_counter1, point_counter2, starting_player, False, False)

	def copy(self):
		row1 = tuple(hole.copy() for hole in self.row1)
		row2 = tuple(hole.copy() for hole in self.row2)
		point_counter1 = self.point_counter1.copy()
		point_counter2 = self.point_counter2.copy()

		return State(row1, row2, point_counter1, point_counter2, self.turn, self.player1_has_kettle, self.player2_has_kettle)

	def __init__(self, row1: tuple[Hole, ...], row2: tuple[Hole, ...], point_counter1: Counter, point_counter2: Counter, turn, player1_has_kettle, player2_has_kettle):
		"""turn: True - player 1, False - player 2"""
		self.row1 = row1
		self.row2 = row2
		self.point_counter1 = point_counter1
		self.point_counter2 = point_counter2
		self.turn = turn
		self.player1_has_kettle = player1_has_kettle
		self.player2_has_kettle = player2_has_kettle

	def counter_of(self, player):
		return self.point_counter1 if player else self.point_counter2
	
	def row_of(self, player):
		return self.row1 if player else self.row2
	
	def __str__(self):
		output = ""
		# first player
		for hole in reversed(self.row1):
			if hole.stones == None:
				output += "_ "
			else:
				output += str(hole.stones) + " "
		output += "Score: " + str(self.point_counter1.count) + "\n"
		# second player
		for hole in self.row2:
			if hole.stones == None:
				output += "_ "
			else:
				output += str(hole.stones) + " "
		output += "Score: " + str(self.point_counter2.count) + "\n"
		
		return output

	def human_play(self, hole_index):
		"""Human natural indexing"""
		self.play(hole_index + 1)			

	def play(self, hole_index: int):
		"""Hole is index of hole from 0 to size -1 for bottom and size -1 to 0 for upper row"""
		hole_iterator = self.hole_iterator(self.turn, hole_index)
		hole = next(hole_iterator) # get starting hole
		if hole.stones == None:
			raise Exception("Unable to start from kettle")
		if hole.stones < self.MINIMUM_STONES_TO_PLAY:
			raise Exception("Forbidden to start from hole with no stones")
		# special scenario for just one stone in the hole
		if hole.stones == 1:
			hole.stones = 0
			hole = next(hole_iterator)
			if hole.stones == None: # kettle
				counter = self.counter_of(hole.player)
				counter.count += 1
			else: # put the stone to the NEXT hole instead of the starting hole
				hole.stones += 1
			self.turn = not self.turn # switch player
			return
		# the player picks up the stones from the starting hole and returns one stone back
		held_stones = hole.stones - 1
		hole.stones = 1

		while held_stones > 0: # for each ball in the players hand, place it into the hole and move to next hole
			hole = next(hole_iterator)
			if hole.stones == None: # special hole
				counter = self.counter_of(hole.player)
				counter.count += 1
			else: # normal hole
				hole.stones += 1
			held_stones -= 1

		# check special conditions
		if hole.stones: # do special actions unless ended in a kettle
			if hole.stones % 2 == 0 and hole.player != self.turn: # stealing from opposite player
				counter = self.counter_of(self.turn)
				counter.count += hole.stones
				hole.stones = 0

			if (
				hole.stones == 3 and
				hole.player != self.turn and
				hole.index != self.SIZE - 1 # prevent creating kettle on the last hole
			): # create kettle
				if hole.player == True and not self.player1_has_kettle:
					self.player1_has_kettle = True
				elif hole.player == False and not self.player2_has_kettle:
					self.player2_has_kettle = True
				else: # prevent creating kettles if one player alredy has one
					return

				counter = self.counter_of(self.turn)
				counter.count += hole.stones # 3
				hole.stones = None # mark as kettle

		# switch player
		self.turn = not self.turn

	def possible_next_moves(self):
		row = self.row_of(self.turn)
		return [
			hole_index for hole_index in range(self.SIZE) # try every hole
			if (stones := row[hole_index].stones) and stones >= self.MINIMUM_STONES_TO_PLAY # check that it isn't a special hole and has at least 2 stones
		]

	def finish_game(self):
		# player on turn has no stones; opposite player gets his own stones
		row = self.row_of(not self.turn)
		counter = self.counter_of(not self.turn)
		for hole in row:
			if not hole.stones: # ignore kettle
				continue
			counter.count += hole.stones
			hole.stones = 0
	
	# minimax
	def eval(self, max_depth) -> Eval:
		"""Calculate the point difference in optimal play after max_depth moves"""
		if max_depth == 0: # return point difference as an estimated evaluation
			return Eval(self.point_counter1.count - self.point_counter2.count)

		possible_moves = self.possible_next_moves()
		if not possible_moves: # no stones left
			self.finish_game()
			# create finished game evaluation
			diff = self.point_counter1.count - self.point_counter2.count
			win = Draw
			if diff > 0:
				win = True
			if diff < 0:
				win = False
			return Eval(diff, win)
		
		# otherwise create eval
		best_found = None
		for move in possible_moves:
			# create copy of current state and evaluate
			state = self.copy()
			state.play(move)
			eval = state.eval(max_depth - 1)
			# add notes to the evaluation
			eval.last_move = move
			eval.moves.append(move)
			if ( # check if it is better than best found
				not best_found
				or (self.turn and eval > best_found)
				or (not self.turn and eval < best_found)
			):
				best_found = eval
		
		if not best_found:
			raise Exception("Haven't found any move even though this should be handled by previous check")

		return best_found


class Draw:
	pass
class Eval:
	def __init__(self, eval, win: bool | None | type[Draw] = None):
		self.eval = eval
		self.win = win
		self.last_move: int | None = None
		self.moves = []
	
	CONVERTER = { # for inequalities
		True: 1,
		Draw: 0,
		None: 0,
		False: -1
	}

	def __eq__(self, other: object) -> bool:
		if type(other) != Eval:
			raise Exception("Cannot compare with objects other than Eval")
		
		return (self.win, self.eval) == (other.win, other.eval)

	def __gt__(self, other):
		if type(other) != Eval:
			raise Exception("Cannot compare with objects other than Eval")
		
		a = (self.CONVERTER[self.win], self.eval)
		b = (self.CONVERTER[other.win], other.eval)
		return a > b
	
	def __lt__(self, other):
		if type(other) != Eval:
			raise Exception("Cannot compare with objects other than Eval")
		
		a = (self.CONVERTER[self.win], self.eval)
		b = (self.CONVERTER[other.win], other.eval)
		return a < b

s = State.new_starting_position()

while True:
	print(s)
	eval = s.eval(6)
	if eval.last_move == None:
		break
	s.play(eval.last_move)
s.finish_game()
print(s)
