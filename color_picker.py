import cv2
import numpy as np
import matplotlib.pyplot as plt

if not 'video' in locals():
	video = cv2.VideoCapture(0)
if not video.isOpened():
	video.open(0)
ret, frame = video.read()
if ret == False:
	print 'Check if camera is connected'
	sys.exit()
rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
hsvFrame = cv2.cvtColor(rgbFrame, cv2.COLOR_RGB2HSV)
plt.imshow(rgbFrame[:,:,1])
coordinates = []
coordinates = np.floor(plt.ginput(n=5, timeout=30, show_clicks=True, mouse_add=1, mouse_pop=3, mouse_stop=2))
xyCordinates = coordinates.astype('int')

hsvValues = hsvFrame[xyCordinates[:,0],xyCordinates[:,1]]
hue,saturation = hsvValues[:,0],hsvValues[:,1]

thresholdArray = np.array([np.min(hue), np.max(hue), np.min(saturation), np.max(saturation)])
np.savetxt('Threshold.txt',thresholdArray,fmt="%s")
