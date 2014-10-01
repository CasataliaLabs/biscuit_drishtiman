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
	threshold = [2, 40, 100, 250]
	hueMin, hueMax, saturationMin, saturationMax = threshold
	ret,frame = video.read()
	frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	minimumValue = np.array([hueMin, saturationMin, 0], np.uint8)
	maximumValue = np.array([hueMax, saturationMax , 255], np.uint8)
	biscuit = cv2.inRange(frameHSV, minimumValue, maximumValue)
	axes1.clear()
	hImshow = axes1.imshow(biscuit, cmap = cm.Greys_r)
	canvas1.show()
	toc = time.time()
	#~ print toc-tic
	
video = cv2.VideoCapture()
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

ret, frame = video.read()
frameRgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
threshold = np.loadtxt('Threshold.txt')

videoFigure = Figure(figsize=(5, 5))
axes1 = videoFigure.add_subplot(111)
videoFigure.suptitle("Live Video")
hImshow = axes1.imshow(frameRgb, cmap = cm.Greys)
canvas1 = FigureCanvasTkAgg(videoFigure, master=guiMain)
canvas1.get_tk_widget().place(x=10, y=20)


#Timer for frame
timerFrameDisplay = videoFigure.canvas.new_timer(interval=10)
timerFrameDisplay.add_callback(showFrame, hImshow)
#Start and Stop Buttons
button1 = Button(guiMain, text="Start", bg='white', command=StartButton).place(x=50, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=StopButton).place(x=200, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=QuitButton).place(x=400, y=600)
