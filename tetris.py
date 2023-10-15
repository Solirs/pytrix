import time
import curses
import random

import sys
import copy
import os

def check_oob(x,y,board):
	return x > len(board[0])-1 or x < 0 or y > len(board)-1 or y<0

class Piece():
	def __init__(self):
		self.form  =0
		self.colour = 1
		self.coords = []
		self.type = ""
		
	def wipe(self, board, coords=None):
		if not coords:
			coords = self.coords
			
		for a, b in coords:
			if (a,b) not in self.coords:
				board[a][b] = 0		
			
		return board
		
	def down(self, board):
		
		index = 0
		cords = list(self.coords)
		board = list(board)
		for y, x in cords:
			if len(board) <= y+1 or (board[y+1][x] > 0 and (y+1,x) not in cords):
				return False
			
		for y,x in cords:
			board[y+1][x] = self.colour
			self.coords[index] = (y+1, x)
			index += 1
			
		board = self.wipe(board, cords)
			
		
		return board
		
	def right(self, board):
		
		index = 0
		cords = list(self.coords)
		brd = list(board)
		
		for y,x in cords:
			if len(board[0]) <= x+1 or (board[y][x+1] > 0 and (y,x+1) not in cords):
				return False			
		for y, x in cords:
			
			brd[y][x+1] =  self.colour
			self.coords[index] = (y, x+1)
			index += 1
		
		return self.wipe(brd, cords)	
		
	def left(self, board):
		
		index = 0
		cords = list(self.coords)
		board = list(board)
		
		for y,x in cords:
			if x <= 0 or (board[y][x-1] > 0 and (y,x-1) not in cords):
				return False	
				
		for y, x in cords:
			
			board[y][x-1] =  self.colour
			self.coords[index] = (y, x-1)
			index += 1
		board = self.wipe(board, cords)
		
		return board		
		
	def rotate(self, board, clock=1):

		brd = copy.deepcopy(board)
		y, x = self.coords[0]

		
		cords = list(self.coords)
		self.coords = [self.coords[0]]
		
		
		for i, j in cords[1::]:
			if clock == -1:
				dstx = x+i-y
				dsty = y+(x-j)
			else:
				dstx = x+y-i
				dsty = y+j-x
				
			if check_oob(dstx, dsty, board):
				self.coords = cords
					
				return brd
			
			if brd[dsty][dstx] != 0 and (dsty,dstx) not in cords:
				self.coords = cords
					
				return brd				
				
			board[dsty][dstx] = self.colour
			self.coords.append((dsty, dstx))			
	


								
		for a ,b in cords:
			if (a,b) not in self.coords:
				board[a][b] = 0								
		return board
				

			
class Line(Piece):
	def __init__(self):
		super(Line, self).__init__()
		
	def spawn(self, x, y, board):

		self.colour = 1
		board = self.wipe(board)
		brd = copy.deepcopy(board)
		crds = list(self.coords)
		
		self.coords = [(y, x), (y, x-2), (y, x-1), (y, x+1)]
		for a,b in self.coords:
			if check_oob(b,a,board) or (brd[a][b] > 0 and (a,b) not in crds):
				sys.exit()
				self.coords = crds
				return brd
		board[y][x] = self.colour
		board[y][x-1] = self.colour
		board[y][x-2] = self.colour
		board[y][x+1] = self.colour
		

		self.form = 0
		
		return board
		
	def rotate(self, board, clock=1):
			
			
			brd = copy.deepcopy(board)
			cords = list(self.coords)
			
			y, x = self.coords[0]
			cords.pop(0)
			
			if self.form == 0:
			
				if check_oob(x,y-1,board):
					return brd
				board[y - 1][x] = self.colour
				board[y + 1][x] = self.colour
				board[y + 2][x] = self.colour
				
				
				self.coords = [(y, x), (y-1, x), (y+1, x), (y+2, x)]
				self.form = 1
				
			
			else:
				board = self.spawn(x, y, board)
				
		
			self.wipe(board, cords)
			self.form = 1

			
			return board
			
	
			
				
