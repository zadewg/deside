import functools
import numpy as np
from scipy.interpolate import interp1d


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
class hyst: #make this class object oriented


	"""
	Aaight fellas, meaningful docstring is it? I've just had a mare night, some massive flying circus geezer came running out the bushes at me,
	God knows why. Anyways, I've lamped him, he's gone flying now... I think I might have killed him.
	"""


	def __init__(self, y, MA, nth, uth, lth):
		ENV = self._env(y)
		self.q_u = ENV[0]
		self.q_l = ENV[1]

		out = self._threshold(y, MA, nth=3, uth=60, lth=10)
		self.th_his = out[0]
		self.th_los = out[1]
		self.offset = out[2] 	
	
		self.hysts = []
		for i in range(0, nth):
			self.hysts.append(self._hystheresis(y, self.th_los[i], self.th_his[i]))


	def _env(self, y): 
		try:  
			y.ndim; 
		except: 
			y = np.array(y)
	
		q_u, q_l = np.zeros(y.shape), np.zeros(y.shape)
	
		u_x = [0,]
		u_y = [y[0],]
		l_x = [0,]
		l_y = [y[0],]
	
		for k in range(1,len(y)-1):
			if (np.sign(y[k]-y[k-1])==1) and (np.sign(y[k]-y[k+1])==1):
				u_x.append(k)
				u_y.append(y[k])
		
			if (np.sign(y[k]-y[k-1])==-1) and ((np.sign(y[k]-y[k+1]))==-1):
				l_x.append(k)
				l_y.append(y[k])
		
		u_x.append(len(y)-1)
		u_y.append(y[-1])
		l_x.append(len(y)-1)
		l_y.append(y[-1])

		#Fit suitable models to the data. cubic splines, similar to the MATLAB example.
		u_p = interp1d(u_x,u_y, kind = 'cubic',bounds_error = False, fill_value=0.0)
		l_p = interp1d(l_x,l_y,kind = 'cubic',bounds_error = False, fill_value=0.0)
		
		for k in range(0, len(y)):
			q_u[k] = u_p(k)
			q_l[k] = l_p(k)
			
		return q_u, q_l
	

	def _threshold(self, y, ma, nth=3, uth=60, lth=10): #number of triggers, max/min th (%)
		
		""" Y points, Moving Average, number of thresholds, maximum th, minimum th (%)"""
	
		utrigs, ltrigs = [], []
	
		#[1:-1] because lateral boundaries are not representative
		ma = (ma[1:-1]).mean() 
		uenv = (self.q_u[1:-1]).mean() 
		lenv = (self.q_l[1:-1]).mean() 
		
		uth = uth / 100.0
		lth = lth / 100.0
	
		pbase = ma + (ma * lth) # min th_lotohi
		nbase = ma - (ma * lth) # min th_hitolo
	
		avamp = (((uenv - ma) + (ma - lenv)) / 2.0)
		offset = ma - (avamp / 2.0)
	
		pbound = ma + (avamp * uth) #max th_lotohi
		nbound = ma + (avamp * uth) #max th_hitolo
	
		wr = (pbound - pbase) / float(nth)

		for i in range(0, nth):
			utrigs.append(pbase + (wr * i))
			ltrigs.append(nbase - (wr * i))		
	
		return utrigs, ltrigs, offset
					

	def _hystheresis(self, y, th_lo, th_hi, initial = False):
	
		#    y : Numpy Array
		#        Series to apply hysteresis to.
		#    th_lo : float or int
		#        Below this threshold the value of hyst will be False (0).
		#    th_hi : float or int
		#        Above this threshold the value of hyst will be True (1).
	
		try:  
			y.ndim; 
		except: 
			y = np.array(y)

		if th_lo > th_hi: # If thresholds are reversed, x must be reversed as well
			y = y[::-1]
			th_lo, th_hi = th_hi, th_lo
			rev = True
		else:
			rev = False

		hi = y >= th_hi
		lo_or_hi = (y <= th_lo) | hi
	
		ind = np.nonzero(lo_or_hi)[0] 

		if not ind.size:  # prevent index error if ind is empty
			y_hyst = np.zeros_like(y, dtype=bool) | initial
		else:
			cnt = np.cumsum(lo_or_hi)  # from 0 to len(x)
			y_hyst = np.where(cnt, hi[ind[cnt-1]], initial)

		if rev:
			y_hyst = y_hyst[::-1]
		return y_hyst

