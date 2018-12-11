# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 23:43:11 2018

@author: rigoc
"""

from tkinter import filedialog as fd
import tkinter as tkint
import readWoollamVase as rwv
class App:
    
    def __init__(self, master):
        """Create the buttons"""
        frame = tkint.Frame(master)
        frame.pack()
        self.muellerData = {}
#        self.buttonQuit = tkint.Button(frame, text="QUIT", command=frame.quit)
#        self.buttonQuit.pack(side=tkint.LEFT)
        self.buttonOpen = tkint.Button(frame, text="Open (No B Field)",
                                        fg="black",command=self.openfile)
        self.buttonOpen.pack(side=tkint.LEFT)
        
        self.buttonAddNorth = tkint.Button(frame, text="Add North", 
                                           fg="red", command=self.addNorth)
        self.buttonAddNorth.pack(side=tkint.LEFT)
    
        self.buttonAddSouth = tkint.Button(frame, text="Add South", 
                                           fg="blue", command=self.addSouth)
        self.buttonAddSouth.pack(side=tkint.LEFT)

    def openfile(self):
        a = fd.askopenfilename(title = "Select No B Field MM", filetypes = (("dat files","*.dat"),("All files", "*.*")))
        
        mueller1 = rwv.dataReader(a)
        self.muellerData["noB"] = mueller1
        self.plot1 = rwv.plotter(mueller1, 'k','B =  0.0 T')
        self.buttonOpen.config(state = tkint.DISABLED)

        
    def addNorth(self):
        nextFileName = fd.askopenfilename(title = "Select North B Field MM", filetypes = (("dat files","*.dat"),("All files", "*.*")))
        muellernext = rwv.dataReader(nextFileName)
        self.muellerData["North"] = muellernext
        self.plot1.addPlot(muellernext, 'r', 'B =  0.7 T')
        self.buttonAddNorth.config(state = tkint.DISABLED)
        
    def addSouth(self):
        nextFileName = fd.askopenfilename(title = "Select South B Field MM", filetypes = (("dat files","*.dat"),("All files", "*.*")))
        muellernext = rwv.dataReader(nextFileName)
        self.muellerData["South"] = muellernext
        self.plot1.addPlot(muellernext, 'b', 'B = -0.7 T')
        self.buttonAddSouth.config(state = tkint.DISABLED)
        
root = tkint.Tk()

app = App(root)

root.mainloop()





