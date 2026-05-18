"""
	"The Hop Size concept"

	For a given window size --- window size or frame referring to
	a batch of frames from the audio data.

	Rules:
	For every 6 frames (6 fps),
	one is to shift exactly by 1/6 of the distance (stride) when getting
	each consecutive frame data from the audio file

	For every 3 frames (3 fps)
	similarly, shift by 1/3 of the distance (stride) when getting
	each consecutive frame data from teh audio file

"""


from rect import Rect
from ticks import Ticks
from text import Text
from source import File, Microphone
from wave import Wave
from spec import Spec
from window import Window
from config import WINDOW_WIDTH, WINDOW_HEIGHT, HOP_SIZE
from utils import logger


class App(Window):

	def init(self):
		logger.info("Init Called")

		# Set the window caption
		self.setWindowTitle("Audio Wave Spectogram")

		self.speed_factor = 2
		global HOP_SIZE
		if HOP_SIZE == 370:
			HOP_SIZE = int(HOP_SIZE / self.speed_factor)
		self.x_scale = self.speed_factor

		print("Hop Size: ", HOP_SIZE)

		#	audio runs in separate thread due to callback pipeline
		# self.source = File("res/scooby.wav")
		self.source = Microphone()


		self.nodes = []
		#	args: ctx, x, y [top left], width, height
		self.wave = Wave(self.ctx, 0, 0, WINDOW_WIDTH, 180)
		self.nodes.append(self.wave)
		self.spec = Spec(self.ctx, 0, self.wave.h, WINDOW_WIDTH, 455)
		self.nodes.append(self.spec)


		bg_color = (0.06, 0.06, 0.07, 1.0);

		#	Wave-Spec Seperation Line
		self.nodes.append(Rect(self.ctx, 0, self.wave.h, WINDOW_WIDTH, 3, bg_color))

		# 	Time axis background
		self.nodes.append(Rect(self.ctx, 0, 635, WINDOW_WIDTH, 70, bg_color))

		# 	Frequency axis background
		self.nodes.append(Rect(self.ctx, 0, 0, 80, WINDOW_HEIGHT, bg_color))

		#	Ticks

		#	1/(10  * self.x_scale) second intermediary ticks
		self.nodes.append(
			# Ticks(self.ctx, x=81, y=635, w=WINDOW_WIDTH, h=15, color=(0.3, 0.3, 0.4, 1.0), gap=6) # of for when x_scale is 1.0
			Ticks(self.ctx, x=81, y=635, w=WINDOW_WIDTH, h=15, color=(0.3, 0.3, 0.4, 1.0), gap=int(12/self.x_scale))
		)

		#	1 * self.x_scale second ticks
		#	the gap of 60 corresponds to the 60 fps so that there is a tick
		#	every 60 frames/1 second
		self.nodes.append(
			Ticks(self.ctx, x=81, y=635, w=WINDOW_WIDTH, h=25, color=(0.4, 0.4, 0.5, 1.0), gap=int(60 * self.x_scale))
		)

		#	2000 Hz ticks
		#	Total Frequency range: 1146 --- comes from SAMPLE_RATE / WINDOW_SIZE * NO_OF_SPECTRAL_LINES
		#	NO_OF_SPECTRAL_LINES = 513
		#	find how many pixels are between each frequencies
		pixels_per_freq = self.spec.h / 11046
		self.nodes.append(
			Ticks(
				self.ctx,
				x=70, y=self.spec.y + pixels_per_freq * 1046,	#	top frequency mark
				w=10, h=pixels_per_freq * 10000, 			 	# 1046-11046=10000
				color=(0.4, 0.4, 0.5, 1.0), 
				gap=pixels_per_freq * 2000, 				 	#	1 tick every gap of 2000 frequencies
				horizontal=False
			)
		)

		#	Text

		#	Create text render
		text = Text(self.ctx)
		self.nodes.append(text)

		#	Seconds text
		for i in range(1, int(20 / self.x_scale) + 1):
			x = WINDOW_WIDTH - i * 60 * self.x_scale
			text.add(f"{i}s", x, 670, align='center')

		#	Hz Text
		for i in range(6):
			hz = i * 2000
			y = 635 - pixels_per_freq * hz + 4
			text.add(f"{hz}Hz", 62, y, align="right")


	def re_size(self, w, h):
		logger.info(f"Resize Called: {w}, {h}")
		for node in self.nodes:
			node.re_size(w, h)

		# self.wave.re_size(w, h)
		# self.spec.re_size(w, h)
		# self.r1.re_size(w, h)
		# self.r2.re_size(w, h)

	def draw(self, dt):
		"""
			A fixed hop size may be too large and may cause insufficient
			available frame, resulting in a None window
		"""
		available = self.source.available()

		#	OG when speed was not changed
		# window = self.source.get()
		# #	check shape of window
		# logger.info(f"{available}, {window.shape if window is not None else None}")


		logger.info(f"{available}")

		for i in range(self.speed_factor):
			window = self.source.get()
			self.wave.add(window)
			self.spec.add(window)

		self.wave.update()
		self.spec.update()

		# self.wave.draw(w, h)
		# self.spec.draw(w, h)
		# self.r1.draw(w, h)
		# self.r2.draw(w, h)
		for node in self.nodes:
			node.draw()
		
		def exit(self):
			logger.info("Exit Called")
			self.source.release()


if __name__ == "__main__":
	App.run()