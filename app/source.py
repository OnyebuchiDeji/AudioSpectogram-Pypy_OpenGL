import time
import math
import pyaudio
import librosa
import numpy as np
from utils import logger
from config import (
	SAMPLE_RATE, BUFFER_SIZE,
	WINDOW_SIZE, HOP_SIZE
	)

class Source:

	def __init__(self, *args, **kwargs):
		self.audio = pyaudio.PyAudio()
		self.complete = False
		self.data = []
		self.index = 0
		self.total = 0
		self.init(*args, **kwargs)

	def init(*args, **kwargs):
		raise NotImplementedError("source.init")

	def callback(self, data, frame_count, time_indo, status):
		raise NotImplementedError("source.callback")

	def get(self):
		if self.index + WINDOW_SIZE > self.total:
			return None
		a = self.index
		b = self.index + WINDOW_SIZE
		data = self.data[a:b]
		self.index = a + HOP_SIZE
		return np.array(data)

	def available(self):
		"""Number of windows available"""
		samples = self.total - self.index
		samples -= WINDOW_SIZE
		available = math.ceil(samples/HOP_SIZE)
		return max(0, available)

	def release(self):
		self.stream.close()
		self.audio.terminate()

class File(Source):
	"""
	Audio input from file
	"""
	def init(self, filename):
		self.data, _ = librosa.load(filename, sr=SAMPLE_RATE)
		self.stream = self.audio.open(
			format=pyaudio.paFloat32,
			channels=1,
			rate=SAMPLE_RATE,
			output=True,
			frames_per_buffer=BUFFER_SIZE,
			stream_callback=self.callback
			)

	def callback(self, in_data, frame_count, time_info, status):
		a = self.total
		b = self.total + BUFFER_SIZE
		data = self.data[a:b]
		self.total = b
		if self.total >= len(self.data):
			self.complete = True
		return data, pyaudio.paContinue
	

class Microphone(Source):
	"""
	Audio input from mic
	"""
	
	def init(self):
		#	Create audio stream
		self.stream = self.audio.open(
			format=pyaudio.paFloat32,
			channels=1,
			rate=SAMPLE_RATE,
			input=True,
			frames_per_buffer=BUFFER_SIZE,
			stream_callback=self.callback
			)

	def callback(self, data, frame_count, time_info, status):
		data = np.frombuffer(data, dtype=np.float32)
		data = data.tolist()
		self.data.extend(data)
		self.total = len(self.data)
		return None, pyaudio.paContinue


if __name__ == "__main__":
	filename = "./res/scooby.wav"

	source = File(filename)

	#	because the make file makes this app
	#	run on a separate thread, the below is needed
	#	to wait for five seconds until the time terminates
	#	which in turn allows the thread to be terminated  
	time.sleep(5)

	#	To test, run `make source`