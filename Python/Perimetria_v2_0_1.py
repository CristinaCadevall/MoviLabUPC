#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project: Tesis Lali
Experiment: Camp Visual -> Perimetria
Created on Sun Feb  3 11:29:49 2019
@author: Aitor Matilla
Hitoria dels canvis
versio 2.0.0 canvi mètode: de dins a fora i de fora a dins (2 voltes) enlloc de 
versio 2.0.1 canvi de nom a Perimetria, afegir time stamp + info versio dins resultat
versio 2.0.2 can crear un nom de resultats de perimetria amb nom fix per tal que el movilab pugui crear la mascara. crearem dos resutats
             ATEMCIO: avancem de versió però pel PC del deslumbrometre ens convé que el nom de l'arxiu sigui sempre el mateix. per tant el nom arxiu a partir d'ara no indica versio
3 voltes de dins a fora.
"""
from tkinter import *
from tkinter import messagebox
import time
import datetime
import math
import shutil

CVVersion = "Perimetria Movilab v 2.0.2"

#Primer llegim de l'arxiu la mida del punt a mostrar a pantalla
file = open('..\DotSize.txt', 'r') 
if file.mode != 'r' :
    print ('Error reading DoSize.txt')
    exit()
    
dotSize = file.readline().rstrip()
idPatient = file.readline().rstrip()
doRightEyeFile = file.readline().rstrip()
doLeftEyeFile = file.readline().rstrip()
doBothEyesFile = file.readline().rstrip()
nIterationsFile = file.readline().rstrip()
crossLineFile = file.readline().rstrip()
file.close()

#Creem/obrim l'arxiu a on escriurem les dades de l'experiment
sep=';'
endl= '\n'
timetag = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S") 
resultsFilename = "..\Resultats\CampVisual_Resultats"+ timetag +".txt" 
file = open(resultsFilename, 'w') 
if file.mode != 'w' :
    print ('Error reading ' + resultsFilename)
    exit()
    
#file.write('-------------------------------------\n')
#file.write('           New experiment            \n')
#file.write('-------------------------------------\n')
strAux = "Version" + sep + CVVersion + endl
file.write(strAux)
strAux = 'Initial Date & Time:' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + sep + endl
file.write(strAux)
strAux = 'Dot size' + sep + dotSize + sep + sep +sep + sep + sep+ endl
file.write(strAux)
strAux = 'ID patient' + sep + idPatient + endl
file.write(strAux)
file.close()


#Variables de configuració
backgroundColor = "black" #"darkgray"
focusColor = "white"
centralColor = "orange"
dotSpeed = 1 #segons

#Variables de fluxe execució
deg90 = 1
deg45 = 2
deg0 = 3
deg315 = 4
deg270 = 5
deg225 = 6
deg180 = 7
deg135 = 8
experimentDone = 9
currentStep = deg90
#numberOfLoops = int(nIterationsFile)
numberOfLoops = 2
eyeLeft=1
eyeRight=2
eyeBoth=3
applyEyeLeft=int(doLeftEyeFile)
applyEyeRight=int(doRightEyeFile)
applyEyeBoth=int(doBothEyesFile)
currentEye=eyeRight
currentLoop = 0
# num keys presseed ha de ser zero per tal que el 1r loop vagi de dins a fora
numberKeysPressed = 0 
maxKeysPressed = 0
GoUp=100
GoDown=101
GoEnter=102
aStr=''
bStr=''
cStr=''
dStr=''
eStr=''
fStr=''
gStr=''
hStr=''
    
if (applyEyeRight == 0) and applyEyeLeft == 1:
    currentEye = eyeLeft
elif applyEyeRight == 0 and applyEyeBoth == 1:
    currentEye = eyeBoth

#Obtenim la resolució del monitor per posicionar el centre
#OS dependent TODO
wMonitorRes = 1920
hMonitorRes = 1080

xPosition = 0
yPosition = 0

def writeToFile (msg):
    global resultsFilename
    file = open(resultsFilename, 'a') 
    file.write (msg + '\n')
    file.close()
    
#Key press action
def kp(event):
    #if event.keysym == 'Return':
        #verticalAxis(w, int(xLine/2), int(yLine/2), dotSizeNumber, 1)
    if event.keysym == 'Up':
        newMovement(w, GoUp)
    elif event.keysym == 'Down':
        newMovement(w, GoDown)
    elif event.keysym == 'Space':
        #     spaceAction = 1 
        print ("space")
    elif event.keysym == 'Return':
        newMovement(w, GoEnter)
        experimentProcedure()
    elif event.keysym == 'Escape':
        writeToFile('Experiment closed')
        master.destroy()
        
#Dibuixem rectangle
def cursorRect(canvas, xPos, yPos, size, on) :
    #print (xPos,yPos)
    color = focusColor
    if on == 0:
        color = backgroundColor
    elif on == 2:
        color = centralColor
        
    canvas.create_rectangle(xPos, yPos, xPos+size, yPos+size, fill=color, outline=focusColor)
    
#Dibuixem grid
def checkered(canvas, line_distance):
   # vertical lines at an interval of "line_distance" pixel
   for x in range(line_distance,canvas_width,line_distance):
      canvas.create_line(x, 0, x, canvas_height, fill=focusColor)
   # horizontal lines at an interval of "line_distance" pixel
   for y in range(line_distance,canvas_height,line_distance):
      canvas.create_line(0, y, canvas_width, y, fill=focusColor)
    
   # cross line if necessary
   if (int(crossLineFile) == 1):       
       
       init_w = int(canvas_width/dotSizeNumber)*dotSizeNumber
       print (init_w)
       canvas.create_line (0,0,xDotCenter*2, yDotCenter*2, fill=focusColor)
       canvas.create_line (init_w,0,0,yDotCenter*2, fill=focusColor)
       
       
#New movement to do
def newMovement(canvas, direction):

    global xLine
    global yLine
    #global isUpPressed
    global numberKeysPressed
    global dotSize
    global currentStep
    global xPosition
    global yPosition
        
    previousOffsetX = 0
    previousOffsetY = 0

    xLine1 = int(xLine/2)
    yLine1 = int(yLine/2)
    xLineCurrent = xLine1
    yLineCurrent = yLine1
    #print("newMovement (1) numberKeysPressed",numberKeysPressed)
    
    prevnumberKeysPressed = numberKeysPressed
    
    #if numberKeysPressed == 0 and direction == GoDown:
    if currentLoop==0 and numberKeysPressed == 0 and direction == GoDown:
        print("can't go close to center")
        return
    if currentLoop==1 and numberKeysPressed == maxKeysPressed and direction == GoUp:
        print("can't go far from center")
        return
    
    if currentStep == deg90:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = 1
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = -1
        yLine1 = yLine1+numberKeysPressed
        yLineCurrent = yLine1
        previousOffsetX = 0
    elif currentStep == deg45:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = 1
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = -1
            previousOffsetX = 2
        yLine1 = yLine1+numberKeysPressed
        yLineCurrent = yLine1
        xLine1 = xLine1-numberKeysPressed
        xLineCurrent = xLine1-1
    elif currentStep == deg0:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = 0
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = 0
            previousOffsetX = 2
        xLine1 = xLine1-numberKeysPressed
        xLineCurrent = xLine1-1
    elif currentStep == deg315:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = -1
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = 1
            previousOffsetX = 2
        yLine1 = yLine1-numberKeysPressed-1+1
        yLineCurrent = yLine1
        xLine1 = xLine1-numberKeysPressed
        xLineCurrent = xLine1-1
    elif currentStep == deg270:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = -1
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = 1
        yLine1 = yLine1-numberKeysPressed+1
        yLineCurrent = yLine1-1
        previousOffsetX = 0
    elif currentStep == deg225:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = -1
            previousOffsetX = 2
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = 1
            previousOffsetX = 0
        yLine1 = yLine1-numberKeysPressed-1+1
        yLineCurrent = yLine1
        xLine1 = xLine1+numberKeysPressed
        xLineCurrent = xLine1-1
    elif currentStep == deg180:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetX = 2
            previousOffsetY = 0
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = 0
            previousOffsetX = 0
        xLine1 = xLine1+numberKeysPressed
        xLineCurrent = xLine1-1
    elif currentStep == deg135:
        if direction == GoUp:
            numberKeysPressed = numberKeysPressed -1
            previousOffsetY = 1
            previousOffsetX = 2
        elif direction == GoDown:
            numberKeysPressed = numberKeysPressed +1
            previousOffsetY = -1
        yLine1 = yLine1+numberKeysPressed
        yLineCurrent = yLine1
        xLine1 = xLine1+numberKeysPressed
        xLineCurrent = xLine1-1    
    #print("newMovement (2) numberKeysPressed",numberKeysPressed,"xLine1",xLine1,"yLine1",yLine1)

    xNextValue = (int)(xLine1-xDotPosition)
    yNextValue = (int)(yLineCurrent-yDotPosition)
    xNextPosition = xLine1 * dotSizeNumber
    yNextPosition = yLineCurrent * dotSizeNumber
    
    #print ('xNextPosition:',xNextPosition,',',yNextPosition,' yNextPosition')
    
    if (xNextValue == 0 and yNextValue ==0) or (xNextPosition < 0) or (xNextPosition > wMonitorRes) or (yNextPosition < 0) or (yNextPosition > hMonitorRes):
        numberKeysPressed = prevnumberKeysPressed;
        return
 
    xPosition = xLine1 * dotSizeNumber
    yPosition = yLineCurrent * dotSizeNumber
    xPrevPosition = (xLineCurrent+previousOffsetX) * dotSizeNumber
    yPrevPosition = (yLineCurrent+previousOffsetY) * dotSizeNumber
    xPrevValue = xLineCurrent+previousOffsetX-xDotPosition
    yPrevValue = yLineCurrent+previousOffsetY-yDotPosition

    #print ('curr:',xPosition,',',yPosition,' xLine1',xNextValue,' yCurrentLine',yNextValue)

    focus=1
    if direction == GoEnter:
        focus = 0
    cursorRect(canvas, xPosition, yPosition, dotSizeNumber, focus)  
    
    if xPrevValue != 0 or yPrevValue != 0:
        cursorRect(canvas, xPrevPosition, yPrevPosition, dotSizeNumber, 0)
    #print ('pre:',xPrevPosition,',',yPrevPosition)
    master.update()

def clearCoords():
    global aStr
    global bStr
    global cStr
    global dStr
    global eStr
    global fStr
    global gStr
    global hStr
    
    aStr=''
    bStr=''
    cStr=''
    dStr=''
    eStr=''
    fStr=''
    gStr=''
    hStr=''
    
def writeCoords2Disk():
    global aStr
    global bStr
    global cStr
    global dStr
    global eStr
    global fStr
    global gStr
    global hStr
    
    writeToFile ('A'+aStr)
    writeToFile ('B'+bStr)
    writeToFile ('C'+cStr)
    writeToFile ('D'+dStr)
    writeToFile ('E'+eStr)
    writeToFile ('F'+fStr)
    writeToFile ('G'+gStr)
    writeToFile ('H'+hStr)
    writeToFile ('Abis'+aStr)
        
#Coneix el procediment del experiment
def experimentProcedure():
    global currentStep
    global currentLoop
    global numberKeysPressed
    global xPosition
    global yPosition
    global currentEye
    global applyEyeRight
    global applyEyeBoth
    global aStr
    global bStr
    global cStr
    global dStr
    global eStr
    global fStr
    global gStr
    global hStr
    
    xPosFile = (xPosition / dotSizeNumber) - xDotPosition
    yPosFile = (yPosition / dotSizeNumber) - yDotPosition

    #Guardem info a disc
    if currentStep == deg90:
        aStr = aStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg45:
        bStr = bStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg0:
        cStr = cStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg315:
        dStr = dStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg270:
        eStr = eStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg225:
        fStr = fStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg180:
        gStr = gStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    elif currentStep == deg135:
        hStr = hStr+sep+'%d'%xPosFile+sep+'%d'%yPosFile
    #writeToFile ('XPosition = %d'%xPosition + ' YPosition = %d'%yPosition)            
        
    currentStep = currentStep + 1

    if currentStep == experimentDone:
        print("experimentProcedure -> experimentDone (iteration)")
        currentLoop = currentLoop +1       
        print ('currentEye:',currentEye,', currentLoop',currentLoop)

        #prepara inici del seguent loop                    
        currentStep = deg90
        maxKeysPressed = -1*yDotPosition-1
        if currentLoop ==0:
            numberKeysPressed = 0
        else:
            numberKeysPressed = maxKeysPressed          

        # si es l'ultima iteracio de l'ull actual        
        if currentLoop == numberOfLoops:
            
            if ((currentEye == eyeRight and applyEyeLeft != 1 and applyEyeBoth != 1) or
               (currentEye == eyeLeft and applyEyeBoth != 1) or
               (currentEye == eyeBoth)):
                    # final experiment
                    messagebox.showinfo("Perimetria", "Experiment done")
                    # escriu resultat de cada eix i cada iteracio
                    writeCoords2Disk()
                    # tancament arxiu
                    writeToFile('Experiment Done at '+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    # copiem arxiu per poder fer la mascara des de movilab
                    resultsFilename_mask = "..\Resultats\CampVisual_Resultats.txt" 
                    shutil.copy(resultsFilename, resultsFilename_mask)

                    return
                    
            elif (currentEye==eyeRight and applyEyeLeft==1):           
                    # escriu resultat de cada eix i cada iteracio
                    writeCoords2Disk()
                    # prepara per seguent ull
                    clearCoords()
                    writeToFile('Eye'+sep+'Left'+sep+sep+sep)
                    writeToFile('Direction'+sep+'Col1'+sep+'Row1'+sep+'Col2'+sep+'Row2')
                    currentEye=eyeLeft
                    currentLoop=0
                    messagebox.showinfo("Perimetria", "Eye: Right")
        
                    
            elif ((currentEye==eyeRight and applyEyeBoth==1) or
                 (currentEye==eyeLeft and applyEyeBoth==1)):
                    # escriu resultat de cada eix i cada iteracio           
                    writeCoords2Disk()
                    # prepara per seguent ull
                    clearCoords()
                    writeToFile('Eye'+sep+'Both'+sep+sep+sep)
                    writeToFile('Direction'+sep+'Col1'+sep+'Row1'+sep+'Col2'+sep+'Row2')
                    currentEye=eyeBoth
                    currentLoop=0
                    messagebox.showinfo("Perimetria", "Eye: Both")
    else:
        print("experimentProcedure -> next step (axis)")
        # num keys presseed ha de ser zero per tal que el 1r loop vagi de dins a fora
        if currentLoop ==0:
            numberKeysPressed = 0
        else:
            numberKeysPressed = 0
            if currentStep == deg90:
                maxKeysPressed = -1*yDotPosition-1
            elif currentStep == deg45:
                maxKeysPressed =  -1*yDotPosition-1
            elif currentStep == deg0:
                maxKeysPressed = -1*xDotPosition-1
            elif currentStep == deg315:
                maxKeysPressed =  -1*yDotPosition-1
            elif currentStep == deg270:
                maxKeysPressed = -1*yDotPosition-1
            elif currentStep == deg225:
                maxKeysPressed =  -1*yDotPosition-1
            elif currentStep == deg180:
                maxKeysPressed = -1*xDotPosition-1
            elif currentStep == deg135:
                maxKeysPressed =  -1*yDotPosition-1
            numberKeysPressed = maxKeysPressed
        
    
#Generem GUI
master = Tk()
master.title('Experiment: Perimetria')
master.bind_all('<KeyPress>', kp)


canvas_width = wMonitorRes
canvas_height = hMonitorRes 
w = Canvas(master, 
           width=canvas_width,
           height=canvas_height,
           bg=backgroundColor)
w.pack()

dotSizeNumber = int(dotSize)

#Dibuixa punt central
xLine = wMonitorRes / dotSizeNumber
yLine = hMonitorRes / dotSizeNumber
cursorRect (w,int(xLine/2)*dotSizeNumber, int(yLine/2)*dotSizeNumber, dotSizeNumber, 2)
xDotCenter = int(xLine/2)*dotSizeNumber+(dotSizeNumber/2)
yDotCenter = int(yLine/2)*dotSizeNumber+(dotSizeNumber/2)
xDotPosition = (int)(xLine/2)
yDotPosition = (int)(yLine/2)

#Dibuixa grid
checkered(w,dotSizeNumber)
#valor inicial per 90deg
maxKeysPressed = -1*yDotPosition-1

#Initial message
strs='Left'
if currentEye==eyeRight:
    strs='Right'
elif currentEye==eyeBoth:
    strs ='Both'
    
#Escriu capçalera a l'arxiu de resultats
messagebox.showinfo("Perimetria", 'Eye:'+strs)
writeToFile('Eye'+sep+strs+sep+sep+sep+sep+sep)
writeToFile('Direction'+sep+'Col1'+sep+'Row1'+sep+'Col2'+sep+'Row2')

mainloop()





