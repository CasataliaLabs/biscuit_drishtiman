'''Biscuit Segmenter
Authors: Subin George, Neethu Joseph, Archana Bade'''

import cv2,sys,time
import numpy as np
from Tkinter import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
plt.ion()

def StartButton():
    timerFrameDisplay.start()
def StopButton():
    timerFrameDisplay.stop()
def QuitButton():
	video.release()
	
def showFrame(hImshow):
	tic=time.time()
	thresholdForMask = [2, 40, 100, 250]
	hueMin, hueMax, saturationMin, saturationMax = thresholdForMask
	ret,frame = video.read()
	hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
	maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
	biscuitMask = cv2.inRange(hsvFrame, minimumValue, maximumValue)
	contour, hierarchy = cv2.findContours(biscuitMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	parents = hierarchy[0,:,3]
	noParents = parents == -1
	indexOfNoParents = np.where(noParents ==True)[0]
	areaOfContour = []
	for itration in range(0,len(indexOfNoParents)):
		areaOfContour.append(cv2.contourArea(contour[indexOfNoParents[itration]]))
	areaOfContourMax = np.max(areaOfContour)
	indexOfAreaOfContourMax = areaOfContour.index(areaOfContourMax)
	for noParentsIndex in range(0,len(indexOfNoParents)):
		if noParentsIndex == indexOfAreaOfContourMax:
			biscuitContour = contour[indexOfNoParents[noParentsIndex]]
			cv2.drawContours(biscuitMask,[biscuitContour],0,255,-1)
		else:
			biscuitContour = contour[indexOfNoParents[noParentsIndex]]
			cv2.drawContours(biscuitMask,[biscuitContour],0,0,-1)
	maskedFrame=np.zeros((frame.shape))
	for color in range(0,3):
		maskedFrame[:,:,color]=rgbFrame[:,:,color]*biscuitMask 
	axesForVideo.clear()
	hImshow = axesForVideo.imshow(maskedFrame, cmap = cm.Greys_r)
	canvasForCanvas.show()
	toc = time.time()
	#~ print toc-tic
	
guiMain = Tk()
guiMain.geometry('850x7000')
guiMain.title('biscuit_inspection')

if not 'video' in locals():
	video = cv2.VideoCapture()
if not video.isOpened():
	video.open(0)
ret, frame = video.read()
if ret == False:
	print 'Check if camera is connected'
	sys.exit() 

frameRgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
threshold = np.loadtxt('Threshold.txt')

videoFigure = Figure(figsize=(5, 5))
axesForVideo = videoFigure.add_subplot(111)
videoFigure.suptitle("BISCUIT SEGMENTATION")
hImshow = axesForVideo.imshow(frameRgb)
canvasForVideo = FigureCanvasTkAgg(videoFigure, master=guiMain)
canvasForVideo.get_tk_widget().place(x=10, y=20)

#Timer for frame
timerFrameDisplay = videoFigure.canvas.new_timer(interval=10)
timerFrameDisplay.add_callback(showFrame, hImshow)
#Start and Stop Buttons
button1 = Button(guiMain, text="Start", bg='white', command=StartButton).place(x=50, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=StopButton).place(x=200, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=QuitButton).place(x=400, y=600)
