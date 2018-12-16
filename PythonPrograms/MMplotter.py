# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:03:37 2018

@author: rigoc
"""
import ReadWoollamVase as rwv
import matplotlib.pyplot as plt

class plotter():
    def __init__(self, muellerData: rwv.dataReader, legend: str):
        """Takes in a mueller matrix data set and plots the elements along 
        with the error bars"""
        rows = muellerData.rows
        cols = muellerData.cols

        self.muellerPlot = plt.figure("Mueller Matrix")
        self.axmuellerarray = []
        self.legendArray = []
        
        self.psiDelPlot = plt.figure("Ellipsometric angles")
        self.psiDelax = self.psiDelPlot.add_subplot(1,1,1)
        
        self.psiDelax2 = self.psiDelax.twinx()
        
        self.jonesPlot = plt.figure("Jones Quality Factor")
        self.jonesax = self.jonesPlot.add_subplot(1,1,1)
        
        
        """Create a 4X3 matrix of subplots, not including the first element (M11) 
        of the matrix"""
        self.legendplot = self.muellerPlot.add_subplot(rows, cols, 1)
        self.legendplot.axis('off')
        for i in range(2,13):
            self.axmuellerarray.append(self.muellerPlot.add_subplot(rows,cols,i))
        self.muellerPlot.subplots_adjust(hspace = 0.5)
        self.muellerPlot.text(0.5, 0.04, 'Photon Energy (eV)', ha='center')
        self.muellerPlot.text(0.04, 0.5, 'Mueller Matrix Elements', 
                              va='center', rotation='vertical')
        for j in range(len(muellerData.angles)):
            legendFix = legend
            if(len(muellerData.angles) > 1):
                legendFix = legend + "_" + str(muellerData.angles[j])
                
            psiDelEnergy = muellerData.MMenergy[j]["AnE"]
            psi = muellerData.MMResult1[j]["AnE"] 
            delta = muellerData.MMResult2[j]["AnE"] 
            
            jonesEnergy = muellerData.MMenergy[j]["qJ"]
            jonesValue = muellerData.MMResult1[j]["qJ"]
            
        
            self.psiDelax.plot(psiDelEnergy, psi, '-', 
                               label = legendFix, linewidth = 1.0)
            self.psiDelax.set_ylabel('$\psi$')
            self.psiDelax.set_xlabel('Photon Energy (eV)')
            self.psiDelax.tick_params(which = "both", direction = "in")
            self.psiDelax.legend(frameon = False)
            
            self.psiDelax2.plot(psiDelEnergy, delta,'--', linewidth = 1.0)
            self.psiDelax2.set_ylabel('$\Delta$')
            self.psiDelax2.tick_params(which = "both", direction = "in")
            
            
            self.jonesax.plot(jonesEnergy, jonesValue,'-', 
                              label = legendFix, linewidth = 1.0)
            self.jonesax.set_xlabel('Photon Energy (eV)')
            self.jonesax.set_ylabel('Jones Quality Factor')
            self.jonesax.tick_params(which = "both", direction = "in")
            self.jonesax.legend(frameon = False)
            
            """Finally, populate the subplots  with the corresponding mueller matrix data"""
            for index, element in enumerate(muellerData.mElementNames):
    #            self.axmuellerarray[index].errorbar(muellerData.MMenergy[element], 
    #            muellerData.MMResult1[element], yerr = muellerData.MMerror1[element])
    #            print(index, element)
                self.axmuellerarray[index].plot(muellerData.MMenergy[j][element], 
                                   muellerData.MMResult1[j][element], '-', 
                                   label = legendFix, linewidth = 1.0)
                if j == 0:
                    self.axmuellerarray[index].set_title(muellerData.MMtitle[j][element])
                    self.axmuellerarray[index].tick_params(which = "both", direction ="in")
                    
        handles, labels = self.axmuellerarray[0].get_legend_handles_labels()
        self.legendplot.legend(handles, labels, frameon = False, loc = 'center') 
               
    def addPlot(self, moreData: rwv.dataReader, legend: str):
        """allows user to plot multiple data sets in the same figure"""
        for j in range(len(moreData.angles)):
            legendFix = legend
            if(len(moreData.angles) > 1):
                legendFix = legend + "_" + str(moreData.angles[j])
        
            for index, element in enumerate(moreData.mElementNames):
    #            self.axmuellerarray[index].errorbar(moreData.MMenergy[element], moreData.MMResult1[element], yerr = moreData.MMerror1[element])
                self.axmuellerarray[index].plot(moreData.MMenergy[j][element],
                                   moreData.MMResult1[j][element],
                                    '-', label = legendFix, linewidth = 1.0)
                
            self.psiDelax.plot(moreData.MMenergy[j]["AnE"], 
                               moreData.MMResult1[j]["AnE"], 
                                '-', label = legendFix, linewidth = 1.0)
            
            self.psiDelax2.plot(moreData.MMenergy[j]["AnE"], 
                                moreData.MMResult2[j]["AnE"], 
                                 '--', linewidth = 1.0)
            
            self.jonesax.plot(moreData.MMenergy[j]["qJ"], 
                              moreData.MMResult1[j]["qJ"], 
                                  '-', label = legendFix, linewidth = 1.0)
        
        self.psiDelax.legend(frameon = False)
        self.jonesax.legend(frameon = False)
        handles, labels =self.axmuellerarray[0].get_legend_handles_labels()
        self.legendplot.legend(handles, labels, frameon = False, loc = 'center')