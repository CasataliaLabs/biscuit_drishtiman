import cv2
import numpy
import matplotlib.pyplot as plt
from repeated_timer import repeatedTimer
from Tkinter import *
from tkMessageBox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

video = cv2.VideoCapture(0)
ret, frame = video.read()

window = Tk()
window.title('Biscuit frame')
window.geometry('500x400')

#Reference Plot
ReferenceFigure = Figure(figsize=(5, 4), dpi=80)
axis1 = ReferenceFigure.add_subplot(111)
axis1.set_title('REFERENCE FRAME')
canvas1 = FigureCanvasTkAgg(ReferenceFigure, master=window)
widget=canvas1.get_tk_widget().place(x=10, y=10)
axis1.imshow(frame)

#initializing variables
count=0
red=[]
green=[]
blue=[]
frame_dup = numpy.ones(frame.shape)
def click(event):
	global count,red,green,blue
	print '\nClicked at: x=',event.x,'  y=', event.y
	Red,Green,Blue=frame1[event.x,event.y]
	red.append(Red)
	green.append(Green)
	blue.append(Blue)
	Red,Green,Blue=frame1[event.x,event.y]
	print Red, Green, Blue
	count=count+1
	if count==10:
		threshArray = numpy.array([numpy.mean(red), numpy.mean(green),numpy.mean(blue)])
		numpy.savetxt('Thresh.txt',threshArray,fmt="%s")
		quit()	

canvas1.mpl_connect('button_press_event', click)

cap.release()
cv2.destroyAllWindows()
window.mainloop()