class Square(Piece):
	def __init__(self):
		super(Square, self).__init__()
		
	def spawn(self, x, y, board):
		self.colour = 2
		board = self.wipe(board)
		
		board[y][x] = self.colour
		board[y][x-1] = self.colour
		board[y+1][x] = self.colour
		board[y+1][x-1] = self.colour
		
		self.coords = [(y, x), (y, x-1), (y+1, x), (y+1, x-1)]

		
		return board
	def rotate(self, board, clock=1):
		return board
		
		
class T_tetromino(Piece):
	def __init__(self):
		super(T_tetromino, self).__init__()
		self.colour = 3
		
	def spawn(self, x, y, board):
		

		board = self.wipe(board)
		
		board[y][x] = self.colour
		board[y][x-1] = self.colour
		board[y+1][x] = self.colour
		board[y][x+1] = self.colour
		
		self.coords = [(y, x), (y, x-1), (y+1, x), (y, x+1)]

		
		return board	



class L_tetromino(Piece):
	def __init__(self):
		super(L_tetromino, self).__init__()
		self.colour = 4
		
	def spawn(self, x, y, board):

		board = self.wipe(board)
		
		board[y][x] = self.colour 
		board[y][x-1] = self.colour 
		board[y+1][x-1] = self.colour 
		board[y][x+1] = self.colour 
		
		self.coords = [(y, x), (y, x-1), (y+1, x-1), (y, x+1)]

		
		return board	

class J_tetromino(Piece):
	def __init__(self):
		super(J_tetromino, self).__init__()
		self.colour = 5
		
	def spawn(self, x, y, board):

		board = self.wipe(board)
		
		board[y][x] = self.colour 
		board[y][x+1] = self.colour 
		board[y+1][x+1] = self.colour 
		board[y][x-1] = self.colour 
		
		self.coords = [(y, x), (y, x+1), (y+1, x+1), (y, x-1)]

		
		return board	


class Z_piece(Piece):
	def __init__(self):
		super(Z_piece, self).__init__()
		self.colour = 6
		
	def spawn(self, x, y, board):

		crds = list(self.coords)
		brd = copy.deepcopy(board)
		
		self.coords = [(y, x), (y, x-1), (y+1, x), (y+1, x+1)]
		
		for a,b in self.coords:
			if check_oob(b,a,board) or (brd[a][b] != 0 and (a,b) not in crds):
				self.coords = crds
				return brd
				
		board[y][x] = self.colour 
		board[y][x-1] = self.colour 
		board[y+1][x] = self.colour 
		board[y+1][x+1] = self.colour 
		

		self.form = 0
		
		board = self.wipe(board, crds)
		
		return board	

	def rotate(self, board, clock=1):
		if self.form == 0:
			return super().rotate(board)
		elif self.form == 1:
			y,x = self.coords[0]
			return self.spawn(x,y,board)
		
class S_piece(Piece):
	def __init__(self):
		super(S_piece, self).__init__()
		self.colour = 7
	def spawn(self, x, y, board):


		crds = list(self.coords)
		brd = copy.deepcopy(board)
		self.coords = [(y, x), (y, x+1), (y+1, x), (y+1, x-1)]
		
		for a,b in self.coords:
			if check_oob(b,a,brd) or (brd[a][b] !=0 and (a,b) not in crds):
				self.coords = crds
				
				return brd				
		
		board[y][x] = self.colour 
		board[y][x+1] = self.colour 
		board[y+1][x] = self.colour 
		board[y+1][x-1] = self.colour 
		

		
		self.form = 0
		
		board = self.wipe(board, crds)
		
		return board	

	def rotate(self, board, clock=1):
		if self.form == 0:
			return super().rotate(board)
		elif self.form == 1:
			y,x = self.coords[0]
			return self.spawn(x,y,board)

