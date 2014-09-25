
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
from Tkinter import *
#~ from repeated_timer1 import RepeatedTimer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import time
import sys
plt.ion()

tol =	70
#Function for starting timers
def StartButton():
    timerFrameDisplay.start()

#Function for stopping timers
def StopButton():
    timerFrameDisplay.stop()
    
def QuitButton():
	video.release()
	print 'quit'
	sys.exit(0)

#Function to display video frame,mean of frame variations,display in a table
def showFrame(hImshow):
	tic = time.time()
	global frameDup1,frameDup2, redMin, redMax, greenMin, greenMax, blueMin, blueMax #, axes1, canvas1
	ret,frame = video.read(0)
	if ret == None:
		print "reading from cam failed"
		return
	frameDup1[:,:,0] = (frame[:,:,0] <= redMax)
	frameDup2[:,:,0] = (frame[:,:,0] >= redMin)
	frameBin1 = frameDup1[:,:,0]*frameDup2[:,:,0]
	#~ frameBin1 = frameBin1==0
	frameDup1[:,:,1] = (frame[:,:,1] <= greenMax)
	frameDup2[:,:,1] = (frame[:,:,1] >= greenMin)
	frameBin2 = frameDup1[:,:,1]*frameDup2[:,:,1]
	#~ frameBin2 = frameBin2==0
	frameDup1[:,:,2] = (frame[:,:,2] <= blueMax)
	frameDup2[:,:,2] = (frame[:,:,2] >= blueMin) 
	frameBin3 = frameDup1[:,:,2]*frameDup2[:,:,2]
	#~ frameBin3 = frameBin3==0
	frameDupBin = frameBin1*frameBin2*frameBin3
	frameDuplicate = frame
	frameDuplicate[:,:,0]=frame[:,:,0]*frameDupBin
	frameDuplicate[:,:,1]=frame[:,:,1]*frameDupBin
	frameDuplicate[:,:,2]=frame[:,:,2]*frameDupBin
	#~ axes1.imshow(frameDuplicate)  #, plot.get_cmap('gray'))
	#~ frameDuplicate = plot.get_cmap('gray')
	#~ axes1.clear()
	#~ showFrame = axes1.imshow(frame)
	hImshow.set_array(frame) #[:,:,2])
	#~ axes1.figure.canvas.show()
	canvas1.show()
	toc = time.time()
	print (toc - tic)
	
	
#Capturing video frame
if not 'video' in locals():
	video = cv2.VideoCapture(0)
while not video.isOpened():
	print 'attempting open video'
	video.open(0)
	time.sleep(1)
else:
	print "video already open"
ret, frame = video.read()

thresh = np.loadtxt('Thresh.txt')
redMean, greenMean, blueMean, length, width,color = thresh
redMin, redMax = redMean-tol, redMean+tol
greenMin, greenMax = greenMean-tol, greenMean+tol
blueMin, blueMax = blueMean-tol, blueMean+tol

print "frame acquired status", ret
frameDup1 = np.zeros((length, width,color))
frameDup2 = np.zeros((length, width,color))

#Creating window with title and geometry
guiMain = Tk()
guiMain.geometry('850x7000')
guiMain.title('biscuit_inspection') #how to set full screen

#Creating figure for showing video frame
videoFigure = Figure(figsize=(4, 4), dpi=100)
axes1 = videoFigure.add_subplot(111)
videoFigure.suptitle("Live Video")
hImshow = axes1.imshow(frame)


#Creating canvass for placing video frame
canvas1 = FigureCanvasTkAgg(videoFigure, master=guiMain)
canvas1.get_tk_widget().place(x=10, y=20)


# table creation
frameValue = Frame(guiMain)
frameValue.pack()
frameValue.place(x=175, y=500, width=175, height=70)
model = TableModel()
table = TableCanvas(frameValue, model=model, editable=False)
table.createTableFrame()
	
#Timer for frame
timerFrameDisplay = videoFigure.canvas.new_timer(interval=10)
timerFrameDisplay.add_callback(showFrame, hImshow)

#Start and Stop Buttons
button1 = Button(guiMain, text="Start", bg='white', command=StartButton).place(x=50, y=600)
button2 = Button(guiMain, text="Stop", bg='white', command=StopButton).place(x=200, y=600)
button3 = Button(guiMain, text="Quit", bg='white', command=QuitButton).place(x=400, y=600)

