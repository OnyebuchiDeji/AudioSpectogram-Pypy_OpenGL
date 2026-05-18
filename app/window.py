import moderngl
import time
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtWidgets import QApplication, QOpenGLWidget, QShortcut

from utils import logger

class Window(QOpenGLWidget):
	"""
		Because framerate has to be set to a whole number
		in milliseconds. But since 1/60 is not a whole number
		use '61' and then Moderngl will limit it to 1/60 properly
	"""
	frame_rate = 61  

	def __init__(self):
		super().__init__()

		self.setFixedSize(1200, 675)

		#	Allow multisampling in render
		#	to improve quality
		fmt = QSurfaceFormat()
		fmt.setVersion(3, 3)
		fmt.setProfile(QSurfaceFormat.CoreProfile)
		fmt.setDefaultFormat(fmt)
		fmt.setSamples(4)
		self.setFormat(fmt) #	a class method

		self.prev_time = None
		QShortcut(Qt.Key_Escape, self, self.quit)

		self.timer = QTimer()
		#	update is contained within the QT object
		#	and when its called it calls the `paint` method
		self.timer.timeout.connect(self.update)
		self.timer.start(int(1000 / self.frame_rate))

	#------------------------------
	#		OpenGL Logic
	#------------------------------
	def initializeGL(self):
		"""
		This sets up the OpenGL context so that
		"""
		self.ctx = moderngl.create_context(require=330)
		# self.ctx.clear(0.04, 0.07, 0.1)
		self.ctx.clear(0, 0, 0)
		self.ctx.enable(moderngl.BLEND) 	#	for freetype font rendering
		self.ctx.multisample = True 		# Improves render quality

		#	Context must exist before opengl functions are called!
		#	Hence why the below init is called here.
		self.init()


	def resizeGL(self, w, h):
		self.re_size(w, h)

	def paintGL(self):
		"""
			For every frame render, for every GL call
			this activates the OpenGL context
			to enable rendering to the screen
		"""
		now = time.time()
		dt = now - self.prev_time if self.prev_time else 1.0 / self.frame_rate
		self.prev_time = now
		self.draw(dt)


	def quit(self):
		self.exit() #	clean OpenGL objects first
		self.close()

	@classmethod
	def run(cls):
		#	tell qt to consider device's set dimension scaling factor
		QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
		app = QApplication([])
		main = cls()			#	main window
		main.show()
		app.exit(app.exec())	#	add app to event loop


	#--------------------------
	#	 	Interface
	#	Interface methods:
	#	sub class this window class and build app from that
	#	these functions will be called automatically
	#	when certain events occur in the app
	#--------------------------
	def init(self):
		logger.info("Init Called")

	def re_size(self, w, h):
		"""
		For when window resizes, then perform
		OpenGL related stuff like updating project matrix etc. 
		""" 
		logger.info(f"Resize Called: {w}, {h}")

	def draw(self, dt):
		"""
			Called to perform screen render and receives
			change in time
		"""
		logger.info(f"Draw  Called: {dt:.4f}")

	def exit(self):
		"""
		Cleanup to release resources
		"""
		logger.info("Exit Called")


if __name__ == "__main__":
	Window.run()