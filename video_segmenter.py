import cv2
import numpy
import pylab
from repeated_timer import repeatedTimer
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plot
import time


tol = 50

def VideoPlot():
	tic = time.time()
	global frameDup1,frameDup2, redMin, redMax, greenMin, greenMax, blueMin, blueMax
	ret,frame = video.read(0)
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
	
	showFrame.set_array(frameDuplicate)  #, plot.get_cmap('gray'))
	canvas1.draw()
	toc = time.time()
	print (toc -tic)
    
def StartButton():
    global timer1
    timer1.start()
    
def StopButton():
	print 'stop'
	timer1.stop()
	
def QuitButton():
    video.release()
    print 'quit'
    quit()

thresh = numpy.loadtxt('Thresh.txt')
redMean, greenMean, blueMean, length, width,color = thresh
redMin, redMax = redMean-tol, redMean+tol
greenMin, greenMax = greenMean-tol, greenMean+tol
blueMin, blueMax = blueMean-tol, blueMean+tol
#~ print thresh   
video = cv2.VideoCapture(0)
frameDup1 = numpy.zeros((length, width,color))
frameDup2 = numpy.zeros((length, width,color))
window = Tk()
window.geometry('850x7000')
window.title('Test gui')

videoFigure = Figure(figsize=(8, 8), dpi=80)
axes1 = videoFigure.add_subplot(111)
axes1.set_title('Video frame')
video.open(0)
ret, frame = video.read(0)
showFrame = axes1.imshow(frame)
# Make a canvas on VideoFigure
canvas1 = FigureCanvasTkAgg(videoFigure, master=window)
canvas1.show()  # Display canvas1
canvas1.get_tk_widget().place(x=10, y=10)

button1 = Button(window, text='Start', fg='green', command=StartButton).place(x=500, y=450)
button2 = Button(window, text='Stop', fg='red', command=StopButton).place(x=500, y=500)
button3 = Button(window, text='Quit', fg='black', bg='red', command=QuitButton).place(x=500, y=550)
# Create timers
timer1 = repeatedTimer(.1, VideoPlot)


# main loop
window.mainloop()
