
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

class BiscuitInspector():
	def FrameAcquisition(self,video):
		ret, frame = video.read()
		hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
		rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		return hsvFrame,rgbFrame
	def MaskForBiscuit(self,hsvFrame):
		thresholdForMask = [2, 40, 100, 250]
		hueMin, hueMax, saturationMin, saturationMax = thresholdForMask
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
				biscuitContourForEllipse = biscuitContour
				cv2.drawContours(biscuitMask,[biscuitContour],0,255,-1)
			else:
				biscuitContour = contour[indexOfNoParents[noParentsIndex]]
				cv2.drawContours(biscuitMask,[biscuitContour],0,0,-1)
		return biscuitMask,areaOfContourMax, biscuitContourForEllipse		
	def EllipseFitting(self,rgbFrame,biscuitMask,biscuitContourForEllipse):
		maskedFrame=np.zeros((rgbFrame.shape))
		for color in range(0,3):
			maskedFrame[:,:,color]=rgbFrame[:,:,color]*biscuitMask 
		ellipseForBiscuit = cv2.fitEllipse(biscuitContourForEllipse)
		cv2.ellipse(maskedFrame,ellipseForBiscuit,(0,1,0),2)
		majorAxisOfEllepse = np.max(ellipseForBiscuit[1])
		minorAxisOfEllepse = np.min(ellipseForBiscuit[1])
		return majorAxisOfEllepse, minorAxisOfEllepse,maskedFrame	
	def ShowGui(self,video):
		tic = time.time()
		hsvFrame,rgbFrame = self.FrameAcquisition(video)
		biscuitMask,areaOfContourMax, biscuitContourForEllipse= self.MaskForBiscuit(hsvFrame)
		majorAxisOfEllepse, minorAxisOfEllepse, maskedFrame = self.EllipseFitting(rgbFrame,biscuitMask,biscuitContourForEllipse)
		axesForVideo.clear()
		axesForVideo.imshow(maskedFrame, cmap = cm.Greys_r)
		toc = time.time()
		timeTakenForSegmentation = '{0:.3f}'.format(toc - tic)
		tableValues=[['Time', timeTakenForSegmentation, ' '], ['Area',int(areaOfContourMax), ''], ['Minor Axis', int(minorAxisOfEllepse), ''], ['Major Axis ', int(majorAxisOfEllepse), ''], ['', '', ''], ['', '', ''], ['', '', '']]
		dataTable = axesForTable.table(cellText=tableValues, colWidths=[0.11]*3, loc='center')
		dataTable.set_fontsize(20)
		dataTable.scale(3, 3)
		
		canvasForGui.show()
	def StartButton(self):
		guiTimer.start()
	def StopButton(self):
		guiTimer.stop()
	def QuitButton(self):
		video.release()
		sys.exit(0)
if not 'video' in locals():
	video = cv2.VideoCapture()
if not video.isOpened():
	video.open(0)
	ret, frame = video.read()
if ret == False:
	print 'Check if camera is connected'
	sys.exit()
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

canvasForGui = FigureCanvasTkAgg(guiFigure, master=guiMain)
canvasForGui.get_tk_widget().pack(fill="both", expand = 1)
canvasForGui.show()

axesForVideo.imshow(rgbFrame, cmap = cm.Greys_r)

timeTakenForSegmentation = 0
tableValues=[['Time', timeTakenForSegmentation, ' '], ['Area','', ''], ['Minor Axis', '', ''], ['Major Axis ','', ''], ['', '', ''], ['', '', ''], ['', '', '']]
dataTable = axesForTable.table(cellText=tableValues, colWidths=[0.11]*3, loc='center')
dataTable.set_fontsize(20)
dataTable.scale(3, 3)

guiTimer = guiFigure.canvas.new_timer(interval=10)
guiTimer.add_callback(biscuitInspectorObj.ShowGui, video)

button1 = Button(guiMain, text="Start", bg='white', command=biscuitInspectorObj.StartButton).place(x=50, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=biscuitInspectorObj.StopButton).place(x=200, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=biscuitInspectorObj.QuitButton).place(x=400, y=600)
