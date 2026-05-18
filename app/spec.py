"""
	Spec for spectogram

	The Hann Window/Wave is a kind of normal-like distribution
	curve that can be used to taper the fourier transform
	of a window. 
	A window is a small section of the audio signal
	This small sectino is needed as opposed to finding
	the frequencies in the whole audio at once
	The fourier transform of a window is used to extract
	the various frequencies.
	Tapering is important to reshape the window as it
	quitens the frequencies at the edges of the audio window.
	The Hanning window ensures only the frequencies in the
	center of the window are promininet and those at the edges
	are quietened. 
	Then after the hanning is applied, the fourier transform
	of the packet is obtained
"""


from config import WINDOW_SIZE, WINDOW_WIDTH
import librosa
import matplotlib
import moderngl
import numpy as np
import time

from utils import orthographic

hann = np.hanning(WINDOW_WIDTH)
color_map = matplotlib.colormaps.get_cmap('inferno')


def stft_slice(window):
	"""
	Short-Term Fourier Transform Slice

	Used to pad sides of the audio wave window that
	does not have enough frequencies/might not be 
	the full WINDOW_SIZE length
	"""
	n = window.shape[0]
	if n < WINDOW_SIZE:
		padded = np.zeros(WINDOW_SIZE, dtype=window.dtype)
		padded[:n] = window
		window = padded
	hann = np.hanning(WINDOW_SIZE)
	tapered = window * hann #	apply hanning
	return np.fft.rfft(tapered)

def stft_color(slice, min_db=-50, max_db=30):
	"""
		Color map of decibels (frequency amount) to represent
		audio spectogram graph
	"""
	slice = np.abs(slice)
	slice = librosa.amplitude_to_db(slice)
	slice = slice.clip(min_db, max_db)
	#	normalize within range of the decibel limits
	slice = (slice - min_db) / (max_db - min_db)
	slice = color_map(slice)
	slice = (slice * 255).astype('u1')
	slice = slice[:, :3]
	return slice


class Spec:
	"""
		Height of frame is 513
		This is gotten from the fast fourier transform's
		window size of 1024. The height is half of 1024 + 1
	"""

	VERTEX = """
		#version 330 core
		uniform mat4 P;
		in vec2 vertex;
		in vec2 uv;
		out vec2 v_uv;
		void main(){
			gl_Position= P * vec4(vertex, 0, 1);
			v_uv = uv;
		}
	"""

	FRAGMENT = """
		#version 330 core
		uniform sampler2D image;
		in vec2 v_uv;
		out vec4 out_color;
		void main(){
			vec4 color = texture(image, v_uv);
			out_color = vec4(color.rgb, 1.0);
		}
	"""

	def __init__(self, ctx, x, y, w, h):
		self.ctx = ctx
		self.x = x; self.y = y
		self.w = w; self.h = h
		self.prog = self.ctx.program(
			vertex_shader=self.VERTEX,
			fragment_shader=self.FRAGMENT
			)
		vertices = np.array([
			0, y,   0, 1, # A
			0, y+h, 0, 0, # B 
			w, y+h, 1, 0, # C
			0, y,   0, 1, # A
			w, y+h, 1, 0, # C
			w, y,   1, 1, # D
			])
		vertices = vertices.astype('f4')
		buffer = self.ctx.buffer(vertices)
		self.vao = self.ctx.vertex_array(
			self.prog, buffer, "vertex", "uv"
			)
		#	frame height of 513
		self.frame = np.zeros((513, self.w, 3), dtype='u1')

		self.texture = self.ctx.texture(
			size=(self.w, 513),
			components=3,
			data=self.frame
			)

		self.texture.repeat_x = False
		self.texture.repeat_y = False
		self.slice = np.zeros((513, 3), dtype='u1')

	# def add(self, window):
	# 	#	reflect the frequency values
	# 	self.frame[:,:-1,:] = self.frame[:,1:,:]
	# 	if window is not None:
	# 		slice = stft_slice(window)
	# 		slice = stft_color(slice)
	# 	else:
	# 		slice = self.slice

	# 	self.frame[:,-1,:] = slice

	def add(self, window):
		#	reflect the frequency values
		self.frame[:,:-1,:] = self.frame[:,1:,:]
		if window is not None:
			slice = stft_slice(window)
			slice = stft_color(slice)
			self.slice = slice

		#	updated to use the currnetly saved slice
		self.frame[:,-1,:] = self.slice

	def update(self):
		self.texture.write(self.frame)

	def re_size(self, w, h):
		P = orthographic(w, h)
		self.prog['P'].write(P)

	def draw(self):
		self.texture.use(0)
		self.vao.render()