# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:43:11 2018

@author: rigoc
"""

from tkinter import filedialog as fd
import tkinter as tkint
import ReadWoollamVase as rwv
import matplotlib.pyplot as plt
import MMplotter as mmp

class App:
    def __init__(self, master):
        """Create the buttons"""
        self.frame = tkint.Frame(master)
        self.mainroot = master
        self.muellerData = {}
        self.muellerTemp = []
        self.buttonOpen = tkint.Button(master, text="Open File",
                                        fg="black",command=self.openfile)
        
        self.buttonOpen.grid(row = 0, column = 0)
        

        
        self.labelTextView = tkint.Label(master, text="Data Set Label").grid(row = 1, column = 0)
        
        self.openedFileString = tkint.StringVar()
        self.openedFileString.set("File: ")
        
        self.openedFileTextView = tkint.Label(master, textvariable = self.openedFileString)
        self.openedFileTextView.grid(row = 0, column = 1)
        
        self.labelTextEditor = tkint.Entry(master)
        self.labelTextEditor.grid(row = 1, column=1)
        
        self.buttonPlot = tkint.Button(master, text ='Plot!', 
                                            command = self.plotLabel)
        
        self.buttonPlot.grid(row = 1, column = 2)
        self.buttonPlot.config(state = tkint.DISABLED)
        
    def openfile(self):
        a = fd.askopenfilename(title = "Select Data Set", filetypes = (("dat files","*.dat"),("All files", "*.*")))

        
        
        self.muellerTemp.append(rwv.dataReader(a))
        
        
        self.buttonOpen.config(state = tkint.DISABLED)
        aarray = a.split("/")
        self.openedFileString.set("File: " + aarray[-1])
        self.buttonPlot.config(state = tkint.NORMAL)
        
    def plotLabel(self):
        self.muellerData[self.labelTextEditor.get()] = self.muellerTemp[0]
        if(plt.fignum_exists(1)):
            self.muellerPlot.addPlot(self.muellerTemp[0], self.labelTextEditor.get())
        
        else:
            self.muellerPlot = mmp.plotter(self.muellerTemp[0], self.labelTextEditor.get())
        self.muellerTemp.clear()
        self.buttonOpen.config(state = tkint.NORMAL)
        self.buttonPlot.config(state = tkint.DISABLED)
        
        



        
root = tkint.Tk()

app = App(root)
app.frame.master.title("Mueller Matrix Data Analyzer")

root.mainloop()





