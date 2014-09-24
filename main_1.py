# Import modules
import sys
import time
import cv2
import numpy
import pylab
from repeated_timer import repeatedTimer
from Tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

'======================================================================='
'======================================================================='
# Function for display Video 
def VideoPlot():
    ret,frame = video.read(0)
    #~ axes1.imshow(frame)
    showFrame.set_array(frame)
    canvas1.draw()
    #canvas1.get_tk_widget().place(x=10, y=10)

# Function for display graph
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
    canvas2.draw()
    #canvas2.get_tk_widget().place(x=430, y=10)

# Function for display table
def TablePlot():
    global status
						#~ data = {'Mean Value':{'1': '{0:.3f}'.format(meanValue)}, 'Status':{'2': '{0:.3f}'.format(meanValue)}}
						#~ table.redrawTable()
						#~ model.importDict(data)
    tableValues=[['Status', 'Mean FrameValue ', ' '], [status, meanValue, ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', '']]
    table1 = axes3.table(cellText=tableValues, colWidths=[0.1]*3, loc='center left')
    table1.set_fontsize(30)
    table1.scale(3, 2)
    canvas3.draw()
    #~ #canvas3.get_tk_widget().place(x=10, y=350)
'======================================================================='
'======================================================================='
# Buttons
# Start Button
def StartButton():
    global timer1, timer2, timer3, status
    timer1.start()
    timer2.start()
    timer3.start()
    status = 'running'
    

# Stop Button
def StopButton():
	status = 'stop'
	timer1.stop()
	timer2.stop()
	timer3.stop()
    

# Quit Button
def QuitButton():
    video.release()
    quit()

'======================================================================='
'======================================================================='

xAxis = pylab.arange(0, 100, 1)
yAxis = pylab.array([0]*100)
 # Video initializing
video = cv2.VideoCapture(0)
# Frame convert into grayscale
gray1 = cv2.cvtColor(video.read(0)[1], cv2.COLOR_BGR2GRAY)

# Make a window
window = Tk()
window.geometry('800x700')
window.title('Test gui')

# 
values = [0 for x in range(100)]
# Make a videoFigure in window
videoFigure = Figure(figsize=(5, 4), dpi=80)
axes1 = videoFigure.add_subplot(111)
axes1.set_title('Video frame')

ret, frame = video.read(0)
showFrame = axes1.imshow(frame)
# Make a canvas on VideoFigure
canvas1 = FigureCanvasTkAgg(videoFigure, master=window)
canvas1.show()  # Display canvas1
canvas1.get_tk_widget().place(x=10, y=10)   # canvas1 place in location

# Make a plotFigure in window
plotFigure = Figure(figsize=(5, 4), dpi=80)
axes2 = plotFigure.add_subplot(111)
axes2.grid(True)
axes2.set_title("Mean value per Frame")
# Make canvas2
canvas2 = FigureCanvasTkAgg(plotFigure, master=window)
canvas2.show()
canvas2.get_tk_widget().place(x=10, y=350)
axes2.axis([0, 100, 0, 255])
# Plot graph in axes2
plotGraph = axes2.plot(xAxis, yAxis, 'o-', color='r', markersize=2)
meanValue = 0

# make tableaFigure
				#~ tableFrame = Frame(window)
				#~ tableFrame.place(x=450, y=10)
				#~ model = TableModel()
				#~ table = TableCanvas(tableFrame,model,height = 600,width=300)
				#~ model = table.model
				#~ table.createTableFrame()
				#~ meanValue1 = 'hai'
				#~ data = {'Mean Value':{'1': '{0:.3f}'.format(meanValue1)}, 'Status':{'2': '{0:.3f}'.format(meanValue1)}}
				#~ table.redrawTable()
				#~ model.importDict(data)

tableFigure = Figure(figsize=(5, 5), dpi=80)
axes3 = tableFigure.add_subplot(111)
axes3.set_title('Data table')

tableValues=[['Status', 'Mean FrameValue ', ' '], ['Stop', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', '']]
table1 = axes3.table(cellText=tableValues, colWidths=[0.1]*3, loc='center left')
table1.set_fontsize(50)
table1.scale(3, 2)

#~ # Make canvas3 on tableFigure
canvas3 = FigureCanvasTkAgg(tableFigure, master=window)
canvas3.show()
canvas3.get_tk_widget().place(x=420, y=10)



# Create buttons
button1 = Button(window, text='Start', fg='green', command=StartButton).place(x=500, y=650)
button2 = Button(window, text='Stop', fg='red', command=StopButton).place(x=600, y=650)
button3 = Button(window, text='Quit', fg='black', bg='red', command=QuitButton).place(x=700, y=650)
# Create timers
timer1 = repeatedTimer(.1, VideoPlot)
timer2 = repeatedTimer(.1, GraphPlot)
timer3 = repeatedTimer(.1, TablePlot)

# main loop
window.mainloop()
