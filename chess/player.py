from chess.pieces import *

class Player(object):
	def __init__(self, color: str, player_id: str):
		self.id = player_id
		self.color = color
		self.pieces = self.initialize_pieces()

	def __repr__(self):
		return f'<Player {self.id}: {self.color}>'

	def initialize_pieces(self) -> list:
		pieces = {}
		for i in range(0,8):
			if not 'pawn' in pieces.keys():
				pieces['pawn'] = []
			pieces['pawn'].append(Pawn(self.color))

			if i < 2:
				if not 'rook' in pieces.keys():
					pieces['rook'] = []
				pieces['rook'].append(Rook(self.color))

				if not 'knight' in pieces.keys():
					pieces['knight'] = []
				pieces['knight'].append(Knight(self.color))

				if not 'bishop' in pieces.keys():
					pieces['bishop'] = []
				pieces['bishop'].append(Bishop(self.color))

		pieces['king'] = [King(self.color)]
		pieces['queen'] = [Queen(self.color)]

		return pieces

	