#Importing standard libraries
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from datetime import date
import os
import threading
from threading import Thread
import tkinter.scrolledtext as tkscrolledtext
import glob
import time
from pynput.keyboard import Listener
from pynput import keyboard as pynputkeyboard

#Serial
import serial

#Reference Files within the SORTER project
import serial_rx_tx
import KeyboardMouseDell as KeyboardMouse
import Data


Interfaces = []  #stores the objects that correspond to each tab
interfaceCounter = 0 #how many tabs are created
timeNow = 0.00 #stores the current time when it is called
SerialPorts = [] #stores the serial port objects for available serial ports


# Looping as a refresh for the entire user interface window
def sdterm_main():
    global timeNow
    timeNow = time.time()

    root.after(200, sdterm_main)  # run the main loop once each 200 ms

#Obtains and outputs the available serial ports
def serial_ports():

    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

#Creates a new interface object, stores in Interfaces array, and addes the interface to the tab notebook , and increments
#the interface counter
def Create_NewInterface():
    global Interfaces, interfaceCounter
    Interfaces.append(Interface())
    Interfaces[interfaceCounter].RegisterReceiveOnReceive()
    tab_notebook.add(Interfaces[interfaceCounter].Return_Frame(), text="Interface %d" % (interfaceCounter + 1))
    interfaceCounter = interfaceCounter + 1

#Creates a new thread for a specific interface, calls the create interface function
def Create_NewThread():
    global Interfaces, interfaceCounter
    thread = Thread(target=Create_NewInterface)
    thread.start()
    # Interfaces.append(Interface())
    # Interfaces[interfaceCounter].RegisterReceiveOnReceive()
    # tab_notebook.add(Interfaces[interfaceCounter].Return_Frame(), text = "Interface %d" % (interfaceCounter+1))
    # interfaceCounter = interfaceCounter + 1


#Removes selected tab
def Remove_Interface():
    global interfaceCounter
    selectedTab = tab_notebook.select() #stores the currently selected tab object
    print(selectedTab)
    tab_notebook.forget(selectedTab) #removes that tab from the notebook, visually
    if (selectedTab[-1]).isalpha():
        selectedTab = "1"
    print(int(selectedTab[-1]))
    Interfaces[int(selectedTab[-1])-1] = None #removes the interface object completely
    ##interfaceCounter -= 1


##Create thread lock, this is for allowing only 1 sorter to be initiating or closing MedPC sessions
threadLock = threading.Lock()

#Obtain the currently available serial ports. All COM ports should be open at the beginning of starting any session
# in the case you want to add another interface during the session
SerialPorts = serial_ports()


# Creates the main interface window
root = tk.Tk()
root.title("Serial Data Terminal v1.01")  #This title is referenced in file KeyboardMouse line 24 as an allowable window to be open
# during the session. All other windows will be closed in the event of pop ups.

#set up the window size and position. The size of the interface window that initially pops up
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = screen_width/2
window_height = screen_width/3
window_position_x = screen_width/2 - window_width/2
window_position_y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d' % (window_width, window_height+500, window_position_x, window_position_y))

#Create the notebook object that holds the tabs inside the root (main window)
tab_notebook = ttk.Notebook(root)
tab_notebook.grid(row = 2, column = 0)

#Creates Add Tab button inside the root (main window)
AddTab_Button = Button(root, text = "Add Interface", command = Create_NewThread)
AddTab_Button.grid(row = 0, column = 0, sticky= "W")

#Creates Remove Tab Button inside the root (main window)
RemoveTab_button = Button(root, text = "Remove Interface", command = Remove_Interface)
RemoveTab_button.grid(row = 1, column = 0, sticky = "W")


