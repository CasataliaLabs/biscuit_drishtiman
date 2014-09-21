
import cv2
import numpy
import matplotlib.pyplot as plt
from Tkinter import *
from tkMessageBox import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

cap = cv2.VideoCapture(0)
ret, frame1 = cap.read()
ret,frame2 =cap.read()
window = Tk()
window.title('Biscuit frame')
window.geometry('500x400')

#Reference Plot
ReferenceFigure = Figure(figsize=(5, 4), dpi=80)
axis1 = ReferenceFigure.add_subplot(111)
axis1.set_title('REFERENCE FRAME')
canvas1 = FigureCanvasTkAgg(ReferenceFigure, master=window)
widget=canvas1.get_tk_widget().place(x=10, y=10)
axis1.imshow(frame1)

#initializing variables
count=0
red=[]
green=[]
blue=[]
frame_dup = numpy.ones(frame1.shape)
def click(event):
	global count,red,green,blue
	print '\nClicked at: x=',event.x,'  y=', event.y
	Red,Green,Blue=frame1[event.x,event.y]
	red.append(Red)
	green.append(Green)
	blue.append(Blue)
	Red,Green,Blue=frame1[event.x,event.y]
	print Red, Green, Blue
	red_min, red_max = numpy.min(red), numpy.max(red) 
	green_min, green_max = numpy.min(green), numpy.max(green)
	blue_min, blue_max = numpy.min(blue), numpy.max(blue)
	count=count+1


	if count==3:
		print 'red=',red_min, red_max,'  green=',green_min, green_max,'  blue=',blue_min, blue_max
		frame_dup[:,:,0] = (frame1[:,:,0] < red_max)*frame1[:,:,0]
		frame_dup[:,:,0] = (frame_dup[:,:,0] > red_min)*1
		frame_dup[:,:,1] = (frame1[:,:,1] < green_max)*frame1[:,:,1]
		frame_dup[:,:,1] = (frame_dup[:,:,1] > green_min)*1
		frame_dup[:,:,2] = (frame1[:,:,2] < blue_max)*frame1[:,:,2]
		frame_dup[:,:,2] = (frame_dup[:,:,2] > blue_min)*1 
		frame_dup1 = frame_dup[:,:,0]+frame_dup[:,:,1]+frame_dup[:,:,2]
		frame_dup1 = frame_dup1==3	
		print frame_dup1
		print numpy.min(frame_dup1),numpy.max(frame_dup1),frame_dup1.shape
		plt.imshow(frame_dup1)
		#~ plt.imshow(frame_dup[:,:,1])
		#~ plt.imshow(frame_dup[:,:,2])
		plt.show()
		exit()	
	
canvas1.mpl_connect('button_press_event', click)
window.mainloop()
cap.release()
cv2.destroyAllWindows()





