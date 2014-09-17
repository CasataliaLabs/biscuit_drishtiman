
import cv2
import numpy
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#performing 10 clicks
def click(event):
	global count,red_sum,green_sum,blue_sum
	#reading x and y coordinate
	print '\nClicked at: x=',event.x,'  y=', event.y
	#reading R,G,B values
	Red,Green,Blue=frame[event.x,event.y]
	print 'red=',Red,'  green=',Green,'  blue=',Blue
	count=count+1
	red_sum=red_sum + Red
	green_sum=green_sum + Green
	blue_sum=blue_sum + Blue
	#calculating and printing mean
	if count==10:
		print '\nMean of red pixels= ',red_sum/10
		print 'Mean of green pixels= ',green_sum/10
		print 'Mean of blue pixels= ',blue_sum/10
		exit()
		
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
window = Tk()
window.geometry('500x500')
videoFigure = Figure(figsize=(5, 4), dpi=80)
axis1 = videoFigure.add_subplot(111)
axis1.set_title('Video frame')
canvas1 = FigureCanvasTkAgg(videoFigure, master=window)
widget=canvas1.get_tk_widget().place(x=10, y=10)
axis1.imshow(frame)

#initializing variables
count=0
red_sum=0
green_sum=0
blue_sum=0

		
	
canvas1.mpl_connect('button_press_event', click)
window.mainloop()
cap.release()
cv2.destroyAllWindows()



'''

import cv2
import numpy
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
window = Tk()
window.geometry('300x400')
videoFigure = Figure(figsize=(5, 4), dpi=80)
axis1 = videoFigure.add_subplot(111)
axis1.set_title('Video frame')
canvas1 = FigureCanvasTkAgg(videoFigure, master=window)
widget=canvas1.get_tk_widget().place(x=10, y=10)
axis1.imshow(frame)
count=0
add=0	
def display(count,add):
	global count
	global add
	count=count+1
	add=add + R
	
def click(event):
	global R
	print '\nClicked at: x=',event.x,'  y=', event.y
	R,G,B=frame[event.x,event.y]
	print 'red=',R,'  green=',G,'  blue=',B
	#print 'sum of red pixels= ',SUM
	display()

	
canvas1.mpl_connect('button_press_event', click)
print count
	
if count==3:
	print 'sum of red pixels= ',add

window.mainloop()
cap.release()
cv2.destroyAllWindows()

'''
