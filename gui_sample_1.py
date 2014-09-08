#!/usr/bin/env python
import matplotlib 
#matplotlib.use('TkAgg')
import numpy
#from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

def destroy(e): sys.exit()

root = Tk.Tk()
root.wm_title("Embedding in TK")
#root.bind("<Destroy>", destroy)

button = Tk.Button(master=root, text='Quit', command=sys.exit)
button.pack(side=Tk.BOTTOM)

#Tk.mainloop()
