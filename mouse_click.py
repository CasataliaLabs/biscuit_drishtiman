
import cv2
import numpy
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

def click(event):
	print '\nClicked at: x=',event.x,'  y=', event.y
	R,G,B=frame[event.x,event.y]
	print 'red=',R,'  green=',G,'  blue=',B


window = Tk()
window.geometry('300x400')

videoFigure = Figure(figsize=(5, 4), dpi=80)
axis1 = videoFigure.add_subplot(111)
axis1.set_title('Video frame')
canvas1 = FigureCanvasTkAgg(videoFigure, master=window)
canvas1.mpl_connect('button_press_event', click)
widget=canvas1.get_tk_widget().place(x=10, y=10)
axis1.imshow(frame)
window.mainloop()

cap.release()
cv2.destroyAllWindows()





