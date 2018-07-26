import matplotlib.pyplot as plt
import numpy as np

from DIMENSIONS import SourceData
from FILTERS import NoiseWork
from THRESHOLD import hyst
#from FFT import fft, inverse  #FFT USED TO FILTER OUT POWER SUPPLY SINE WAVES 50MHZ FOR ELECTRICAL WIRING IN EUROPE, PLUS COMPUTER POWER SUPPLY
#from DECODERS import * #IF CANT FEED BINARY TO RIPYL, USE DICTIONARY ATTACK FROM RIPYL ALFABET. CHECHK CHECKSUMS TOO.

#ADD ASYNCRONOUS SAMPLE RADTE CONVERION (GRIDING?) FOR CHEAP OSCILOSCOPES # https://dsp.stackexchange.com/questions/8488/what-is-an-algorithm-to-re-sample-from-a-variable-rate-to-a-fixed-rate

#ADD PLOTING COUNTER AS FOR UNASYNC, FFT, TO CUSTOMIZE PLOTTING WINDOWS
#ADD COLORS

x = np.linspace(0,20, 1000)
yy = np.sin(x) + 4


#	np.random.seed(1234)
#
#	time_step = 0.02
#	period = 5.
#
#	time_vec = np.arange(0, 20, time_step)
#	sig = (np.sin(2 * np.pi / period * time_vec) + 0.5 * np.random.randn(time_vec.size))
#
#	plt.figure(figsize=(6, 5))
#	plt.plot(time_vec, sig, label='Original signal')



plt.figure('Demo')  

Y = SourceData(X=x, Y=yy).Ypoints

plt.subplot(231)
plt.title('Original')
plt.plot(Y)


n = NoiseWork(Y).AN

plt.subplot(232)
plt.title('Received')
plt.plot(n)


ma = NoiseWork(n, window_len=100).MA

plt.subplot(233)
plt.title('Denoised')
plt.plot(ma)


denoised= ma
q_u = hyst(denoised, ma, 3, 60, 10).q_u
q_l = hyst(denoised, ma, 3, 60, 10).q_l

plt.subplot(234)
plt.title('Treshold Calc.')
plt.plot(ma);plt.hold(True);plt.plot(q_u,'r');plt.plot(q_l,'g')


offset = hyst(Y, ma, 3, 60, 10).offset
hysts = hyst(Y, ma, 3, 60, 10).hysts

plt.subplot(235)
plt.title('Hystheresis')
plt.plot(offset+hysts[0], 'y');plt.hold(True);plt.plot(offset+hysts[1], 'orange');plt.plot(offset+hysts[2], 'black')

plt.subplot(236)
plt.title('Digital 1')
plt.plot(hysts[0], 'o', color='C1')

plt.tight_layout(True)
plt.gray()
plt.show()
