import cv2
import numpy as np
import sys
import time
# import v4l_module
from Tkinter import *
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
plt.ion()
#Function for starting timers
def StartButton():
    timerFrameDisplay.start()
#Function for stopping timers
def StopButton():
    timerFrameDisplay.stop()
def QuitButton():
	video.release()
	print 'no quit \n please close'
#Function to display video frame,mean of frame variations,display in a table
def showFrame(hImshow):
	hueMin, hueMax, saturationMin, saturationMax = threshold
	ret,frame = video.read()
	if ret == None:
		print "reading from cam failed"
		return
	ret, frame = video.read()
	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	h,s,v=cv2.split(frameHSV)
	minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
	maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
	biscuit = cv2.inRange(frameHSV, minimumValue, maximumValue)
	biscuit = biscuit==0
	biscuit=biscuit*255
	#~ print biscuit
	hImshow.set_array(biscuit)
	canvas1.show()
	toc = time.time()
	'''data = {'1': {'Time': '{0:.3f}'.format(toc - tic)}}
	model = table.model
	model.importDict(data)
	table.redrawTable()'''
print 'start'	
guiMain = Tk()
guiMain.geometry('850x7000')
guiMain.title('biscuit_inspection') #how to set full screen
print 'gui created'
#Capturing video frame
if not 'video' in locals():
	video = cv2.VideoCapture()
while not video.isOpened():
	print 'attempting open video'
	video.open(0)
	time.sleep(1)
else:
	print "video already open"
ret, frame = video.read()
frameRgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
print "frame acquired status", ret
threshold = np.loadtxt('Threshold.txt')
#Creating figure for showing video frame
videoFigure = Figure(figsize=(5, 5))
axes1 = videoFigure.add_subplot(111)
videoFigure.suptitle("Live Video")
hImshow = axes1.imshow(frameRgb, cmap = cm.Greys)
#Creating canvass for placing videou frame
canvas1 = FigureCanvasTkAgg(videoFigure, master=guiMain)
canvas1.get_tk_widget().place(x=10, y=20)
# table creation
'''frameValue = Frame(guiMain)
frameValue.pack()
frameValue.place(x=100, y=500,width=300, height=70)
model = TableModel()
table = TableCanvas(frameValue, model=model, editable=False)
table.createTableFrame()'''
#Timer for frame
timerFrameDisplay = videoFigure.canvas.new_timer(interval=10)
timerFrameDisplay.add_callback(showFrame, hImshow)
#Start and Stop Buttons
button1 = Button(guiMain, text="Start", bg='white', command=StartButton).place(x=50, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=StopButton).place(x=200, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=QuitButton).place(x=400, y=600)
