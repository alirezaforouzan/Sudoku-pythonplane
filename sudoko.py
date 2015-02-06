import time
import sys
from random import randint
from random import shuffle

class Sudoku(object):
	"""docstring for SudokuSolver"""
	def __init__(self, board_file_name):
		self.board=[]
		board_file=file(board_file_name,'rb')
		board_line_text=board_file.readline()
		while board_line_text:
			board_line_array=[]
			for num in board_line_text.split(','):
				board_line_array.append(int(num))
			self.board.append(board_line_array)
			board_line_text=board_file.readline()
		self.board_n=int(pow(len(self.board),0.5))
		self.debug=False
		
	def solve(self):
		if self.is_solved():
			return True
		
		point=self.get_unsolved_position();
		options=self.get_options(point);
		
		if (options==[] and not(self.is_solved())):
			return False
		
		for option in options:
			if self.debug:
				print 'Solving point:'+str(point)+' with option:'+str(option)+' from options:'+str(options)
			self.board[point[0]][point[1]]=option
			if not(self.solve()):
				if self.debug:
					print 'Revert the option:'+str(point)+' with option:'+str(option)
				self.board[point[0]][point[1]]=0
			else:
				return True
		if self.debug:
			print 'Evaluated all the options for point:'+str(point)+'. This board can not be solved.'
		return False;
		
	def is_solved(self):
		for row in self.board:
			for num in row:
				if (num==0):
					return False;
		return True;

	def get_unsolved_position(self):
		min_point=None
		min_options=100
		for i in range(0,len(self.board)) :
			for j in range(0,len(self.board)):
				#if (board[i][j]=='x'):
					#return [i,j];
				if (self.board[i][j]==0):
					options=self.get_options([i,j])
					if (len(options)<min_options):
						min_options=len(options);
						min_point=[i,j];
		return min_point

	def get_options(self,point):
		horz_row=self.board[point[0]][:point[1]]+self.board[point[0]][point[1]+1:]
		vert_row=[]
		for i in range(0,len(self.board)):
			if (i!=point[0]):
				vert_row.append(self.board[i][point[1]])
		square=[]
		i_range=range((point[0]/self.board_n)*self.board_n,(point[0]/self.board_n)*self.board_n+self.board_n)
		j_range=range((point[1]/self.board_n)*self.board_n,(point[1]/self.board_n)*self.board_n+self.board_n)
		for i in i_range:
			for j in j_range:
				if i!=point[0] or j!=point[1]:
					square.append(self.board[i][j])


		aggregate=set(horz_row+vert_row+square)
		if ('x' in aggregate):
			aggregate.remove('x')


		options=range(1,self.board_n*self.board_n+1)
		for i in range(1,self.board_n*self.board_n+1):
			if i in aggregate:
				options.remove(i)
		shuffle(options)
		return options

	def print_board(self):
		for row in self.board:
			row_str=''
			for num in row:
				row_str=row_str+str(num)+' '
			print row_str

	def generate_board(self,size):
		#Generate emtpy board
		self.board=[[0 for i in range(0,size)] for j in range(0,size)]
		self.solve()

		#Continue until no point is left
		difficulty=0
		while difficulty<50:
			i=randint(0,size-1)
			j=randint(0,size-1)
			if self.board[i][j]!=0:
				self.board[i][j]=0
				difficulty=self.evaluate_difficculty()
				print difficulty
		#if len(options)>
		#Pick next location and evaluate options. Pick 1 randomly
		self.print_board()

	def evaluate_difficculty(self):
		options_sum=0
		unknown_cells=0
		for i in range(0,len(self.board)):
			for j in range(0,len(self.board)):
				if (self.board[i][j]==0):
					options=self.get_options([i,j])
					options_sum=options_sum+len(options)
					unknown_cells=unknown_cells+1

		return options_sum;#/unknown_cells

if __name__ == "__main__":
	board_name=sys.argv[1]
	print board_name
	sudoku=Sudoku(board_name)
	print 'The initial board is:'
	sudoku.print_board();
	print '----------------------------'
	t1=time.time()
	print 'Start solving the board'
	sudoku.solve()
	t2=time.time()
	print 'Finished solving the board in:'+str(t2-t1)+' seconds'
	print '----------------------------'
	print 'Solved board:'
	sudoku.print_board()
