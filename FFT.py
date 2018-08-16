import numpy as np
import scipy
import matplotlib.pyplot as plt

np.random.seed(1234)

time_step = 0.02
period = 5.
time_vec = np.arange(0, 20, time_step)

signal = (np.sin(2 * np.pi / period * time_vec) + 0.5 * np.random.randn(time_vec.size))


class Fourier:

	def __init__(self, *args, **kwargs):
		pass


	def _fft(self, signal):
		fft = scipy.fft(signal)
		return fft


	def _ifft(self, signal):
		ifft = scipy.ifft(signal)
		return ifft


	def normalize(self, sig1, sig2, *args):

	#	sig1 = sig1/max(sig1)
	#	sig2 = sig2/max(sig2)
	#	return sig1, sig2

		signals = []
		signals.append(sig1, sig2, args)

		for sig in signals:
			sig = sig/max(sig)

		return signals

	def calc_err(self, sig1, sig2):
		err = abs(sig1) - abs(sig2)
		return err


	def degrid(self, sig, freq=[50]): #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.iirnotch.html
	
		sig_fft = self._fft(sig)	                # The FFT of the signal.

		bp = sig_fft[:]
		for i in range(len(bp)):                        # Frequency cancelation.
			for f in freq:
	
				if f == 'europe':
					f = 50
				if f == 'america':
					f = 60
	
				if i == f:
					bp[i] = 0
	
		filtered = self._ifft(bp)                       # Band filtered out.
		return filtered

# Required input defintions are as follows;
# time:   Time between samples
# band:   The bandwidth around the centerline freqency that you wish to filter
# freq:   The centerline frequency to be filtered
# ripple: The maximum passband ripple that is allowed in db
# order:  The filter order.  For FIR notch filters this is best set to 2 or 3,
#         IIR filters are best suited for high values of order.  This algorithm
#         is hard coded to FIR filters
# filter_type: 'butter', 'bessel', 'cheby1', 'cheby2', 'ellip'
# data:         the data to be filtered
#def Implement_Notch_Filter(time, band, freq, ripple, order, filter_type, data):
#    from scipy.signal import iirfilter
#    fs   = 1/time
#    nyq  = fs/2.0
#    low  = freq - band/2.0
#    high = freq + band/2.0
#    low  = low/nyq
#    high = high/nyq
#    b, a = iirfilter(order, [low, high], rp=ripple, btype='bandstop',
#                     analog=False, ftype=filter_type)
#    filtered_data = lfilter(b, a, data)
#    return filtered_data

	


'''
fourier = Fourier()
out = fourier.degrid(signal)

plt.plot(out, 'r')
plt.show()
'''
