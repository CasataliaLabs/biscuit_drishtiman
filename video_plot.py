import cv2
from repeated_timer_video_plot import RepeatedTimer
from Tkinter import *
import pylab
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

#================================Functions==================================================
def video():

    global Gray_1 
    #global  cap
    ret, frame = cap.read()
    axis.imshow(frame)
    canvas.show()

    Gray_2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    Difference = abs(Gray_2 - Gray_1)
    Mean_value = numpy.mean(Difference)
    print Mean_value
    data = {'1':{'Mean Value': '{0:.3f}'.format(Mean_value)}}
    table.redrawTable()
    model.importDict(data)

    Gray_1 = Gray_2
    Values.append(Mean_value)
    Values.remove(Values[0])
    Plot[0].set_data(X_Axis, pylab.array(Values))
    canvas2.show()

    #if cv2.waitKey(1) & 0xFF == ord('q'):
     #   exit()


def video_start():
    t.start()

def video_stop():
    #cap.release()
    t.stop()
#================================Functions==================================================

#================================Main Program===============================================
cap = cv2.VideoCapture(0)
Gray_1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2GRAY)
t = RepeatedTimer(0.01,video)
Values = [0 for x in range(100)]
#===========================================================================================

#=================================GUI Section=============================================
root = Tk()
root.geometry('1000x700')

f = Figure(figsize=(4,4), dpi=50)
axis = f.add_subplot(111)
canvas = FigureCanvasTkAgg(f, master=root)
canvas.get_tk_widget().place(x=10,y=30)
frame2 = Frame(root)
frame2.place(x=20,y=300)
X_Axis = pylab.arange(0, 100, 1)
plotFigure = Figure(figsize=(4,4),dpi=50)
axis2 = plotFigure.add_subplot(111)
axis2.grid(True)
axis2.set_title("Mean value per Frame")
axis2.axis([0, 100, 0, 255])
Plot = axis2.plot(X_Axis, [0]*100, 'o-', color='r', markersize=6)

model = TableModel()
table = TableCanvas(frame2,model,height = 100,width=300)
model = table.model
table.createTableFrame()

canvas2 = FigureCanvasTkAgg(plotFigure, master=root)
canvas2.get_tk_widget().place(x=500,y=30)

b1 = Button(root,text="Start", bg='white', command=video_start).place(x=50,y=600)
b2 = Button(root,text="Stop", bg='white', command=video_stop).place(x=400,y=600)
root.mainloop()
#===========================================================================================
