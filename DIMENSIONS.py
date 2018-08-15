import functools
import numpy as np


def exception_handler(f): 
	@functools.wraps(f)
	def func(*args, **kwargs): 
		try:  
			return f(*args, **kwargs)

		except Exception as e: 
			print('Caught an exception in', f.__name__)
			try: 
				print("\n{}".format(eval(f.__name__).__doc__))
			except: 
				pass
			print(e)
			raise SystemExit
	return func


@exception_handler
class SourceData:


	"""
	Feed collected data here, no matter dimension.
	Arg keys: Matrix, X, Y, CSV.
	Returns: Matrix, Xpoints, Ypoints.
	
	Example: y = SourceData(CSV='data.csv').Ypoints
	"""


	def __init__(self, **kwargs): 
		if kwargs is not None:
			for key, value in kwargs.items():
				if key == 'Matrix':
					self.Xpoints = self._genonedee(value)[0]
					self.Ypoints = self._genonedee(value)[1]
					self.Matrix = value
				elif key == 'X':
					self.Xpoints = value
				elif key == 'Y':
					self.Ypoints = value
				elif key == 'CSV':
					self.Xpoints = self._genonedee(self._fileinput(value))[0]
					self.Ypoints = self._genonedee(self._fileinput(value))[1]
					self.Matrix = self._fileinput(value)
							
			if len(locals()) > 1:
				self.Matrix = self._gentwodee(self.Xpoints, self.Ypoints)
		#else: raise Exception

	def parse_csv(self, inputfile):  
		matrix = []
		f = open(inputfile, "r")
		lines = f.read().split("\n") 
		for line in lines:
			if line != "": # add other needed checks to skip titles
				array = line.split(",")
				matrix.append(array)
		return matrix

	def _fileinput(self, FILE):
		return self.parse_csv(FILE)

	def _genonedee(self, matrix):
		x, y = [], []
		for i in matrix:
			x.append((i)[0])
			y.append((i)[1])
		return x, y
	
	def _gentwodee(self, Xpoints, Ypoints):
		w, h = 2, len(Xpoints)
		matrix = [[0 for x in range(w)] for y in range(h)]
		for i in range(0,h):
			matrix[i][0] = Xpoints[i]
			matrix[i][1] = Ypoints[i]		
		return matrix	



			if len(locals()) > 1:
				self.Matrix = self._gentwodee(self.Xpoints, self.Ypoints)
		#else: raise Exception

	def parse_csv(inputfile):  
		matrix = []
		f = open(inputfile, "r")
		lines = f.read().split("\n") 
		for line in lines:
			if line != "": # add other needed checks to skip titles
				array = line.split(",")
				matrix.append(array)
		return matrix

	def _fileinput(FILE):
		return parse_csv(FILE)

	def _genonedee(self, matrix):
		x, y = [], []
		for i in matrix:
			x.append((i)[0])
			y.append((i)[1])
		return x, y
	
	def _gentwodee(self, Xpoints, Ypoints):
		w, h = 2, len(Xpoints)
		matrix = [[0 for x in range(w)] for y in range(h)]
		for i in range(0,h):
			matrix[i][0] = Xpoints[i]
			matrix[i][1] = Ypoints[i]		
		return matrix	



