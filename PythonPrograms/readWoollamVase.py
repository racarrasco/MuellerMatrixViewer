# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 19:42:46 2018

@author: rigoc

WVASE32  mueller matrix data set reader and plotter
organizes the data in to multiple dictionaries (dictionary)
"""
import numpy as np
import matplotlib.pyplot as plt

"""Reading  the mueller matrix data"""
class dataReader:
     def __init__(self, filename):
        self.file = open(filename, "r")     
        """The user's comment"""
        self.comment = self.file.readline()
        """The measurement parameters"""
        self.info = self.file.readline()
        """The unit of energy"""
        self.unit = self.file.readline()
        """Reads in the ellipsometer type from the information"""
        self.ellipsometerType = int(self.info[28])
        self.rows = 0
        self.cols = 0
        if(self.ellipsometerType == 3):
            self.rows = 4
            self.cols = 3
        elif(self.ellipsometerType == 5):
            self.rows = 3
            self.cols = 4
            self.file.readline()
        
        theElements = []
        energy = []
        data1 = [] #the mueller matrix element
        data2 = [] #repeated mueller matrix element
        error1 = [] #error in mueller matrix element
        error2 = []
        """Begin reading the data"""
        for line in self.file.readlines():
            data = line.strip().split("\t")
            theElements.append(data[0].strip()) #label of the row
            energy.append(float(data[1])) #energy 
            data1.append(float(data[3])) #mueller matrix element or psi
            
            
            if(data[0].strip()!= 'qJ' ): 
                data2.append(float(data[4])) # repeated mueller matrix element or delta
                error1.append(float(data[5])) # error in mueller matrix element
                error2.append(float(data[6]))# error in other result
                
            else: #Jones Matrix quality factor
                error1.append(float(data[4]))
                
        if self.unit == "1/cm\n": #Convert 1/cm to eV
            energy = np.array(energy)
            energy = energy/ 8065.6
            
        """Begin interpreting the data and creating the mueller matrix data structure""" 
        """A dictionary that contains each element and data type (ie: M12, AnE, qJ...)"""
        """IRVASE elements: MM12, MM13, MM21, MM22, MM23, MM31, MM32, MM33, MM41,MM42, MM43 
        V-VASE elements: MM12, MM13, MM14, MM21, MM22, MM23, MM24, M31, M32, M33, M34"""
        self.mElementNames = []
        self.MplotTitles = []
        
        for row in range(int(self.rows)):
            for col in range(int(self.cols)):
                self.mElementNames.append("mm"+str(row+1) + str(col+1))
                self.MplotTitles.append("M" + str(row+1) + str(col+1))


        """Remove the M11 element"""
        del self.mElementNames[0]
        del self.MplotTitles[0]
        
        self.otherElements = ["AnE","Asp","Aps"]

        self.MMenergy = {}
        self.MMResult1 = {}
        self.MMResult2 = {}     
        self.MMerror1 = {}
        self.MMerror2 = {}
        self.MMtitle = {}
        
        """Takes the the mueller matrix elements"""
        
        for index, element in enumerate(self.mElementNames):
        #    print(element == theElements[0])
            thaEnergy = [energy[index] for index, value 
                         in enumerate(theElements) if value == element] 
            """The data point to the corresponding energy value"""
            thaelementResult1 = [data1[index] for index, value 
                                 in enumerate(theElements) if value == element]
            
            """Add the array to the dictionary for the element, so 
            MMenergy["mm12"] will return an array of energies corresponding to 
            the mueller matrix element "M12" """
            self.MMenergy[element] = thaEnergy
            self.MMResult1[element] = thaelementResult1
           
            self.MMtitle[element] = self.MplotTitles[index]
            thaelementResult2 = [data2[index] for index, value 
                                 in enumerate(theElements) if value == element]
            self.MMResult2[element] = thaelementResult2
                
            thaerror1 = [error1[index] for index, value 
                         in enumerate(theElements) if value == element]
            self.MMerror1[element] = thaerror1
                
            thaerror2 = [error2[index] for index, value 
                         in enumerate(theElements) if value == element]
            self.MMerror2[element] = thaerror2
            
            """Takes the relfectance ratios"""
        for index, element in enumerate(self.otherElements):
            thaEnergy = [energy[index] for index, value 
                         in enumerate(theElements) if value == element] 

            thaEnergy = [energy[index] for index, value 
                         in enumerate(theElements) if value == element] 
            thaelementResult1 = [data1[index] for index, value 
                                 in enumerate(theElements) if value == element]
            
            self.MMenergy[element] = thaEnergy
            self.MMResult1[element] = thaelementResult1
           
           
            thaelementResult2 = [data2[index] for index, value 
                                 in enumerate(theElements) if value == element]
            self.MMResult2[element] = thaelementResult2
                
            thaerror1 = [error1[index] for index, value 
                         in enumerate(theElements) if value == element]
            self.MMerror1[element] = thaerror1
                
            thaerror2 = [error2[index] for index, value 
                         in enumerate(theElements) if value == element]
            self.MMerror2[element] = thaerror2
        """Read the jones quality factor which is formatted differently"""
        jonesEnergy = [energy[index] for index, value in enumerate(theElements) 
        if value == "qJ"]
        
        jonesValue = [data1[index] for index, value in enumerate(theElements) 
        if value == "qJ"]   
        
        jonesErr = [error1[index] for index, value in enumerate(theElements) 
        if value == "qJ"]
        self.MMenergy["qJ"] = jonesEnergy
        self.MMResult1["qJ"] = jonesValue
        self.MMerror1["qJ"] = jonesErr



