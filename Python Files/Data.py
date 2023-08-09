import os
import csv
import numpy as np

# #### INPUT FILES
#TransIV ="C:\MED-PC IV\MPC\LF_20200520_cue&pellet cdtg.MPC"
#MEDDATA = "C:\MED-PC IV\Data\!2020-06-26"
#
# #### OUTPUT FILES
# outputTXTFilename = "TEST OUTPUT TXT.txt"  #####will need to get thi info from the user
# outputCSVFilename = "TEST OUTPUT CSV.csv" ###will need to get this infor from user

#### MEDPC DATA INFO
header = 13
gap_btw_session = 3 ###Might need to change

headerArrayTitle = []
headerArrayVals = []

def file_len(filename):
    with open(filename) as f:
        for i, line in enumerate(f):
            pass
    return i + 1

def create_output_file_txt(filename):
    output_file = open(filename,"x")
    output_file.close()

def create_output_file_csv(filename):
    output_file = open(filename,"x")
    output_file.close()


def copy_sealed_data(filenameIN, filenameIN2, filenameOUT,SessionTime):
    headerArray = [0,0,0,0,0,0,0,0,0]
    count = 0

    rowCount = 0
    rowCount2 = 1
    colCount = 0
    VarTitleCounter = 0


    ####Create matrix
    CM = create_matrix(filenameIN, filenameIN2)
    D = CM[0]
    rowsMatrix = CM[1]
    numArrays = CM[2]

    ArrayTiltelCol = 9 +26 - numArrays


    ####Read Trans IV
    RT = read_transIV(filenameIN2)
    VarsTitles = RT[2]
    ArrayTitles = RT[4]
    Vars = RT[1]



    with open(filenameIN) as input:
        with open(filenameOUT +".txt", "a") as output:
            for i, row in enumerate(input):
                output.write(row)


                ##### Start/End Date and Subject Output to Matrix
                if i in range(4, 7):
                    D[rowCount, colCount] = (row.strip("\n").split(": "))[0]
                    rowCount += 1
                    ####Fill all rows of the Start/End Date and Subject columns with their single value
                    for k in range(0, rowsMatrix -2):
                        #print(rowCount,colCount,(row.strip("\n").split(": "))[1])
                        D[rowCount, colCount] = (row.strip("\n").split(": "))[1]
                        rowCount += 1

                    rowCount = 0
                    colCount += 1

                ###### Remaining Header lines to Matrix
                if i in range(7, header):
                    D[rowCount, colCount] = (row.strip("\n").split(": "))[0]
                    rowCount += 1
                    D[rowCount, colCount] = (row.strip("\n").split(": "))[1]

                    colCount += 1
                    rowCount = 0

                    ##ADDED 10/23 for total session time adding to csv file
                    if i == 12:
                        D[rowCount, colCount] = "Total Session Time (mins)"
                        rowCount += 1
                        D[rowCount, colCount] = SessionTime
                        colCount += 1
                        rowCount = 0

                UnusedVar = False  #### added for unassigned vars


                ##### Variables: Output
                if len(row.split()) == 2 and row[0] != " " and i not in range(0, header):   ### changed range from 4 to 0

                    #### Check to see if Var in Header was unused from Trans IV and output to Matrix
                    for n, line in enumerate(Vars):

                        if (row.strip("\n").split(": "))[0].strip(" ") == line:
                            UnusedVar = True

                    if UnusedVar == False:
                        D[rowCount, colCount] = (row.strip("\n").split(": "))[0].strip(" ") + ":"
                        D[rowCount + 1, colCount] = 0
                        colCount += 1
                        rowCount = 0

                    if UnusedVar == True:
                        D[rowCount, colCount] = (row.strip("\n").split(": "))[0].strip(" ") + ":" + VarsTitles[VarTitleCounter]
                        D[rowCount + 1, colCount] = (row.strip("\n").split(": "))[1].strip(" ")
                        colCount += 1
                        rowCount = 0
                        VarTitleCounter += 1

                #### Arrays: Find the line location for the beginning of each array
                if len(row.strip("\n")) == 2:
                    #arrayLocations.append(i)
                    rowCount2 += 1
                    colCount = ArrayTiltelCol
                    D[rowCount2, colCount] = row.strip("\n").strip(":")[0] + ":" + ArrayTitles[rowCount2-2]
                    colCount += 1

                if i > (header + (26-numArrays) -1) and len(row.strip("\n")) != 2:
                    rowSplit = row.split()
                    del rowSplit[0]  ###remove counter string
                    for k, col in enumerate(rowSplit):
                        D[rowCount2, colCount] = col
                        colCount += 1


            for i in range(0,gap_btw_session):
                output.write("\n")          ###create spaces between sessions

            #### Write to CSV
            with open(filenameOUT+".csv", "a", newline = '') as csvfile:
                csvwriter = csv.writer(csvfile)
                for i in range(0, rowsMatrix):
                    csvwriter.writerow(D[i])
    ###clear input file
    #open(filenameIN,"w").close()
    os.remove(filenameIN)




