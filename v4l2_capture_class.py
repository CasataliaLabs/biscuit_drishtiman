import Image
import select
import v4l2capture
import numpy as np
import pylab as plt
import os as os
import time
plt.ion()
from glob import glob as glob
import sys

class CaptureFromCam():
	def __init__(self, camPath):
		cameraAvailable = glob('/dev/video*')
		print cameraAvailable
		self.camPath = camPath
		#~ sys.exit(0)
		if os.path.exists(self.camPath):
			print 'declared cam exists'
		elif cameraAvailable >= 1:
			self.camPath = cameraAvailable[0]
			#~ self.camLink = v4l2capture.Video_device(self.camPath)
		else:
			self.camLink = None
			print 'no camera available'
			#~ os.lsdir('/dev/video*')
			#~ cameraAvailable = glob('/dev/video*')
			#~ print cameraAvailable
		try:
			self.camLink = v4l2capture.Video_device(self.camPath)
			self.camLink.set_format(640, 480)
			self.resolution = self.camLink.get_format()
			self.camLink.create_buffers(1)
			self.camLink.queue_all_buffers()
			print 'camera link established'
			self.stat = 'initialized'
			self.start()
			self.stat = 'running'
			print 'camera status: ', self.stat
		except:
			print 'camera already in use, either exit old program or remove and reconnect camera'
			sys.exit(0)	
	def start(self):
		self.stop()
		self.camLink.start()
		select.select((self.camLink,), (), ())
		self.stat = 'running'
	def read(self):
		try:
			self.frameScrap = self.camLink.read_and_queue()
			self.frameIPL = Image.fromstring("RGB", (self.resolution[0], self.resolution[1]), self.frameScrap)
			self.frameNp = np.asarray(self.frameIPL)
			self.stat = 'running read frame(s)'
			return self.frameNp
		except:
			#~ print a
			print 'camera reading failed'
			self.stat = 'stopped'
			self.__init__(self.camPath)
	def stop(self):
		self.camLink.stop()
		self.stat = 'stopped'
	def close(self):
		self.camLink.close()
		self.stat = 'closed'
