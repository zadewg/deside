class Sync:
	
	def _init__(self, x, y):
		self.x = x
		self.y = y

	def _isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
		return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

	def check(self, x):
	
		i, f = 0
		while i < (len(x) - 1):
			if i > 1:
				a = (float(times[i]) - float(times[i - 1]))
				b = (float(times[i + 1]) - float(times[i]))
				if not (self.isclose(a, b)):
					f += 1
					
			i += 1
		if f:
			return 'True'
		else:
			return 'False'

	def resample(self, x, y):
		pass