def remove_zeros(filenameIN,filenameIN2,filenameOUT):
    arrayLocations = []
    largestArray = []


    rowCount = 0
    colCount = 0

    ####Create matrix
    CM = create_matrix(filenameIN,filenameIN2)
    D = CM[0]
    rowsMatrix = CM[1]

    ####Read Trans IV
    RT = read_transIV(filenameIN2)
    VarsTitles = RT[2]
    ArrayTitles = RT[4]
    Vars = RT[1]

##### get array beginning locations
    with open(filenameIN) as f:
         with open(filenameOUT +".txt", "a") as output:
             f_enumerated = enumerate(f)
             for i, row in f_enumerated:


                  #### Entire Header Output to txt
                  if i in range(0,header):
                     output.write(row)


                  ##### Start/End Date and Subject Output to Matrix
                  if i in range (4,7):
                     D[rowCount,colCount] = (row.strip("\n").split(": "))[0]

                     ####Fill all rows of the Start/End Date and Subject columns with their single value
                     for k in range(0,rowsMatrix-2):
                        rowCount += 1
                        D[rowCount,colCount] = (row.strip("\n").split(": "))[1]

                     rowCount = 0
                     colCount += 1

                  ###### Remaining Header lines to Matrix
                  if i in range(7,header):
                      D[rowCount,colCount] = (row.strip("\n").split(": "))[0]
                      rowCount += 1
                      D[rowCount,colCount] = (row.strip("\n").split(": "))[1]

                      colCount += 1
                      rowCount = 0



                  UnusedVar = False #### added for unassigned vars
                  VarTitleCounter = 0

                  ##### Variables: Output to TXT
                  if len(row.split()) == 2 and row[0] != " " and i not in range(4,header):  ####  changed from elif
                      output.write(row)


                      #### Check to see if Var in Header was unused from Trans IV and output to Matrix
                      for n, line in enumerate(Vars):

                          if (row.strip("\n").split(": "))[0].strip(" ") == line:
                              UnusedVar = True

                      if UnusedVar == False:
                        D[rowCount, colCount] = (row.strip("\n").split(": "))[0].strip(" ") + ":"
                        D[rowCount + 1, colCount] = 0
                        colCount += 1
                        rowCount = 0

                      if UnusedVar == True:
                        D[rowCount, colCount] = (row.strip("\n").split(": "))[0].strip(" ") + ":" + VarsTitles[VarTitleCounter]
                        D[rowCount + 1, colCount] = (row.strip("\n").split(": "))[1].strip(" ")
                        colCount += 1
                        rowCount =0
                        VarTitleCounter += 1


                  #### Arrays: Find the line location for the beginning of each array
                  if len(row.strip("\n")) == 2:
                      arrayLocations.append(i)
                      D[rowCount+2, colCount] = row.strip(":").strip("\n")[0] + ":" + ArrayTitles[rowCount-2]
                      rowCount += 1

             rowCount = 2
             ArrayTiltelCol = colCount + 1
             colCount = ArrayTiltelCol

             #### Find last non-zero row for each array
             for j in range(0,len(arrayLocations)):
                    lastNonzero = [0,0]
                    allZeros = True

                    for i, row in enumerate(open(filenameIN)):

                        #### Last Array
                        if j == len(arrayLocations)-1:
                            if i in range(int(arrayLocations[j])+1,int(file_len(filenameIN)-1)):
                                rowSplit = row.split()
                                del rowSplit[0]  ####remove counter string
                                for k, col in enumerate(rowSplit):
                                    if col != "0.000":
                                        lastNonzero[0] = i
                                        lastNonzero[1] = k
                                        allZeros = False

                        ### All Arrays except for the last one
                        elif i in range(int(arrayLocations[j])+1, int(arrayLocations[j+1])):
                                rowSplit = row.split()
                                del rowSplit[0]   ###remove counter string
                                for k, col in enumerate(rowSplit):
                                    if col != "0.000":
                                        lastNonzero[0] = i
                                        lastNonzero[1] = k
                                        allZeros = False
                    ##### Case when Array is filled with zeros
                    if  allZeros:
                        lastNonzero[0] = arrayLocations[j]


                    #### Use last non-zero row for each array to output to TXT and Matrix
                    count = 0
                    for i, row in enumerate(open(filenameIN)):

                        if i in range(arrayLocations[j], lastNonzero[0]+1):
                            output.write(row)
                            rowSplit = row.split()
                            del rowSplit[0]  ###remove counter string

                            for k, col in enumerate(rowSplit):
                                D[rowCount, colCount] = col
                                colCount += 1
                            count += 1



                        if j == len(arrayLocations) -1 and lastNonzero[0] < arrayLocations[j]:
                            if i >= arrayLocations[j]:
                                output.write(row)
                                rowSplit = row.split()
                                del rowSplit[0]  ###remove counter string

                                for k, col in enumerate(rowSplit):
                                    D[rowCount, colCount] = col
                                    colCount += 1
                                count += 1

                    rowCount += 1
                    colCount = ArrayTiltelCol
                    largestArray.append(count)

             #### Add gap between session
             for i in range(0, gap_btw_session):
                output.write("\n")


    #### Write to CSV
    with open(filenameOUT +".csv","a", newline = '') as csvfile:
        csvwriter = csv.writer(csvfile)
        for i in range (0, rowsMatrix):
            csvwriter.writerow(D[i])

    os.remove(filenameIN)  ###clear input file
    return headerArrayTitle, headerArrayVals


