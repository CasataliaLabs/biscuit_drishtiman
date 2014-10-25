
import cv2,sys,time,glob
import numpy as np
import pylab
from Tkinter import *
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class BiscuitInspector():
	
    def FrameAcquisition(self,video):
        ret, frame = video.read()
        if ret == True:
			rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
			hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			return hsvFrame,rgbFrame,grayFrame
        else:
            return None
            
    def MaskForBiscuit(self,hsvFrame):
        thresholdForMask = [2, 40, 100, 250]
        hueMin, hueMax, saturationMin, saturationMax = thresholdForMask
        minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
        maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
        biscuitMask = cv2.inRange(hsvFrame, minimumValue, maximumValue)
        contour, hierarchy = cv2.findContours(biscuitMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contour) == 0:
            print 'error: contour not found'
            return None
        parents = hierarchy[0,:,3]
        noParents = parents == -1
        
        if len(noParents) == 0:
            print 'error: biscuit not found'
            return None
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
        thresholdForAlmond = [200, 255, 120, 150]
        hueMin, hueMax, saturationMin, saturationMax = thresholdForAlmond
        minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
        maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
        almondMask = cv2.inRange(maskedHsvFrame, minimumValue, maximumValue)
        contour, hierarchy = cv2.findContours(almondMask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        areaOfContour = []
       
        for iteration in range(0,len(contour)):
            area = cv2.contourArea(contour[iteration])
            if area>20:
                areaOfContour.append(cv2.contourArea(contour[iteration]))
                cv2.drawContours(maskedFrame, contour, iteration,(1,0,0),2)
        almondArea = np.sum(areaOfContour)
        numberOfAlmonds = len(areaOfContour)
        return almondArea, numberOfAlmonds, maskedFrame
        
    def BakingCurve(self,maskedHsvFrame,biscuitContourForEllipse):
        momentOfBiscuit = cv2.moments(biscuitContourForEllipse)
        xCenter = int(momentOfBiscuit['m10']/momentOfBiscuit['m00'])
        yCenter = int(momentOfBiscuit['m01']/momentOfBiscuit['m00']) 
        yAxis1 = list(maskedHsvFrame[yCenter,xCenter:])
        xAxis = pylab.arange(0, len(yAxis1), 1)
        return xAxis,yAxis1,xCenter,yCenter
        
    def ShowGui(self,video):
        tic = time.time()
        if self.FrameAcquisition(video) == None:
            print 'error: frame not found'
        else:
            hsvFrame,rgbFrame,grayFrame = self.FrameAcquisition(video)			
            if self.MaskForBiscuit(hsvFrame) == None:
                print "error: biscuit mask couldn't found"
            else:
                biscuitMask,areaOfContourMax, biscuitContourForEllipse= self.MaskForBiscuit(hsvFrame)
                majorAxisOfEllepse, minorAxisOfEllepse, maskedFrame, maskedHsvFrame = self.EllipseFitting(rgbFrame, hsvFrame,biscuitMask, biscuitContourForEllipse)
               
                maskedHsvFrameGray = grayFrame*biscuitMask
                xAxis,yAxis1,xCenter,yCenter = self.BakingCurve(maskedHsvFrameGray,biscuitContourForEllipse)
                almondArea, numberOfAlmonds,maskedAlmondFrame = self.AlmondSegment(maskedFrame,maskedHsvFrame)
                maskedFrameDisplay = maskedFrame
                maskedFrameDisplay[yCenter,xCenter:,:] = 0
				
                axesForVideo.clear()
                axesForPlot.clear()
                axesForTable.clear()
                toc = time.time()
                axesForVideo.imshow(maskedFrameDisplay)
                
                timeTakenForSegmentation = '{0:.3f}'.format(toc - tic)
                tableValues=[['Time', timeTakenForSegmentation], ['Area',int(areaOfContourMax)], ['Minor Axis', int(minorAxisOfEllepse)], ['Major Axis ', int(majorAxisOfEllepse)], ['Number Of Almonds', numberOfAlmonds], ['Almond area', almondArea]]
                dataTable = axesForTable.table(cellText=tableValues, colWidths=[0.111]*3, loc='center')
                dataTable.set_fontsize(20)
                dataTable.scale(3, 3)
                
                axesForPlot.plot(xAxis, yAxis1, 'g-',markersize=1)
                canvasForGui.show()
                
            toc = time.time()
            print '{0:.3f}'.format(toc - tic)
    def StartButton(self):
        guiTimer.start()
    def StopButton(self):
        guiTimer.stop()
    def QuitButton(self):
        video.release()
        sys.exit(0)

devList=glob.glob('/dev/video*')
if len(devList)==0:
    sys.exit()
else:
    camPosition=int(devList[0][10])
    if not 'video' in locals():
        video = cv2.VideoCapture(camPosition)
    if not video.isOpened():
        video.open(camPosition)
    ret, frame = video.read()
    if ret == False:
        print 'error: Check if camera is connected'
        sys.exit()
        
biscuitInspectorObj = BiscuitInspector()

guiMain = Tk()
screenWidth=guiMain.winfo_screenwidth()
screenHeight=guiMain.winfo_screenheight()
guiMain.geometry(("%dx%d")%(screenWidth,screenHeight))
guiMain.title('Biscuit Inspector v1.1')
guiFigure = Figure()

axesForVideo = guiFigure.add_subplot(221)
axesForVideo.axes.get_xaxis().set_visible(False)
axesForVideo.axes.get_yaxis().set_visible(False)
axesForTable = guiFigure.add_subplot(222)
axesForTable.axes.get_xaxis().set_visible(False)
axesForTable.axes.get_yaxis().set_visible(False)
axesForPlot = guiFigure.add_subplot(223)

canvasForGui = FigureCanvasTkAgg(guiFigure, master=guiMain)
canvasForGui.get_tk_widget().pack(fill="both", expand = 1)
canvasForGui.show()

rgbFrame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)	
axesForVideo.imshow(rgbFrame)


timeTakenForSegmentation = 0
tableValues=[['Time', timeTakenForSegmentation, ' '], ['Area','', ''], ['Minor Axis', '', ''], ['Major Axis ','', ''], ['Number Of Almonds', '', ''], ['Almond area', '', ''], ['', '', '']]
dataTable = axesForTable.table(cellText=tableValues, colWidths=[0.111]*3, loc='center')
dataTable.set_fontsize(20)
dataTable.scale(3, 3)

axesForPlot.grid(True)
xAxis = pylab.arange(0, 100, 1)
yAxis = pylab.array([0]*100)
axesForPlot.axis([0, rgbFrame.shape[1], 0, 255])
axesForPlot.plot(xAxis, yAxis, 'o-', color='g', markersize=1)


guiTimer = guiFigure.canvas.new_timer(interval=10)
guiTimer.add_callback(biscuitInspectorObj.ShowGui, video)

button1 = Button(guiMain, text="Start", bg='white', command=biscuitInspectorObj.StartButton).place(x=700, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=biscuitInspectorObj.StopButton).place(x=800, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=biscuitInspectorObj.QuitButton).place(x=900, y=600)


