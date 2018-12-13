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
#        frame.pack()
        self.mainroot = master
        self.muellerData = {}
        self.muellerTemp = []
        
        
        
#        self.buttonQuit = tkint.Button(frame, text="QUIT", command=frame.quit)
#        self.buttonQuit.pack(side=tkint.LEFT)
        self.buttonOpen = tkint.Button(master, text="Open File",
                                        fg="black",command=self.openfile)
        
        self.buttonOpen.grid(row = 0, column = 0)
        
#        self.buttonAddPlot = tkint.Button(master, text="Add More Data", 
#                                            command=self.addMoreData)
#        
#        self.buttonAddPlot.grid(row = 0, column = 1)
##    
#        self.buttonAddSouth = tkint.Button(master, text="Add South", 
#                                           fg="blue", command=self.addSouth)
#        
#        self.buttonAddSouth.grid(row = 0, column = 2)
#        
        
        self.txtWindow = tkint.Label(master, text="Data Set Label").grid(row = 1, column = 0)
        self.fileString = tkint.StringVar()
        self.fileString.set("File: ")
        self.fileTextView = tkint.Label(master, textvariable = self.fileString).grid(row = 0, column = 1)
        
        self.e1 = tkint.Entry(master)
        self.e1.grid(row = 1, column=1)
        
        self.buttonLabelPlot = tkint.Button(master, text ='Show', 
                                            command = self.plotLabel)
        
        self.buttonLabelPlot.grid(row = 1, column = 2)
        self.buttonLabelPlot.config(state = tkint.DISABLED)
    def openfile(self):
        a = fd.askopenfilename(title = "Select Data Set", filetypes = (("dat files","*.dat"),("All files", "*.*")))

        
        
        self.muellerTemp.append(rwv.dataReader(a))
        
#        rwv.plotter(mueller1, name)
        
        self.buttonOpen.config(state = tkint.DISABLED)
        aarray = a.split("/")
        self.fileString.set("File: " + aarray[-1])
        self.buttonLabelPlot.config(state = tkint.NORMAL)
        
    def plotLabel(self):
        self.muellerData[self.e1.get()] = self.muellerTemp[0]
        if(plt.fignum_exists(1)):
            self.muellerPlot.addPlot(self.muellerTemp[0], self.e1.get())
        
        else:
            self.muellerPlot = mmp.plotter(self.muellerTemp[0], self.e1.get())
        self.muellerTemp.clear()
        self.buttonOpen.config(state = tkint.NORMAL)
        self.buttonLabelPlot.config(state = tkint.DISABLED)
        
        
#    def show_entry_fields(self, window , name: str, newdata: rwv.dataReader):
#        self.muellerData[name] = newdata
#        
        




        
root = tkint.Tk()

app = App(root)
app.frame.master.title("Mueller Matrix Data Analyzer")

root.mainloop()





