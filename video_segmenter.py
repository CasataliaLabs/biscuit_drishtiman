
import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
import time
import sys
import matplotlib.cm as cm
plt.ion()
tol =	50
#Function for starting timers
def StartButton():
    timerFrameDisplay.start()

#Function for stopping timers
def StopButton():
    timerFrameDisplay.stop()
    
def QuitButton():
	video.release()
	print 'no quit \n please close'
	#~ sys.exit(0)

#Function to display video frame,mean of frame variations,display in a table
def showFrame(hImshow):
	tic = time.time()
	global frameDup, thresh
	frameDup1 = frameDup2 = frameDup
	ret,frame = video.read()
	if ret == None:
		print "reading from cam failed"
		return
	frameDuplicate = frame
	for i in range(0,3):
		frameDup1[:,:,i] = (frame[:,:,i] <= thresh[i]+tol)
		frameDup2[:,:,i] = (frame[:,:,i] >= thresh[i]-tol)
		frameDup[:,:,i] = frameDup1[:,:,i]*frameDup2[:,:,i]
	frameMask = frameDup[:,:,0]*frameDup[:,:,1]*frameDup[:,:,2]
	frameDuplicate[:,:,0]=frame[:,:,0]*frameMask
	frameDuplicate[:,:,1]=frame[:,:,1]*frameMask
	frameDuplicate[:,:,2]=frame[:,:,2]*frameMask
	hImshow.set_array(frameDuplicate)
	canvas1.show()
	toc = time.time()
	
	data = {'1': {'Time': '{0:.3f}'.format(toc - tic)}}
	model = table.model
	model.importDict(data)
	table.redrawTable()
	#~ print (toc - tic)
	
print 'start'	
guiMain = Tk()
guiMain.geometry('850x7000')
guiMain.title('biscuit_inspection') #how to set full screen
print 'gui created'
	
	
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
print "frame acquired status", ret
thresh = np.loadtxt('Thresh.txt')
redMean, greenMean, blueMean, length, width,color = thresh
frameDup = np.zeros((length, width,color))

#Creating figure for showing video frame
videoFigure = Figure(figsize=(5, 5))
axes1 = videoFigure.add_subplot(111)
videoFigure.suptitle("Live Video")
hImshow = axes1.imshow(frame,cmap = cm.Greys_r, vmin=20, vmax=80)

#Creating canvass for placing videou frame
canvas1 = FigureCanvasTkAgg(videoFigure, master=guiMain)
canvas1.get_tk_widget().place(x=10, y=20)

#~ # table creation
frameValue = Frame(guiMain)
frameValue.pack()
frameValue.place(x=100, y=500,width=300, height=70)
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

