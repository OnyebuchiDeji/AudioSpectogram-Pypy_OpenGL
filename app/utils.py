import logging
from pyrr import Matrix44

#--------------
#	Logger
#--------------

#	Create Custom Logger
logger = logging.getLogger("Spectogram")

#	Set Level
#	By changing the level, one can toggle whether or not
#	to print out anything to the command line.
# logger.setLevel(logging.INFO)   #	to log all info
logger.setLevel(logging.ERROR)  #	to log only errors


#	Create Handler
handler = logging.StreamHandler()

#	Set Formatter
format = "%(asctime)s - %(levelname)s - %(filename)s - %(message)s"
formatter = logging.Formatter(format)
handler.setFormatter(formatter)

#	Add handler to the logger
logger.addHandler(handler)



#-----------------------------
#	Orthographic Proj Formula
#-----------------------------

def orthographic(w, h):
	return Matrix44.orthogonal_projection(
		0, w, h, 0, 1, -1, dtype='f4')
