
import time

from pynput.mouse import Button,Controller as mouseController
import keyboard
import win32gui, win32con


mouse = mouseController()

boxes_load_coords = [(619, 489), (664, 489), (708, 490), (752, 490)]
boxes_issuestart_coords = [(22, 241), (66, 242), (113, 240), (157, 242)]
boxes_close_coords= [(17, 186), (63, 186), (108, 189), (151, 188)]
protocols_list_coords = [(521, 368), (520, 381), (524, 396), (519, 406), (517, 421)]


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

    time.sleep(.1)

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
    time.sleep(.05)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.press_and_release('ctrl+o')
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (544, 253) #Subject entry box position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.press_and_release('backspace')
    CheckForegroundWindow()
    time.sleep(.05)
    #keyboard.press_and_release(MouseNum)
    keyboard.write(MouseNum)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (546, 283) #Experiment entry box position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.press_and_release('backspace')
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.write(ExperimentName)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (574, 349) #Protocol drop down box position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    time.sleep(.05)
    ##mouse.position = (728, 433)
    ##CheckForegroundWindow()
    time.sleep(.05)
    ##mouse.click(Button.left, 5)
    mouse.position = protocols_list_coords[protocolNum]
    CheckForegroundWindow()
    time.sleep(.05)
    time.sleep(.2)
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (737, 522) #Deselect all button position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = boxes_load_coords[OperantChamber-1] ###### operant box selection
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (912, 451) #OK button position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left,1)
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.press_and_release("esc")


def IssueStart(OperantChamber):
    #MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (126, 63) #Position of fifth icon from the left (has a light blue signal like symbol)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = boxes_issuestart_coords[OperantChamber-1] ###Operant Box Selection
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (452, 83) #Issue button position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.press_and_release("esc")
    CheckForegroundWindow()
    time.sleep(.05)



def CloseSession(OperantChamber):
    #MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (72, 62) #Position of third icon from the left (closed blue book)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = boxes_close_coords[OperantChamber-1]   ##Operant Box Selection
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (266, 161) #OK button position
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    #keyboard.press_and_release('esc')


def IssueKPulse(OperantChamber):
    # MEDPCwindow = win32gui.FindWindow(None, "MED-PC IV")
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (126, 63) #Position of fifth icon from the left (has a light blue signal like symbol)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left)
    CheckForegroundWindow()
    time.sleep(.05)

    ##ADDED 10/16 to select k pulse in send signals to boxes window
    mouse.position = (29, 118) #Issue K Pulse selection circle position
    time.sleep(.05)
    CheckForegroundWindow()
    mouse.click(Button.left,1)
    time.sleep(.05)
    CheckForegroundWindow()


    mouse.position = boxes_issuestart_coords[OperantChamber - 1]  ###Operant Box Selection
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.position = (452, 83) #Issue button position
    CheckForegroundWindow()
    time.sleep(.05)
    mouse.click(Button.left, 1)
    CheckForegroundWindow()
    time.sleep(.05)
    keyboard.press_and_release("esc")
    CheckForegroundWindow()
    time.sleep(.05)

