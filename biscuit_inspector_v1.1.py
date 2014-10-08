
import cv2,sys,time
import numpy as np
import pylab
from Tkinter import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import matplotlib.pyplot as plt

import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
plt.ion()

class BiscuitInspector():
	def FrameAcquisition(self,video):
		ret, frame = video.read()
		rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		return hsvFrame,rgbFrame,grayFrame
	def MaskForBiscuit(self,hsvFrame):
		thresholdForMask = [2, 40, 100, 250]
		hueMin, hueMax, saturationMin, saturationMax = thresholdForMask
		minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
		maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
		biscuitMask = cv2.inRange(hsvFrame, minimumValue, maximumValue)
		contour, hierarchy = cv2.findContours(biscuitMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		#~ if len(hierarchy[0,:,3])>0:
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
				biscuitContourForEllipse = biscuitContour
				cv2.drawContours(biscuitMask,[biscuitContour],0,255,-1)
			else:
				biscuitContour = contour[indexOfNoParents[noParentsIndex]]
				cv2.drawContours(biscuitMask,[biscuitContour],0,0,-1)
		return biscuitMask,areaOfContourMax, biscuitContourForEllipse
	def EllipseFitting(self,rgbFrame,hsvFrame,biscuitMask,biscuitContourForEllipse):
		maskedFrame=np.zeros((rgbFrame.shape))
		maskedHsvFrame=np.zeros((rgbFrame.shape))
		for color in range(0,3):
			maskedFrame[:,:,color]=rgbFrame[:,:,color]*biscuitMask
			maskedHsvFrame[:,:,color]=hsvFrame[:,:,color]*biscuitMask
		ellipseForBiscuit = cv2.fitEllipse(biscuitContourForEllipse)
		cv2.ellipse(maskedFrame,ellipseForBiscuit,(0,1,0),2)
		majorAxisOfEllepse = np.max(ellipseForBiscuit[1])
		minorAxisOfEllepse = np.min(ellipseForBiscuit[1])
		return majorAxisOfEllepse, minorAxisOfEllepse,maskedFrame,maskedHsvFrame
	def AlmondSegment(self,maskedFrame, maskedHsvFrame):
		thresholdForAlmond = [200, 255, 130, 255]
		#~ maskedHsvFrame=cv2.cvtColor(maskedHsvFrame, cv2.COLOR_BGR2HSV)
		hueMin, hueMax, saturationMin, saturationMax = thresholdForAlmond
		minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
		maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
		almondMask = cv2.inRange(maskedHsvFrame, minimumValue, maximumValue,0)
		contour, hierarchy = cv2.findContours(almondMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		areaOfContour = []
		almondContour = []
		for iteration in range(0,len(contour)):
			area = cv2.contourArea(contour[iteration])
			if area>20:
				areaOfContour.append(cv2.contourArea(contour[iteration]))
				almondContour.append(contour[iteration])
				cv2.drawContours(maskedFrame, contour, iteration,(1,0,0),2)
		#~ cv2.cvtColor(maskedFrame, cv2.COLOR_HSV2RGB)
		#~ print areaOfContour
		almondArea = np.sum(areaOfContour)
		numberOfAlmonds = len(areaOfContour)
		return almondArea, numberOfAlmonds, maskedFrame
	def BakingCurve(self,maskedHsvFrame,biscuitContourForEllipse):
		momentOfBiscuit = cv2.moments(biscuitContourForEllipse)
		xCenter = int(momentOfBiscuit['m10']/momentOfBiscuit['m00'])
		yCenter = int(momentOfBiscuit['m01']/momentOfBiscuit['m00']) 
		yAxis = list(maskedHsvFrame[yCenter,xCenter:])
		#~ yAxis2 = list(maskedHsvFrame[yCenter,xCenter:,1])
		#~ yAxis3 = list(maskedHsvFrame[yCenter,xCenter:,2])
		xAxis = pylab.arange(0, len(yAxis), 1)
		return xAxis,yAxis,xCenter,yCenter
	def ShowGui(self,video):
		tic = time.time()
		hsvFrame,rgbFrame,grayFrame = self.FrameAcquisition(video)
		biscuitMask,areaOfContourMax, biscuitContourForEllipse= self.MaskForBiscuit(hsvFrame)
		majorAxisOfEllepse, minorAxisOfEllepse, maskedFrame, maskedHsvFrame = self.EllipseFitting(rgbFrame, hsvFrame,biscuitMask, biscuitContourForEllipse)
		#~ maskedFramedDup = maskedFrame
		maskedHsvFrameGray = grayFrame*biscuitMask
		xAxis,yAxis1,xCenter,yCenter = self.BakingCurve(maskedHsvFrameGray,biscuitContourForEllipse)
		almondArea, numberOfAlmonds,maskedAlmondFrame = self.AlmondSegment(maskedFrame,maskedHsvFrame)
		maskedFrameDisplay = maskedFrame
		maskedFrameDisplay[yCenter-1:yCenter+1,xCenter:,:] = 0
		axesForVideo.clear()
		axesForPlot.clear()
		
		axesForVideo.imshow(maskedFrameDisplay, cmap = cm.Greys_r)
		toc = time.time()
		timeTakenForSegmentation = '{0:.3f}'.format(toc - tic)
		tableValues=[['Time', timeTakenForSegmentation, ' '], ['Area',int(areaOfContourMax), ''], ['Minor Axis', int(minorAxisOfEllepse), ''], ['Major Axis ', int(majorAxisOfEllepse), ''], ['Number Of Almonds', numberOfAlmonds, ''], ['Almond area', almondArea, ''], ['', '', '']]
		dataTable = axesForTable.table(cellText=tableValues, colWidths=[0.11]*3, loc='center')
		dataTable.set_fontsize(20)
		dataTable.scale(3, 3)
		axesForPlot.plot(xAxis, yAxis1,  'o-', color='r', markersize=1)
		#~ axesForPlot.plot(xAxis, yAxis2,  'o-', color='g', markersize=1)
		#~ axesForPlot.plot(xAxis, yAxis3,  'o-', color='b', markersize=1)
		
		canvasForGui.show()
	def StartButton(self):
		guiTimer.start()
	def StopButton(self):
		guiTimer.stop()
	def QuitButton(self):
		video.release()
		sys.exit(0)
camPosition=0
#~ while True:
if not 'video' in locals():
	video = cv2.VideoCapture(camPosition)
if not video.isOpened():
	video.open(camPosition)
	camPosition+=1
ret, frame = video.read()
if ret == False:
	print 'Check if camera is connected'
	sys.exit()
#~ else:
	#~ break
#~ print i
rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)	
biscuitInspectorObj = BiscuitInspector()

guiMain = Tk()
screenWidth=guiMain.winfo_screenwidth()
screenHeight=guiMain.winfo_screenheight()
guiMain.geometry(("%dx%d")%(screenWidth,screenHeight))
guiMain.title('biscuit_inspection')
guiFigure = Figure()

axesForVideo = guiFigure.add_subplot(221)
axesForTable = guiFigure.add_subplot(222)
axesForPlot = guiFigure.add_subplot(223)

canvasForGui = FigureCanvasTkAgg(guiFigure, master=guiMain)
canvasForGui.get_tk_widget().pack(fill="both", expand = 1)
canvasForGui.show()

axesForVideo.imshow(rgbFrame, cmap = cm.Greys_r)

timeTakenForSegmentation = 0
tableValues=[['Time', timeTakenForSegmentation, ' '], ['Area','', ''], ['Minor Axis', '', ''], ['Major Axis ','', ''], ['Number Of Almonds', '', ''], ['Almond area', '', ''], ['', '', '']]
dataTable = axesForTable.table(cellText=tableValues, colWidths=[0.11]*3, loc='center')
dataTable.set_fontsize(20)
dataTable.scale(3, 3)

axesForPlot.grid(True)
xAxis = pylab.arange(0, 100, 1)
yAxis = pylab.array([0]*100)
#~ axesForPlot.axis([0, rgbFrame.shape[1], 0, 255])
axesForPlot.plot(xAxis, yAxis, 'o-', color='g', markersize=1)


guiTimer = guiFigure.canvas.new_timer(interval=10)
guiTimer.add_callback(biscuitInspectorObj.ShowGui, video)

button1 = Button(guiMain, text="Start", bg='white', command=biscuitInspectorObj.StartButton).place(x=700, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=biscuitInspectorObj.StopButton).place(x=800, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=biscuitInspectorObj.QuitButton).place(x=900, y=600)
