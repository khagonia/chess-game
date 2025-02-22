from chess.pieces import *
from chess.player import Player

class Board(object):
	def __init__(self, white: Player, black: Player):
		self.tiles: list = []
		self.initialize_board(white, black)

	def initialize_board(self, white: Player, black: Player) -> None:
		for i in range(0,64):
			v = int(i/8) + 1
			h = chr(i - (v-1)*8 + 97)
			self.tiles.append(Tile(f'{h}{v}'))

		for i in range(0,8):
			self.add_piece(white.pieces.get('pawn')[i], f'{chr(i+97)}2')
			self.add_piece(black.pieces.get('pawn')[i], f'{chr(i+97)}7')

		self.add_piece(white.pieces.get('rook')[0], 'a1')
		self.add_piece(white.pieces.get('rook')[1], 'h1')
		self.add_piece(black.pieces.get('rook')[0], 'a8')
		self.add_piece(black.pieces.get('rook')[1], 'h8')

		self.add_piece(white.pieces.get('knight')[0], 'b1')
		self.add_piece(white.pieces.get('knight')[1], 'g1')
		self.add_piece(black.pieces.get('knight')[0], 'g8')
		self.add_piece(black.pieces.get('knight')[1], 'b8')

		self.add_piece(white.pieces.get('bishop')[0], 'c1')
		self.add_piece(white.pieces.get('bishop')[1], 'f1')
		self.add_piece(black.pieces.get('bishop')[0], 'c8')
		self.add_piece(black.pieces.get('bishop')[1], 'f8')

		self.add_piece(white.pieces.get('king')[0], 'e1')
		self.add_piece(black.pieces.get('king')[0], 'e8')
		self.add_piece(white.pieces.get('queen')[0], 'd1')
		self.add_piece(black.pieces.get('queen')[0], 'd8')

	def add_piece(self, piece: Piece, location: str) -> None:
		i = (ord(location[0]) - 97) + (int(location[1]) - 1) * 8
		piece.location = location
		self.tiles[i].occupant = piece
		self.tiles[i].isOccupied = True

	def remove_piece(self, location: str) -> None:
		i = (ord(location[0]) - 97) + (int(location[1]) - 1) * 8
		self.tiles[i].occupant = None
		self.tiles[i].isOccupied = False

	def move_piece(self, from_loc: str, to_loc) -> None:
		from_i = (ord(from_loc[0]) - 97) + (int(from_loc[1]) - 1) * 8
		to_i = (ord(to_loc[0]) - 97) + (int(to_loc[1]) - 1) * 8

		if not self.tiles[to_i].isOccupied:
			if self.tiles[from_i].occupant:
				self.tiles[to_i].occupant = self.tiles[from_i].occupant
				self.tiles[to_i].isOccupied = True

				self.tiles[from_i].occupant = None
				self.tiles[from_i].isOccupied = False

				print(f'{self.tiles[to_i].occupant.color.capitalize()} {self.tiles[to_i].occupant.name} moved from {from_loc} to {to_loc}')
			else:
				print(f'Invalid move, no piece to move at {from_loc}')
		else:
			print(f'Invalid move, {to_loc} is occupied.')


	def show(self, flipped = False):
		if flipped:
			board = []
			line = []
			for i, tile in enumerate(self.tiles[::-1]):
				line.append(tile)
				if i%8 == 7:
					line = line[::-1]
					board.extend(line)
					line = []
		else:
			board = self.tiles

		print('-'*56)
		for i, tile in enumerate(board):
			if i % 8 == 0 and i != 0:
				print()
				print('-'*56)
			print(tile, end='')
		print()
		print('-'*56)


class Tile(object):
	def __init__(self, address):
		self.address: str = address
		self.isOccupied: bool = False
		self.occupant: Piece = None

	def __repr__(self):
		if self.occupant:
			return f'Tile {self.address}: {self.occupant.alias}'
		else:
			return 'None'

	def __str__(self):
		if self.occupant:
			return f'|{self.occupant.alias}|'
		else:
			return '|     |'