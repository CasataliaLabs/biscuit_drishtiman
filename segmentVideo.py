
import cv2
import numpy
import pylab
from repeated_timer import repeatedTimer
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def VideoPlot():
	global frame_dup, red_min, red_max, green_min, green_max, blue_min, blue_max
	frame1 = video.read(0)[1]
	frame_dup[:,:,0] = (frame1[:,:,0] <= red_max)*frame1[:,:,0]
	frame_dup[:,:,0] = (frame_dup[:,:,0] >= red_min)*1
	frame_dup[:,:,1] = (frame1[:,:,1] <= green_max)*frame1[:,:,1]
	frame_dup[:,:,1] = (frame_dup[:,:,1] >= green_min)*1
	frame_dup[:,:,2] = (frame1[:,:,2] <= blue_max)*frame1[:,:,2]
	frame_dup[:,:,2] = (frame_dup[:,:,2] >= blue_min)*1 
	frame_dup1 = frame_dup[:,:,0]+frame_dup[:,:,1]+frame_dup[:,:,2]
	frame_dup1 = frame_dup1==3	
	
	#~ plt.imshow(frame_dup1)
	#~ plt.show()
	axes1.imshow(frame_dup1)
	canvas1.draw()
    
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
redMean, greenMean, blueMean = thresh
red_min, red_max = redMean-5, redMean+5
green_min, green_max = greenMean-5, greenMean+5
blue_min, blue_max = blueMean-5, blueMean+5
#~ print thresh   
video = cv2.VideoCapture(0)
frame_dup = video.read(0)[1]
window = Tk()
window.geometry('850x7000')
window.title('Test gui')

videoFigure = Figure(figsize=(8, 8), dpi=80)


axes1 = videoFigure.add_subplot(111)
axes1.set_title('Video frame')
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
