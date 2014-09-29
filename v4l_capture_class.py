import Image
import select
import v4l2capture
import numpy
import pylab
import os as os
import time
from glob import glob as glob

class CaptureFromCam():
	def __init__(self, camPath):
		self.camPath = camPath
		if os.path.exists(self.camPath):
			self.camLink = v4l2capture.Video_device(self.camPath)
			self.camLink.set_format(640, 480)
			self.resolution = self.camLink.get_format()
			self.camLink.create_buffers(1)
			self.camLink.queue_all_buffers()
			print 'camera link established'
			self.stat = 'initialized'
		else:
			print 'available cameras'
			#~ os.lsdir('/dev/video*')
			cameraAvailable = glob('/dev/video*')
			print cameraAvailable
	
	def start(self):
		self.camLink.start()
		select.select((self.camLink,), (), ())
		self.stat = 'running'
	def read(self):
		#~ try:
		self.frameIPL = self.camLink.read_and_queue()
		self.frameNp = Image.fromstring("RGB", (self.resolution[0], self.resolution[1]), self.frameIPL)
		self.stat = 'running read frame(s)'
		#~ except a:
			#~ print a
			#~ print 'camera reading failed'
			#~ self.stat = 'stopped'
	def stop(self):
		self.camLink.stop()
		self.stat = 'stopped'
	def close(self):
		self.camLink.close()
		self.stat = 'closed'
