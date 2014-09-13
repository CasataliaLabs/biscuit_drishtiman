import cv2
import numpy
import pylab
from repeated_timer import repeatedTimer
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def VideoPlot():
    frame = video.read(0)[1]
    axis1.imshow(frame)
    canvas1.show()
    #canvas1.get_tk_widget().place(x=10, y=10)


def GraphPlot():
    global gray1, values, meanValue, xAxis

    gray2 = cv2.cvtColor(video.read(0)[1], cv2.COLOR_BGR2GRAY)
    difference = abs(gray1 - gray2)
    meanValue = numpy.mean(difference)
    gray1 = gray2
    values.append(meanValue)
    values.remove(values[0])
    # changeInXAxis = pylab.arange(len(values)-100, len(values), 1)
    plotGraph[0].set_data(xAxis, pylab.array(values[-100:]))
    # axis2.axis([changeInXAxis.min(), changeInXAxis.max()+1, 0, 255])
    canvas2.show()
    #canvas2.get_tk_widget().place(x=430, y=10)


def TablePlot():
    tableValues=[['Mean frame', ' ', ' '], [meanValue, '', ''], ['', '', '']]
    table1 = axis3.table(cellText=tableValues, colWidths=[0.1]*3, loc='center right')
    table1.set_fontsize(30)
    table1.scale(3, 2)
    canvas3.show()
    #canvas3.get_tk_widget().place(x=10, y=350)


def StartButton():
    global timer1, timer2, timer3
    timer1 = repeatedTimer(.1, GraphPlot)
    timer2 = repeatedTimer(.1, VideoPlot)
    timer3 = repeatedTimer(.1, TablePlot)


def StopButton():
    timer1.stop()
    timer2.stop()
    timer3.stop()


def QuitButton():
    video.release()
    quit()


xAxis = pylab.arange(0, 100, 1)
yAxis = pylab.array([0]*100)

video = cv2.VideoCapture(0)
gray1 = cv2.cvtColor(video.read(0)[1], cv2.COLOR_BGR2GRAY)

window = Tk()
window.geometry('850x7000')
window.title('Test gui')

values = [0 for x in range(100)]

videoFigure = Figure(figsize=(5, 4), dpi=80)
axis1 = videoFigure.add_subplot(111)
axis1.set_title('Video frame')
canvas1 = FigureCanvasTkAgg(videoFigure, master=window)
canvas1.show()
canvas1.get_tk_widget().place(x=10, y=10)

plotFigure = Figure(figsize=(5, 4), dpi=80)
axis2 = plotFigure.add_subplot(111)
axis2.grid(True)
axis2.set_title("Mean value per Frame")
canvas2 = FigureCanvasTkAgg(plotFigure, master=window)
canvas2.show()
canvas2.get_tk_widget().place(x=420, y=10)
axis2.axis([0, 100, 0, 255])
plotGraph = axis2.plot(xAxis, yAxis, 'o-', color='r', markersize=2)
meanValue = 0

tableFigure = Figure(figsize=(5, 4), dpi=80)
axis3 = tableFigure.add_subplot(111)
axis3.set_title('Data table')
canvas3 = FigureCanvasTkAgg(tableFigure, master=window)
canvas3.show()
canvas3.get_tk_widget().place(x=10, y=350)

button1 = Button(window, text='Start', fg='green', command=StartButton).place(x=500, y=450)
button2 = Button(window, text='Stop', fg='red', command=StopButton).place(x=500, y=500)
button3 = Button(window, text='Quit', fg='black', bg='red', command=QuitButton).place(x=500, y=550)

window.mainloop()