# def find_show(filenameIN):
#     showVars =[]
#     tORf = False
#     with open(filenameIN) as f:
#         for i, row in enumerate(f):
#             if tORf:
#                 if row == "\n": ### will require specific format
#                     break
#                 else:
#                     showVars.append(row.strip("\n").strip("\\").split(" = "))
#                     print(showVars)
#             if row == "\SHOW\n":   #### will require specific format
#                 tORf = True
#
# def output_show(filenameIN, filenameOUT):
#     with open(filenameIN) as f:
#          with open(filenameOUT, "a") as output:
#              find_show(filenameIN)

def read_transIV(filenameIN):
    tORfV = False
    tORfA = False
    tORfL = False
    # tORfOTH= False
    Vars = []
    Varstitle = []
    ArrayVars = []
    ArrayVarstitle = []
    with open(filenameIN) as f:
        for i, row in enumerate(f):


            if tORfV:
                if row == "\n":
                    tORfV = False

                rowSplit = row.strip("\\").strip("\n").split(" = ")
                if rowSplit[0].isupper():
                    Vars.append(rowSplit[0])
                    Varstitle.append(rowSplit[1])

            if tORfA:
                if row =="\n":
                    tORfA = False

                rowSplit = row.strip("dim ").strip("\n").split(" \\")

                if rowSplit[0].isupper():
                    ArrayVars.append(rowSplit[0][0])
                    ArrayVarstitle.append(rowSplit[1].strip("\\"))
                if row =="\n":
                    tORfA = False

            if tORfL:
                if row == "\n":
                    tORfL = False
                else:
                    rowSplit = row.strip("List ").split("=")
                    ArrayVars.append(rowSplit[0])
                    ArrayVarstitle.append("List")

            # if tORfOTH:
            #     if row == "\n":
            #         tORfOTH = False
            #     else:
            #         rowSplit = row.strip("\\").split()
            #         ArrayVars.append(rowSplit[0])
            #         ArrayVarstitle.append(rowSplit[1])

            if row.strip("\n") == "\VARIABLES":  ####Requires special formatting when writing protocol
                    tORfV = True
            if row.strip("\n") == "\ARRAYS":  #####Requires special formatting when writing protocol
                    tORfA = True
            if row.strip("\n") == "\LISTS":  #####Requires special formatting when writing protocol
                    tORfL = True
            # if row.strip("\n") == "\OTHER": #####Requires special formatting when writing protocol
            #         tORfOTH = True

    return len(ArrayVars),Vars,Varstitle,ArrayVars,ArrayVarstitle


def find_largest_array(filenameIN):
     largestArray = [0,0]
     with open(filenameIN) as f:
         for i, row in enumerate(f):
             if i > header-1 and row[0] == " ":
                 rowSplit = row.replace(":","").split()
                 if int(rowSplit[0]) > int(largestArray[0]):
                     largestArray[0] = int(rowSplit[0])
                     largestArray[1] = int(len(rowSplit)-1)
                 if int(rowSplit[0]) == int(largestArray[0]) and int(len(rowSplit)) > int(largestArray[1]):
                    largestArray[1] = int(len(rowSplit) - 1)
     #print(largestArray)
     return(largestArray)

def create_matrix(filenameIN, filenameIN2):
    numArrays = read_transIV(filenameIN2)[0]
    largestArray = find_largest_array(filenameIN)

    ##ADDED because we wanted session time in csv
    columns = 9+26-numArrays+1+largestArray[0]+largestArray[1] +1
    rows = 2 + numArrays
    D = np.empty((rows,columns), dtype ="object")
    return D, rows, numArrays




#print(read_transIV(TransIV))
#print(create_matrix(MEDDATA,TransIV))

#create_output_file_txt("TEST123TXT")
#create_output_file_csv("TEST123CSV")
#copy_sealed_data(MEDDATA, TransIV, 'TEST123TXT')
#remove_zeros(MEDDATA,TransIV,outputTXTFilename,outputCSVFilename)
#read_transIV(TransIV)