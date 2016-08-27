# Romain Ducarrouge

''' Looking into Audio Data '''
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav

from scipy.fftpack import fft
import numpy as np

# plotting result from audio files
rate, data = wav.read('data/audio/test(5people).wav')
name = 'test(5people)'

plt.plot(data)
plt.savefig('data/audio/Graph_'+name+'.png')

print('sampling rate = {} Hz, length = {} samples, channels = {}'.format(rate, *data.shape))


''' performing Fast Fourier Transform
fft_out = fft(data)

plt.plot(data, np.abs(fft_out))
plt.savefig('data/audio/FFT_'+name+'.png')
'''

plt.plot(data)
plt.savefig('data/audio/Graph_Channels.png')



# https://github.com/BlackWolf/Connichiwa/issues/44

# Issues with memory due to files too large