#Class for interface object which is in each tab of the notebook (General structure of each tab to collect and show experiment info)
class Interface:
    global tab_notebook, timeNow, threadLock, SerialPorts

    #Declares characteristics for a each interface being created. They will be updated by the user
    def __init__(self):

        ## INPUT FILES
        self.TransIV = ""
        self.MEDDATA = ""


        #### EXPERIMENT TIMER
        self.ExperimentStartTimer = 0.00
        self.sessionStartTime = 0.00
        #self.timeNow = 0

        # Input Data
        ##ADDED 10/16 Data entry array for checking if there is missing data
        self.DataEntryArray = []

        ## OUTPUT FILES
        self.outputFolderPath = ""

        self.outputFilenameUser = ""
        self.DataEntryArray.append(self.outputFilenameUser)

        self.CompleteOutputFilename = ""


        self.expName = ""
        self.DataEntryArray.append(self.expName)

        self.opCham = ""
        self.DataEntryArray.append(self.opCham)

        self.numMice = 0
        self.DataEntryArray.append(self.numMice)

        self.totExpTime = 0.00
        self.DataEntryArray.append(self.totExpTime)

        self.minSesTime = 0.00
        self.DataEntryArray.append(self.minSesTime)

        self.maxSesTime = 0.00
        self.DataEntryArray.append(self.maxSesTime)

        self.maxNumMouseEntries = 0
        self.DataEntryArray.append(self.maxNumMouseEntries)

        self.timeoutTime = 0.00
        self.DataEntryArray.append(self.timeoutTime)

        #Boolean for determining if all input values declared
        self.InterfaceFilled = False


        # Testing Data
        self.Mouse = 0

        # Mouse ID/Name Data frame
        # Widget Objects
        self.IDarray = []  # Specifc ID entry box widget
        self.RevNameArray = []  # Subject Name entry box wiget object
        self.ProtocolsDropdwnObjArray = []  # Array containing the protocol dropdown widget objects
        self.protocolVarArray = []  # The selected item var for each protocol dropdown widget object
        self.SubjectLabelArray = []  # Subject Name label object for Current Data
        self.EntriesLabelArray = []  # Entry value label object for Current Data
        self.TotalTestTimeLabelArray = []  # Total Test time label object for Current Data
        self.TimerObjArray = []  # Timeout Timer for each mouse *******

        # Mouse data
        self.SubjectNames = []
        self.IDs = []
        self.MouseProtocolsKeyboard = []
        self.MouseProtocols = []
        self.Entries = []
        self.EntryTimes = []
        self.TotalTestTime = []
        self.AttemptedEntries = []
        self.TimeoutBool = []
        self.G = []  #added
        self.serialPort = serial_rx_tx.SerialPort()


        ##Create Interface Frame within the notebook
        self.Individual_frame = Frame(tab_notebook)
        self.Individual_frame.grid(row=0, column=0)



        #ADDED 10/23
        #Create Frame for Serial Monitor
        self.SerialMonitor_frame = Frame(self.Individual_frame)
        self.SerialMonitor_frame.grid(row =0, column = 1, rowspan = 4)
        self.SerialMonitor_frame.config(bg = "")

        ###Input Data label frame
        self.inputData_frame = LabelFrame(self.Individual_frame, text="Experiment & Files", bd=2)
        self.inputData_frame.grid(row=0, column=0, sticky="W", ipadx=10, ipady=10)

        # Input Data labels

        #D1: Experiment Name, D2: Outputfilenames, D3: Operant Chamber #, D4: NumMice
        #D5: Total Exp Time, D6: Min Session Time, D7: Max Session Time, D8: Max Num Entries D9: Timeout time
        # Col 1
        self.D1_label = Label(self.inputData_frame, text="Experiment Name:")
        self.D1_label.grid(row=0, column=0)
        self.D1_label.config(font="bold")

        self.D2_label = Label(self.inputData_frame, text="Output Filenames:")
        self.D2_label.grid(row=1, column=0)
        self.D2_label.config(font="bold")

        self.D3_label = Label(self.inputData_frame, text="Operant Chamber #:")
        self.D3_label.grid(row=4, column=0)
        self.D3_label.config(font="bold")

        self.D4_label = Label(self.inputData_frame, text="# of Mice:")
        self.D4_label.grid(row=5, column=0)
        self.D4_label.config(font="bold")

        # Col 2
        self.D5_label = Label(self.inputData_frame, text="Total Experiment Time(mins):")
        self.D5_label.grid(row=0, column=2)
        self.D5_label.config(font="bold")

        self.D6_label = Label(self.inputData_frame, text="Min Session Time(mins):")
        self.D6_label.grid(row=1, column=2)
        self.D6_label.config(font="bold")

        self.D7_label = Label(self.inputData_frame, text="Max Session Tim(mins):")
        self.D7_label.grid(row=2, column=2)
        self.D7_label.config(font="bold")

        self.D8_label = Label(self.inputData_frame, text="Max # of Entries:")
        self.D8_label.grid(row=3, column=2)
        self.D8_label.config(font="bold")

        self.D9_label = Label(self.inputData_frame, text="Timeout Time(mins)")
        self.D9_label.grid(row=4, column=2)
        self.D9_label.config(font="bold")

        # Input Data Entry Boxes
        # Col 1
        self.D1_entry = Entry(self.inputData_frame)
        self.D1_entry.grid(row=0, column=1,sticky = "W")
        self.D1_entry.config(font="bold")
        self.D1_entry.insert(END, "")

        self.D2_entry = Entry(self.inputData_frame)
        self.D2_entry.grid(row=1, column=1,sticky = "W")
        self.D2_entry.config(font="bold")
        self.D2_entry.insert(END, "")

        self.D3_entry = Entry(self.inputData_frame)
        self.D3_entry.grid(row=4, column=1,sticky = "W")
        self.D3_entry.config(font="bold",width = 5)
        self.D3_entry.insert(END, "")

        self.D4_entry = Entry(self.inputData_frame)
        self.D4_entry.grid(row=5, column=1,sticky = "W")
        self.D4_entry.config(font="bold", width = 5)
        self.D4_entry.insert(END, "")

        # Col 2
        self.D5_entry = Entry(self.inputData_frame)
        self.D5_entry.grid(row=0, column=3,sticky = "W")
        self.D5_entry.config(font="bold", width = 7)
        self.D5_entry.insert(END, "")

        self.D6_entry = Entry(self.inputData_frame)
        self.D6_entry.grid(row=1, column=3,sticky = "W")
        self.D6_entry.config(font="bold", width = 7)
        self.D6_entry.insert(END, "")

        self.D7_entry = Entry(self.inputData_frame)
        self.D7_entry.grid(row=2, column=3,sticky = "W")
        self.D7_entry.config(font="bold",width = 7)
        self.D7_entry.insert(END, "")

        self.D8_entry = Entry(self.inputData_frame)
        self.D8_entry.grid(row=3, column=3,sticky = "W")
        self.D8_entry.config(font="bold",width = 7)
        self.D8_entry.insert(END, "")

        self.D9_entry = Entry(self.inputData_frame)
        self.D9_entry.grid(row=4, column=3, sticky = "W")
        self.D9_entry.config(font="bold",width = 7)
        self.D9_entry.insert(END, "")


        # OUTPUT FILE PATH UPLOAD
        self.SelectOutFilePath_Button = tk.Button(self.inputData_frame, text="Create Files in Specified Path",
                                             command=self.browse_folder)
        self.SelectOutFilePath_Button.grid(row=2, column=0)
        self.SelectOutFilePath_text = tk.Text(self.inputData_frame, height=1, width=20)
        self.SelectOutFilePath_text.grid(row=2, column=1)
        self.SelectOutFilePath_text.config(font="bold")
        self.SelectOutFilePath_text.insert(END, "")

        self.OutputFilesCreated_frame = LabelFrame(self.inputData_frame, text=" ")
        self.OutputFilesCreated_frame.grid(row=3, column=1)
        self.OutputFilesCreated_colorbox = tk.Text(self.OutputFilesCreated_frame, height=1, width=3)
        self.OutputFilesCreated_colorbox.grid(row=3, column=1)

        # Clear All Entry Box Value Button
        self.ClearValues_Button = tk.Button(self.inputData_frame, text="Clear all entry boxes",
                                            command=self.Clear_Values)
        self.ClearValues_Button.grid(row=5, column=2)

        # Update values from entry
        self.UpdateValues_Button = tk.Button(self.inputData_frame, text="Update Values", command=self.Update_Values)
        self.UpdateValues_Button.grid(row=5, column=3)

        ###Mouse ID/Naming Frame
        self.MouseID_frame = LabelFrame(self.Individual_frame, text="Mice ID/Protocol Selection", bd=2)
        self.MouseID_frame.grid(row=1, column=0, sticky="W", ipadx=5, ipady=5)

        self.ID_title = Label(self.MouseID_frame, text="MOUSE ID")
        self.ID_title.grid(row=0, column=1)
        self.NewMouseName_title = Label(self.MouseID_frame, text="Subject Name")
        self.NewMouseName_title.grid(row=0, column=2)

        # Update Values2
        self.UpdateValues2_button = Button(self.MouseID_frame, text="Update Values", command=self.Update_Values2)
        self.UpdateValues2_button.grid(row=4, column=0, padx=5)

        # Scan in ID
        self.ScaninID_button = Button(self.MouseID_frame, text="Scan in ID", command=self.Scan_IN_ID)
        self.ScaninID_button.grid(row=1, column=0, padx=5)

        # Save IDs to txt file
        self.SaveIDs_button = Button(self.MouseID_frame, text="Save IDs", command=self.Save_IDs)
        self.SaveIDs_button.grid(row=2, column=0)

        # Upload IDs from txt file
        self.UploadIDs_button = Button(self.MouseID_frame, text="Upload IDs", command=self.Upload_IDs)
        self.UploadIDs_button.grid(row=3, column=0)

        # Clear ID/Name entries
        self.ClearIDName_button = Button(self.MouseID_frame, text="Clear IDs/Names", command=self.Clear_ID_Names)
        self.ClearIDName_button.grid(row=5, column=0)

        # Select Specific Protocol Label
        self.SelectSpecificProtocol_label = Label(self.MouseID_frame, text="Select Specific Protocol")
        self.SelectSpecificProtocol_label.grid(row=0, column=3, ipadx=5)

        # Protocol Label
        self.UploadedProtocol_label = Label(self.MouseID_frame, text="Uploaded Protocols")
        self.UploadedProtocol_label.grid(row=0, column=4)

        # Protocol Listbox
        self.Protocol_listbox = Listbox(self.MouseID_frame, width=20)
        self.Protocol_listbox.grid(row=1, column=4)


        # Browse TransIV
        self.BrowseTransIV_button = Button(self.MouseID_frame, text="Browse Trans IV File(s)", command=self.browse_file)
        self.BrowseTransIV_button.grid(row=1, column=5, padx=5, sticky="W")

        # Remove Protocol
        self.RemoveProtocol_button = Button(self.MouseID_frame, text="Remove Selected Protocol",
                                       command=self.Remove_Selected_Protocol)
        self.RemoveProtocol_button.grid(row=2, column=5, padx=5, sticky="W")

        # Use selected protocol for all Checkbox
        self.checkboxVar = IntVar(self.Individual_frame)
        self.checkbox = Checkbutton(self.MouseID_frame, text="Check to use selected protocol for all", onvalue=1, offvalue=0,
                         variable=self.checkboxVar, command=self.Checkbox_click).grid(row=3, column=5)

        ###Serial Control Frame
        self.SerialControl_frame = LabelFrame(self.Individual_frame, text="Sorter Connection", bd=2)
        self.SerialControl_frame.grid(row=2, column=0, sticky="W", ipadx=10, ipady=10)

        # Begin Experiment
        self.BeginExperiment_button = Button(self.SerialControl_frame, text="Begin Experiment", command=self.Begin_Experiment)
        self.BeginExperiment_button.config(bg = "green", font = "bold")
        self.BeginExperiment_button.grid(row=1, column=3)

        # COM Port label
        self.Comport_label = Label(self.SerialControl_frame, text="COM Port:")
        self.Comport_label.grid(row=0, column=0)
        self.Comport_label.config(font="bold")

        #Refresh COM Ports Button. Was working on this so that the available COM ports could be updated throughout any session
        # so that you wouldnt need to plug in all sorters before starting a session. This is work in progress
        self.ComportRefresh_button = Button(self.SerialControl_frame, text = "Refresh Ports", command = self.RefreshCOMPorts)
        self.ComportRefresh_button.grid(row = 1, column = 0)


        # I removed this because always communicating @9600. Tried going faster but encountered errors. Didn't want to leave
        # this as an option since it would just cause problems. Can use if you know what youre doing
        # # #Baud Rate label
        # self.label_baud = Label(self.SerialControl_frame, width=10, height=2, text="Baud Rate:")
        # self.label_baud.grid(row=0, column=2)
        # self.label_baud.config(font="bold")
        #
        # # #Baud Rate entry box
        # self.baudrate_entry = Entry(self.SerialControl_frame, width=10)
        # self.baudrate_entry.grid(row=0, column=3)
        # self.baudrate_entry.config(font="bold")
        # self.baudrate_entry.insert(END, "9600")

        # #COM PORT OPEN/CLOSE Color Box
        self.color_box = Entry(self.SerialControl_frame, width=5)
        self.color_box.grid(row=0, column=4, padx = 10)
        self.color_box.config({"background": "Red"})

        self.COMopenclose_button = Button(self.SerialControl_frame, text="Open COM Port", width=15, command=self.OpenCommand)
        self.COMopenclose_button.grid(row=0, column=3, padx=20)

        #Used this when user was answering questions from arduino, now its just entered all at once thru the interface.
        #Can be uncommented and used if you want this function
        # # Send Data label
        # self.senddata_label = Label(self.SerialControl_frame, text="Send Data")
        # self.senddata_label.grid(row=1, column=0)
        # self.senddata_label.config(font="bold")
        #
        # # #Send Data entry box
        # self.senddata_edit = Entry(self.SerialControl_frame, width=15)
        # self.senddata_edit.grid(row=1, column=1)
        # self.senddata_edit.config(font="bold")
        # self.senddata_edit.insert(END, "")

        # Clear Serial Monitor Data button
        self.button_cleardata = Button(self.SerialControl_frame, text="Clear Monitor Data", width=15,
                                  command=self.ClearDataCommand)
        self.button_cleardata.grid(row=1, column=1)

        ###Current Data
        self.Current_Data = LabelFrame(self.SerialControl_frame, text="Current Data", bd=2)
        self.Current_Data.grid(row=0, column=6, rowspan=4, sticky="NW")

        # Subject Label
        self.Subject_label = Label(self.Current_Data, text="Subject")
        self.Subject_label.grid(row=0, column=6)

        # Entries Label
        self.Entries_label = Label(self.Current_Data, text="Entries")
        self.Entries_label.grid(row=0, column=7)

        # Total Test Time
        self.TotalTestTime_label = Label(self.Current_Data, text="Total Test Time")
        self.TotalTestTime_label.grid(row=0, column=8)

        # Serial Monitor Frame, this is located on the right side, you may need to make the window larger to see it.
        # We tried to make a vertical scroll bar in a tab because there wasnt enough space and you couldnt access the
        #serial monitor. However, we were not able to implement and this was the next best option.
        self.serial_frame = LabelFrame(self.SerialMonitor_frame, text="Serial Monitor", bd=2)
        self.serial_frame.grid(row=0, column=0)

        # Scrolled text box to display serial info
        self.textbox = tkscrolledtext.ScrolledText(master= self.serial_frame, wrap='word', width=40,
                                              height=15)  # width=characters, height=lines
        self.textbox.grid(row=0, column=0)
        self.textbox.config(font="bold")

        #This is for the dropdown menu for COM ports
        self.tkvar = StringVar() #variable that stores the currently selected COM Port
        self.tkvar.set("COM X")
        self.dropdown = OptionMenu(self.SerialControl_frame, self.tkvar, *SerialPorts)
        self.dropdown.grid(row=0, column=1)

    #Returns the frame object corresponding to an interface so that the frame can be added as a tab in the notebook
    def Return_Frame(self):
        return self.Individual_frame

    # This was used for sending data function
    # # Keyboard Listener
    # def OnPress(self,key):
    #     if key == pynputkeyboard.Key.enter:
    #         self.SendDataCommand()
    #
    # listener = pynputkeyboard.Listener(on_press=OnPress)
    # listener.start()

    # serial data callback function. THIS IS THE MAIN FUNCTION WHERE MED SESSIONS ARE STARTED/ENDED, TIMES ARE CHECKED , AND DATA COPIED
    def OnReceiveSerialData(self,message):
        # global expName, opCham, Mouse, outputFilenameUser, ExperimentStartTimer, totExpTime, EntryTimes
        # global TimerObjArray, TimeoutBool  # KeyMouseTime
        # global sessionStartTime, SubjectNames, EntriesLabelArray, TotalTestTimeLabelArray, MouseProtocolsKeyboard, Entries, MEDDATA

        str_message = message.decode('utf-8').strip() #stores the serial data from arduino
        strSplit = str_message.split(":")

        if str_message == "Maxtimechck" or str_message == "Mintimechck":

            #During a MedPC session while a mouse is in the chamber, arduino is constantly asking Python whether the miniimum or
            #maximum time has been reached. This communication does not get written into the serial monitor on the interface
            if str_message == "Maxtimechck":
                if (timeNow - self.sessionStartTime) > self.maxSesTime * 60:
                    self.serialPort.Write_False()
                else:
                    self.serialPort.Write_True()

            if str_message == "Mintimechck":
                if (timeNow - self.sessionStartTime) > self.minSesTime * 60:
                    self.serialPort.Write_False()
                else:
                    self.serialPort.Write_True()
        #This information is written to the serial monitor on the interface
        else:

            if str_message == "Update Timeout":
                # Write TimeoutBool Array vals to Arduino
                self.TimeoutString = ""
                for i in range(0, self.numMice):
                    # serialPort.serialport.write((IDs[i]+"\r").encode("utf-8"))
                    self.TimeoutString = self.TimeoutString + str(self.TimeoutBool[i])
                print("timeoutstring update")
                print(self.TimeoutString)
                self.serialPort.serialport.write(self.TimeoutString.encode("utf-8"))  #Writes the timeout status as a string to arduino

            #This is not used anymore, but didn't want to remove and cause an issue. Was used when we still used CoolTerm
            if str_message == "0x0c":
                self.ClearDataCommand()

            if strSplit[0] == "ScanID":
                self.MouseID_frame.focus_get().insert(0, strSplit[1]) #Obtains the current entry box with the cursor

            #When a mouse is entering the chamber
            if strSplit[0] == "M":
                self.Mouse = int(strSplit[1]) #obtain which mouse is entering and store as int
                self.textbox.insert(tk.INSERT, str_message + "\n") #print to serial monitor mouse number
                print(self.Mouse)

            if strSplit[0] == 'StartMED':
                # Mouse = int(strSplit[1])
                # KeyMouseTime = time.time()
                # print(KeyMouseTime)
                # CheckKeyMouse()
                threadLock.acquire() #the interface attempts to acquire the lock which is needed for keyboard/cursor movements.
                #If it cannot acquire will wait until the other interface is done with the lock
                KeyboardMouse.OpenSession(str(self.expName), int(self.opCham), self.SubjectNames[self.Mouse],
                                          self.MouseProtocolsKeyboard[self.Mouse]) #Once the lock is acquired then the open session
                #command in the KeyboardMouse file can be initiated

                today = date.today() #Don't use this anywhere can probably be deleted
                self.MEDDATA = "!_Subject_" + self.SubjectNames[self.Mouse] + "_Experiment_" + self.expName +".Group_0"

                KeyboardMouse.IssueStart(int(self.opCham)) #Issue start command for MEDPC
                threadLock.release() # once its completed doing all of the movements for starting a session release the lock for another session to be started
                self.serialPort.Write_True() #Writes to arduino true (1) becasue Arduino was waiting in an empty loop until receiving a signal from python
                self.sessionStartTime = time.time() #starts the session timer

            # This is used when the minimum time is less than the protocol time and a mouse will leave early.
            if str_message == 'CloseMED':
                # KeyMouseTime = time.time()
                # CheckKeyMouse()
                threadLock.acquire()  #Acquires lock so that it can make keyboard/cursor movements necessary for closing a session

                #Replaced Close session for K pulse. We did this to avoid having to use the remove zeros function since that function was taking minutes to execute on
                # large arrays. The k pulse function built into MEDPC does the truncating for us.
                ##KeyboardMouse.CloseSession(int(self.opCham))
                KeyboardMouse.IssueKPulse(int(self.opCham))
                threadLock.release() #release the lock after completing the keyboard/cursor movements
                # KeyMouseTime = 0.00

            # Writes the output txt file from MEDPC sessions to a single txt file and single use] = int(self.Entries[self.Mouse]) + 1
                self.TotalTestTime[self.Mouse] = self.TotalTestTime[self.Mouse] + self.SessionTime
                self.EntriesLabelArray[self.Mouse].config(text=str(self.Entries[self.Mouse]))
                print(round(self.TotalTestTime[self.Mouse], 2))
                print(self.EntryTimes)
                self.TotalTestTimeLabelArray[self.Mouse].config(text=str(round(self.TotalTestTime[self.Mouse], 2)))

                # Start timeout timer for mouse that exited and set timeoutbool for that mouse to 0 so that Arduino has the updated timeout criteria
                #so that it can decide whether to let that mouse in again
                self.TimerObjArray[self.Mouse].start()
                self.TimeoutBool[self.Mouse] = 0

                # Write TimeoutBool Array vals to Arduino
                self.TimeoutString = ""
                for i in range(0, self.numMice):
                    # serialPort.serialport.write((IDs[i]+"\r").encode("utf-8"))
                    self.TimeoutString = self.TimeoutString + str(self.TimeoutBool[i])
                print("timeoutstring")
                print(self.TimeoutString)
                self.serialPort.serialport.write(self.TimeoutString.encode("utf-8"))


            if str_message == "Check Exp Time":
                #if total time elapsed since experiment started is greater than total allowable time than write false to arduino
                # Arduino will then decide whether to exit its main loop or not.
                print(timeNow)
                print(self.ExperimentStartTimer)
                print(self.totExpTime*60)
                if (timeNow - self.ExperimentStartTimer) > self.totExpTime * 60:
                    self.serialPort.Write_False()
                    print("False")
                else:
                    self.serialPort.Write_True()
                    print("True")

            #This writes all messages from arduino to the serial monitor on the interface
            self.textbox.insert(tk.INSERT, str_message + "\n")

    # Register the callback above with the serial port object
    def RegisterReceiveOnReceive(self):
        self.serialPort.RegisterReceiveCallback(self.OnReceiveSerialData)

    #Outputs an array with the protocols uploaded to the interface
    def Get_Protocols(self):
        Protocols = []
        for i in range(0, self.Protocol_listbox.size()):
            Protocols.append(self.Protocol_listbox.get(i))
        return Protocols

    #THIS IS NOT USED ANYMORE. Was using this when we were sending info thru the serial monitor
    def GetSerialPorts(self):

        if __name__ == '__main__':
            self.textbox.insert(tk.INSERT, self.serial_ports())




    #Commands associated with button presses


    def ClearDataCommand(self):  # Clear serial monitor data
        self.textbox.delete("1.0", END)

    #Not really used anymore since we just enter the data into entry boxes
    def SendDataCommand(self):
        message = self.senddata_edit.get()
        if self.serialPort.IsOpen():
            # message += '\r\n'  removed
            self.serialPort.Send(message)
            # textbox.insert('1.0',message)  removed
            self.senddata_edit.delete(0, END)  ####added
        else:
            self.textbox.insert(tk.INSERT, "Not sent - COM port is closed\r\n")

    #Clearing the values in the input data frame
    def Clear_Values(self):
        if self.D1_entry.index(END) != 0:
            self.D1_entry.delete(0, END)
        if self.D2_entry.index(END) != 0:
            self.D2_entry.delete(0, END)
        if self.D3_entry.index(END) != 0:
            self.D3_entry.delete(0, END)
        if self.D4_entry.index(END) != 0:
            self.D4_entry.delete(0, END)
        if self.D5_entry.index(END) != 0:
            self.D5_entry.delete(0, END)
        if self.D6_entry.index(END) != 0:
            self.D6_entry.delete(0, END)
        if self.D7_entry.index(END) != 0:
            self.D7_entry.delete(0, END)
        if self.D8_entry.index(END) != 0:
            self.D8_entry.delete(0, END)
        if self.SelectOutFilePath_text.index(END) != 0:
            self.SelectOutFilePath_text.delete(1.0, END)

    #This is for saving (to a variable)/updating the values entered in the entry boxes in the input data frame
    def Update_Values(self):

        if self.D1_entry.index(END) != 0:
            self.expName = self.D1_entry.get()

        ## ADDED 10/16 Didnt have outputfile name here and needed it for a check later
        if self.D2_entry.index(END) !=0:
            self.outputFilenameUser = self.D2_entry.get()


        if self.D3_entry.index(END) != 0:
            self.opCham = self.D3_entry.get()

        ## moved D9 here to update timeouttime var independently from the number of mice. Doing this fixed the issue we had
        # when timeout time was not updating
        if self.D9_entry.index(END) != 0:
            self.timeoutTime = float(self.D9_entry.get()) * 60.00

        #If the number of mice inputted changes
        if self.D4_entry.index(END) != 0:
            if self.numMice != int(self.D4_entry.get()):

                # Destory widgets in MiceID/Protocol Selection Frame and reset arrays associated with those widgets
                if len(self.ProtocolsDropdwnObjArray) != 0:
                    for i in range(self.numMice):
                        #widgets
                        self.IDarray[i].destroy()
                        self.RevNameArray[i].destroy()
                        self.ProtocolsDropdwnObjArray[i].destroy()
                        self.SubjectLabelArray[i].destroy()
                        self.EntriesLabelArray[i].destroy()
                        self.TotalTestTimeLabelArray[i].destroy()

                    #arrays
                    self.ProtocolsDropdwnObjArray = []
                    self.RevNameArray = []
                    self.IDarray = []
                    self.SubjectLabelArray = []
                    self.EntriesLabelArray = []
                    self.TotalTestTimeLabelArray = []
                    self.TotalTestTime = []
                    self.Entries = []

                # Set numMice to new value and format other widgets that change with mouse quantity
                self.numMice = int(self.D4_entry.get())
                self.Protocol_listbox.grid(row=1, column=4, rowspan=self.numMice)

                ## Commented out on 10/23
                ##Modified on 10/9 with Lulu bc of issues when each mouse could enter only 1, timer issues, when update was clicked but then a new timeout time was entered and update clicked again
                ### Reset Timerobjarray and timeoutbool
                ##self.TimerObjArray.clear()
                # self.TimeoutBool.clear()
                # if len(self.TimerObjArray) != 0:
                #     for i in range(self.numMice):
                #         self.TimerObjArray[i].destroy
                #
                # # Create timers for # mice
                # for i in range(self.numMice):
                #     self.TimeoutBool.append(1)
                #     print(self.timeoutTime)
                #     print("HERE WE ARE")
                #     self.TimerObjArray.append(threading.Timer(self.timeoutTime, self.TimeoutComplete, args=[i]))
                # UpdateNames_button.grid(row=numMice + 1, column=2)
                # ScaninID_button.grid(row=1, column=0, rowspan=numMice)


                # Create a new widgets for ID/SubjectName/Optionmenu because these change with number of mice
                for i in range(self.numMice):
                    self.IDarray.append(Entry(self.MouseID_frame, width=15, ))
                    self.IDarray[-1].grid(row=i + 1, column=1)
                    self.IDarray[-1].insert(END, "")
                    self.IDarray[-1].config(font="bold")

                    self.RevNameArray.append(Entry(self.MouseID_frame))
                    self.RevNameArray[-1].grid(row=i + 1, column=2,sticky = "W")
                    self.RevNameArray[-1].insert(END, "")
                    self.RevNameArray[-1].config(font="bold", width = "8")

                    self.protocolVarArray.append(tk.StringVar(self.MouseID_frame))
                    self.protocolVarArray[-1].set("PROTOCOL")
                    self.ProtocolsDropdwnObjArray.append(OptionMenu(self.MouseID_frame, self.protocolVarArray[-1], (), *self.Get_Protocols()))
                    # Protocols_dropdown = OptionMenu(MouseID_frame,protocol,"-",*Get_Protocols())
                    self.ProtocolsDropdwnObjArray[-1].grid(row=i + 1, column=3)

                    self.SubjectLabelArray.append(Label(self.Current_Data))
                    self.SubjectLabelArray[-1].grid(row=i + 1, column=6)

                    self.EntriesLabelArray.append(Label(self.Current_Data))
                    self.EntriesLabelArray[-1].grid(row=i + 1, column=7)

                    self.TotalTestTimeLabelArray.append(Label(self.Current_Data))
                    self.TotalTestTimeLabelArray[-1].grid(row=i + 1, column=8)

                    self.TotalTestTime.append(0.00)
                    self.Entries.append(0)

        #for other input data if they change
        if self.D5_entry.index(END) != 0:
            self.totExpTime = float(self.D5_entry.get())
        if self.D6_entry.index(END) != 0:
            self.minSesTime = float(self.D6_entry.get())
        if self.D7_entry.index(END) != 0:
            self.maxSesTime = float(self.D7_entry.get())
        if self.D8_entry.index(END) != 0:
            self.maxNumMouseEntries = int(self.D8_entry.get())


        #10/23 Moved timer object creation here after new values of numMice and timeout time are obtained
        ##Timeout timers for each mouse are created only if the numMice and timeout time are nonzero
        if self.numMice != 0 and self.timeoutTime != 0:
            self.TimeoutBool.clear()

            ##ADDED 10/23 best way to delete timer objects
            del(self.TimerObjArray)
            self.TimerObjArray = [] # Set to zero

            # Create timers for # mice
            for i in range(self.numMice):
                self.TimeoutBool.append(1)
                self.TimerObjArray.append(threading.Timer(self.timeoutTime, self.TimeoutComplete, args=[i]))

        #For detecting if there is missing input data. Obtains the current variable value for each input
        for i in range (len(self.DataEntryArray)):
            if i == 0:
                self.DataEntryArray[i]= self.outputFilenameUser
            if i == 1:
                self.DataEntryArray[i]= self.expName
            if i == 2:
                self.DataEntryArray[i] = self.opCham
            if i == 3:
                self.DataEntryArray[i] = self.numMice
            if i == 4:
                self.DataEntryArray[i]=  self.totExpTime
            if i == 5:
                self.DataEntryArray[i] = self.minSesTime
            if i ==6:
                self.DataEntryArray[i]= self.maxSesTime
            if i ==7:
                self.DataEntryArray[i]= self.maxNumMouseEntries
            if i ==8:
                self.DataEntryArray[i]=self.timeoutTime




        ##ADDED 10/16 to update the interface filled variable to see if all data entry boxes have been filled out
        for i in range (len(self.DataEntryArray)):
            print(i)
            if i < 2:
                if self.DataEntryArray[i]!= "":
                    self.InterfaceFilled = True
                    print("True")
                else:
                    self.InterfaceFilled = False
                    print("False")
                    break
            else:
                if self.DataEntryArray[i]!= 0:
                    self.InterfaceFilled = True
                    print(i)
                else:
                    self.InterfaceFilled = False
                    print(i)
                    break


        print(self.expName, self.opCham, self.numMice, self.totExpTime, self.minSesTime, self.maxSesTime, self.maxNumMouseEntries, self.timeoutTime)
        print(self.TimeoutBool)


    #When the timeout timer is done it calls this command which updates the TimeoutBool array for the mouse whose timer just ended
    def TimeoutComplete(self,Mousenum):
        self.TimeoutBool[Mousenum] = 1
        print("Timer Completed:")
        print(self.TimeoutBool)
        self.TimerObjArray[Mousenum] = threading.Timer(self.timeoutTime, self.TimeoutComplete, args=[Mousenum]) #Make a new timer for the mouse whose timer just ended

    def Scan_IN_ID(self):
        self.serialPort.Write_True()
        ##Wait for ID response
        # MouseID_frame.focus_get()

    #This is for selecting one protocol for all of the mice
    def Checkbox_click(self):
        if self.checkboxVar.get() == 1:
            # MouseProtocolsKeyboard = []
            for i in range(self.numMice):
                # MouseProtocolsKeyboard.append(Protocol_listbox.curselection(ACTIVE))
                self.protocolVarArray[i].set(self.Protocol_listbox.get(ACTIVE))

    #Updates the protocol dropdown menus for each mouse
    def Update_OptionMenus(self):

        if len(self.ProtocolsDropdwnObjArray) != 0:
            for i in range(self.numMice):
                self.ProtocolsDropdwnObjArray[i].destroy()
                # protocolVarArray[i].destroy()
            self.ProtocolsDropdwnObjArray = []
            self.protocolVarArray = []

            for i in range(self.numMice):
                self.protocolVarArray.append(tk.StringVar(self.MouseID_frame))
                self.protocolVarArray[-1].set("PROTOCOL")
                self.ProtocolsDropdwnObjArray.append(OptionMenu(self.MouseID_frame, self.protocolVarArray[-1], *self.Get_Protocols()))
                self.ProtocolsDropdwnObjArray[-1].grid(row=i + 1, column=3)

    #Removes the selected protocol from the listbox
    def Remove_Selected_Protocol(self):
        self.Protocol_listbox.delete(ACTIVE)
        self.Update_OptionMenus()

    #Saves values in the entry boxes of the MouseID/Protocol frame to variables
    def Update_Values2(self):
        # global IDs, AttemptedEntries, SubjectNames, MouseProtocols, MouseProtocolsKeyboard
        self.IDs = []
        self.SubjectNames = []
        self.MouseProtocolsKeyboard = []
        self.MouseProtocols = []
        self.G = self.Get_Protocols()
        for i in range(0, self.numMice):
            self.SubjectNames.append(self.RevNameArray[i].get().strip("\n"))
            self.IDs.append(self.IDarray[i].get())
            self.AttemptedEntries.append(0)
            self.SubjectLabelArray[i].config(text=self.IDarray[i].get())

            for j, line in enumerate(self.G):
                if self.protocolVarArray[i].get() == line:
                    self.MouseProtocolsKeyboard.append(j)
                    self.MouseProtocols.append(line)

            # MouseProtocolsKeyboard.append((ProtocolsDropdwnObjArray[i].getindex()))
        print(self.SubjectNames, self.IDs, self.MouseProtocolsKeyboard, self.MouseProtocols)

    #Clears the IDs and names in the MouseID/Protocol frame
    def Clear_ID_Names(self):

        for i in range(self.numMice):
            if self.IDarray[i].index(END) != 0:
                self.IDarray[i].delete(0, END)

            if self.RevNameArray[i].index(END) != 0:
                self.RevNameArray[i].delete(0, END)

    #Saves ID's that are stored in th variables to a txt file with the name of the experiment
    def Save_IDs(self):
        self.output = open(os.path.join(self.outputFolderPath, self.D2_entry.get()) + "IDs", "x")
        for i in range(self.numMice):
            self.output.write(self.IDarray[i].get() + ":" + self.RevNameArray[i].get() + "\n")
        self.output.close()

    ## ADDE 10/16 to popup error windows
    # This is used when there is missing input data and a user tries to begin the experiment
    def PopupErrorWindow (self,text):
        self.root2 = tk.Tk()
        self.root2.title("Error")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = screen_width / 6
        window_height = screen_width / 8
        window_position_x = screen_width / 2 - window_width / 2
        window_position_y = screen_height / 2 - window_height / 2
        self.root2.geometry('%dx%d+%d+%d' % (window_width, window_height, window_position_x, window_position_y))

        self.InterfaceFilled_label = Label(self.root2, text= text + ";)", bg="yellow")
        self.InterfaceFilled_label.config(font=300)
        self.InterfaceFilled_label.place(anchor="center")
        self.InterfaceFilled_label.pack()


    #Function to begin experiment. Transfers all of the relevant data that Arduino needs for checking the criteria of the mice
    def Begin_Experiment(self):

        ##ADDED Line below 10/16 to check if all inputs have been filled out and output files created
        if self.InterfaceFilled:
            self.ExperimentStartTimer = time.time() #change by Yashi
            self.serialPort.Write_False()
            time.sleep(2)
            self.serialPort.serialport.write(str(self.numMice).encode("utf-8"))
            time.sleep(2)
            self.serialPort.serialport.write(str(self.maxNumMouseEntries).encode("utf-8"))
            time.sleep(2)

            for i in range(0, self.numMice):
                print(self.IDs[i])
                # serialPort.serialport.write((IDs[i]+"\r").encode("utf-8"))
                self.serialPort.serialport.write((self.IDs[i]).encode("utf-8"))  # New code
                time.sleep(2)
        else:
            ##Create a popwindowot
            self.PopupErrorWindow("Missing Experiment Data")

    # Upload ID's from a txt file. This is format specific so it must be in the same format that the SaveID functions writes in
    def Upload_IDs(self):
        UploadID = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetype=(("", ""), ("All Files", "*.*")))
        with open(UploadID) as input:
            for i, line in enumerate(input):
                string = line.split(":")
                if i < self.numMice:
                    self.IDarray[i].insert(0, string[0])
                    self.RevNameArray[i].insert(0, string[1])

    #This is for uploading MEDPC protocols
    def browse_file(self):
        global TransIV, ProtocolsDropdwnObjArray

        TransIV = filedialog.askopenfilenames(initialdir="/", title="Select a File",
                                              filetype=(("MPC", "*.MPC"), ("All Files", "*.*")))

        self.G = self.Get_Protocols()
        TransIVlst = list(TransIV)
        Alphabetical = sorted(self.G + TransIVlst)
        for i, line in enumerate(Alphabetical):
            self.Protocol_listbox.insert(i, line[17:].strip(".MPC"))

        self.Update_OptionMenus()

    #This is for selecting a folder to write output files to
    def browse_folder(self):
        # if browseFileCounter == 1:

        #ADDE 10/16 incase someone tries to create a outfile when the variable is empty. Causes a popup window
        if self.outputFilenameUser != "":


            self.outputFolderPath = filedialog.askdirectory()
            self.CompleteOutputFilename = os.path.join(self.outputFolderPath, self.outputFilenameUser)
            if not os.path.exists(self.CompleteOutputFilename + ".txt"):
                Data.create_output_file_txt(self.CompleteOutputFilename + ".txt")
                Data.create_output_file_csv(self.CompleteOutputFilename + ".csv")

                if self.SelectOutFilePath_text.compare("end-1c", "!=", "1.0"):
                    self.SelectOutFilePath_text.delete(1.0, END)
                    self.SelectOutFilePath_text.insert(END, self.outputFolderPath)
                    self.OutputFilesCreated_frame.config(text="Output Files Created")
                    self.OutputFilesCreated_colorbox.config({"background": "Green"}, width=20)

                else:
                    self.SelectOutFilePath_text.insert(END, self.outputFolderPath)
                    self.OutputFilesCreated_frame.config(text="Output Files Created")
                    self.OutputFilesCreated_colorbox.config({"background": "Green"}, width=20)

            else:
                self.OutputFilesCreated_frame.config(text="File Already Exists")
                self.OutputFilesCreated_colorbox.config({"background": "Red"}, width=19)


        else:
            self.PopupErrorWindow("Missing input for 'Output Filename'")



    # COM Port open/close button
    def OpenCommand(self):
        if self.COMopenclose_button.cget("text") == 'Open COM Port':
            print(self.tkvar.get())
            comport = self.tkvar.get()
            ####EDITED 9/10 because theres not point to have user edit baudrate
            #baudrate = self.baudrate_entry.get()
            baudrate = 9600
            self.serialPort.Open(comport,baudrate)
            self.COMopenclose_button.config(text='Close COM Port')
            #textbox.insert(tk.INSERT, "COM Port Opened\r\n") removed
            self.color_box.config({"background": "Green"})
        elif self.COMopenclose_button.cget("text") == 'Close COM Port':
                self.serialPort.Close()
                self.COMopenclose_button.config(text='Open COM Port')
                self.color_box.config({"background": "Red"})

    #Work in progress
    def RefreshCOMPorts(self):
        global SerialPorts
        self.dropdown.destroy()
        SerialPorts = serial_ports()
        self.dropdown = OptionMenu(self.SerialControl_frame, self.tkvar, *SerialPorts)
        self.dropdown.grid(row=0, column=1)


# The main loop

root.after(200, sdterm_main)
root.mainloop()
#
