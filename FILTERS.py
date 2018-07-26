import functools
import random
import numpy as np
from scipy.signal import lfilter, savgol_filter


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
class NoiseWork():
	

	"""
	Feed Y values only. 'Noise Reduction' (Function smoothing):  Finite Impulse Response, Moving Average, Savitzky-Golay. 
	Noise Generation: <AN> function adds given noise in array form. Else, it wil generate random noise. (Noise array must be exactly same length as data array)
	Moving Average <MA> Takes (Optional) window length and type arguments. Window vector must be smaller than input vector.
	Supported window types: flat, hanning, hammnig, barlett, blackman. Default: 3, flat.
	ALL ARGUMENTS ARE FED TO CLASS CALL; METHOD CALLS TAKE NO ARGUMENTS:
	
	y = NoiseWork(y, window_len=11, window='hannning').MA    #This is correct
	y = NoiseWork().MA(y, window_len=11, window='hannning')  #This is not correct
	"""


	def __init__(self, data, *arg, **kwargs):
		self.FIR = self._fir(data)
		self.MA = self._ma(data, **kwargs)
		self.SG = self._sg(data)
		if arg is not None:
			self.AN = self._an(data, *arg)
		else:
			self.AN = self._an(data)


	def _an(self, data, *arg):
		#if arg is not None and len(arg[0]) == len(y):
		#	y = [sum(x) for x in zip(y, arg)] # delete []?
		#else:
		#	y += (np.random.normal(0, 1, y.shape))/5 #+ int = + noise
		#return y
		data += (np.random.normal(0, 1, data.shape))/5 #+ int = + noise
		return data
		

	def _fir(self, data): 
		n = 1000;
		a, b = 1, [1.0 / n] * n  # the larger n is, the smoother curve will be   {15}
		data = lfilter(b, a, data)
		return data


	def _ma(self, data, window_len=11, window='hanning'): 
		try:  
			data.ndim; 
		except:
			data = np.array(data)

		s = np.r_[data[window_len-1:0:-1], data, data[-2:-window_len-1:-1]]
		if window == 'flat': 
			w = np.ones(window_len, 'd')
		else:
			w = eval('np.' + window + '(window_len)')
		
		data = np.convolve(w/w.sum(), data, mode='valid')
		return data[int(window_len/2-1):int(-(window_len/2)-1)]
	

	def _mm(self, data, window_len=11, window='hanning'): #less vulnerable to single spikes. MOVING MEDIAN ·calulate stdev in auto mode to choose this one over MA
		pass


	def _sg(self, data): 
		data = savgol_filter(data, 101, 2)
		return data


