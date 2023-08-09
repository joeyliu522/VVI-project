
import time

from pynput.mouse import Button,Controller as mouseController
import keyboard
import win32gui, win32con


mouse = mouseController()

boxes_load_coords = [(704, 540), (750, 540), (793, 540), (837, 540)]
boxes_issuestart_coords = [(21, 243), (66, 242), (113, 240), (157, 242)]
boxes_close_coords= [(18, 191), (61, 191), (107, 191), (152, 191)]
protocols_list_coords = [(535, 419), (535, 433), (535, 446)] # adjust depending on displayed protocols

def CheckForegroundWindow():
    TestWindows = False

    while TestWindows == False:
        windowNum = win32gui.GetForegroundWindow()
        windowText = win32gui.GetWindowText(windowNum)
        ##ADDED windowtext == "" on 9/28E
        if windowText == "Serial Data Terminal v1.01" or windowText == "MED-PC IV" or windowText == "Open Experimental Session" or windowText =="Send Signals to Boxes" or windowText == "Close Experimental Sessions" or windowText == "SORTER – terminal.py (Administrator)" or windowText == "Shut Down Windows" or windowText == "":
            TestWindows = True
            print(windowText)
        else:
            win32gui.PostMessage(windowNum, win32con.WM_CLOSE, 0, 0)
            print("Closed", windowText)

    pause()


### Checked 1
def OpenSession(ExperimentName,OperantChamber,MouseNum,protocolNum):
    #mouse.position = (305, 489)
    ###ADDED 7/16
    # keyboard.press_and_release('enter')
    # time.sleep(.2)
    ###
    ##ADDED 7/17
    #MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    #CheckForegroundWindow()
    CheckForegroundWindow()
    #####
    mouse.position = (82, 18) #Clicks the MED-PC Window frame to make it come to the forefront
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    keyboard.press_and_release('ctrl+o')
    CheckForegroundWindow()
    pause()
    mouse.position = (590, 300) #Subject entry box position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    keyboard.press_and_release('backspace')
    CheckForegroundWindow()
    pause()
    #keyboard.press_and_release(MouseNum)
    keyboard.write(MouseNum)
    CheckForegroundWindow()
    pause()
    mouse.position = (590, 330) #Experiment entry box position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    pause()
    keyboard.press_and_release('backspace')
    CheckForegroundWindow()
    pause()
    keyboard.write(ExperimentName)
    CheckForegroundWindow()
    pause()
    mouse.position = (574, 400) #Protocol drop down box position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    pause()
    ##mouse.position = (728, 433)
    ##CheckForegroundWindow()
    pause()
    ##mouse.click(Button.left, 5)
    mouse.position = protocols_list_coords[protocolNum] # UPDATE: location of each protocol in drop-down list
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    pause()
    mouse.position = (820, 570) #Deselect all button position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    mouse.position = boxes_load_coords[OperantChamber-1] ###### operant box selection
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    pause()
    mouse.position = (1000, 500) #OK button position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    pause()
    keyboard.press_and_release("esc")

# Check 1
def IssueStart(OperantChamber):
    #MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    CheckForegroundWindow()
    pause()
    mouse.position = (126, 65) #Position of fifth icon from the left (has a light blue signal like symbol)
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left)
    CheckForegroundWindow()
    pause()
    mouse.position = boxes_issuestart_coords[OperantChamber-1] ###Operant Box Selection
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    mouse.position = (459, 87) #Issue button position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    keyboard.press_and_release("esc")
    CheckForegroundWindow()
    pause()



def CloseSession(OperantChamber):
    #MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    CheckForegroundWindow()
    pause()
    mouse.position = (72, 62) #Position of third icon from the left (closed blue book)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    mouse.position = boxes_close_coords[OperantChamber-1]   ##Operant Box Selection
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    mouse.position = (262, 167) #OK button position
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    #keyboard.press_and_release('esc')

# Check 1
def IssueKPulse(OperantChamber):
    # MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    CheckForegroundWindow()
    pause()
    mouse.position = (126, 63) #Position of fifth icon from the left (has a light blue signal like symbol)
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left)
    CheckForegroundWindow()
    pause()

    ##ADDED 10/16 to select k pulse in send signals to boxes window
    mouse.position = (30, 119) #Issue K Pulse selection circle position
    pause()
    CheckForegroundWindow()
    mouse.click(Button.left,1)
    pause()
    CheckForegroundWindow()


    mouse.position = boxes_issuestart_coords[OperantChamber - 1]  ###Operant Box Selection
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    mouse.position = (458, 88) #Issue button position
    CheckForegroundWindow()
    pause()
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    pause()
    keyboard.press_and_release("esc")
    CheckForegroundWindow()
    pause()

def pause():
    time.sleep(.05)