class plotter():
    def __init__(self, muellerData: dataReader, color:str, legend: str):
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
        psiDelEnergy = muellerData.MMenergy["AnE"]
        psi = muellerData.MMResult1["AnE"] 
        delta = muellerData.MMResult2["AnE"] 
        
        jonesEnergy = muellerData.MMenergy["qJ"]
        jonesValue = muellerData.MMResult1["qJ"]
        
        
        self.psiDelax.plot(psiDelEnergy, psi, color + '-', 
                           label = legend, linewidth = 1.0)
        self.psiDelax.set_ylabel('$\psi$')
        self.psiDelax.set_xlabel('Photon Energy (eV)')
        self.psiDelax.tick_params(which = "both", direction = "in")
        self.psiDelax.legend(frameon = False)
        
        self.psiDelax2.plot(psiDelEnergy, delta, color+ '--', linewidth = 1.0)
        self.psiDelax2.set_ylabel('$\Delta$')
        self.psiDelax2.tick_params(which = "both", direction = "in")
        
        
        self.jonesax.plot(jonesEnergy, jonesValue, color +'-', 
                          label = legend, linewidth = 1.0)
        self.jonesax.set_xlabel('Photon Energy (eV)')
        self.jonesax.set_ylabel('Jones Quality Factor')
        self.jonesax.tick_params(which = "both", direction = "in")
        self.jonesax.legend(frameon = False)
        
        """Finally, populate the subplots  with the corresponding mueller matrix data"""
        for index, element in enumerate(muellerData.mElementNames):
#            self.axmuellerarray[index].errorbar(muellerData.MMenergy[element], 
#            muellerData.MMResult1[element], yerr = muellerData.MMerror1[element])
#            print(index, element)
            self.axmuellerarray[index].plot(muellerData.MMenergy[element], 
                               muellerData.MMResult1[element], color + '-', 
                               label = legend, linewidth = 1.0)
            self.axmuellerarray[index].set_title(muellerData.MMtitle[element])
            self.axmuellerarray[index].tick_params(which = "both", direction ="in")
        handles, labels = self.axmuellerarray[0].get_legend_handles_labels()
        self.legendplot.legend(handles, labels, frameon = False, loc = 'center') 
               
    def addPlot(self, moreData: dataReader, color: str, legend: str):
        """allows user to plot multiple data sets in the same figure"""
        for index, element in enumerate(moreData.mElementNames):
#            self.axmuellerarray[index].errorbar(moreData.MMenergy[element], moreData.MMResult1[element], yerr = moreData.MMerror1[element])
            self.axmuellerarray[index].plot(moreData.MMenergy[element],
                               moreData.MMResult1[element],
                               color + '-', label = legend, linewidth = 1.0)
            
        self.psiDelax.plot(moreData.MMenergy["AnE"], 
                           moreData.MMResult1["AnE"], 
                           color + '-', label = legend, linewidth = 1.0)
        
        self.psiDelax2.plot(moreData.MMenergy["AnE"], 
                            moreData.MMResult2["AnE"], 
                            color + '--', linewidth = 1.0)
        
        self.jonesax.plot(moreData.MMenergy["qJ"], 
                          moreData.MMResult1["qJ"], 
                          color + '-', label = legend, linewidth = 1.0)
        
        self.psiDelax.legend(frameon = False)
        self.jonesax.legend(frameon = False)
        handles, labels =self.axmuellerarray[0].get_legend_handles_labels()
        self.legendplot.legend(handles, labels, frameon = False, loc = 'center')
