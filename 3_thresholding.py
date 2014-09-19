
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
showinfo('','click on the biscuit 10 times')

#initializing variables
count=0
red_sum=0
green_sum=0
blue_sum=0
def click(event):
	global count,red_sum,green_sum,blue_sum
	print '\nClicked at: x=',event.x,'  y=', event.y
	Red,Green,Blue=frame1[event.x,event.y]
	print 'red=',Red,'  green=',Green,'  blue=',Blue
	count=count+1
	red_sum=red_sum + Red
	green_sum=green_sum + Green
	blue_sum=blue_sum + Blue

	if count==10:
		RedMean=red_sum/10
		GreenMean=green_sum/10
		BlueMean=blue_sum/10
		print '\nMean of red pixels= ',RedMean
		print 'Mean of green pixels= ',GreenMean
		print 'Mean of blue pixels= ',BlueMean

		#array of mean of 10 clicks
		MeanArray=numpy.array([RedMean,GreenMean,BlueMean])
		diff_frame = MeanArray-frame2
		abs_diff_frame=abs(diff_frame)
		threshold=abs_diff_frame<80
		r, g, b = threshold[:,:,0], threshold[:,:,1], threshold[:,:,2]
   		gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
		plt.imshow(gray)
		plt.show()
		exit()	
	
canvas1.mpl_connect('button_press_event', click)
window.mainloop()
cap.release()
cv2.destroyAllWindows()





