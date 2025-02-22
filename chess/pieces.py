class Piece(object):
	def __init__(self) -> None:
		self.name: str = ''
		self.location: str = None
		self.color: str = None
		self.isActive: bool = True
		self.alias: str = ''

	def __repr__(self) -> str:
		if self.isActive:
			return f'({self.name}, {self.location})'
		else:
			return f'<{self.name} is inactive/captured>'
		
	def __str__(self) -> str:
		if self.isActive:
			return self.alias
		else:
			return f'<{self.name} is inactive/captured>'

	def move(self, to) -> None:
		valid_locations = self.show_valid()

		if to in valid_locations:
			self.location = to
	
	def show_moves(self, pieces: list) -> list:
		h = ord(self.location[0]) - 96
		v = int(self.location[1])

		piece_location = [x.location for x in pieces]
		piece_color = [x.color for x in pieces]

		return (h,v,piece_location, piece_color)


class Pawn(Piece):
	def __init__(self, color: str):
		super().__init__()
		self.name = 'Pawn'
		self.color = color
		self.alias = 'PN(W)' if color == 'white' else 'PN(B)'
		self.isFirstMove = True

		if self.color == 'white':
			self.promote_list = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

		else:
			self.promote_list = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1']

	def show_moves(self, pieces: list) -> list:
		h, v, location, color = super().show_moves(pieces)

		moves = []

		if self.color == 'white':
			move_up = (h,v+1)
			move_2up = (h,v+2)
			move_up_left = (h-1,v+1)
			move_up_right = (h+1,v+1)			

		else:
			move_up = (h,v-1)
			move_2up = (h,v-2)
			move_up_left = (h-1,v-1)
			move_up_right = (h+1,v-1)

		move_up_loc = f'{chr(move_up[0]+96)}{move_up[1]}'
		if 1<=move_up[0]<=8 and 1<=move_up[1]<=8 and (not move_up_loc in location):
			moves.append(move_up_loc)

			move_2up_loc = f'{chr(move_2up[0]+96)}{move_2up[1]}'
			if 1<=move_2up[0]<=8 and 1<=move_2up[1]<=8 and (not move_2up_loc in location) and self.isFirstMove:
				moves.append(move_2up_loc)

		move_up_left_loc = f'{chr(move_up_left[0]+96)}{move_up_left[1]}'
		if 1<=move_up_left[0]<=8 and 1<=move_up_left[1]<=8 and move_up_left_loc in location:
			if color[location.index(move_up_left_loc)] != self.color:
				moves.append(move_up_left_loc)

		move_up_right_loc = f'{chr(move_up_right[0]+96)}{move_up_right[1]}'
		if 1<=move_up_right[0]<=8 and 1<=move_up_right[1]<=8 and move_up_right_loc in location:
			if color[location.index(move_up_right_loc)] != self.color:
				moves.append(move_up_right_loc)

		return moves		


class Rook(Piece):
	def __init__(self, color: str):
		super().__init__()
		self.name = 'Rook'
		self.color = color
		self.alias = 'RK(W)' if color == 'white' else 'RK(B)'

	def show_moves(self, pieces: list) -> list:
		h, v, location, color = super().show_moves(pieces)

		moves = []

		stop_flag = [0,0,0,0]
		for i in range(1,9):
			move_templates = [(h+i,v), (h-i,v), (h,v-i), (h,v+i)]
			for j, move in enumerate(move_templates):
				move_loc = f'{chr(move[0]+96)}{move[1]}'
				if 1<=move[0]<=8 and 1<=move[1]<=8:
					if not move_loc in location:
						if stop_flag[j] == 0:
							moves.append(move_loc)
					else:
						if color[location.index(move_loc)] != self.color and stop_flag[j] == 0:
							moves.append(move_loc)
						stop_flag[j] = 1
		return moves
	
	def show_moves_enpassant(self, pieces: list) -> list:
		...