class Game():
	def __init__(self):
		self.tick = 0
		self.screen = curses.initscr()
		curses.noecho()
		curses.cbreak()
		
		self.screen.nodelay(1)
		self.screen.keypad(True)
		
		
		self.piecelist = [J_tetromino, Line, T_tetromino, L_tetromino, Z_piece, S_piece, Square]
		
		self.bag = []
		
		self.nextpieces = []
		
		self.currentpiece = None
		self.board = []
		for i in range(20):
			self.board.append([0,0,0,0,0,0,0,0,0,0])
		self.score = 0
		self.level = 1
		self.levelprogression = 0
		self.gameend = False
		self.pause = False
		
		
	def is_row_full(self, row):
		for i in row:
			if not i:
				return False
		return True
		
	
	def check_game_status(self):
		
		if self.board[0][5] != 0:
			return False
		
		
		
		for i in self.board:
			if self.is_row_full(i):
				self.board.pop(self.board.index(i))
				self.board.insert(0, [0,0,0,0,0,0,0,0,0,0])

				self.levelprogression += 1
				self.score += 40*self.level
				if self.levelprogression == 10:
					self.level += 1
					self.levelprogression = 0
									
				
		return True
		
	def update_screen(self):
		updt = ""
		line = 1
		pos = 0
		maxx= self.screen.getmaxyx()[1]
		maxy= self.screen.getmaxyx()[0]
		
		for i in range(len("tetris.py")):
			self.screen.addstr(0,i, "tetris.py"[i], curses.color_pair(i+10))
			
		
		
		for i in self.board:

			self.screen.addstr(line,maxx//2-11+pos, "|",  curses.color_pair(8))			
			for x in i:
				
				if x == 0:
					self.screen.addstr(line,maxx//2-10+pos, " ")
					self.screen.addstr(line,maxx//2-10+pos+1, " ")
					

				elif x == -1:
					self.screen.addstr(line,maxx//2-10+pos, "XX")
					
				else:
					self.screen.addstr(line,maxx//2-10+pos, u'\u3042'.encode('utf-8'), curses.color_pair(x))
					
					
				pos += 2
					
				
			self.screen.addstr(line,maxx//2-10+pos, "|\n", curses.color_pair(8))			
			pos = 0
			
			line+= 1
		
			
		self.screen.addstr(6, maxx//2+15, f"Score: {self.score}")
		self.screen.addstr(7, maxx//2+15, f"Level: {self.level}")		
		self.screen.addstr(8, maxx//2+15, f"Next: ")
			
			
		renderboard = []
		for i in range(3):
			renderboard.append([0,0,0,0])
						
						
		if not self.bag:
			self.bag = random.sample(self.piecelist, len(self.piecelist))
						
		piece=self.bag[-1]

		if self.bag:
			piece().spawn(2,1, renderboard)
				


		self.screen.redrawln(9, 2)

		for i in range(len(renderboard)):
			ps = 0
			for j in range(len(renderboard[0])):
				
				if renderboard[i][j] > 0:					
					self.screen.addstr(9 + i, maxx//2+15 + j + ps, u'\u3042'.encode('utf-8'), curses.color_pair(renderboard[i][j]))
				else:
					self.screen.addstr(9 + i, maxx//2+15 + j+ps+2, "  ")
					ps += 1
						
						
					
		
		
		if self.pause:
			self.screen.addstr(10, maxx//2-10+6, "[PAUSED]")
			
		self.screen.addstr(line,maxx//2-11+pos, "----------------------",  curses.color_pair(8))			
		self.screen.refresh()
			
		
	
	def bagnext(self):
		if not self.bag:
			self.bag = random.sample(self.piecelist, len(self.piecelist))
			
		ret = self.bag[-1]
		self.bag.pop()
		return ret
					
					
	def gameloop(self, m):

		
		curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_CYAN)		
		curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)		
		curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)		
		curses.init_pair(4, curses.COLOR_RED, curses.COLOR_RED)	
		curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLUE)		
		curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_GREEN)		
		curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_WHITE)		
		curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_WHITE)
		curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_BLACK)
		
		
		# For title colours
		curses.init_pair(10, curses.COLOR_CYAN, curses.COLOR_BLACK)		
		curses.init_pair(11, curses.COLOR_YELLOW, curses.COLOR_BLACK)		
		curses.init_pair(12, curses.COLOR_MAGENTA, curses.COLOR_BLACK)		
		curses.init_pair(13, curses.COLOR_RED, curses.COLOR_BLACK)	
		curses.init_pair(14, curses.COLOR_BLUE, curses.COLOR_BLACK)		
		curses.init_pair(15, curses.COLOR_GREEN, curses.COLOR_BLACK)		
		curses.init_pair(16, curses.COLOR_CYAN, curses.COLOR_BLACK)		
		curses.init_pair(17, curses.COLOR_YELLOW, curses.COLOR_BLACK)	
		curses.init_pair(18, curses.COLOR_MAGENTA, curses.COLOR_BLACK)		
			
		self.screen = m
		
		while not self.gameend:
			time.sleep(0.05/(self.level/1.5))
			if self.pause:
				key = self.screen.getch()
				if key == 27:
					self.pause = False
				else:
					continue
			self.tick += 1
			

			key = 0
			for i in range(len(self.board)):
				for j in range(len(self.board[i])):
					if self.board[i][j] == -1:
						self.board[i][j] = 0						
						
			
			if not self.currentpiece:
				c = self.check_game_status()
				if not c:
					self.quit()
					return					
				
				piece = self.bagnext()()
				self.board = piece.spawn(5, 0, self.board)
				self.currentpiece = piece
				self.tick = 0

				
				
			else:
				key = self.screen.getch()

				if key == curses.KEY_RIGHT:
					
					res = self.currentpiece.right(self.board)
					self.board = res if res else self.board
				elif key == curses.KEY_LEFT:
					res = self.currentpiece.left(self.board)
					self.board = res if res else self.board
					
				elif key == curses.KEY_DOWN:
					res = self.currentpiece.down(self.board)
					if res:
						self.board = res
					else:
						self.currentpiece = None
						
				
				elif key == curses.KEY_UP:
					self.board = self.currentpiece.rotate(self.board, clock=1)	
				elif key == 122:
					# Z 
					self.board = self.currentpiece.rotate(self.board, clock=-1)	
										
				elif key ==	27:
					# Escape
					self.pause = True
				
				elif key == 32:
					# Space
					res = self.currentpiece.down(self.board)
					while res:
						res = self.currentpiece.down(res)
						self.board = res if res else self.board
					self.currentpiece = None			
					
				if self.currentpiece:
					# Ghost pieces
					cords = copy.deepcopy(self.currentpiece.coords)
					notdone = True
					
					while notdone:
						tempcords = copy.deepcopy(cords)
						
						for y,x in cords:
							if (check_oob(x,y+1,self.board) or self.board[y+1][x] != 0) and (y+1,x) not in cords:
								notdone = False
							else:
								tempcords[tempcords.index((y,x))] = (y+1,x)
						if notdone:
							cords = copy.deepcopy(tempcords)
					for y,x in cords:
						if self.board[y][x] == 0:
							self.board[y][x] = -1
									

					
				if self.tick == 6 and self.currentpiece and not self.pause:
					res = self.currentpiece.down(self.board)
					if res:
						self.board = res
					else:

						res = self.currentpiece.down(self.board)
						if res:
							self.board = res
						else:

							
							self.currentpiece = None	
				m.erase()
				self.update_screen()

					

			if self.tick == 6:
				self.tick = 0
				
	def quit(self):
		
		pass


if __name__ == "__main__":
	os.environ.setdefault('ESCDELAY', '25')
	
	
	scr = curses.initscr()
	curses.curs_set(0)
	
	curses.start_color()
	curses.noecho()
	curses.cbreak()
	try:
		scr.keypad(True)
		g = Game()
		g.gameloop(scr)
	finally:
		curses.nocbreak()
		scr.keypad(False)
		curses.echo()		
		curses.endwin()	
	print("You lost noob")
