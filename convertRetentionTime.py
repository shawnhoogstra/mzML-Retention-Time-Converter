import pandas as pd
from scipy.interpolate import Akima1DInterpolator
import numpy as np
import PySimpleGUI as sg

def main():
    layout = [[sg.Text('Convert Retention Times')],
              [sg.Text('Reference File', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
              [sg.Text('MzML Data File', size=(15, 1)), sg.InputText(), sg.FileBrowse()],
              [sg.Text('Output Data File', size=(15, 1)), sg.Input(), sg.FileSaveAs()],
              [sg.Button('Convert'), sg.Exit()]]

    window = sg.Window('Retention Time Converter', layout)

    while True:
        event, values = window.Read()
        if event is None or event == 'Exit':
            break
        if event == 'Convert':
            reference_path, raw_files_path, save_file_path = values[0], values[1], values[2]
            convertFile(reference_path, raw_files_path, save_file_path)

    window.Close()


def convertFile(referenceFile, mzmlFile, save_file_path):

    #Open reference file and calculate spline function for RT conversion

    if (referenceFile.endswith('.csv') and mzmlFile.endswith('.mzML')):
        ## Calculate Spline Function
        data = pd.read_csv(referenceFile)

        index = data.iloc[:, 0].values
        ref_retention_time = data.iloc[:, 2].values
        cs = Akima1DInterpolator(ref_retention_time, index)



        #Open mzML file and convert retention times
        file = open(mzmlFile, "r")
        readFile = file.readlines()
        file.close()

        #Set up output file
        outFile = open(save_file_path, "w")


        #loop through mzML file
        while i < readFile.__len__():
            if "spectrum index=" in readFile[i]: #check if we are at the next spectrum
                tempStr = ""#temporary file for current spectrum info
                flag = False
                retentionTime = 0

                #Locate retention time Tag
                while flag == False: #flag to indicate end of spectrum
                    if "MS:1000016" in readFile[i]:
                        elements = readFile[i].split(" ")

                        #Grab Retention Time
                        flagValue = False #secondary flag for finding retention time
                        j = 0
                        while (flagValue == False):
                            if "value" in elements[j]:
                                flagValue = True
                                tempSplit = elements[j].split("\"")
                                retentionTime = float(tempSplit[1])
                                convRetentionTime = cs(retentionTime) #convert retention time

                                elements[j] = (tempSplit[0] + "\"" + str(convRetentionTime) + "\"")
                            j += 1

                        #turn array back into string
                        separator = " "
                        newElement = separator.join(elements)

                        tempStr = tempStr + newElement


                        i += 1

                    #end of spectrum flag, end
                    elif "</spectrum>" in readFile[i]:
                        tempStr = tempStr + readFile[i]
                        flag = True
                        i += 1
                        #end

                    #have not found end of spectrum or retention time flag: continue to scan
                    else:
                        tempStr = tempStr + readFile[i]
                        i += 1

                #write tempStr to file. contains converted spectrum info. ONLY include spectrums within spline function range.
                if (retentionTime >= np.amin(ref_retention_time) and retentionTime <= np.amax(ref_retention_time)):
                    outFile.write(tempStr)
                #on end  test RT and either save to final file or not if in range

            # write line to file, no spectrum info. (standard mzML info likely)
            else:
                outFile.write(readFile[i])
                i += 1


        outFile.close()
        sg.Popup('Conversion Complete')
    else:
        sg.PopupError(
            'Wrong data format. Please select a .csv file for the reference file and a .mzML file for the data file.')

main()