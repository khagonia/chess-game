from chess.board import Board, Tile
from chess.pieces import *
from chess.player import Player
from datetime import datetime
import random

class ChessGame(object):
	def __init__(self, white_id: str, black_id: str) -> None:
		self.game_id: str = datetime.now().strftime('%Y%m%d') + ''.join([str(random.randint(0,9)) for x in range(3)])
		self.white: Player = Player('white', white_id)
		self.black: Player = Player('black', black_id)
		self.board: Board = Board(self.white, self.black)
		self.turn: str = 'white'
		self.history: list = []
		self.turn_count: int = 0

		print(f'Game initiated with id {self.game_id}. White player\'s turn.')

	def player_move(self, from_loc: str, to_loc: str) -> None:
		to_i = (ord(to_loc[0]) - 97) + (int(to_loc[1]) - 1) * 8

		if self.isMoveValid(from_loc, to_loc):
			if self.board.tiles[to_i].isOccupied:
				self.capture_piece(from_loc, to_loc)
			else:
				self.move_piece(from_loc, to_loc)

			if self.board.tiles[to_i].occupant.name == 'King':
				if self.board.tiles[to_i].occupant.canCastle and self.board.tiles[to_i].location in self.board.tiles[to_i].castling_locations:
					self.castle_move_rook()
			
			if self.board.tiles[to_i].occupant.name == 'Pawn':
				self.board.tiles[to_i].isFirstMove = False
				if to_loc in self.board.tiles[to_i].occupant.promote_list:
					self.promote_piece(to_loc)

			self.turn_count = self.turn_count + 1 if self.turn=='black' else self.turn_count
			self.turn = 'black' if self.turn == 'white' else 'white'
						
			
	def isMoveValid(self, from_loc: str, to_loc: str) -> bool:
		from_i = (ord(from_loc[0]) - 97) + (int(from_loc[1]) - 1) * 8
		to_i = (ord(to_loc[0]) - 97) + (int(to_loc[1]) - 1) * 8

		if not self.board.tiles[from_i].occupant:
			print(f'Invalid move, no piece to move at {from_loc}')
			return False
		
		if not self.board.tiles[from_i].occupant.color == self.turn:
			print('Invalid move, should only move white pieces.')
			return False
	
		pieces = [x.occupant for x in self.board.tiles if not x.occupant is None]
		valid_moves = self.board.tiles[from_i].occupant.show_moves(pieces)
		if self.board.tiles[from_i].occupant.name == 'King':
			valid_moves = [x for x in valid_moves if not self.isCheck(x, self.board.tiles)]
			valid_moves = valid_moves + self.board.tiles[from_i].occupant.name.show_castling()

		if not to_loc in valid_moves:
			print(f'Invalid move, {self.board.tiles[from_i].occupant.name} cannot move to {to_loc}')
			return False
		
		return True

	def capture_piece(self, from_loc, to_loc) -> None:
		history = self.add_history(from_loc, to_loc, state='capture')
		print(history)
		self.board.remove_piece(to_loc)
		self.board.move_piece(from_loc, to_loc)
		self.isCheck(to_loc, self.board.tiles)

	def move_piece(self, from_loc, to_loc) -> None:
		history = self.add_history(from_loc, to_loc, state='move')
		print(history)
		self.board.move_piece(from_loc, to_loc)
		self.isCheck(to_loc, self.board.tiles)

	def promote_piece(self, loc: str) -> None:
		choose = True
		while choose:
			promote = input('Promote pawn to:')
			match promote.lower():
				case 'rook':
					choose = False
					piece = Rook(self.turn)
				case 'knight':
					choose = False
					piece = Knight(self.turn)
				case 'bishop':
					choose = False
					piece = Bishop(self.turn)
				case 'queen':
					choose = False
					piece = Queen(self.turn)
				case _:
		
					print('Invalid piece name.')
		self.board.remove_piece(loc)
		self.board.add_piece(piece, loc)
		history = self.add_history(None, loc, state='promote')
		print(history)
	
	def castle_move_rook(self) -> None:
		...

	def isCheck(self, king_loc: str, pieces: list) -> bool:
		...
		

	def add_history(self, from_loc: str, to_loc: str, state: str) -> str:
		if from_loc:
			from_i = (ord(from_loc[0]) - 97) + (int(from_loc[1]) - 1) * 8
		if to_loc:
			to_i = (ord(to_loc[0]) - 97) + (int(to_loc[1]) - 1) * 8
		
		match state:
			case 'move':
				message = f'{self.turn.capitalize()} {self.board.tiles[from_i].occupant.name} moved from {from_loc} to {to_loc}'
				self.history.append((
					self.turn_count,
					self.turn,
					state,
					(from_loc, to_loc),
					message
				))
			case 'capture':
				message = f'{self.turn.capitalize()} {self.board.tiles[from_i].occupant.name} from {from_loc} captures {self.board.tiles[to_i].occupant.name} at {to_loc}'
				self.history.append((
					self.turn_count,
					self.turn,
					state,
					(from_loc, to_loc, self.board.tiles[to_i].occupant.name),
					message
				))
			case 'promote':
				message = f'{self.turn.capitalize()} Pawn promoted to {self.board.tiles[to_i].occupant.name} at {to_loc}'
				self.history.append((
					self.turn_count,
					self.turn,
					state,
					(from_loc, to_loc, self.board.tiles[to_i].occupant.name),
					message
				))
			
			case 'castle':
				pass

		return message