class Bishop(Piece):
	def __init__(self, color: str):
		super().__init__()
		self.name = 'Bishop'
		self.color = color
		self.alias = 'BP(W)' if color == 'white' else 'BP(B)'

	def show_moves(self, pieces: list) -> list:
		h, v, location, color = super().show_moves(pieces)

		moves = []

		stop_flag = [0,0,0,0]
		for i in range(1,9):
			move_templates = [(h+i,v+i), (h+i,v-i), (h-i,v+i), (h-i,v-i)]
			for j, move in enumerate(move_templates):
				move_loc = f'{chr(move[0]+96)}{move[1]}'
				if 1<=move[0]<=8 and 1<=move[1]<=8:
					if not move_loc in location:
						if stop_flag[j] == 0:
							moves.append(move_loc)
					else:
						if color[location.index(move_loc)] != self.color and stop_flag[j] == 0:
							moves.append(move_loc)
						stop_flag[j] = 1

		return moves


class Knight(Piece):
	def __init__(self, color: str):
		super().__init__()
		self.name = 'Knight'
		self.color = color
		self.alias = 'KT(W)' if color == 'white' else 'KT(B)'

	def show_moves(self, pieces: list) -> list:
		h, v, location, color = super().show_moves(pieces)

		moves = []

		move_template = [(h-2,v+1),(h+2,v+1),(h-2,v-1),(h+2,v-1),
						(h-1,v-2),(h-1,v+2),(h+1,v-2),(h+1,v+2)]

		for i, move in enumerate(move_template):
			if 1<=move[0]<=8 and 1<=move[1]<=8:
				move_loc = f'{chr(move[0]+96)}{move[1]}'
				if move_loc in location:
					if color[location.index(move_loc)] != self.color:
						moves.append(move_loc)
				else:
					moves.append(move_loc)

		return moves


class King(Piece):
	def __init__(self, color: str):
		super().__init__()
		self.name = 'King'
		self.color = color
		self.alias = 'KG(W)' if color == 'white' else 'KG(B)'
		self.isFirstMove = True
		self.canCastle = False
		
		if self.color == 'white':
			self.castling_locations = ['c1', 'g1']
		else:
			self.castling_locations = ['c8', 'g8']


	def show_moves(self, pieces: list) -> list:
		h, v, location, color = super().show_moves(pieces)

		move_template = [(h+1,v), (h-1,v), (h,v+1), (h,v-1),
				(h+1,v+1), (h+1,v-1), (h-1,v+1), (h-1,v-1)]
		
		moves = []
		
		for move in move_template:
			move_loc = f'{chr(move[0]+96)}{move[1]}'
			if 1<=move[0]<=8 and 1<=move[1]<=8:
				moves.append(move_loc)
				
		return moves
	
	def show_castling_moves(self, pieces: list) -> list:
		...


class Queen(Piece):
	def __init__(self, color: str):
		super().__init__()
		self.name = 'Queen'
		self.color = color
		self.alias = 'QN(W)' if color == 'white' else 'QN(B)'


	def show_moves(self, pieces: list) -> list:
		h, v, location, color = super().show_moves(pieces)

		moves = []

		stop_flag = [0,0,0,0]
		for i in range(1,9):
			move_templates = [(h+i,v), (h-i,v), (h,v-i), (h,v+i)]
			for j, move in enumerate(move_templates):
				move_loc = f'{chr(move[0]+96)}{move[1]}'
				if 1<=move[0]<=8 and 1<=move[1]<=8:
					if not move_loc in location:
						if stop_flag[j] == 0:
							moves.append(move_loc)
					else:
						if color[location.index(move_loc)] != self.color and stop_flag[j] == 0:
							moves.append(move_loc)
						stop_flag[j] = 1

		stop_flag = [0,0,0,0]
		for i in range(1,9):
			move_templates = [(h+i,v+i), (h+i,v-i), (h-i,v+i), (h-i,v-i)]
			for j, move in enumerate(move_templates):
				move_loc = f'{chr(move[0]+96)}{move[1]}'
				if 1<=move[0]<=8 and 1<=move[1]<=8:
					if not move_loc in location:
						if stop_flag[j] == 0:
							moves.append(move_loc)
					else:
						if color[location.index(move_loc)] != self.color and stop_flag[j] == 0:
							moves.append(move_loc)
						stop_flag[j] = 1

		return moves