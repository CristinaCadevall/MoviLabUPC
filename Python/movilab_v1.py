"""
Arxiu: movilab_v1_0_0.py
Project: Tesis Lali, programa Movilab
Experiment: SC, AV, MO, EN i PV
Created on Sat Feb 23 11:17:29 2019
@author: ccadevall
Movilab v1.0.0
Hitoria dels canvis
versio 1.0.12 afegir version dins resultats
              afegir pregunta confirmació de inici de tests per protegir resultats
versió 1.0.13 enmarcar la lletra de ENt amb un cercle gris
              fix problema mida font més gran que fila anterior en monitor CUV -> createAVFontSize
versió 1.0.14 afegir camera per controlar la mirada durant els tests
versió 1.0.15 nou test ENt2 amb mida lletra fixe per a proves amb el deslumbrometro
             ATEMCIO: avancem de versió però pel PC del deslumbrometre ens convé que el nom de l'arxiu sigui sempre el mateix. per tant el nom arxiu a partir d'ara no indica versio
Copyright © E.Sánchez 2021 (tots els drets reservats)
Autors: C.Cadevall, J.Gispets, A.Matilla, E.Sánchez, A.Torrents i M.Vilaseca
Per solicitar una llicència contactar eulalia.sanchez@upc.edu

"""

# from tkinter import * as tk
import tkinter as tk
from tkinter import messagebox
import random
import numpy as np
import matplotlib.pyplot as plt
import csv
import time
import datetime
from PIL import Image,ImageTk, ImageDraw  
from PIL import ImageFont
import os 
import cv2

movilabVersion = "Movilab v 1.0.15"

# Obtenim la resolució del monitor per posicionar el centre
# OS dependent TODO
wMonitorRes = 1920
hMonitorRes = 1080

# ajust files Map result
wrapLengthAV = 100
wrapLengthSC = 160
# mida font controls tests
fontSizeT1 = 20
fontSizeC1 = 16
fontSizeC2 = 12
fontSizeC3 = 8

# depen del monitor canviem variables
monitorHPOmen = True
if monitorHPOmen == False:
    # portatil DELL Cristina
    # wMonitorRes = 3840
    # hMonitorRes = 2160  
    wrapLengthAV = 100
    wrapLengthSC = 160
    # mida font controls tests
    fontSizeT1 = 16
    fontSizeC1 = 12
    fontSizeC2 = 10
    fontSizeC3 = 6

# mida en mm zona on es pinten lletres en el test MO2 i imatge en MO3
widthMO_MM = 341
heightMO_MM = 218

# llista de tests de llicencia.csv
gEnable = np.zeros(7,dtype=np.int16)
# index dels tests de llicencia.csv
indexAV = 0
indexSC = 1
indexENSC = 2
indexENT = 3
indexCV = 4
indexMO = 5
indexPV = 6

gCamera = np.zeros(5,dtype=np.int16)
# index dels items config camera
indexId = 0
indexTop = 1
indexLeft = 2
indexHeight = 3
indexWidth = 4
# nom elements config
gCameraName =["Id","Top","Left","Height","Width"]

#enlluernament 
gEnlluernament = np.zeros(3,dtype=np.int16)
indexUsarAVFixe = 0
indexAVFixe = 1
indexTempsON = 2

# test ENSC sempre amb AV 1.1 logMAR (gran però que hi cap tota la taula de SC a la pantalla)
# depen de la distancia pacient
indexAVtestENSC_500 = 4
indexAVtestENSC_1000 = 8

# Variables de configuració
backgroundColor = "white"
backgroundColorInv = "black"

# colorsText
numColorsText = 48

# lletres que farem servir per AV i SC
masterLettersList = ['C', 'D', 'H', 'K', 'N', 'O', 'R', 'S', 'V', 'Z']
masterLettersListEN = ['C', 'H', 'K', 'N', 'R', 'S', 'V', 'Z']

# AV nominals
"""
listAVNom = [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.15, 0.2, 0.25,
             0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
"""
listAVLogMARNom = [1.5, 1.4, 1.3, 1.2, 1.1, 1, 0.9, 0.8, 0.7, 0.6, 
                   0.5, 0.4, 0.3, 0.2, 0.15 , 0.1, 0.05, 0, -0.05, -0.1, -0.2]
indexLastAVOK = 0
# AV calculades i font size calculat
listAV = np.zeros(len(listAVLogMARNom))
listAVLogMAR = np.zeros(len(listAVLogMARNom))
listFontSize = np.zeros(len(listAVLogMARNom))

textSimulaCV = ["E N  U N  L U G A R   D E  L A  M A N C H A ,  D E  C U Y O  N O M B R E  N O  Q U I E R O  A C O R D A R M E ,  N O  H A  M U C H O  T I E M P O  Q U E  V I V I A  U N  H I D A L G O  D E  L O S  D E  L A N Z A  E N  A S T I L L E R O ,  A D A R G A  A N T I G U A ,  R O C I N  F L A C O  Y  G A L G O  C O R R E D O R .  U N A  O L L A  D E  A L G O  M A S  V A C A  Q U E  C A R N E R O ,  S A L P I C O N  L A S  M A S  N O C H E S ,  D U E L O S  Y  Q U E B R A N T O S  ",
                "L O S  S A B A D O S ,  L E N T E J A S  L O S  V I E R N E S ,  A L G U N  P A L O M I N O  D E  A N A D I D U R A  L O S  D O M I N G O S ,  C O N S U M I A N  L A S  T R E S  P A R T E S  D E  S U  H A C I E N D A .  E L  R E S T O  D E L L A  C O N C L U I A N  S A Y O  D E  V E L A R T E ,  C A L Z A S  D E  V E L L U D O  P A R A  L A S  F I E S T A S  C O N  S U S  P A N T U F L O S  D E  L O  M I S M O ,  L O S  D I A S  D E  E N T R E  S E M A N A  S E  H O N R A B A",
                "C O N  S U  V E L L O R I  D E  L O  M A S  F I N O .  T E N I A  E N  S U  C A S A  U N A  A M A  Q U E  P A S A B A  D E  L O S  C U A R E N T A ,  Y  U N A  S O B R I N A  Q U E  N O  L L E G A B A  A  L O S  V E I N T E ,  Y  U N  M O Z O  D E  C A M P O  Y  P L A Z A ,  Q U E  A S I  E N S I L L A B A  E L  R O C I N  C O M O  T O M A B A  L A  P O D A D E R A .  F R I S A B A  L A  E D A D  D E  N U E S T R O  H I D A L G O  C O N  L O S  C I N C U E N T A ",
                "A N O S ,  E R A  D E  C O M P L E X I O N  R E C I A ,  S E C O  D E  C A R N E S ,  E N J U T O  D E  R O S T R O ;  G R A N  M A D R U G A D O R  Y  A M I G O  D E  L A  C A Z A .  Q U I E R E N  D E C I R  Q U E  T E N I A  E L  S O B R E N O M B R E  D E  Q U I J A D A  O  Q U E S A D A  ( Q U E  E N  E S T O  H A Y  A L G U N A  D I F E R E N C I A  E N  L O S  A U T O R E S  Q U E  D E S T E  C A S O  E S C R I B E N ) ,  A U N Q U E  P O R  C O N J E T U R A S ",
                "V E R O S I M I L E S  S E  D E J A  E N T E N D E R  Q U E  S E  L L A M A  Q U I J A N A ;  P E R O  E S T O  I M P O R T A  P O C O  A  N U E S T R O  C U E N T O ;  B A S T A  Q U E  E N  L A  N A R R A C I O N  D É L  N O  S E  S A L G A  U N  P U N T O  D E  L A  V E R D A D .",
                "E S ,  P U E S ,  D E  S A B E R ,  Q U E  E S T E  S O B R E D I C H O  H I D A L G O ,  L O S  R A T O S  Q U E  E S T A B A  O C I O S O  ( Q U E  E R A N  L O S  M A S   D E L  A N O )  S E  D A B A  A  L E E R  L I B R O S  D E  C A B A L L E R I A S  C O N  T A N T A  A F I C I O N  Y  G U S T O ,  Q U E  O L V I D O  C A S I  D E  T O D O  P U N T O  E L  E J E R C I C I O  D E  L A  C A Z A,  Y  A U N  L A  A D M I N I S T R A C I O N  D E  S U  H A C I E N D A ; "
                "Y  L L E G O  A  T A N T O  S U  C U R I O S I D A D  Y  D E S A T I N O  E N  E S T O ,  Q U E  V E N D I O  M U C H A S  H A N E G A S  D E  T I E R R A  D E  S E M B R A D U R A ,  P A R A  C O M P R A R  L I B R O S  D E  C A B A L L E R I A S  E N  Q U E  L E E R ;  Y  A S I  L L E V O  A  S U  C A S A  T O D O S  C U A N T O S  P U D O  H A B E R  D E L L O S ;  Y  D E  T O D O S  N I N G U N O S  L E  P A R E C I A N  T A N  B I E N  C O M O  L O S  Q U E  C O M P U S O ",
                "E L  F A M O S O  F E L I C I A N O  D E  S I L V A :  P O R Q U E  L A  C L A R I D A D  D E  S U  P R O S A ,  Y  A Q U E L L A S  I N T R I N C A D A S  R A Z O N E S  S U Y A S ,  L E  P A R E C I A N  D E  P E R L A S ;  Y  M A S  C U A N D O  L L E G A B A  A  L E E R  A Q U E L L O S  R E Q U I E B R O S  Y  C A R T A S  D E  D E S A F I O ,  D O N D E  E N  M U C H A S  P A R T E S  H A L L A B A  E S C R I T O :  L A  R A Z O N  D E  L A  S I N R A Z O N  Q U E  A  M I ",
                "R A Z O N  S E  H A C E ,  D E  T A L  M A N E R A  M I  R A Z O N  E N F L A Q U E C E ,  Q U E  C O N  R A Z O N  M E  Q U E J O  D E  L A  V U E S T R A  F E R M O S U R A ,  Y  T A M B I E N  C U A N D O  L E I A :  L O S   A L T O S  C I E L O S  Q U E  D E  V U E S T R A  D I V I N I D A D  D I V I N A M E N T E  C O N  L A S  E S T R E L L A S  S E  F O R T I F I C A N ,  Y  O S  H A C E N  M E R E C E D O R A  D E L  M E R E C I M I E N T O  Q U E  M E R E C E  L A ",
                "V U E S T R A  G R A N D E Z A .  C O N  E S T A S  Y  S E M E J A N T E S  R A Z O N E S  P E R D I A  E L  P O B R E  C A B A L L E R O  E L  J U I C I O ,  Y  D E S V E L A B A S E  P O R  E N T E N D E R L A S ,  Y  D E S E N T R A N A R L E S  E L  S E N T I D O ,  Q U E  N O  S E  L O  S A C A R A ,  N I  L A S  E N T E N D I E R A  E L  M I S M O  A R I S T O T E L E S ,  S I  R E S U C I T A R A  P A R A  S O L O  E L L O .  N O  E S T A B A  M U Y  B I E N  C O N  L A S ",
                "H E R I D A S  Q U E  D O N  B E L I A N I S  D A B A  Y  R E C I B I A ,  P O R Q U E  S E  I M A G I N A B A  Q U E  P O R  G R A N D E S  M A E S T R O S  Q U E  L E  H U B I E S E N  C U R A D O ,  N O  D E J A R I A  D E  T E N E R  E L  R O S T R O  Y  T O D O  E L  C U E R P O  L L E N O  D E  C I C A T R I C E S  Y  S E N A L E S ;  P E R O  C O N  T O D O  A L A B A B A  E N  S U  A U T O R  A Q U E L  A C A B A R  S U  L I B R O  C O N  L A  P R O M E S A  D E ",
                "A Q U E L L A  I N A C A B A B L E  A V E N T U R A ,  Y  M U C H A S  V E C E S  L E  V I N O  D E S E O  D E  T O M A R  L A  P L U M A ,  Y  D A R L E  F I N  A L  P I E  D E  L A  L E T R A  C O M O  A L L I  S E  P R O M E T E ;  Y  S I N  D U D A  A L G U N A  L O  H I C I E R A ,  Y  A U N  S A L I E R A  C O N  E L L O ,  S I   O T R O S   M A Y O R E S  Y  C O N T I N U O S  P E N S A M I E N T O S  N O  S E  L O  E S T O R B A R A N."]

# calib Monitor -------------------------------------------------------------
# amb valors cal L del 19 març
# hp Omen pol de grau 3
# [ 0.75029647  0.1455833   0.09839749 -0.00325266]
# hp Omen Gamma ajustats manualment 22 març
iGamma = 0
iOffset = 1
iGain = 2
iMidaQmm = 3
iMidaQpix = 4
iFactorMidaFont = 5
vCalMonitor = [2.6, 0.015, 0.985, 170, 600, 0.0599]
iDistPacient = 0
iMidaPix = 1
iMidaGrauPix = 2
vCalTests = [500, 0.283, 30]

# llista imatges PV
vPV_VisualMemory = []
vPV_VisualFigureGround = []
vPV_VisualClosure = []


# Key press action
def kp(event):
    # envia key a la app
    app.newLetterPress(event.keysym)
    # print(event.keysym)

def mouseLeftClick(event):
    app.mouseLeftClick(event)

def mouseEnter(event):
    app.mouseEnter(event)

def mouseLeave(event):
    app.mouseLeave(event)

def on_closing():
    app.destroy()
    master.destroy()
    
# busca nom arxius imatge del test de PV
def findPVImages(polaritatInversa):
    # This is to get the directory that the program  
    # is currently running in. 
    #dir_path = os.path.dirname(os.path.realpath(__file__)) 
    # al final buscar els noms no es prou robuts; he escrit tots els noms
    dir_path = "..\TVPS4\S2_Visual Memory"
    if polaritatInversa == True:
        dir_path = "..\TVPS4Inv\S2_Visual Memory"
    """
    for root, dirs, files in os.walk(dir_path): 
        for file in files:  
            # change the extension from '.mp3' to  
            # the one of your choice. 
            # atencio walk es sensible a majuscules / min en l'extensio depen de quin PC !!!
            if file.endswith('.tif'): 
                vPV_VisualMemory.append(root+'/'+str(file)) 
    """
    fileName = dir_path +"\Sub 2 A0.tif";
    vPV_VisualMemory.clear()
    vPV_VisualMemory.append(fileName) 
    fileName = dir_path +"\Sub 2 A1.tif";
    vPV_VisualMemory.append(fileName) 
    fileName = dir_path +"\Sub 2 A2.tif";
    vPV_VisualMemory.append(fileName) 
    fileName = dir_path +"\Sub 2 A3.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 01-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 01-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 02-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 02-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 03-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 03-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 04-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 04-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 05-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 05-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 06-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 06-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 07-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 07-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 08-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 08-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 09-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 09-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 10-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 10-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 11-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 11-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 12-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 12-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 13-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 13-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 14-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 14-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 15-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 15-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 16-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 16-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 17-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 17-2.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 18-1.tif";
    vPV_VisualMemory.append(fileName)      
    fileName = dir_path +"\Sub 2 MEM 18-2.tif";
    vPV_VisualMemory.append(fileName)      

    dir_path = "..\TVPS4\S6_Visual Figure_Ground"
    if polaritatInversa == True:
        dir_path = "..\TVPS4Inv\S6_Visual Figure_Ground"
    """
    for root, dirs, files in os.walk(dir_path): 
        for file in files:  
            # change the extension from '.mp3' to  
            # the one of your choice. 
            if file.endswith('.tif'):            
                vPV_VisualFigureGround.append(root+'/'+str(file)) 
    """
    vPV_VisualFigureGround.clear()
    fileName = dir_path +"\Ex A FGR Sub 6.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Ex B FGR Sub 6.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 01.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 02.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 03.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 04.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 05.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 06.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 07.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 08.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 09.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 10.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 11.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 12.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 13.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 14.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 15.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 16.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 17.tif";
    vPV_VisualFigureGround.append(fileName) 
    fileName = dir_path +"\Sub 6 FRG 18.tif";
    vPV_VisualFigureGround.append(fileName) 


    dir_path = "..\TVPS4\S7_Visual Closure"
    if polaritatInversa == True:
        dir_path = "..\TVPS4Inv\S7_Visual Closure"
    """
    for root, dirs, files in os.walk(dir_path): 
        for file in files:  
            # change the extension from '.mp3' to  
            # the one of your choice. 
            if file.endswith('.tif'): 
                vPV_VisualClosure.append(root+'/'+str(file)) 
    """
    vPV_VisualClosure.clear()
    fileName = dir_path +"\CLO EX A.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\CLO EX B.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 01.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 02.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 03.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 04.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 05.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 06.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 07.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 08.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 09.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 10.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 11.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 12.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 13.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 14.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 15.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 16.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 17.tif";
    vPV_VisualClosure.append(fileName) 
    fileName = dir_path +"\Sub 7 CLO 18.tif";
    vPV_VisualClosure.append(fileName) 
    
    print(len(vPV_VisualMemory))
    print(len(vPV_VisualFigureGround))
    print(len(vPV_VisualClosure))
    

def SetColorPolaritat(self):
    if self.polaritatInversa == True:
        self.backgroundColor = backgroundColorInv
        self.frontColor = backgroundColor
    else:
        self.backgroundColor = backgroundColor
        self.frontColor = backgroundColorInv

# getEnableTests ho agafa d'un arxiu
def getEnableTests():
    with open('..\license.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if row[0] == "AV":
                gEnable[indexAV] = int(row[1])
            if row[0] == "SC":
                gEnable[indexSC] = int(row[1])
            if row[0] == "ENSC":
                gEnable[indexENSC] = int(row[1])
            if row[0] == "ENT":
                gEnable[indexENT] = int(row[1])
            if row[0] == "PV":
                gEnable[indexPV] = int(row[1])
            if row[0] == "P":
                gEnable[indexCV] = int(row[1])
            if row[0] == "B":
                gEnable[indexMO] = int(row[1])
        csv_file.close()

# getCameraConfig ho agafa d'un arxiu
def getCameraConfig():
    with open('..\camera.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            if row[0] == gCameraName[indexId]:
                gCamera[indexId] = int(row[1])
            if row[0] == gCameraName[indexTop]:
                gCamera[indexTop] = int(row[1])
            if row[0] == gCameraName[indexLeft]:
                gCamera[indexENSC] = int(row[1])
            if row[0] == gCameraName[indexHeight]:
                gCamera[indexHeight] = int(row[1])
            if row[0] == gCameraName[indexWidth]:
                gCamera[indexWidth] = int(row[1])
        csv_file.close()

# guardar config camera
def saveCameraConfig():
    writer = open("..\camera.csv", 'w')
    for i in range(0, len(gCamera)):
        valName = "%s" % gCameraName[i]
        val = "%d" % gCamera[i]
        row = valName + ";" + val + "\n"
        writer.write(row)
    writer.close()

# ajustos enlluernament ho agafa d'un arxiu
def getEnlluernament():
    with open('..\enlluernament.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            print(row[0],row[1])
            if row[0] == "UsarAVFixe":
                gEnlluernament[indexUsarAVFixe] = int(row[1])
            if row[0] == "IndexAVfixe":
                gEnlluernament[indexAVFixe] = int(row[1])
            if row[0] == "TempsON":
                gEnlluernament[indexTempsON] = int(row[1])
        csv_file.close()

# valors distancia examen 
def getDistanciaExamen():
    # distancia pacient a monitor en mm
    distanciaPacient = 500.0
    with open('..\distanciaExamen.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if row[0] == "DP":
               distanciaPacient = float(row[1])
            line_count += 1
        csv_file.close()
    return distanciaPacient

# guardar distancia examen 
def saveDistanciaExamen(distanciaPacient):
    writer = open("..\distanciaExamen.csv", 'w')
    row = "DP;%f" % distanciaPacient
    row += "\n"
    writer.write(row)
    writer.close()

# valors actuals calibracio Monitor els obtinc d'un arxiu extern
def getCalMonitor():
    with open('..\calMonitor.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        for row in csv_reader:
            if line_count == 1:
                for i in range(len(row)):
                    vCalMonitor[i] = float(row[i])
            line_count += 1
        csv_file.close()


# guardar calibracio Lluminancia
def saveCalMonitor():
    writer = open("..\calMonitor.csv", 'w')
    row = "gamma;offset;gain;midaQuadratMM;midaQuadratPix;factorMidaFont"+"\n"
    writer.write(row)
    row = "%f" % vCalMonitor[0]
    for i in range(1, len(vCalMonitor)):
        row += ";" + "%f" % vCalMonitor[i]
    row += "\n"
    writer.write(row)
    writer.close()


# guardar calibracio Lluminancia
def saveCalGrisosMonitor(vG, vL):
    """ no funciona !!!
    with open('..\calNivelsGris.csv','w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        for i in range(len(vLCal)):
            nivell = "%f" % vNDG[i]
            cal = "%f" % vLCal[i]
            row = nivell + ";" + cal
            csv_writer.writerow(row)
    """
    writer = open("..\calNivelsGris.csv", 'w')
    for i in range(0, len(vL)):
        nivell = "%f" % vG[i]
        cal = "%f" % vL[i]
        row = nivell + ";" + cal + "\n"
        writer.write(row)
    writer.close()

# valors resultat cv
def getCV_AmbosOjos():
    numAxis = 9
    vCol = np.zeros(numAxis)
    vRow = np.zeros(numAxis)
    with open('..\Resultats\CampVisual_Resultats.txt') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        line_count = 0
        iAxis = 0
        isBoth = False
        lineAxisBoth = 0
        for row in csv_reader:
            # detecta inici Eye Both
            if row[0] == 'Eye' and row[1] == 'Both':
                isBoth = True
                lineAxisBoth = line_count+2
            else:
                if isBoth == True and line_count >= lineAxisBoth: 
                    # calculo promig iteracions de cada eix
                    avCol = 0.0
                    avRow = 0.0
                    nIt = 0
                    for i in range(len(row)):
                        if i == 1 or i == 3 or i == 5:
                            avCol += float(row[i])
                            nIt +=1
                        if i == 2 or i == 4 or i == 6:
                            avRow += float(row[i])
                    # si tenim valors eix els guardo
                    if nIt>0:
                        avCol = avCol / nIt
                        avRow = avRow / nIt
                        vCol[iAxis] = avCol
                        vRow[iAxis] = avRow
                        iAxis +=1
                    # detecta final de Eye Both
                    if row[0] == 'Abis': 
                        isBoth = False
            line_count += 1
        csv_file.close()
    return vCol,vRow

def createPhotoImage(imBackground):
    imCombined = imBackground    
    photoImage = ImageTk.PhotoImage(imCombined)
    return photoImage

def createPhotoImageBackground(imBackground,doApplyOverlay):
    # d'entrada combined es sense overlay -> només background
    imCombined = imBackground
    if doApplyOverlay == True:
        # si calia overlay la creo combined amb overlay
        wi = imBackground.width
        hi = imBackground.height
        #sombra = (196,196,196,196) més "lletós"
        sombra = (128,128,128,128)
        imOverlay = Image.new("RGBA", (wi,hi), sombra)
        drawOverlay = ImageDraw.Draw(imOverlay)
        # load posicions resultat CV
        vX_CV,vY_CV = getCV_AmbosOjos()
        # canvi coordenades de graus a pixels imatge
        numGrausCV_w = 61
        numGrausCV_h = 35
        hGrau = hi/numGrausCV_h
        wGrau = wi/numGrausCV_w
        vPoints = np.zeros(2*len(vX_CV))
        index = 0
        for i in range(0,len(vX_CV)):
            vPoints[index] = (vX_CV[i] + numGrausCV_w/2)*wGrau
            index +=1
            vPoints[index] = (vY_CV[i] + numGrausCV_h/2)*hGrau
            index +=1
        # pinta poligon
        drawOverlay.polygon(tuple(vPoints),fill=(0,0,0,0))
        # crea imatge amb overlay
        imCombined = Image.alpha_composite (imBackground, imOverlay)
    photoImage = ImageTk.PhotoImage(imCombined)
    return photoImage

def createPhotoImageSimulaCV(hi,wi,fontSize,heigthL,widthL,idPacient):
    # crea una imatge nova
    sombra = (128,128,128,128)
    imOverlay = Image.new("RGBA", (wi,hi), sombra)
    drawOverlay = ImageDraw.Draw(imOverlay)
    # load posicions resultat CV
    vX_CV,vY_CV = getCV_AmbosOjos()
    # canvi coordenades de graus a pixels imatge
    numGrausCV_w = 61
    numGrausCV_h = 35
    hGrau = hi/numGrausCV_h
    wGrau = wi/numGrausCV_w
    vPoints = np.zeros(2*len(vX_CV))
    index = 0
    for i in range(0,len(vX_CV)):
        vPoints[index] = (vX_CV[i] + numGrausCV_w/2)*wGrau
        index +=1
        vPoints[index] = (vY_CV[i] + numGrausCV_h/2)*hGrau
        index +=1
    # pinta poligon
    drawOverlay.polygon(tuple(vPoints),fill=(0,0,0,0))  
    # posa lletres en 1 fila a la pantalla, centrada
    incFila = heigthL*2
    numFiles = int(hi/incFila)
    xCol = widthL
    # crear una imatge amb les lletres
    imageExport = Image.new("RGBA",(wi,hi),(255,255,255))
    drawExport = ImageDraw.Draw(imageExport)
    font = ImageFont.truetype('Sloan', fontSize)
    yFila = 0
    for i in range (0,numFiles):
        iText = i%len(textSimulaCV)
        if (iText ==0):
            yFila = yFila + incFila*0.5
        drawExport.text((xCol,yFila),textSimulaCV[iText],(0,0,0),font=font)
        yFila = yFila + incFila
    # crea imatge amb overlay
    imCombined = Image.alpha_composite (imageExport, imOverlay)
    # convertir de imatge a photo imatge
    photoImage = ImageTk.PhotoImage(imCombined)
    filename = "temp.png"
    timetag = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S") 
    filename = "..\Resultats\mascaraCV_" + idPacient + timetag + ".png"
    imCombined.save(filename)
    return photoImage

# actualitzo els valors de mides font i AV reals a partir AV nominals
# calibracio factor mida font i distancia Pacient
def createAVFontSize():
    # càlcul S font en funcio AV depen de distància d'observació
    # Decimal: AV = 1/u’
    # LogMAR: AV = log(u')
    # on s/d = tan(u')
    # on d és la distància observació en mm
    # calculem les S nominals amb les AV nominals desitjades
    # calculem la mida font a partir del factor mida font calibrat
    # Decimal: s = d*tan(1/AV)
    # LogMAR: s = d*tan(10^LogMAR)
    global indexLastAVOK
    indexLastAVOK = 0
    print("AVnominal FontSize AV LogMAR")
    for i in range(0, len(listAVLogMARNom)):
        # Smm = vCalTests[iDistPacient] * np.tan(1/listAVNom[i]/60*np.pi/180.0)
        u = np.power(10,listAVLogMARNom[i])
        # per calcular tan cal convertir els minuts de grau en radians
        Smm = vCalTests[iDistPacient] * np.tan(u/60*np.pi/180.0)
        listFontSize[i] = round(Smm/vCalMonitor[iFactorMidaFont])
        # no pot ser igual o més gran que l'anterior
        if (i>0 and listFontSize[i] >= listFontSize[i-1]):
            listFontSize[i] = listFontSize[i]-1
        # la fila primera que té font size 3 és la ultima que faré servir
        if (listFontSize[i] == 3 and indexLastAVOK == 0):
            indexLastAVOK = i
            print("Last Line %d" % indexLastAVOK)
        # no podem representar lletres mes petites de 3
        if (listFontSize[i] < 3):
            listFontSize[i]=3            
        
        # calculem la AV que correspon a la mida font que podem representar
        Smm = listFontSize[i]*vCalMonitor[iFactorMidaFont]
        u = np.arctan(Smm/vCalTests[iDistPacient])*180.0/np.pi*60
        listAVLogMAR[i] = np.log10(u)
        listAV[i] = 1/u
        print("%f %f %f %f " % (listAVLogMARNom[i], listFontSize[i], 
                                listAV[i], listAVLogMAR[i]))


# calcul dels colors del text
# calcul nivells digitals (ND) per dibuixar 48 logCS del "Mars Letter"
# que comencen en 0,04 i augmenten fins a 1,92 sumant 0,04 cada cop
# el calcul de contrast unbral (Cu) està ok (comprovat amb Excel)
# el pas de Cu a ND no el tinc clar i no sembla correcte comparant el
# resultat visual amb les imatges del "Mars Letter". Cal determinar la
# lluminancia minima (L) i a partir d'aquest valor el ND (entre 0 i 1)
def createND(numColors):
    incLogCS = 0.04
    vND = np.zeros(numColors)
    for k in range(0, numColors):
        logCS = incLogCS*(k+1)
        CS = pow(10, logCS)
        Cu = 1/CS
        # L = (2/Cu-1)/(2/Cu+1) Prova 0 no és una de les dues opcions
        # que diu la Meritxell
        Lfons = 1
        # opcio 1 de tests de AV -> C = (Lfons - Ltest)/ Ltest
        L = Lfons*(1 - Cu)
        # opcio 2 de tests de SC (Michelson) ->
        # L = Lfons*(1-Cu)/(1+Cu)
        # es calcula ND a partir de L amb correcció pel monitor, pero resultats
        # visuals s'allunyen molt més del test Mars Letter, cal revisar
        # de moment agafo com a valor ND la L directament, i encara no es veu
        # a nivell visual com el test Mars Letter
        vAux = (pow(L, 1/vCalMonitor[iGamma]) - vCalMonitor[iOffset])
        vND[k] = (vAux / vCalMonitor[iGain])
        # ND[k]=L
    return vND


# converteix valor de gris entre 0 i 1 -> 0 i 255
def strColorGray(fGrayLevel):
    return "#%02x%02x%02x" % (int(fGrayLevel*255),
                              int(fGrayLevel*255), int(fGrayLevel*255))


def strAV(AV):
    return "%.2f" % AV

def strAVLogMAR(AV):
    return "%.2f" % AV

def createRandomLetters(numLettersTest):
    # masterLettersList = ['C', 'D', 'H', 'K', 'N','O','R','S','V','Z']
    # creo list empty
    lettersList = []
    resultList = []
    # creo vector aux d'on anar extreient lletres
    auxLettersList = list(masterLettersList)
    # omplo amb el num de lletres desitjat
    for i in range(0, numLettersTest):
        # no puc repetir lletres fins que no les esgoto totes, faig servir una
        # llista auxilar que vaig buidant
        resultList.append('*')
        if len(auxLettersList) > 1:
            # si la llista aux té més d'un element
            # lletra aleatoria
            iLetter = random.randint(0, len(auxLettersList)-1)
            # si la llista aux està completa i la llista final ja te elements
            # he de vigilar que no hagi escollit
            # la mateixa lletra amb la que havia acabat la llista aux anterior
            if ((len(auxLettersList) == len(masterLettersList) and
                 len(lettersList) > 1)):
                while (lettersList[i-1] == auxLettersList[iLetter]):
                    iLetter = random.randint(0, len(auxLettersList)-1)
            lettersList.append(auxLettersList[iLetter])
            auxLettersList.remove(auxLettersList[iLetter])
        else:
            # si la llista aux només te un element faig servir aquest
            # i torno a generar la llista aux
            lettersList.append(auxLettersList[0])
            auxLettersList = list(masterLettersList)
    return lettersList, resultList

def createRandomLettersEN(numLettersTest):
    # creo list empty
    lettersList = []
    resultList = []
    # creo vector aux d'on anar extreient lletres
    auxLettersList = list(masterLettersListEN)
    # omplo amb el num de lletres desitjat
    for i in range(0, numLettersTest):
        # no puc repetir lletres fins que no les esgoto totes, faig servir una
        # llista auxilar que vaig buidant
        resultList.append('*')
        if len(auxLettersList) > 1:
            # si la llista aux té més d'un element
            # lletra aleatoria
            iLetter = random.randint(0, len(auxLettersList)-1)
            # si la llista aux està completa i la llista final ja te elements
            # he de vigilar que no hagi escollit
            # la mateixa lletra amb la que havia acabat la llista aux anterior
            if ((len(auxLettersList) == len(masterLettersListEN) and
                 len(lettersList) > 1)):
                while (lettersList[i-1] == auxLettersList[iLetter]):
                    iLetter = random.randint(0, len(auxLettersList)-1)
            lettersList.append(auxLettersList[iLetter])
            auxLettersList.remove(auxLettersList[iLetter])
        else:
            # si la llista aux només te un element faig servir aquest
            # i torno a generar la llista aux
            lettersList.append(auxLettersList[0])
            auxLettersList = list(masterLettersListEN)
    return lettersList, resultList

def createRandomLettersMO(numLettersTest,letter1,letter2,numC, posFixe):
    # creo list empty
    lettersList = []
    indexFixeC = [1, 5, 6, 14, 20]
    # omplo amb 'V' el num de lletres desitjat
    for i in range(0, numLettersTest):
        lettersList.append(letter1)
    # substitueixo 'V' per 'C' en unes quantes posicions aleatories
    nC = 0
    while nC < numC:
        # posicio aleatoria dins de la llista
        iLetter = random.randint(0,numLettersTest-1)
        if numC == 5 and posFixe == True:
            iLetter = indexFixeC [nC]
        if lettersList[iLetter] == letter1:
            lettersList[iLetter] = letter2
            nC +=1
    return lettersList



# funcio que calcula mida de la font al pintar-la al canvas
def GetTextSize(canvas, fontSize , width, height):
    # escriu un espai en blanc
    canvas_id = canvas.create_text(width/2, height/2, font=('Sloan', fontSize),
                                   anchor='center', justify='center')
    canvas.itemconfig(canvas_id, text=' ')
    bounds = canvas.bbox(canvas_id) 
    heightL = bounds[3]-bounds[1]
    widthL = bounds[2]-bounds[0]
    return heightL,widthL


# crea conjunt de lletres del "Mars Letter" per test SC
def insertTextSC(canvas, fontSize , width, height):
    numFilesText = 8
    numColumnesText = 6
    numLettersTest = numFilesText * numColumnesText
    # esborra elements de dins del canvas de tests anteriors
    canvas.delete("all")
    # mida text
    heightL,widthL = GetTextSize(canvas,fontSize,width,height)

    # calcula els nivells de gris de cada lletra
    ND = createND(numLettersTest)
    # crea un conjunt de lletres random
    lettersTest, resultTest = createRandomLetters(numLettersTest)

    # mira si les lletres hi caben al canvas
    # si em falta alçada faig més gran el canvas i farem scroll vertical
    doResize = False
    new_height = (numFilesText*2)*heightL
    if (new_height > height):
        doResize = True
    else:
        new_height = height
    yFila0 = (new_height-(numFilesText*2-1)*heightL)/2    
    # si em falta amplada redueixo espaiat entre lletres
    espaiL = widthL
    xCol0 = (width-(numColumnesText*2-1)*widthL)/2
    if xCol0<0:
        # espaiat entre lletres no pot ser de la mida de la lletra
        espaiL = (width-numColumnesText*widthL) / numColumnesText
        xCol0 = (width-numColumnesText*widthL-(numColumnesText-1)*espaiL)/2
            
    # resize canvas
    if doResize == True:
        canvas.config(width=width,height=new_height,
                            scrollregion=(0,0,width,new_height))

    # posa lletres en 8 files a la pantalla, centrades
    # configura el color de la lletra amb el nivell de gris de la lletra
    k = 0
    for fila in range(0, numFilesText):
        y = yFila0 + heightL*(2*fila)
        # num de fila
        x = 0
        canvas_id = canvas.create_text(x, y, font=('Courier', 10),
                                   anchor='nw', justify='left')
        strAux ="%d_____" % (fila + 1)
        canvas.itemconfig(canvas_id, text=strAux)
        # fila amb lletres random
        for col in range(0, numColumnesText):
            x = xCol0 + widthL*(col) + espaiL*(col)
            canvas_id = canvas.create_text(x, y, font=('Sloan', fontSize),
                                       anchor='nw', justify='center')
            canvas.itemconfig(canvas_id, text=lettersTest[k])
            canvas.itemconfig(canvas_id, fill=strColorGray(ND[k]))
            strND = "%d" % k
            canvas.itemconfig(canvas_id, tags=strND)
            canvas.tag_bind(canvas_id,"<Button-1>", mouseLeftClick)
            canvas.tag_bind(canvas_id,"<Enter>", mouseEnter)
            canvas.tag_bind(canvas_id,"<Leave>", mouseLeave)
            k += 1
    return lettersTest, resultTest


# posa el text del map dels resultats del Test SC
def updateResultMapTestSC(text, resultTest, fontSize):
    tagMap = "map"
    text.tag_config(tagMap, font=('Helvetica', fontSize), justify='left')
    text.insert(tk.BEGIN, resultTest, tagMap)

# crea conjunt de lletres del "Mars Letter" per test SC
def insertTextAVnew(canvas, width, height,color):
    numFilesText = indexLastAVOK+1
    numColumnesText = 5
    # creo list empty per retornar vector de lletres random
    lettersTestFinal = []
    resultTestFinal = []
    # esborra elements de dins del canvas de tests anteriors
    canvas.delete("all")

    # mira si les lletres hi caben al canvas
    # si em falta alçada faig més gran el canvas i farem scroll vertical
    new_height = 0
    heightLFila = np.zeros(numFilesText)
    widthFila = np.zeros(numFilesText)
    for fila in range(0, numFilesText):
        # cada fila correspon a un valor AV diferent,l'escrivim a l'esquerra
        # mida text
        fontsize = int(listFontSize[fila])
        heightLFila[fila],widthFila[fila] = GetTextSize(canvas,fontsize,width,height)
        if fontsize<10:
            heightLFila[fila]=heightLFila[fila-1]
        new_height += 2*heightLFila[fila]
    new_height += 2*heightLFila[numFilesText-1]    
    doResize = False
    if (new_height > height):
        doResize = True
    else:
        new_height = height            
    # resize canvas
    if doResize == True:
        canvas.config(width=width,height=new_height,
                            scrollregion=(0,0,width,new_height))

    # posa lletres en 8 files a la pantalla, centrades
    # configura la mida de la lletra amb la AV
    y = 0
    for fila in range(0, numFilesText):
        y = y + heightLFila[fila]
        # valor de AV
        x = 0
        canvas_id = canvas.create_text(x, y, font=('Courier', 10),
                                   anchor='nw', justify='left',fill = color)
        # cada fila correspon a un valor AV diferent,l'escrivim a l'esquerra
        strAux = strAVLogMAR(listAVLogMAR[fila]) + " " + strAV(listAV[fila])
        if fila < 4:
            strAux += " ___"
        elif fila < 9:
            strAux += " _________________________"
        elif fila < 13:
            strAux += " ______________________________________________"
        else:
            strAux += " ______________________________________________________________"
        canvas.itemconfig(canvas_id, text=strAux)
        fontSize = int(listFontSize[fila])
        # crea un conjunt de lletres random
        lettersTest, resultTest = createRandomLetters(numColumnesText)
        # si em falta amplada redueixo espaiat entre lletres
        espaiL = widthFila[fila]
        xCol0 = (width-(numColumnesText*2-1)*widthFila[fila])/2
        if xCol0<0:
            # espaiat entre lletres no pot ser de la mida de la lletra
            espaiL = (width-numColumnesText*widthFila[fila]) / numColumnesText
            xCol0 = (width-numColumnesText*widthFila[fila]-(numColumnesText-1)*espaiL)/2
        # fila amb lletres random
        for col in range(0, numColumnesText):
            x = xCol0 + widthFila[fila]*(col) + espaiL*(col)
            canvas_id = canvas.create_text(x, y, font=('Sloan', fontSize),
                                       anchor='nw', justify='center')
            canvas.itemconfig(canvas_id, text=lettersTest[col])
            canvas.itemconfig(canvas_id, fill=color)
            # per poder fer click a cada lletre i fer una acció
            sAV = "%d" % fila
            canvas.itemconfig(canvas_id, tags=sAV)
            canvas.tag_bind(canvas_id,"<Button-1>", mouseLeftClick)
            canvas.tag_bind(canvas_id,"<Enter>", mouseEnter)
            canvas.tag_bind(canvas_id,"<Leave>", mouseLeave)
            lettersTestFinal.append(lettersTest[col])
            resultTestFinal.append(resultTest[col])
        y = y + heightLFila[fila]
    return lettersTestFinal, resultTestFinal

# crea conjunt de lletres del "Mars Letter" per test SC
def insertTextAV(text):
    numFilesText = len(listFontSize)
    numColumnesText = 5
    # numLettersTest =numFilesText*numColumnesText
    # creo list empty
    lettersTestFinal = []
    resultTestFinal = []
    
    text.delete('1.0', tk.END)
    text.configure(font=('Sloan', 64))

    text.tag_config('valorAV', font=('Courier', 12), justify='left')

    # crea el text amb lletres random separades per espai en blanc
    # afegeix una linia en blanc a dalt de tot, entre cada fila de lletres
    # color de lletra sempre negre
    # definint un tag per cada fila al fer insert i utilitzant el tag per
    # definir el font size
    for fila in range(0, numFilesText):
        # cada fila correspon a un valor AV diferent,l'escrivim a l'esquerra
        strValor = strAVLogMAR(listAVLogMAR[fila]) + " " + strAV(listAV[fila])
        if fila < 4:
            strValor += "____________"
        elif fila < 8:
            strValor += "_____________________"
        elif fila < 12:
            strValor += "_____________________________"
        else:
            strValor += "______________________________________"

        text.insert(tk.INSERT, strValor, 'valorAV')
        # cada fila te una mida de font diferent
        tagFila = "F%d" % fila
        text.tag_config(tagFila, font=('Sloan', int(listFontSize[fila])),
                        justify='center')
        # fila espais en blanc
        for col in range(0, numColumnesText):
            text.insert(tk.INSERT, "  ", tagFila)
        text.insert(tk.INSERT, "\n", tagFila)
        # crea un conjunt de lletres random
        lettersTest, resultTest = createRandomLetters(numColumnesText)
        # fila amb lletres random
        for col in range(0, numColumnesText):
            if col > 0:
                text.insert(tk.INSERT, " ", tagFila)
            text.insert(tk.INSERT, lettersTest[col], tagFila)
            lettersTestFinal.append(lettersTest[col])
            resultTestFinal.append(resultTest[col])
        text.insert(tk.INSERT, "\n", tagFila)
    # fila final te una mida de font com ultima fila de test
    tagFila = "F%d" % (numFilesText-1)
    text.tag_config(tagFila,
                    font=('Sloan', int(listFontSize[numFilesText-1])),
                    justify='center')
    # fila espais en blanc
    for col in range(0, numColumnesText):
        text.insert(tk.INSERT, "  ", tagFila)
    text.insert(tk.INSERT, "\n", tagFila)
    return lettersTestFinal, resultTestFinal

# crea lletra per test ENLLUERNAMENT
def insertTextEN(canvas, iND, iAV, width, height):
    numLettersTest = 1
    # esborra elements de dins del canvas de tests anteriors
    canvas.delete("all")
    # mida text
    fontSize = int(listFontSize[iAV])
    heightL,widthL = GetTextSize(canvas,fontSize,width,height)

    # calcula els nivells de gris de cada lletra
    ND = createND(8*6)
    # crea un conjunt de lletres random
    lettersTest, resutTest = createRandomLettersEN(numLettersTest)
    # posa lletra a la pantalla, centrada
    incFila = heightL
    incCol = widthL
    x = (width-incCol)/2
    y = (height-incFila)/2
    
    # cercle per emmarcar lletra
    radi = widthL*3
    x0 = x-radi
    y0 = y-radi
    x1 = x+radi
    y1 = y+radi
    canvas.create_oval(x0, y0, x1, y1, outline='gray', fill='white',width=3)

    strAux = " "+ lettersTest[0]+" "
    widget = tk.Label(canvas, text=strAux, font=('Sloan', fontSize),
                      fg=strColorGray(ND[iND]), bg='white')
    widget.pack()
    canvas.create_window(x, y, window=widget)

    return lettersTest[0]


# crea conjunt de lletres per test MO #1
def insertTextMO1(canvas, fontSize, width, height, numC, posFixe, color):
    numFilesText = 3
    numColumnesText = 7
    # esborra elements de dins del canvas de tests anteriors
    canvas.delete("all")
    bgColor = "white"
    if color == "white":
        bgColor="black"
    canvas.create_rectangle(0, 0, width, height, fill=bgColor)
    # mida text
    heightL,widthL = GetTextSize(canvas,fontSize,width,height)
    # crea un conjunt de lletres random
    lettersTest = createRandomLettersMO(numFilesText*numColumnesText,'V','C', numC, posFixe)
    # posa lletres en 3 files a la pantalla, centrades
    incFila = heightL
    #calculo un sepacació entre lletres
    #però hem de tenir en compte mida de la lletra per fer el càlcul
    if heightL < 100:
        incCol = widthL*0.9
    else:
        incCol = widthL*0.7
    xCol0 = (width-14*incCol)/2
    yFila0 = (height-4*incFila)/2
    k = 0
    for fila in range(0, numFilesText):
        y = yFila0 + incFila*(fila*2)
        # fila amb lletres random
        for col in range(0, numColumnesText):
            x = xCol0 + incCol*(col*2+1)
            canvas_id = canvas.create_text(x, y, font=('Sloan', fontSize),
                                       anchor='center', justify='center',
                                       fill=color)
            canvas.itemconfig(canvas_id, text=lettersTest[k])
            canvas.tag_bind(canvas_id,"<Button-1>", mouseLeftClick)
            k += 1

# crea conjunt de lletres per test MO #2
def insertTextMO2(canvas, fontSize, width, height, numC, posFixe, color):
    aspectRatio = 26.35/16.35
    x0 = 0.925
    y0 = 0.375
    posCFixeX = [ -10.2, 12.6, 11.2, 5.75, 5.9]
    posCFixeY = [ 6.0, 6.8, 5.5, 1.7, -2.2]
    posVFixeX = [ -8.4, -1.5, 4.85, 13.2, 4.2, -1.6, -8.4, -7.25, -3.4, 2.25, 9.75, 12.4, -3.1, -9.8, 6.8, -0.7]
    posVFixeY = [ 7.8, 6.8, 7.75, 4.4, 3.8, 4.3, 3.9, 0.15, 1.7, 0.5, 0.7, -2.1, -3.2, -4.9, -4.45, -7.0 ]
    numLetters = 7*3
    canvas.delete("all")
    bgColor = "white"
    if color == "white":
        bgColor="black"
    canvas.create_rectangle(0, 0, width, height, fill=bgColor)
    # crea un conjunt de lletres random 1a fila
    lettersTest = createRandomLettersMO(numLetters,'V','C', numC, False)
    # mida de la zona del canvas on reparteixo lletres
    widthMO_pix =widthMO_MM / vCalTests[iMidaPix]
    if (width > widthMO_pix):
        margeW = int((width - widthMO_pix)/2)
    else:
        margeW = 75
    heightMO_pix =heightMO_MM / vCalTests[iMidaPix]
    if (height > heightMO_pix):
        margeH = int((height - heightMO_pix)/2)
    else:
        margeH = 75
    if posFixe == True:
        # posa lletres coordenades fixes
        iC = 0
        iV = 0
        factorNorm = (width-2*margeW)/26.35
        for i in range(0, numLetters):
            # converteix coordinades disseny a pantalla
            x = 0
            y = 0
            if lettersTest[i]=="C":
                x = (posCFixeX[iC]-x0)*factorNorm + width/2
                y = -1.0*(posCFixeY[iC]-y0)*factorNorm + height/2
                iC = iC + 1
            else:
                x = (posVFixeX[iV]-x0)*factorNorm + width/2
                y = -1.0*(posVFixeY[iV]-y0)*factorNorm + height/2                
                iV = iV + 1
            canvas_id = canvas.create_text(x, y, font=('Sloan', fontSize),
                                    anchor='center', justify='center',
                                    fill = color)
            canvas.itemconfig(canvas_id, text=lettersTest[i])
    else:
        # posa lletres aleatoriament a la pantalla
        listBounds = []
        maxIteracions = 50000
        conta = 0
        for i in range(0, numLetters):
            ok = False
            while ok == False and conta < maxIteracions:
                x = random.randint(margeW,width-margeW)
                y = random.randint(margeH,height-margeH)
                ok = True
                if i>0:
                    for j in range (0,i):
                        if (x>=listBounds[j][0] and x<=listBounds[j][2] and
                            y>=listBounds[j][1] and y<=listBounds[j][3]):
                            # coordenada dins d'una lletra ja pintada
                            ok = False
                conta +=1
            canvas_id = canvas.create_text(x, y, font=('Sloan', fontSize),
                                        anchor='center', justify='center',
                                        fill = color)
            canvas.itemconfig(canvas_id, text=lettersTest[i])
            #canvas.itemconfig(canvas_id, text='O')
            #pointBounds =(x,y,x+5,y+5)
            #canvas.create_oval(pointBounds)
            bounds = canvas.bbox(canvas_id) 
            heightL = bounds[3]-bounds[1]
            widthL = bounds[2]-bounds[0]
            #calculo un bounding box més gran per evitar que es "toquin" les lletres
            #però hem de tenir en compte mida de la lletra per fer el càlcul
            if heightL < 100:            
                xmin = bounds[0] - widthL*0.75
                xmax = bounds[2] + widthL*0.75      
                ymin = bounds[1] - heightL*0.75
                ymax = bounds[3] + heightL*0.75      
            else:
                xmin = bounds[0] - widthL*0.5
                xmax = bounds[2] + widthL*0.5      
                ymin = bounds[1] - heightL*0.5
                ymax = bounds[3] + heightL*0.5      
            newBounds =(xmin,ymin,xmax,ymax)
            listBounds.append(newBounds)
        
# crea imatge i text test MO #3
def insertTextMO3(canvas, im):
    canvas.delete("all")
    #canvas.pack(expand=YES, fill=BOTH)
    # put gif image on canvas
    # pic's upper left corner (NW) on the canvas is at x=10 y=10
    canvas.create_image(25, 50, image=im, anchor=tk.NW)
    # la imatge té 4 lletres a respondre
    numC = 5
    return numC

# fa load d'una imatge i resize a la mida del canvas
def loadPVimage(imFilename,canvasWidth):
    im = Image.open(imFilename)
    basewidth = canvasWidth
    wpercent = (basewidth/float(im.size[0]))
    hsize = int((float(im.size[1])*float(wpercent)))
    im = im.resize((basewidth,hsize), Image.ANTIALIAS)
    return im
    
# crea imatge i text test MO #3
def insertImagePV(canvas, im):
    canvas.delete("all")
    canvas.create_image(0,0, image=im, anchor=tk.NW)

def colorModel(vG, vL):
    deltaNG = 1.0/(len(vL)-1)
    for i in range(0, len(vL)):
        vG[i] = i*deltaNG
    for i in range(0, len(vL)):
        vAux = vCalMonitor[iGain]*vG[i] + vCalMonitor[iOffset]
        vL[i] = vAux**vCalMonitor[iGamma]



class App:

    def say_hi(self):
        print("hola a tothom!")

    def iniWebCam(self):
        self.isVideoOn = False       
        self.videoCaptureObject = cv2.VideoCapture( gCamera[indexId])
        self.cameraIniciada = True

    def releaseWebCam(self):
        self.isVideoOn = False       
        if self.cameraIniciada == True:
            self.videoCaptureObject.release()

    def startVideo(self):   
        # Memoria Visual test imatge de prova ha d'estar 5 segons visible
        self.isVideoOn = True
        self.timerVideo()

    def stopVideo(self):
        self.isVideoOn = False

    def timerVideo(self):
        y=gCamera[indexTop]
        x=gCamera[indexLeft]
        h=gCamera[indexHeight]
        w=gCamera[indexWidth]
        ret,frame = self.videoCaptureObject.read()    
        if ret == False:
            self.isVideoOn = False
            return   
        crop = frame[y:y+h, x:x+w]       
        if self.videoFinestra == True:
            # display image in new window "Capturing Video"
            cv2.imshow('Capturing Video',crop)
        else:
            # display image in canvas
            self.showCVimage(self.testVideo,crop,"null")
        if (self.isVideoOn == True):
            self.testVideo.after(20, self.timerVideo)     

    def showCVimage(self,canvas,imgCV_in,layout):
        """
        Showimage() is a function used to display OpenCV images in the canvas control of tkinter.
            Need to import the library before use
        import cv2 as cv
        from PIL import Image,ImageTktkinter
            And note that due to the needs of the response function, this function defines a global variable imgTK, please do not use this variable name in other places!
            Parameters:
            imgCV_in: OpenCV image variable to be displayed
            canva: tkinter canvas canvas variable for display
            layout: The format of the display. The options are:
                    "fill": The image automatically adapts to the canvas size and is completely filled, which may cause the screen to stretch
                    "fit": According to the size of the canvas, the image is displayed to the maximum extent without stretching the image, which may cause blank edges
                    Given other parameters or not, it will be displayed in the original image size, which may be incomplete or left blank
        """
        #global imgTK
        canvawidth = int(canvas.winfo_reqwidth())
        canvaheight = int(canvas.winfo_reqheight())
        sp = imgCV_in.shape
        cvheight = sp[0]#height(rows) of image
        cvwidth = sp[1]#width(colums) of image
        if (layout == "fill"):
            imgCV = cv2.resize(imgCV_in,(canvawidth,canvaheight), interpolation=cv2.INTER_AREA)
        elif(layout == "fit"):
            if (float(cvwidth/cvheight) > float(canvawidth/canvaheight)):
                imgCV = cv2.resize(imgCV_in,(canvawidth,int(canvawidth*cvheight/cvwidth)), interpolation=cv2.INTER_AREA)
            else:
                imgCV = cv2.resize(imgCV_in,(int(canvaheight*cvwidth/cvheight),canvaheight), interpolation=cv2.INTER_AREA)
        else:
            imgCV = imgCV_in
        imgCV2 = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGBA)#Convert color from BGR to RGBA
        current_image = Image.fromarray(imgCV2)#Convert image into Image object
        self.imgTK = ImageTk.PhotoImage(image=current_image)#Convert image object to imageTK object
        canvas.create_image(0,0,anchor = "nw", image = self.imgTK)

    def selectROI(self):
        ret,frame = self.videoCaptureObject.read()        
        r = cv2.selectROI('Select Video ROI',frame)
        print(r)
        gCamera[indexTop] = r[1]
        gCamera[indexLeft] = r[0]
        gCamera[indexHeight] = r[3]
        gCamera[indexWidth] = r[2]


    def setCurrentAV(self):
        av = self.listBoxAV.curselection()
        self.currentAV = av[0]
        self.vAVpacient.set("AV LogMAR test: " +
                            strAVLogMAR(listAVLogMAR[self.currentAV]))
        
    # actualitzo els valors de calibracio necessaris per als tests
    def updateCalTests(self,distPacient):
        vCalTests[iDistPacient] = distPacient
        vCalTests[iMidaPix] = vCalMonitor[iMidaQmm]/vCalMonitor[iMidaQpix]
        vCalTests[iMidaGrauPix] = ((vCalTests[iDistPacient] *
                                    np.tan(1*np.pi/180.0))/vCalTests[iMidaPix])
        self.saveDotSize()

    # guardar calibracio mida quadrat 1 grau en pixels
    def saveDotSize(self):
        writer = open("..\DotSize.txt", 'w')
        row = "%.0f" % vCalTests[iMidaGrauPix] +"\n"
        writer.write(row)
        row = self.IDPacient +"\n"
        writer.write(row)
        row = str(self.doRightEyeCV) +"\n"
        writer.write(row)
        row = str(self.doLeftEyeCV) +"\n"
        writer.write(row)
        row = str(self.doBothEyesCV) +"\n"
        writer.write(row)
        row = str(self.nIterationsCV) +"\n"
        writer.write(row)
        row = str(self.fixDiagonalCV) +"\n"
        writer.write(row)
        writer.close()

    # valors default per al CV
    def defaultsTestCV(self):
        self.doRightEyeCV = 0
        self.doLeftEyeCV = 0
        self.doBothEyesCV = 1
        self.nIterationsCV = 3
        self.fixDiagonalCV = 0

    def paintRectNivellGris(self, ng, showMida):
        size = self.canvas_height/3*2
        xPos = (self.canvas_width-size)/2
        yPos = (self.canvas_height-size)/2
        rectColor = strColorGray(ng)
        self.testCanvas.create_rectangle(xPos, yPos, xPos+size, yPos+size,
                                         fill=rectColor, outline=rectColor)
        if showMida is True:
            vCalMonitor[iMidaQpix] = float(size)
            labMidaQ = tk.Label(self.controlsFrameCalGrisos,
                                text="Mida quadrat en pixels:%d" % size,
                                font=('Helvetica', fontSizeC1))
            labMidaQ.pack(side=tk.TOP)

    def displayRectNivellGris(self):
        self.gridNivells()
        ng = self.valNivellsGris[self.iCurrentNivellGris]
        self.vLabNG.set("Nivell %d/%d (%f)" % (self.iCurrentNivellGris+1,
                        self.numNivellsGris, ng))
        self.paintRectNivellGris(ng, False)
        # debug: per facilitar crear el resultat de calibracio sense escriure
        self.vCalNG.set("%f" % float(self.iCurrentNivellGris+1))

    def nivellBlanc(self):
        # pinta blanc
        self.gridNivells()
        self.paintRectNivellGris(1.0, False)

    def nivellNegre(self):
        # pinta blanc
        self.gridNivells()
        self.paintRectNivellGris(0.0, False)

    def gridNivells(self):
        # pinta tots els nivells
        size = self.canvas_height/(self.numNivellsGris+2)
        for i in range(0, self.numNivellsGris):
            xPos = size*(i+1)
            yPos = size
            ng = self.valNivellsGris[i]
            rectColor = strColorGray(ng)
            self.testCanvas.create_rectangle(xPos, yPos, xPos+size,
                                             yPos+size, fill=rectColor,
                                             outline=rectColor)

    def segNivellGris(self):
        # pinta amb un altre nivell de gris
        if self.iCurrentNivellGris == -1:
            # reset per tornar a començar
            self.resetCalNivellsGris()
            self.displayRectNivellGris()
            return
        # guarda valor
        value = self.vCalNG.get()
        self.calNivellsGris[self.iCurrentNivellGris] = float(value)
        # si hem arribat al limit torna enrrera comptador i marca final test
        if self.iCurrentNivellGris >= self.numNivellsGris-1:
            self.iCurrentNivellGris = -1
            self.finalCalNivellsGris()
        else:
            # avança 1 nivell
            self.iCurrentNivellGris = self.iCurrentNivellGris + 1
            self.displayRectNivellGris()

    def finalCalNivellsGris(self):
        # guarda valors en arxiu csv
        saveCalGrisosMonitor(self.valNivellsGris, self.calNivellsGris)
        # pinta grafica
        plt.subplot(2, 1, 1)
        plt.plot(self.valNivellsGris, self.calNivellsGris,
                 linestyle='--', marker='o')
        plt.xlabel("nivell gris digital")
        plt.ylabel("L (cd/m2)")
        plt.title("Calibració Nivells Gris")
        plt.grid(True, which='both')
        # model de Lr en funcio Ng
        # calcula lluminancia relativa
        Lmax = max(self.calNivellsGris)
        vLR = np.zeros(len(self.calNivellsGris))
        vLR[:] = [x/Lmax for x in self.calNivellsGris]
        # vLR[:] = [x /Lmax for x in vLR]
        vNGD = np.zeros(101)
        vLRMod = np.zeros(101)
        # model
        colorModel(vNGD, vLRMod)
        # pinta grafica
        plt.subplot(2, 1, 2)
        plt.plot(self.valNivellsGris, vLR, linestyle='--', marker='o',)
        plt.plot(vNGD, vLRMod)
        plt.xlabel("nivell gris digital")
        plt.ylabel("L rel")
        plt.grid(True, which='both')

    def resetCalNivellsGris(self):
        # valors entre 0 i 1.0
        deltaGris = 1.0/(self.numNivellsGris-1.0)
        self.valNivellsGris[0] = 0
        self.calNivellsGris[0] = 0
        for i in range(1, self.numNivellsGris):
            self.valNivellsGris[i] = deltaGris*i
            self.calNivellsGris[i] = 0
        self.iCurrentNivellGris = 0

    def guardaMidaQ(self):
        # guarda valor
        value = self.vCalMidaQ.get()
        vCalMonitor[iMidaQmm] = float(value)
        # guardar a l'arxiu de cal monitor
        saveCalMonitor()

    def guardaMidaFont(self):
        # guarda valor
        value = self.vCalMidaFont.get()
        # calcula factor lineal entre mida font en punts i mm
        vX = [0, 72]
        vY = [0, float(value)/5]
        z = np.polyfit(vX, vY, 1)
        # p = np.poly1d(z)
        vCalMonitor[iFactorMidaFont] = z[0]
        # guardar a l'arxiu de cal monitor
        saveCalMonitor()

    def guardaPolaritatInv(self):
        # guarda valor
        value = self.vCalPolaritatInv.get()
        if value == '1':
            self.polaritatInversa = True
        else:
            self.polaritatInversa = False
        findPVImages(self.polaritatInversa)
        SetColorPolaritat(self)
 
    def guardaDistP(self):
        # guarda valor
        value = float(self.vCalDistP.get())
        self.updateCalTests(value)
        # actualitza etiqueta GUI
        self.vDistanciaPacient.set("Distància pacient: %d mm" % value)
        # guarda a disc
        saveDistanciaExamen(value)

    def guardaCameraROI(self):
        # guarda valors a disc
        saveCameraConfig()

    def guardaNovaVal(self):
        # guarda resultat anterior
        self.guardaValRes()
        # guarda valor
        self.IDPacient = self.vNovaIDPacient.get()
        self.IDOpt = self.vNovaIDOpt.get()
        value = self.vEdatPacient.get()
        self.edatPacient = int(value);
        # actualitza etiqueta GUI
        self.vIDPacient.set("ID Pacient: " + self.IDPacient)
        self.vIDOpt.set("ID Optometrista: " + self.IDPacient)
        # guarda configuracio del camp visual
        self.doRightEyeCV = self.vCheckboxRightEye.get()
        self.doLeftEyeCV = self.vCheckboxLeftEye.get()
        self.doBothEyesCV = self.vCheckboxBothEyes.get()
        self.nIterationsCV = self.vNumItCV.get()
        self.fixDiagonalCV = self.vCheckboxFixDiag.get()
        # surt a del mode de crear Nova Val (guarda valors a l'arxiu dotsize)
        self.guiTest(True)
        
    def guardaValRes(self):
        # crear nom arxiu amb dia i hora per evitar sobrescriure
        timetag = datetime.datetime.now().strftime("_%Y%m%d_%H%M%S") 
        nomFile = "..\Resultats\Movilab_" + self.IDPacient + timetag + ".csv"
        # obrir arxiu per escriure
        writer = open(nomFile, 'w')
        # escriure la capçalera
        row = "Version" + ";" + movilabVersion + "\n"
        writer.write(row)        
        row = "Date and Time" + ";" + self.DateTime +";Errors B/Tiempo Neto;Resp B;Num B\n"
        writer.write(row)        
        row = "ID Pacient;%s\n" % self.IDPacient
        writer.write(row)        
        row = "Edat Pacient;%d\n" % self.edatPacient
        writer.write(row)        
        row = "ID Optometrista;%s\n" % self.IDOpt
        writer.write(row)        
        row = "Polaritat Inversa;%d\n" % self.polaritatInversa
        writer.write(row)        
        row = "Distància exàmen;%d\n" % vCalTests[iDistPacient]
        writer.write(row)        
        # escriure resultats AV
        avTest = self.currentAV
        if gEnlluernament[indexUsarAVFixe] == 1:
            avTest = gEnlluernament[indexAVFixe]
        row = "AV test LogMAR;%.2f\n" % listAVLogMAR[avTest]
        writer.write(row)        
        if gEnable[indexAV]== 1:
            row = "AV LogMAR;%.2f\n" % self.resultatAVLogMAR
            writer.write(row)        
            row = "AV Decimal;%.2f\n" % self.resultatAV
            writer.write(row)   
        # escriure resultats SC
        row = "SC test;%.2f\n" % self.currentSC
        writer.write(row)        
        if gEnable[indexSC]== 1:
            row = "SC;%.2f\n" % self.resultatSC
            writer.write(row)        
        # escriure resultats ENSC
        if gEnable[indexENSC]== 1:
            row = "AV test ENSC LogMAR;%.2f\n" % listAVLogMAR[self.indexAVtestENSC]
            writer.write(row)        
            row = "ENsc;%.2f\n" % self.resultatTestENsc[0]
            writer.write(row)        
            row = "ENsc Filtre;%.2f\n" % self.resultatTestENsc[1]
            writer.write(row)        
        # escriure resultats ENt
        if gEnable[indexENT]== 1:
            row = "ENt # respostes;%d\n" % self.numLettersEN[0]
            writer.write(row)        
            row = "ENt Temps resposta;%.2f\n" % self.tempsTestEN[0]
            writer.write(row)        
            row = "ENt # respostes Filtre 1;%d\n" % self.numLettersEN[1]
            writer.write(row)        
            row = "ENt Temps resposta Filtre 1;%.2f\n" % self.tempsTestEN[1]
            writer.write(row)        
            row = "ENt # respostes Filtre 2;%d\n" % self.numLettersEN[2]
            writer.write(row)        
            row = "ENt Temps resposta Filtre 2;%.2f\n" % self.tempsTestEN[2]
            writer.write(row)        
            row = "ENt # respostes Filtre 3;%d\n" % self.numLettersEN[3]
            writer.write(row)        
            row = "ENt Temps resposta Filtre 3;%.2f\n" % self.tempsTestEN[3]
            writer.write(row)        
            row = "ENt # respostes Filtre 4;%d\n" % self.numLettersEN[4]
            writer.write(row)        
            row = "ENt Temps resposta Filtre 4;%.2f\n" % self.tempsTestEN[4]
            writer.write(row)        
        # escriure resultats MO -----------------
        if gEnable[indexMO]== 1:
            strRes = "Error"
            if (self.numMO[0] == self.resMO[0]):
                strRes = "Correcte"
            row = "B Test #1 Num 'C';%s;%d;%d;%d\n" % (strRes,self.numMO[0]-self.resMO[0],self.resMO[0],self.numMO[0])
            writer.write(row)        
            row = "B Test #1 Temps resposta;%.2f;%.2f\n" % (self.tempsTestMO[0],self.tempsTestNetoMO[0])
            writer.write(row)        
            strRes = "Error"
            if (self.numMO[1] == self.resMO[1]):
                strRes = "Correcte"
            row = "B Test #2 Num 'C';%s;%d;%d;%d\n" % (strRes,self.numMO[1]-self.resMO[1],self.resMO[1],self.numMO[1])
            writer.write(row)        
            row = "B Test #2 Temps resposta;%.2f;%.2f\n" % (self.tempsTestMO[1],self.tempsTestNetoMO[1])
            writer.write(row)        
            if (self.numMO[2] == self.resMO[2]):
                strRes = "Correcte"
            row = "B Test #3 Linies;%s;%d;%d;%d\n" % (strRes,self.numMO[2]-self.resMO[2],self.resMO[2],self.numMO[2])
            writer.write(row)        
            row = "B Test #3 Temps resposta;%.2f;%.2f\n" % (self.tempsTestMO[2],self.tempsTestNetoMO[2])
            writer.write(row)        
            strRes = "Error"
            if (self.numMO[3] == self.resMO[3]):
                strRes = "Correcte"
            row = "B Test #4 Mentonera Num 'C';%s;%d;%d;%d\n" % (strRes,self.numMO[3]-self.resMO[3],self.resMO[3],self.numMO[3])
            writer.write(row)        
            row = "B Test #4 Temps resposta;%.2f;%.2f\n" % (self.tempsTestMO[3],self.tempsTestNetoMO[3])
            writer.write(row)        
            strRes = "Error"
            if (self.numMO[4] == self.resMO[4]):
                strRes = "Correcte"
            row = "B Test #5 Num 'C';%s;%d;%d;%d\n" % (strRes,self.numMO[4]-self.resMO[4],self.resMO[4],self.numMO[4])
            writer.write(row)        
            row = "B Test #5 Temps resposta;%.2f;%.2f\n" % (self.tempsTestMO[4],self.tempsTestNetoMO[4])
            writer.write(row)        
            if (self.numMO[5] == self.resMO[5]):
                strRes = "Correcte"
            row = "B Test #6 Linies;%s;%d;%d;%d\n" % (strRes,self.numMO[5]-self.resMO[5],self.resMO[5],self.numMO[5])
            writer.write(row)        
            row = "B Test #6 Temps resposta;%.2f;%.2f\n" % (self.tempsTestMO[5],self.tempsTestNetoMO[5])
            writer.write(row)        
        # escriure resultats PV -----------------
        if gEnable[indexPV]== 1:
            row = "PV Test Memoria Visual;%d\n" % (self.resPV[0])
            writer.write(row)        
            row = "PV Test Memoria Visual Temps resposta;%.2f\n" % self.tempsTestPV[0]
            writer.write(row)        
            row = "PV Test Figura Fondo;%d\n" % (self.resPV[1])
            writer.write(row)        
            row = "PV Test Figura Fondo Temps resposta;%.2f\n" % self.tempsTestPV[1]
            writer.write(row)        
            row = "PV Test Cierre Visual;%d\n" % (self.resPV[2])
            writer.write(row)        
            row = "PV Test Cierre Visual Temps resposta;%.2f\n" % self.tempsTestPV[2]
            writer.write(row)        
            # guarda totes les respostes i tots els temps
            #for i in range(3):
            i=0
            row =  "%s;%f\n" % (self.vNameTestPV[i],self.tempsTestPV[i]) 
            writer.write(row)
            row = "Tots els resultats i temps de resposta\n"
            writer.write(row)
            for j in range(18):
                head, tail = os.path.split(vPV_VisualMemory[j+4])
                row = "%s;%.0f;%f\n" % (tail,self.resAllPV[i][j],self.tempsAllPV[i][j])
                writer.write(row)        
            i=1
            row =  "%s;%f\n" % (self.vNameTestPV[i],self.tempsTestPV[i]) 
            writer.write(row)
            row = "Tots els resultats i temps de resposta\n"
            writer.write(row)
            for j in range(18):
                head, tail = os.path.split(vPV_VisualFigureGround[j+2])
                row = "%s;%.0f;%f\n" % (tail,self.resAllPV[i][j],self.tempsAllPV[i][j])
                writer.write(row)        
            i=2
            row =  "%s;%f\n" % (self.vNameTestPV[i],self.tempsTestPV[i]) 
            writer.write(row)
            row = "Tots els resultats i temps de resposta\n"
            writer.write(row)
            for j in range(18):
                head, tail = os.path.split(vPV_VisualClosure[j+2])
                row = "%s;%.0f;%f\n" % (tail,self.resAllPV[i][j],self.tempsAllPV[i][j])
                writer.write(row)        
        writer.close()
        
    def resetAllDoing(self):
        self.isDoingAV = False
        self.isDoingEN = False
        self.isDoingENsc = False
        self.isDoingExamplesPV = False 
        self.isDoingMO = False
        self.isDoingSC = False
        self.isDoingPV = False

    def resetTestAV(self):
        self.resetAllDoing()
        self.currentAV = 5
        self.resultatAVLogMAR = 0.0
        self.resultatAVLogMARPrevLine = -1
        self.resultatAV = 0.0
        self.lettersTestAV = []
        self.resultMapTestAV = []
        self.bestLineReadAV = 0
        self.indexCurrentLetter = 0
        self.indexLastLetterOk = -2
        self.indexLastLetterError = -2
        self.totalNum1LetterErrorsTestAV = 0
        
    def calculaAVLogMARTestRes(self):
        # increment de AV associat a cada lletra; 5 lletres són 1 fila
        # el desitjat es 0.02 pero el calculem en funcio de la AV real
        # que puc representar amb les fonts que fagi servir
        incLogMAR = 0.02
        if self.bestLineReadAV>0:
            incLogMAR = (listAVLogMAR[self.bestLineReadAV-1] - listAVLogMAR[self.bestLineReadAV])/5
        # la correccio depen de les lletres que ha fallat
        correccioLogMAR = incLogMAR*self.totalNum1LetterErrorsTestAV
        # valor fina de AV
        AVLogMAR = listAVLogMAR[self.bestLineReadAV] + correccioLogMAR
        return AVLogMAR

    def finalTestAV(self):
        self.isDoingAV = False
        self.vEstatTestAV.set("Estat del test: FINAL")
        # valor de AV del pacient es pot calcular amb més precisió
        # depen de si hem vist alguna lletra be en la current line
        if self.totalNum1LetterErrorsTestAV == 5:
            # cap lletra vista -> AV calculada en la Prev Line
            self.resultatAVLogMAR = self.resultatAVLogMARPrevLine
            # index best line read determina mida lletra: fila actual - 3
            self.currentAV = self.bestLineReadAV-3
        else:
            # alguna lletra vista -> calculem AV ara
            self.resultatAVLogMAR = self.calculaAVLogMARTestRes()
            # index best line read determina mida lletra: fila actual - 2
            self.currentAV = self.bestLineReadAV-2
        # check que estiguem dins dels limits de AV possibles
        if self.currentAV < 0:
            self.currentAV = 0
        # AV en decimal
        u = np.power(10.0,self.resultatAVLogMAR)
        self.resultatAV = 1/u
        #self.vAVpacient.set("AV LogMAR test: " + strAVLogMAR(listAVLogMAR[self.currentAV]))
        self.vMapTestAV.set(self.resultMapTestAV)
        self.vResultatTestAV.set("Resultat AV (logMAR)=%.2f (Dec)=%.2f" % (self.resultatAVLogMAR,self.resultatAV))
        # debug
        print(str(self.indexCurrentLetter))
        print(str(self.indexLastLetterOk))
        print(str(self.totalNum1LetterErrorsTestAV))
        
    def setFilaInicialTestAV(self,indexFilaAV):
        self.bestLineReadAV = indexFilaAV
        if indexFilaAV == 0:
            # calculem AV Prev Line: no es pot saber, posem -1
            self.resultatAVLogMARPrevLine =  -1        
            # altres settings
            self.indexCurrentLetter = 0
            self.indexLastLetterOk = -2
            self.indexLastLetterError = -2
            for index in range (0,len(self.resultMapTestAV)):
                self.resultMapTestAV[index] = '*'
        else:         
            # calculem AV Prev Line
            self.resultatAVLogMARPrevLine =  listAVLogMAR[self.bestLineReadAV-1]        
            # altres settings
            self.indexCurrentLetter = indexFilaAV*5
            self.indexLastLetterOk = self.indexCurrentLetter
            self.indexLastLetterError = -2
            for index in range (0,self.indexCurrentLetter):
                self.resultMapTestAV[index] = '1'
            for index in range (self.indexCurrentLetter+1,len(self.resultMapTestAV)):
                self.resultMapTestAV[index] = '*'
        self.vMapTestAV.set(self.resultMapTestAV)

    def resetTestSC(self):
        self.resetAllDoing()
        self.currentND = 0
        self.resultatSC = 0.0
        self.currentSC = 0.0
        self.lettersTestSC = []
        self.resultMapTestSC = []
        self.indexCurrentLetter = 0
        self.indexLastLetterOk = -2
        self.indexLastLetterError = -2
        self.totalNum1LetterErrorsTestSC = 0

    def finalTestSC(self):
        self.isDoingSC = False
        self.vEstatTestSC.set("Estat del test: FINAL")
        # index last letter ok
        incLogCS = 0.04
        correccioSC = incLogCS*self.totalNum1LetterErrorsTestSC
        self.resultatSC = incLogCS*(self.indexLastLetterOk + 1) - correccioSC
        # pel test de enlluernament hem de fer servir un valor de gris
        # més fosc que la última lletra ok
        factorReservaSC = 1
        if self.indexLastLetterOk >= 0:
            self.currentND = int(self.indexLastLetterOk/factorReservaSC)
        else:
            self.currentND = 0
        # calculem el nivell de SC del nivell de gris que farem servir per test EN
        self.currentSC = incLogCS*(self.currentND + 1) - correccioSC
        self.vResultatTestSC.set("Resultat SC (log): %.2f" % self.resultatSC)
        self.vMapTestSC.set(self.resultMapTestSC)
        # debug
        print(str(self.indexCurrentLetter))
        print(str(self.indexLastLetterOk))
        print(str(self.totalNum1LetterErrorsTestSC))

    def setFilaInicialTestSC(self,indexFilaSC):
        if indexFilaSC == 0:
            self.indexCurrentLetter = 0
            self.indexLastLetterOk = -2
            self.indexLastLetterError = -2
            for index in range (0,len(self.resultMapTestSC)):
                self.resultMapTestSC[index] = '*'
        else:         
            self.indexCurrentLetter = indexFilaSC*6
            self.indexLastLetterOk = self.indexCurrentLetter
            self.indexLastLetterError = -2
            for index in range (0,self.indexCurrentLetter):
                self.resultMapTestSC[index] = '1'
            for index in range (self.indexCurrentLetter+1,len(self.resultMapTestSC)):
                self.resultMapTestSC[index] = '*'
        self.vMapTestSC.set(self.resultMapTestSC)

    def resetTestENsc(self):
        self.resultatTestENsc = [-1, -1]
        self.resetAllDoing()
        self.iTestENsc = 0
        self.indexAVtestENSC = indexAVtestENSC_500
        if vCalTests[iDistPacient] > 500:
            self.indexAVtestENSC = indexAVtestENSC_1000
        print(self.indexAVtestENSC)

    def cleanTestENsc(self):
        # esborra elements de dins del canvas de tests anteriors
        self.testCanvas.delete("all")
    
    def startTestENsc(self):
        # checkbox determina quin test estem fent
        if self.vCheckboxFiltersENsc.get() == 0:
            self.iTestENsc = 0
        else:
            self.iTestENsc = 1
        # crea lletra
        lettersTestENsc, resultMapTestSC = insertTextSC(self.testCanvas,
                                    int(listFontSize[self.indexAVtestENSC]),
                                    self.canvas_width,self.canvas_height )
        # activa mouse click check
        self.isDoingENsc = True

    def stopTestENsc(self):
        # desactiva mouse click check
        self.isDoingENsc = False
        # resultat el poso a -1 -> ha fallat
        logCS = -1
        self.resultatTestENsc[self.iTestENsc] = logCS
        if self.iTestENsc == 0:
            strAux ="Resultat ENsc (log): %.2f"%logCS 
        else: 
            strAux ="Resultat ENsc Filtres (log): %.2f"%logCS 
        self.vResultatTestENsc[self.iTestENsc].set(strAux )

    def finalTestENsc(self,indexSC):
        # desactiva mouse click check
        self.isDoingENsc = False
        incLogCS = 0.04
        logCS = incLogCS*(indexSC+1)
        #print(strAux)
        #tk.messagebox.showinfo("SC", strAux)
        self.resultatTestENsc[self.iTestENsc] = logCS
        if self.iTestENsc == 0:
            strAux ="Resultat ENsc (log): %.2f"%logCS 
        else: 
            strAux ="Resultat ENsc Filtres (log): %.2f"%logCS 
        self.vResultatTestENsc[self.iTestENsc].set(strAux )

    def resetTestEN(self):
        self.numLettersEN = [0, 0, 0, 0, 0]
        self.tempsTestEN = [-1, -1, -1, -1, -1]
        self.resetAllDoing()
        self.iTestEN = 0

    def cleanTestEN(self):
        # esborra elements de dins del canvas de tests anteriors
        self.testCanvas.delete("all")
    
    def updateTestEN(self):
        # mostra widgets
        self.iTestEN = int(self.vQuinTestEN.get())
        self.cleanTestEN()

    def startTestEN(self):
        # checkbox determina quin test estem fent
        #if self.vCheckboxFilters.get() == 0:
        #    self.iTestEN = 0
        #else:
        #    self.iTestEN = 1
        # crea lletra
        self.letterTestEN = insertTextEN(self.testCanvas, self.currentND,
                                         self.AV_SC_EN,
                                         self.canvas_width,self.canvas_height)
        # registra temps inici
        self.tempsTestEN[self.iTestEN] = time.time()
        self.numLettersEN[self.iTestEN] = 0
        # activa
        self.isDoingEN = True
        self.master.config(cursor="watch")

    def stopTestEN(self):
        # desactiva keyboard check
        self.isDoingEN = False
        # temps el poso a -1 -> ha fallat
        self.tempsTestEN[self.iTestEN] = -1
        tAux = "Temps rec."
        tAux = tAux + ": %.1f s." % self.tempsTestEN[self.iTestEN]
        self.vResultatTestEN[self.iTestEN].set(tAux)
        self.master.config(cursor="arrow")

    def finalTestEN(self):
        # desactiva keyboard check
        self.isDoingEN = False
        # temps
        tFinal = (time.time() - self.tempsTestEN[self.iTestEN])
        # restem el temps d'enlluernament (depen settings enlluernament, normalment 5 seg)
        self.tempsTestEN[self.iTestEN] = tFinal - gEnlluernament[indexTempsON]
        tAux = "Temps rec."
        tAux = tAux + ": %.1f s." % self.tempsTestEN[self.iTestEN]
        self.vResultatTestEN[self.iTestEN].set(tAux)
        self.master.config(cursor="arrow")

    def resetTestMO(self):
        self.resetAllDoing()
        self.iTestMO = 0
        self.newTestMO = True
        self.numMO = [5, 5, 5, 5, 5, 5]
        self.resMO = [0, 0, 0, 0, 0, 0]
        self.tempsTestMO = [-1, -1, -1, -1, -1, -1]
        self.tempsTestNetoMO = [-1, -1, -1, -1, -1, -1]
        self.lettersMO3b =['P','R','L','J','N']
        self.lettersMO3c =['J','R','P','N','L']
        self.indexCurrentLetter = 0 
        self.numCMO = 5
        self.posMOFixe = False

    def updateTestMO(self):
        # mostra widgets
        self.iTestMO = int(self.vQuinTestMO.get())
        self.newTestMO = True
        # defineixo numC de la 1a imatge de forma aleatoria
        self.numCMO = random.randint(4,9)
        self.posMOFixe = False
        self.drawTestMO()

    def cleanTestMO(self):
        self.testCanvas.delete("all")

    def drawTestMO(self):
        # pinta el test
        if self.iTestMO == 0 or self.iTestMO == 3:
            # text mida AV determinada en test AV
            #self.numMO[self.iTestMO]
            insertTextMO1(self.testCanvas, 
                  int(listFontSize[self.currentAV]),
                  self.canvas_width, self.canvas_height, self.numCMO, self.posMOFixe,
                  self.frontColor)
        if self.iTestMO == 1 or self.iTestMO == 4:
            # text mida AV determinada en test AV
            insertTextMO2(self.testCanvas, 
                  int(listFontSize[self.currentAV]),
                  self.canvas_width, self.canvas_height, self.numCMO,self.posMOFixe,
                  self.frontColor)
        if self.iTestMO == 2  or self.iTestMO == 5:
            # text mida AV determinada en test AV
            if self.iTestMO == 2:
                if self.polaritatInversa == False:
                    self.imMOb = createPhotoImage(self.imMOb_bg)
                else:
                    self.imMOb = createPhotoImage(self.imMObInv_bg)
                im = self.imMOb
            else:
                if self.polaritatInversa == False:
                    self.imMOc = createPhotoImage(self.imMOc_bg)
                else:
                    self.imMOc = createPhotoImage(self.imMOcInv_bg)
                im = self.imMOc
            if self.newTestMO == True:
                if self.polaritatInversa == False:
                    self.imMOa = createPhotoImage(self.imMOa_bg)
                else:
                    self.imMOa = createPhotoImage(self.imMOaInv_bg)
                im = self.imMOa
                self.newTestMO = False
            #photoIm = self.imMOa
            self.numMO[self.iTestMO] = insertTextMO3(self.testCanvas,im)

    def startTestMO(self):
        # reset resultats
        self.resMO[self.iTestMO] = 0
        self.indexCurrentLetter = 0 
        # per fer el test que compta el temps el num de "C" és sempre 5
        self.numCMO = 5
        # per fer el test #2 i #5 les posicions seran fixes
        self.posMOFixe = True
        # pinta el test
        self.drawTestMO()
        # registra temps inici
        self.tempsTestMO[self.iTestMO] = time.time()
        # activa
        self.isDoingMO = True
        self.master.config(cursor="watch")
        #activa eye tracker
        self.tracEyes()

    def stopTestMO(self):
        # desactiva keyboard check
        self.isDoingMO = False
        # temps el poso a -1 -> ha fallat
        self.tempsTestMO[self.iTestMO] = -1
        tAux = "temps: %.1f s." % (self.tempsTestMO[self.iTestMO])
        self.vTempsMO[self.iTestMO].set(tAux)
        strRes = "Aturat"
        self.vResMO[self.iTestMO].set("Test #%d: %s (%d/%d)" % (
                   self.iTestMO+1,strRes, 
                   self.resMO[self.iTestMO],self.numMO[self.iTestMO] ))
        self.master.config(cursor="arrow")

    def finalTestMO(self):
        # desactiva keyboard check
        self.isDoingMO = False
        # temps
        tFinal = (time.time() - self.tempsTestMO[self.iTestMO])
        self.tempsTestMO[self.iTestMO] = tFinal
        tAux = "temps: %.1f s." % (self.tempsTestMO[self.iTestMO])
        self.vTempsMO[self.iTestMO].set(tAux)
        # resultat
        strRes = "Error"
        if (self.numMO[self.iTestMO] == self.resMO[self.iTestMO]):
            strRes = "Correcte"
        if (self.iTestMO != 2 and self.iTestMO != 5 and self.numMO[self.iTestMO] > self.resMO[self.iTestMO]):
            # excepte en test 3 i 6, si ha donat per solucio menys lletres que les correctes calculem temps neto
            self.tempsTestNetoMO[self.iTestMO] = tFinal + (tFinal/self.resMO[self.iTestMO])*(self.numMO[self.iTestMO]-self.resMO[self.iTestMO])
        else:
            # neto igual a bruto
            self.tempsTestNetoMO[self.iTestMO] = tFinal
        self.vResMO[self.iTestMO].set("Test #%d: %s (%d/%d)" % (
                   self.iTestMO+1,strRes, 
                   self.resMO[self.iTestMO],self.numMO[self.iTestMO] ))
        self.master.config(cursor="arrow")

    def resetTestPV(self):
        self.resetAllDoing()
        self.iTestPV = 0
        self.newTestPV = True
        self.numPV = [18, 18, 18]
        self.resPV = [0, 0, 0]
        self.tempsTestPV = [-1, -1, -1]
        self.lettersPV1 =['3','2','3','1','2','2','3','2','4','1','2','1','3','4','2','4','3','1']
        self.lettersPV2 =['2','1','3','2','4','1','4','1','4','3','2','3','1','2','4','3','1','2']
        self.lettersPV3 =['4','2','2','3','1','4','2','2','3','4','1','4','3','1','4','3','1','2']
        self.indexCurrentLetter = 0 
        self.indexCurrentImage = 0
        self.numImExPV = [4, 2, 2]
        self.vNameTestPV= ['Memòria Visual','Figura Fons','Tancament Visual']
        self.resAllPV = np.zeros(shape=(3,18))
        self.tempsAllPV = np.zeros(shape=(3,18))
        self.tStartPV = 0.0

    def updateTestPV(self):
        # mosstra widgets
        self.iTestPV = int(self.vQuinTestPV.get())
        self.newTestPV = True
        self.drawTestPV()

    def cleanTestPV(self):
        self.testCanvas.delete("all")

    def drawTestPV(self):
        if self.isDoingPV == False and self.isDoingExamplesPV == False:
            return
        # pinta el test
        imFilename = ""
        if self.iTestPV == 0 and self.indexCurrentImage < 40:
            # imatges de PV - Memoria Visual
            imFilename = vPV_VisualMemory[self.indexCurrentImage]
        if self.iTestPV == 1 and self.indexCurrentImage < 20:
            # imatges de PV - Figura Fondo
            imFilename = vPV_VisualFigureGround[self.indexCurrentImage]
        if self.iTestPV == 2 and self.indexCurrentImage < 20:
            # imatges de PV - Cierre Visual
            imFilename = vPV_VisualClosure[self.indexCurrentImage]
        if imFilename != "":
            im = loadPVimage(imFilename,1300)
            self.imPV = ImageTk.PhotoImage(im)
            print(self.indexCurrentImage,imFilename)
            insertImagePV(self.testCanvas,self.imPV)
            self.tStartPV = time.time()
            if self.isDoingExamplesPV == False and self.iTestPV == 0:
                if (self.indexCurrentImage % 2) == 0:
                    # Memoria Visual test imatge de prova ha d'estar 5 segons visible
                    self.testCanvas.after(5000, self.timerPV)
                    
    def timerPV(self):
        #print("timer")
        # envio un click amb un '0'
        self.newLetterPressPV('0')
        
    def examplesTestPV(self):
        writer = open("..\logs.txt", 'a')
        row = "examplesTestPV"+"\n"
        writer.write(row)
        writer.close()
        # pinta el test
        self.indexCurrentImage = 0
        self.isDoingExamplesPV = True
        self.isDoingPV = False
        self.drawTestPV()

    def startTestPV(self):
        writer = open("..\logs.txt", 'a')
        row = "startTestPV"+"\n"
        writer.write(row)
        writer.close()
        # reset resultats
        self.resPV[self.iTestPV] = 0
        self.indexCurrentLetter = 0 
        self.indexCurrentImage = self.numImExPV[self.iTestPV]
        for i in range(18):
            self.resAllPV[self.iTestPV][i] = 0
            self.tempsAllPV[self.iTestPV][i] = 0
        self.vResPV[self.iTestPV].set(self.vNameTestPV[self.iTestPV]+": ?" )
        self.vTempsPV[self.iTestPV].set("temps: ?")
        # activa
        self.isDoingExamplesPV = False
        self.isDoingPV = True
        self.master.config(cursor="watch")
        # pinta el test
        self.drawTestPV()
        # registra temps inici
        self.tempsTestPV[self.iTestPV] = time.time()
        self.tLastDrawPV  = self.tempsTestPV[self.iTestPV]

    def stopTestPV(self):
        writer = open("..\logs.txt", 'a')
        row = "stopTestPV"+"\n"
        writer.write(row)
        writer.close()
        # desactiva keyboard check
        self.isDoingPV = False
        # temps el poso a -1 -> ha fallat
        self.tempsTestPV[self.iTestPV] = -1
        tAux = "temps: %.1f s." % (self.tempsTestPV[self.iTestPV])
        self.vTempsPV[self.iTestPV].set(tAux)
        self.vResPV[self.iTestPV].set("%s: aturat (%d/%d)" % (
                   self.vNameTestPV[self.iTestPV], 
                   self.resPV[self.iTestPV],self.numPV[self.iTestPV] ))
        self.master.config(cursor="arrow")

    def finalTestPV(self):
        # desactiva keyboard check
        self.isDoingPV = False
        # temps
        tNow = time.time()
        tFinal = (tNow - self.tempsTestPV[self.iTestPV])
        self.tempsTestPV[self.iTestPV] = tFinal
        tAux = "temps: %.1f s." % (self.tempsTestPV[self.iTestPV])
        self.vTempsPV[self.iTestPV].set(tAux)
        # memoritzo temps de test
        self.tempsAllPV[self.iTestPV][self.indexCurrentLetter-1] = tNow - self.tLastDrawPV
        # resultat final 
        self.vResPV[self.iTestPV].set("%s: raw score %d" % (
                   self.vNameTestPV[self.iTestPV], 
                   self.resPV[self.iTestPV] ))
        self.master.config(cursor="arrow")

    def newLetterPress(self, letter):
        writer = open("..\logs.txt", 'a')
        row = "newLetterPress "+letter+"\n"
        writer.write(row)
        writer.close()
        if self.isDoingAV is True:
            self.newLetterPressAV(letter)
        if self.isDoingSC is True:
            self.newLetterPressSC(letter)
        if self.isDoingEN is True:
            self.newLetterPressEN(letter)
        if self.isDoingMO is True:
            self.newLetterPressMO(letter)
        if self.isDoingPV is True:
            self.newLetterPressPV(letter)
        if self.isDoingExamplesPV is True:
            self.newLetterPressExamplesPV(letter)

    def newLetterPressAV(self, letter):
        # esta fent el test de PV
        if self.lettersTestAV[self.indexCurrentLetter] == letter.upper():
            # print("OK")
            self.resultMapTestAV[self.indexCurrentLetter] = '1'
            self.indexLastLetterOk = self.indexCurrentLetter
        else:
            # print("Error")
            self.resultMapTestAV[self.indexCurrentLetter] = 'X'
            # lletra no encaixa amb la que toca identificar
            # sumo 1 al total d'erros d'una sola lletra
            self.totalNum1LetterErrorsTestAV += 1
            self.indexLastLetterError = self.indexCurrentLetter
        # detecto final del test
        line = int((self.indexCurrentLetter+1)/5)
        dif = (self.indexCurrentLetter+1) - line*5
        if ((self.indexCurrentLetter == len(self.lettersTestAV)-1) or 
            (dif == 0 and self.totalNum1LetterErrorsTestAV >= 3)):
            # ha arribat al final del test o es final de linia i error dins linia >=3 -> acabo test 
            self.finalTestAV()
            return
        if (dif == 0 and self.totalNum1LetterErrorsTestAV < 3):
            # es canvi linia sense 3 errors, 
            # calculem AV Prev Line
            self.resultatAVLogMARPrevLine = self.calculaAVLogMARTestRes()           
            # incrementa best line read
            self.bestLineReadAV +=1;
            # reset errors (no els tindrem en compte en la nova linia)
            self.totalNum1LetterErrorsTestAV = 0
        self.vMapTestAV.set(self.resultMapTestAV)
        self.indexCurrentLetter += 1
        self.vFilaTestAV.set("Fila: %d" % (self.indexCurrentLetter/5+1))
        self.vEstatTestAV.set("Estat del test: %d/%d" %
                              (self.indexCurrentLetter,
                               len(self.lettersTestAV)))
            
    def newLetterPressSC(self, letter):
        # esta fent el test de SC
        if self.lettersTestSC[self.indexCurrentLetter] == letter.upper():
            # print("OK")
            self.resultMapTestSC[self.indexCurrentLetter] = '1'
            self.indexLastLetterOk = self.indexCurrentLetter
        else:
            # print("Error")
            self.resultMapTestSC[self.indexCurrentLetter] = 'X'
            # lletra no encaixa amb la que toca identificar
            if self.indexLastLetterError == self.indexCurrentLetter - 1:
                # es el segon error consecutiu
                # resto un al total d'errors d'una sola lletra
                self.totalNum1LetterErrorsTestSC -= 1
                self.finalTestSC()
                return
            else:
                # sumo 1 al total d'erros d'una sola lletra
                self.totalNum1LetterErrorsTestSC += 1
                self.indexLastLetterError = self.indexCurrentLetter
        if (self.indexCurrentLetter == len(self.lettersTestSC)-1):
            # ha arribat al final del test
            # si ultima lletra ha sigut un error he restar un als errors
            # de 1 lletra pel calcul del factor corrector
            if self.indexLastLetterError == self.indexCurrentLetter:
                self.totalNum1LetterErrorsTestSC -= 1
            self.finalTestSC()
            return
        self.vMapTestSC.set(self.resultMapTestSC)
        self.indexCurrentLetter += 1
        self.vFilaTestSC.set("Fila: %d" % (self.indexCurrentLetter/6+1))
        self.vEstatTestSC.set("Estat del test: %d/%d" %
                              (self.indexCurrentLetter,
                               len(self.lettersTestSC)))

    def newLetterPressEN(self, letter):
        # esta fent el test d'enlluernament
        self.numLettersEN[self.iTestEN] += 1
        tAux = "Num resp."
        if self.iTestEN >= 1:
            tAux += (" Filtre %d" % self.iTestEN)
        tAux = tAux + ": %d" % (self.numLettersEN[self.iTestEN])
        self.vEstatTestEN[self.iTestEN].set(tAux)
        if self.letterTestEN == letter.upper():
            # print("OK")
            self.finalTestEN()

    def newLetterPressMO(self, letter):
        # esta fent el test de motilitat ocular
        if self.iTestMO == 2 or self.iTestMO == 5:
            if self.iTestMO == 2:
                if self.lettersMO3b[self.indexCurrentLetter] == letter.upper():
                    self.resMO[self.iTestMO] += 1
            else:
                if self.lettersMO3c[self.indexCurrentLetter] == letter.upper():
                    self.resMO[self.iTestMO] += 1                
            self.indexCurrentLetter +=1
            if self.indexCurrentLetter>4:
                self.finalTestMO()
        else:
            if (letter>='0' and letter <='9'):
                # ha entrat un numero
                self.resMO[self.iTestMO] = int(letter)
                self.finalTestMO()
                
    def newLetterPressExamplesPV(self, letter):
        # esta fent el test exemple de PV
        if self.indexCurrentImage == self.numImExPV[self.iTestPV]-1:
            self.isDoingExamplesPV = False
        else:
            self.indexCurrentImage += 1
            self.drawTestPV()

    def newLetterPressPV(self, letter):
        # esta fent el test de percepcio visual
        isModel = False
        refLetter = ''
        if self.iTestPV == 0:
            # per memoria visual son dos imatges per cada test
            # i les imatges inicials de mostra són parells
            if (self.indexCurrentImage % 2) == 0:
                isModel = True
                # memoritza temps inici display del test
                self.tLastDrawPV = self.tStartPV
            else:
                refLetter =  self.lettersPV1[self.indexCurrentLetter]
        if self.iTestPV == 1:
            refLetter =  self.lettersPV2[self.indexCurrentLetter]
            # memoritza temps inici display del test
            self.tLastDrawPV = self.tStartPV
        if self.iTestPV == 2:
            refLetter =  self.lettersPV3[self.indexCurrentLetter]        
            # memoritza temps inici display del test
            self.tLastDrawPV = self.tStartPV
        if isModel == False:
            # si no es lletres 1,2,3 o 4 ignoro tecla
            if (letter.upper() != '1' and letter.upper() != '2' and
                letter.upper() != '3' and letter.upper() != '4'):
                writer = open("..\logs.txt", 'a')
                row = "newLetterPressPV isModel(false) invalid letter"+"\n"
                writer.write(row)
                writer.close()
                return
            # si no es imatge model hem de comparar lletra amb lletra entrada
            if refLetter == letter.upper():
                self.resPV[self.iTestPV] += 1
                self.resAllPV[self.iTestPV][self.indexCurrentLetter] = 1
            # avança lletra
            self.indexCurrentLetter +=1
            print(self.indexCurrentLetter)
        else:
            # si no es lletra 0 no avança
            if (letter.upper()!= '0'):
                writer = open("..\logs.txt", 'a')
                row = "newLetterPressPV isModel(true) invalid letter"+"\n"
                writer.write(row)
                writer.close()
                return
        # mira si estem al final
        if self.indexCurrentLetter>17:
            writer = open("..\logs.txt", 'a')
            row = "newLetterPressPV finalTestPV"+"\n"
            writer.write(row)
            writer.close()
            self.finalTestPV()
        else:
            #tLastDraw = self.tStartPV
            # pinta seguent imatge
            self.indexCurrentImage += 1
            writer = open("..\logs.txt", 'a')
            row = "newLetterPressPV next Image(%d" % self.indexCurrentImage
            row += ") isModel(%d" % isModel
            row +=")\n"
            writer.write(row)
            writer.close()
            self.drawTestPV()
            if isModel == False:
                # si no es model memoritzo temps entre dos draws = temps de test
                self.tempsAllPV[self.iTestPV][self.indexCurrentLetter-1] = self.tStartPV -self.tLastDrawPV
            # resultat provisional 
            self.vResPV[self.iTestPV].set("%s: raw score %d (%d/%d)" % (
                       self.vNameTestPV[self.iTestPV], 
                       self.resPV[self.iTestPV],
                       self.indexCurrentLetter,self.numPV[self.iTestPV] ))

    def mouseLeftClick(self,event):    
        #print("clicked at", event.x, event.y,event.widget)
        if self.isDoingSC is True:
            self.mouseLeftClickSC()
        if self.isDoingENsc is True:
            self.mouseLeftClickENsc()
        if self.isDoingAV is True:
            self.mouseLeftClickAV()
            
    def mouseLeftClickSC(self):
        if self.testCanvas.winfo_exists():
            # el tab del text ens dóna el index de AV
            aux = self.testCanvas.gettags(tk.CURRENT)
            indexFilaSC = int(int(aux[0])/6)
            self.setFilaInicialTestSC(indexFilaSC)

    def mouseLeftClickENsc(self):
        self.isDoingENsc = False
        if self.testCanvas.winfo_exists():
            # el tab del text ens dóna el index de SC
            aux = self.testCanvas.gettags(tk.CURRENT)
            indexSC = int(aux[0])
            self.finalTestENsc(indexSC)

    def mouseLeftClickAV(self):
        if self.testCanvas.winfo_exists():
            # el tab del text ens dóna el index de AV
            aux = self.testCanvas.gettags(tk.CURRENT)
            indexFilaAV = int(aux[0])
            self.setFilaInicialTestAV(indexFilaAV)

    def mouseEnter(self,event):
        self.master.config(cursor="hand1")
        
    def mouseLeave(self,event):
        self.master.config(cursor="arrow")
        
    def drawSimulaCV(self):
        # mida text
        fontSize = int(listFontSize[self.currentAV])
        heightL,widthL = GetTextSize(self.testCanvas,fontSize,
                                     self.canvas_width,self.canvas_height)
        self.imSimulaCV = createPhotoImageSimulaCV(self.canvas_height,
                                                   self.canvas_width,
                                           fontSize,heightL,widthL,
                                           self.IDPacient)
        insertTextMO3(self.testCanvas,self.imSimulaCV)
            
    def updateLeftFrame(self,infoVisible):
        # buida frame left anterior per si un altre test hi havia posat
        # elements
        self.LeftFrame.destroy()
        # frame de l'esquerra amb toolbar
        self.LeftFrame = tk.Frame(master)
        self.LeftFrame.pack(side=tk.LEFT)

        # logo movilab
        addLogo = True
        if addLogo is True:
            logo = tk.Label(self.LeftFrame, image=self.logoImage)
            logo.pack(side=tk.TOP)
        if (infoVisible==True):
            l0 = tk.Label(self.LeftFrame, text=movilabVersion,
                        font=('Helvetica', fontSizeC3))
            l0.pack(side=tk.TOP)
            l0 = tk.Label(self.LeftFrame, text="Copyright © E.Sánchez 2021 (tots els drets reservats)",
                        font=('Helvetica', fontSizeC3))
            l0.pack(side=tk.TOP)
            l0b = tk.Label(self.LeftFrame, text="Autors: C.Cadevall, J.Gispets, A.Matilla, E.Sánchez, A.Torrents i M.Vilaseca",
                        font=('Helvetica', fontSizeC3))
            l0b.pack(side=tk.TOP)
            l0c = tk.Label(self.LeftFrame, text="Per solicitar una llicència contactar eulalia.sanchez@upc.edu",
                        font=('Helvetica', fontSizeC3))
            l0c.pack(side=tk.TOP)

            # distància exàmen
            self.vDistanciaPacient = tk.StringVar()
            tAux = "Distància exàmen: %d mm" % vCalTests[iDistPacient]
            self.vDistanciaPacient.set(tAux)
            l1 = tk.Label(self.LeftFrame, textvariable=self.vDistanciaPacient,
                        font=('Helvetica', fontSizeC1))
            l1.pack(side=tk.TOP)
            # dia i hora
            self.vDateTime = tk.StringVar()
            self.vDateTime.set("Initial Date & Time: "+self.DateTime)
            l2 = tk.Label(self.LeftFrame,
                        textvariable=self.vDateTime, font=('Helvetica', fontSizeC1))
            l2.pack()
            # id Pacient
            self.vIDPacient = tk.StringVar()
            self.vIDPacient.set("ID Pacient: "+self.IDPacient)
            l3 = tk.Label(self.LeftFrame, textvariable=self.vIDPacient,
                        font=('Helvetica', fontSizeC1))
            l3.pack(side=tk.TOP)
            # id Optometrista
            self.vIDOpt = tk.StringVar()
            self.vIDOpt.set("ID Optometrista: "+self.IDOpt)
            l4 = tk.Label(self.LeftFrame, textvariable=self.vIDOpt,
                        font=('Helvetica', fontSizeC1))
            l4.pack(side=tk.TOP)
        # separador
        l0 = tk.Label(self.LeftFrame, text="_____________________",
                      font=('Helvetica', fontSizeC1))
        l0.pack(side=tk.TOP)
        
    def updateTestFrame(self):
        # buida frame Right anterior per si un altre test hi havia posat
        # elements
        self.testFrame.destroy()
        # frame a sota amb part grafica test
        self.testFrame = tk.Frame(self.master, width=self.testFrameSizeW,
                                  height=self.testFrameSizeH, bg="white",
                                  borderwidth=1, relief=tk.SUNKEN)
        self.testFrame.pack()

    def updateControlsFrame(self):
        # buida frame controls anterior per si un altre test hi havia posat
        # elements
        self.controlsFrame.destroy()
        # frame a sota amb controls de cada test
        self.controlsFrame = tk.Frame(self.LeftFrame)
        self.controlsFrame.pack(side=tk.TOP)

    def guiTest(self,infoVisible=True):
        # update tests amb calibracio
        self.updateCalTests(vCalTests[iDistPacient])
        createAVFontSize()

        # left frame -------------------------------------------------------
        self.updateLeftFrame(infoVisible)

        # frame a dalt tipus tab amb tipus de test
        tabsFrame = tk.Frame(self.LeftFrame)
        tabsFrame.pack(side=tk.TOP)

        if gEnable[indexAV] == 1:
            bTestAV = tk.Button(tabsFrame, text="AV",
                                 command=self.testAV, padx=5, pady=5,
                                 font=('Helvetica', fontSizeT1))
            bTestAV.pack(side=tk.LEFT)

        if gEnable[indexSC] == 1:
            bTestSC = tk.Button(tabsFrame, text="SC",
                                 command=self.testSC, padx=5, pady=5,
                                 font=('Helvetica', fontSizeT1))
            bTestSC.pack(side=tk.LEFT)

        if gEnable[indexENSC] == 1:
            bTestENsc = tk.Button(tabsFrame, text="ENsc",
                                 command=self.testENsc, padx=5, pady=5,
                                 font=('Helvetica', fontSizeT1))
            bTestENsc.pack(side=tk.LEFT)
        
        if gEnable[indexENT] == 1:
            bTestEN = tk.Button(tabsFrame, text="ENt",
                                 command=self.testENt, padx=5, pady=5,
                                 font=('Helvetica', fontSizeT1))
            bTestEN.pack(side=tk.LEFT)

        if gEnable[indexCV] == 1:
            bTestCV = tk.Button(tabsFrame, text="P",
                                     command=self.testCV, padx=5, pady=5,
                                     font=('Helvetica', fontSizeT1))
            bTestCV.pack(side=tk.LEFT)

        if gEnable[indexMO] == 1:
            bTestMO = tk.Button(tabsFrame, text="B",
                                     command=self.testMO, padx=5, pady=5,
                                     font=('Helvetica', fontSizeT1))
            bTestMO.pack(side=tk.LEFT)
        
        if gEnable[indexPV] == 1:
            bTestPV = tk.Button(tabsFrame, text="PV",
                                 command=self.testPV, padx=5, pady=5,
                                 font=('Helvetica', fontSizeT1))
            bTestPV.pack(side=tk.LEFT)

        # boto sortida agafat exemple tkinter pero aqui dins no funciona
        # self.button = Button(leftFrame,text="SORTIR",fg="red",
        #                          command=frame.quit)
        # self.button.pack(side=LEFT)

        # frame a sota amb controls de cada test
        self.controlsFrame = tk.Frame(self.LeftFrame)
        self.controlsFrame.pack(side=tk.TOP)

        # frame a la dreta amb els test --------------------------------------
        self.updateTestFrame()

    def guiNovaVal(self):
        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Save
        self.controlsFrameNovaVal = tk.Frame(self.LeftFrame)
        self.controlsFrameNovaVal.pack(side=tk.TOP)

        self.DateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.vDateTime.set("Initial Date & Time: "+self.DateTime)

        l0 = tk.Label(self.controlsFrameNovaVal,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0.pack(side = tk.TOP)     


        l1 = tk.Label(self.controlsFrameNovaVal,
                      text="ID Pacient:", font=('Helvetica', fontSizeC1))
        l1.pack(side = tk.TOP)     
        self.vNovaIDPacient = tk.StringVar()
        self.vNovaIDPacient.set(self.IDPacient)
        e1 = tk.Entry(self.controlsFrameNovaVal,
                      textvariable=self.vNovaIDPacient,
                      font=('Helvetica', fontSizeC1))
        e1.pack(side = tk.TOP)

        l1b = tk.Label(self.controlsFrameNovaVal,
                      text="Edat Pacient:", font=('Helvetica', fontSizeC1))
        l1b.pack(side = tk.TOP)     
        self.vEdatPacient = tk.StringVar()
        self.vEdatPacient.set("0")
        e1b = tk.Entry(self.controlsFrameNovaVal,
                      textvariable=self.vEdatPacient,
                      font=('Helvetica', fontSizeC1))
        e1b.pack(side = tk.TOP)

        l2 = tk.Label(self.controlsFrameNovaVal,
                      text="ID Optometrista:", font=('Helvetica', fontSizeC1))
        l2.pack(side = tk.TOP)
        self.vNovaIDOpt = tk.StringVar()
        self.vNovaIDOpt.set(self.IDOpt)
        e2 = tk.Entry(self.controlsFrameNovaVal,
                      textvariable=self.vNovaIDOpt, font=('Helvetica', fontSizeC1))
        e2.pack(side = tk.TOP)

        # checkbox per escollir si fa ull Dret CV
        self.vCheckboxRightEye = tk.IntVar()
        self.vCheckboxRightEye.set(self.doRightEyeCV)
        c1 = tk.Checkbutton(self.controlsFrameNovaVal, text="P Ull Dret",
                            variable=self.vCheckboxRightEye,
                            onvalue=1, offvalue=0,
                            font=('Helvetica', fontSizeC1))
        c1.pack(side = tk.TOP)
        # checkbox per escollir si fa ull Esq CV
        self.vCheckboxLeftEye = tk.IntVar()
        self.vCheckboxLeftEye.set(self.doLeftEyeCV)
        c2 = tk.Checkbutton(self.controlsFrameNovaVal, text="P Ull Esquerra",
                            variable=self.vCheckboxLeftEye,
                            onvalue=1, offvalue=0,
                            font=('Helvetica', fontSizeC1))
        c2.pack(side = tk.TOP)
        # checkbox per escollir si fa ambdos ulls CV
        self.vCheckboxBothEyes = tk.IntVar()
        self.vCheckboxBothEyes.set(self.doBothEyesCV)
        c3 = tk.Checkbutton(self.controlsFrameNovaVal, text="P Ambdós Ulls",
                            variable=self.vCheckboxBothEyes,
                            onvalue=1, offvalue=0,
                            font=('Helvetica', fontSizeC1))
        c3.pack(side = tk.TOP)
        
        l2 = tk.Label(self.controlsFrameNovaVal,
                      text="# Iteracions P:", font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.TOP)
        self.vNumItCV = tk.StringVar()
        self.vNumItCV.set(self.nIterationsCV)
        e2 = tk.Entry(self.controlsFrameNovaVal,
                      textvariable=self.vNumItCV, font=('Helvetica', fontSizeC1))
        e2.pack(side = tk.TOP)

        # checkbox per escollir si fa ambdos ulls CV
        self.vCheckboxFixDiag = tk.IntVar()
        self.vCheckboxFixDiag.set(self.fixDiagonalCV)
        c4 = tk.Checkbutton(self.controlsFrameNovaVal, text="Fixació diagonal P",
                            variable=self.vCheckboxFixDiag,
                            onvalue=1, offvalue=0,
                            font=('Helvetica', fontSizeC1))
        c4.pack(side = tk.TOP)

        b1 = tk.Button(self.controlsFrameNovaVal, text="Guardar",
                       command=self.guardaNovaVal, padx=5, pady=5,
                       font=('Helvetica', fontSizeC1))
        b1.pack(side = tk.TOP)

        # right frame ---------------------------------------------------
        self.updateTestFrame()

    def guiCalDistanciaPacient(self):
        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Save
        self.controlsFrameCalGrisos = tk.Frame(self.LeftFrame)
        self.controlsFrameCalGrisos.pack(side=tk.TOP)

        l1 = tk.Label(self.controlsFrameCalGrisos,
                      text="Distància exàmen (mm):", font=('Helvetica', fontSizeC1))
        l1.pack()
        self.vCalDistP = tk.StringVar()
        self.vCalDistP.set(vCalTests[iDistPacient])
        e1 = tk.Entry(self.controlsFrameCalGrisos,
                      textvariable=self.vCalDistP, font=('Helvetica', fontSizeC1))
        e1.pack()

        b1 = tk.Button(self.controlsFrameCalGrisos, text="Guardar",
                       command=self.guardaDistP, padx=5, pady=5,
                       font=('Helvetica', fontSizeC1))
        b1.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()

    def guiCalGrisos(self):

        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Next
        self.controlsFrameCalGrisos = tk.Frame(self.LeftFrame)
        self.controlsFrameCalGrisos.pack(side=tk.TOP)

        bCalBlanc = tk.Button(self.controlsFrameCalGrisos,
                              text="Blanc", command=self.nivellBlanc,
                              padx=5, pady=5, font=('Helvetica', fontSizeC1))
        bCalBlanc.pack()
        bCalNegre = tk.Button(self.controlsFrameCalGrisos,
                              text="Negre", command=self.nivellNegre,
                              padx=5, pady=5, font=('Helvetica', fontSizeC1))
        bCalNegre.pack()

        self.vLabNG = tk.StringVar()
        self.vLabNG.set("Nivell")
        labNG = tk.Label(self.controlsFrameCalGrisos,
                         textvariable=self.vLabNG, font=('Helvetica', fontSizeC1))
        labNG.pack(side=tk.TOP)

        labCNG = tk.Label(self.controlsFrameCalGrisos,
                          text="L(cd/m2):", font=('Helvetica', fontSizeC1))
        labCNG.pack()
        self.vCalNG = tk.StringVar()
        self.vCalNG.set("0.0")
        eCalGris = tk.Entry(self.controlsFrameCalGrisos,
                            textvariable=self.vCalNG, font=('Helvetica', fontSizeC1))
        eCalGris.pack()

        self.bSegNivellCalGrisos = tk.Button(self.controlsFrameCalGrisos,
                                             text="Següent Nivell Gris",
                                             command=self.segNivellGris,
                                             padx=5, pady=5,
                                             font=('Helvetica', fontSizeC1))
        self.bSegNivellCalGrisos.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()

        # reset per tornar a començar
        self.displayRectNivellGris()

    def guiCalMidaPix(self):

        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Save
        self.controlsFrameCalGrisos = tk.Frame(self.LeftFrame)
        self.controlsFrameCalGrisos.pack(side=tk.TOP)

        l1 = tk.Label(self.controlsFrameCalGrisos,
                      text="Mida quadrat (mm):", font=('Helvetica', fontSizeC1))
        l1.pack()
        self.vCalMidaQ = tk.StringVar()
        self.vCalMidaQ.set("0.0")
        e1 = tk.Entry(self.controlsFrameCalGrisos,
                      textvariable=self.vCalMidaQ, font=('Helvetica', fontSizeC1))
        e1.pack()

        b1 = tk.Button(self.controlsFrameCalGrisos,
                       text="Guardar", command=self.guardaMidaQ, padx=5,
                       pady=5, font=('Helvetica', fontSizeC1))
        b1.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame, width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()

        # pinta quadrat negre
        self.paintRectNivellGris(0.0, True)

    def guiCalMidaFont(self):

        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Save
        self.controlsFrameCalGrisos = tk.Frame(self.LeftFrame)
        self.controlsFrameCalGrisos.pack(side=tk.TOP)

        tAux = "Mida de la font (72 punts) en mm:"
        l1 = tk.Label(self.controlsFrameCalGrisos,
                      text=tAux, font=('Helvetica', fontSizeC1))
        l1.pack()
        self.vCalMidaFont = tk.StringVar()
        self.vCalMidaFont.set("0.0")
        e1 = tk.Entry(self.controlsFrameCalGrisos,
                      textvariable=self.vCalMidaFont, font=('Helvetica', fontSizeC1))
        e1.pack()

        b1 = tk.Button(self.controlsFrameCalGrisos,
                       text="Guardar", command=self.guardaMidaFont, padx=5,
                       pady=5, font=('Helvetica', fontSizeC1))
        b1.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()
        t1 = tk.Text(self.testFrame)
        t1.pack()
        t1.configure(font=('Sloan', 72))
        text = "D"
        t1.insert(tk.INSERT, text)

    def guiCalPolaritatInversa(self):

        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Save
        self.controlsFrameCalPI = tk.Frame(self.LeftFrame)
        self.controlsFrameCalPI.pack(side=tk.TOP)

        tAux = "Polaritat Inversa:"
        l1 = tk.Label(self.controlsFrameCalPI,
                      text=tAux, font=('Helvetica', fontSizeC1))
        l1.pack()
        self.vCalPolaritatInv = tk.StringVar()
        if self.polaritatInversa == False:
            self.vCalPolaritatInv.set("0")
        else: 
            self.vCalPolaritatInv.set("1")
        e1 = tk.Entry(self.controlsFrameCalPI,
                      textvariable=self.vCalPolaritatInv, font=('Helvetica', fontSizeC1))
        e1.pack()

        b1 = tk.Button(self.controlsFrameCalPI,
                       text="Guardar", command=self.guardaPolaritatInv, padx=5,
                       pady=5, font=('Helvetica', fontSizeC1))
        b1.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()
        self.testCanvas.create_image(25, 50, image=self.imPolInv, anchor=tk.NW)


    def guiCalAVTest(self):

        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        self.vAVpacient = tk.StringVar()
        self.vAVpacient.set("AV LogMAR test: " +
                            strAVLogMAR(listAVLogMAR[self.currentAV]))
        l1 = tk.Label(self.LeftFrame,textvariable=self.vAVpacient,
                      font=('Helvetica', fontSizeC1))
        l1.pack()

        # frame per tenir una llista amb scrollbar
        self.listAVFrame = tk.Frame(self.LeftFrame)
        self.listAVFrame.pack(side=tk.TOP)
        # barra scroll per llista valors AV
        scrollbar = tk.Scrollbar(self.listAVFrame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # llista de valors AV
        self.listBoxAV = tk.Listbox(self.listAVFrame, selectmode=tk.SINGLE,
                                    yscrollcommand=scrollbar.set,
                                    font=('Helvetica', fontSizeC1))
        for i in range(0, len(listAV)):
            self.listBoxAV.insert(tk.END, strAVLogMAR(listAVLogMAR[i]))
        self.listBoxAV.pack(side=tk.TOP, fill=tk.BOTH)
        scrollbar.config(command=self.listBoxAV.yview, orient=tk.VERTICAL)
        # selecciono current AV
        self.listBoxAV.selection_set(self.currentAV)
        # poso l'element seleccionat visible dins de la llista
        self.listBoxAV.see(self.currentAV)

        b1 = tk.Button(self.LeftFrame,
                       text="Guardar", command=self.setCurrentAV, padx=5,
                       pady=5, font=('Helvetica', fontSizeC1))
        b1.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()

    def guiSelectROICamera(self):
        # left frame -------------------------------------------------------
        self.updateLeftFrame(True)

        # frame a dalt amb label i botó Save
        self.controlsSelectROICamera = tk.Frame(self.LeftFrame)
        self.controlsSelectROICamera.pack(side=tk.TOP)

        l1 = tk.Label(self.controlsSelectROICamera,
                      text="Select ROI Camera:", font=('Helvetica', fontSizeC1))
        l1.pack()

        b1 = tk.Button(self.controlsSelectROICamera, text="Guardar",
                       command=self.guardaCameraROI, padx=5, pady=5,
                       font=('Helvetica', fontSizeC1))
        b1.pack()

        # right frame ---------------------------------------------------
        self.updateTestFrame()

        self.selectROI()


    def guiSimulaCV(self):
        # buida frames anterior per si un altre test hi havia posat
        # elements
        self.LeftFrame.destroy()        
        self.testFrame.destroy()
        # frame a sota amb part grafica test
        # crea frame amb una imatge per simular efecte del CV a pantalla
        # completa
        hFrame = master.winfo_height()*0.95
        wFrame = master.winfo_width()
        self.testFrame = tk.Frame(self.master, width=wFrame,
                                  height=hFrame, bg="white",
                                  borderwidth=1, relief=tk.SUNKEN)
        self.testFrame.pack()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()
        self.drawSimulaCV()

    def __init__(self, master):
        # load images
        self.imMOa_bg = Image.open('..\MO3a.png')
        self.imMOa_bg = self.imMOa_bg.convert("RGBA")
        self.imMOa = createPhotoImage(self.imMOa_bg)
        self.imMOb_bg = Image.open('..\MO3b.png')
        self.imMOb_bg = self.imMOb_bg.convert("RGBA")
        self.imMOb = createPhotoImage(self.imMOb_bg)
        self.imMOc_bg = Image.open('..\MO3c.png')
        self.imMOc_bg = self.imMOc_bg.convert("RGBA")
        self.imMOc = createPhotoImage(self.imMOc_bg)
        # polaritat inversa
        self.imMOaInv_bg = Image.open('..\MO3aInv.png')
        self.imMOaInv_bg = self.imMOaInv_bg.convert("RGBA")
        self.imMOaInv = createPhotoImage(self.imMOaInv_bg)
        self.imMObInv_bg = Image.open('..\MO3bInv.png')
        self.imMObInv_bg = self.imMObInv_bg.convert("RGBA")
        self.imMObInv = createPhotoImage(self.imMObInv_bg)
        self.imMOcInv_bg = Image.open('..\MO3cInv.png')
        self.imMOcInv_bg = self.imMOcInv_bg.convert("RGBA")
        self.imMOcInv = createPhotoImage(self.imMOcInv_bg)
        # per escollir polaritat inversa o no
        self.imPolInv_bg = Image.open('..\PolInv.png')
        self.imPolInv_bg = self.imPolInv_bg.convert("RGBA")
        self.imPolInv = createPhotoImage(self.imPolInv_bg)
    
        self.logoImage = tk.PhotoImage(file="..\logo.png")
        # crear variable amb una imatge qualsevol, després ja la dibuixa
        self.imSimulaCV = createPhotoImage(self.imMOc_bg)
        
        getEnableTests()
        if gEnable[indexPV] == 1:
            # load PV images
            findPVImages(False)
            im = loadPVimage(vPV_VisualMemory[0],1300)
            self.imPV = ImageTk.PhotoImage(im)
        else:
            self.imPV = ImageTk.PhotoImage(self.imMOa_bg)
        # ini variables
        getCalMonitor()        
        self.defaultsTestCV()
        self.IDPacient = "No id"
        self.edatPacient = 0
        self.IDOpt = "No id"
        self.DateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # aquesta funcio escriu arxiu DotSize.txt
        distanciaPacient = getDistanciaExamen()
        self.updateCalTests(distanciaPacient)
        self.master = master
        self.numNivellsGris = 21
        self.calNivellsGris = np.zeros(self.numNivellsGris)
        self.valNivellsGris = np.zeros(self.numNivellsGris)
        self.currentNivellGris = 0
        self.resetCalNivellsGris()
        self.polaritatInversa = False
        SetColorPolaritat(self)
        self.resetTestAV()
        self.resetTestSC()
        self.resetTestENsc()
        self.resetTestEN()
        self.resetTestMO()
        self.resetTestPV()

        # ini web cam
        getCameraConfig()
        self.imgTK = ImageTk.PhotoImage(self.imMOa_bg)
        self.iniWebCam()

        writer = open("..\logs.txt", 'a')
        row = "new execution ------------------ "+"\n"
        writer.write(row)
        writer.close()

        # set AV per a SC i ENt TFM Deslumbrometro potser fixe enlloc de la del pacient
        getEnlluernament()
        self.AV_SC_EN = gEnlluernament[indexAVFixe]


        # crear menu
        menubar = tk.Menu(master)

        # create a pulldown menu, and add it to the menu bar
        calmenu = tk.Menu(menubar, tearoff=0)
        resmenu = tk.Menu(menubar, tearoff=0)
        mainmenu = tk.Menu(menubar, tearoff=0)
        # movilab
        mainmenu.add_command(label="Nova Valoració", command=self.guiNovaVal)
        mainmenu.add_command(label="Guarda Valoració", command=self.guardaValRes)
        menubar.add_cascade(label="Movilab", menu=mainmenu)
        # resultats
        resmenu.add_command(label="Simula Camp Visual", command=self.guiSimulaCV)
        resmenu.add_separator()
        resmenu.add_command(label="Sortir de resultats",
                            command=self.guiTest)
        menubar.add_cascade(label="Resultats", menu=resmenu)
        # calibratges
        calmenu.add_command(label="Distància exàmen",
                            command=self.guiCalDistanciaPacient)
        calmenu.add_command(label="Mida pixel", command=self.guiCalMidaPix)
        calmenu.add_command(label="Mida font", command=self.guiCalMidaFont)
        calmenu.add_command(label="Nivells Gris (SC)",
                            command=self.guiCalGrisos)
        calmenu.add_command(label="AV test",
                            command=self.guiCalAVTest)
        calmenu.add_command(label="Polaritat Inversa",
                            command=self.guiCalPolaritatInversa)
        calmenu.add_separator()
        calmenu.add_command(label="Camera ROI",
                            command=self.guiSelectROICamera)
        calmenu.add_separator()
        calmenu.add_command(label="Sortir de calibratges",
                            command=self.guiTest)
        menubar.add_cascade(label="Calibratges", menu=calmenu)
        self.master.config(menu=menubar)

        # frame a l'esquerra amb els toolbar -----------------------------
        self.LeftFrame = tk.Frame(master)
        self.LeftFrame.pack(side=tk.LEFT)
        self.LeftFrame.update()

        # frame a la dreta amb graf. test mida depen de la pantalla -----
        # la calculo a partir del height
        self.testFrameSizeH = master.winfo_height()*0.95
        self.testFrameSizeW = master.winfo_height()*1.4
        self.testFrame = tk.Frame(self.master, width=self.testFrameSizeW,
                                  height=self.testFrameSizeH, bg="white",
                                  borderwidth=1, relief=tk.SUNKEN)
        self.testFrame.pack()
        self.testFrame.update()

        # mostra guiTest
        self.guiTest(True)

    def destroy(self):
        # es crida al tancar app
        self.guardaValRes()
        self.releaseWebCam()

    def testAV(self):
        if gEnable[indexAV] == 0:
            return
        response = messagebox.askyesno("Movilab", "Iniciar el test AV esborra els resultats anteriors AV. Vols continuar?")
        if response == False:
            return

        # ini variables test
        self.resetTestAV()
        self.isDoingAV = True

        # left frame -------------------------------------------------------
        self.guiTest(True)
        # controls -------------------------------
        self.updateControlsFrame()
        # etiquetes amb estat del test de AV
        self.vEstatTestAV = tk.StringVar()
        self.vEstatTestAV.set(
                    "Estat del test: %d/%d" % (self.indexCurrentLetter,
                                              len(self.lettersTestAV)))
        l2 = tk.Label(self.controlsFrame,
                      textvariable=self.vEstatTestAV,
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.TOP)
        self.vFilaTestAV = tk.StringVar()
        self.vFilaTestAV.set("Fila: %d" % (self.indexCurrentLetter/5+1))
        l2b = tk.Label(self.controlsFrame, textvariable=self.vFilaTestAV,
                       padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2b.pack(side=tk.TOP)
        # label status
        self.vMapTestAV = tk.StringVar()
        l3 = tk.Label(self.controlsFrame, textvariable=self.vMapTestAV,
                      wraplength=wrapLengthAV, padx=10, pady=10,
                      font=('Courier', fontSizeC2))
        l3.pack(side=tk.TOP)
        self.vResultatTestAV = tk.StringVar()
        self.vResultatTestAV.set("Resultat AV: ?")
        l4 = tk.Label(self.controlsFrame, textvariable=self.vResultatTestAV,
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l4.pack(side=tk.TOP)
        
        # test --------------------------------------
        self.updateTestFrame()
        """

        scrollB = tk.Scrollbar(self.testFrame)
        scrollB.pack(side=tk.RIGHT, fill=tk.Y)
        # creo text
        if wMonitorRes < 2000:
            self.wText = tk.Text(self.testFrame, height=17, width=34)
        else:
            self.wText = tk.Text(self.testFrame, height=27, width=54)
        self.wText.pack(side=tk.LEFT, fill=tk.Y)
        scrollB.config(command=self.wText.yview)
        self.wText.config(yscrollcommand=scrollB.set)
        self.lettersTestAV, self.resultMapTestAV  = insertTextAV(self.wText)
        """
        self.testFrame.update()
        # scrollbar
        scrollB = tk.Scrollbar(self.testFrame)
        scrollB.pack(side=tk.RIGHT, fill=tk.Y)
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor,
                                    scrollregion=(0,0,
                                        self.canvas_width,self.canvas_height))
        self.testCanvas.pack()
        # scrollbar
        scrollB.config(command=self.testCanvas.yview)
        self.testCanvas.config(yscrollcommand=scrollB.set)
        # text mida AV determinada en test AV
        self.lettersTestAV, self.resultMapTestAV = insertTextAVnew(self.testCanvas,
                                    self.canvas_width,self.canvas_height,
                                    self.frontColor)

        # update label status
        self.vMapTestAV.set(self.resultMapTestAV)        

    def testSC(self):
        if gEnable[indexSC] == 0:
            return
        response = messagebox.askyesno("Movilab", "Iniciar el test SC esborra els resultats anteriors SC. Vols continuar?")
        if response == False:
            return

        # ini variables test
        self.resetTestSC()
        self.isDoingSC = True

        # left frame -------------------------------------------------------
        self.guiTest(True)
        # controls -------------------------------
        self.updateControlsFrame()

        # etiqueta amb AV del pacient (escollida en el test AV) o fixe en funció settings de Enlluernament
        self.AV_SC_EN = self.currentAV
        if gEnlluernament[indexUsarAVFixe]==1:
            self.AV_SC_EN = gEnlluernament[indexAVFixe]
        tAux = "AV LogMAR test: " + strAVLogMAR(listAVLogMAR[self.AV_SC_EN])
        lAV = tk.Label(self.controlsFrame, text=tAux, padx=10, pady=10,
                       font=('Helvetica', fontSizeC1))
        lAV.pack(side=tk.TOP)
        # etiquetes amb estat del test de SC
        self.vEstatTestSC = tk.StringVar()
        self.vEstatTestSC.set(
                    "Estat del test: %d/%d" % (self.indexCurrentLetter,
                                              len(self.lettersTestSC)))
        l2 = tk.Label(self.controlsFrame,
                      textvariable=self.vEstatTestSC,
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.TOP)
        self.vFilaTestSC = tk.StringVar()
        self.vFilaTestSC.set("Fila: %d" % (self.indexCurrentLetter/6+1))
        l2b = tk.Label(self.controlsFrame, textvariable=self.vFilaTestSC,
                       padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2b.pack(side=tk.TOP)
        # label status
        self.vMapTestSC = tk.StringVar()
        l3 = tk.Label(self.controlsFrame, textvariable=self.vMapTestSC,
                      wraplength=wrapLengthSC, padx=10, pady=10,
                      font=('Courier', fontSizeC1))
        l3.pack(side=tk.TOP)
        self.vResultatTestSC = tk.StringVar()
        self.vResultatTestSC.set("Resultat SC (log): ?")
        l4 = tk.Label(self.controlsFrame, textvariable=self.vResultatTestSC,
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l4.pack(side=tk.TOP)

        # test --------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # scrollbar
        scrollB = tk.Scrollbar(self.testFrame)
        scrollB.pack(side=tk.RIGHT, fill=tk.Y)
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        """
        if self.currentAV<4:
            self.canvas_height = self.canvas_height*2.0
        """
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg="white",
                                    scrollregion=(0,0,
                                        self.canvas_width,self.canvas_height))
        self.testCanvas.pack()
        # scrollbar
        scrollB.config(command=self.testCanvas.yview)
        self.testCanvas.config(yscrollcommand=scrollB.set)
        # text mida AV determinada en test AV o per mida fixe depen settings enlluernament
        self.lettersTestSC, self.resultMapTestSC = insertTextSC(self.testCanvas,
                                    int(listFontSize[self.AV_SC_EN]),
                                    self.canvas_width,self.canvas_height )
        # update label status
        self.vMapTestSC.set(self.resultMapTestSC)

    def testENsc(self):
        if gEnable[indexENSC] == 0:
            return
        response = messagebox.askyesno("Movilab", "Iniciar el test ENsc esborra els resultats anteriors ENsc. Vols continuar?")
        if response == False:
            return

        # ini variables test
        self.resetTestENsc()
        self.isDoingENsc = True

        # left frame -------------------------------------------------------
        self.guiTest(True)
        # controls -------------------------------
        self.updateControlsFrame()

        # etiqueta amb AV que es fa servir per test ENSC; és fixe
        self.indexAVtestENSC = indexAVtestENSC_500
        if vCalTests[iDistPacient] > 500:
            self.indexAVtestENSC = indexAVtestENSC_1000
        print(self.indexAVtestENSC)
        tAux = "AV LogMAR test ENSC: " + strAVLogMAR(listAVLogMAR[self.indexAVtestENSC])
        lAV = tk.Label(self.controlsFrame, text=tAux, padx=10, pady=10,
                       font=('Helvetica', fontSizeC1))
        lAV.pack(side=tk.TOP)

        # checkbox per escollir si pacient porta filtres
        self.vCheckboxFiltersENsc = tk.IntVar()
        self.vCheckboxFiltersENsc.set(0)
        c1 = tk.Checkbutton(self.controlsFrame, text="Filtres",
                            variable=self.vCheckboxFiltersENsc,
                            onvalue=1, offvalue=0,
                            font=('Helvetica', fontSizeC1))
        c1.pack()
        
        # frame per agrupar botons tipus tab
        tabsFrame = tk.Frame(self.controlsFrame)
        tabsFrame.pack(side=tk.TOP)
        # boto per esborrar la lletra visible d'entrada
        b1 = tk.Button(tabsFrame, text='Esborra',
                       command=self.cleanTestENsc, font=('Helvetica', fontSizeC1))
        b1.pack(side=tk.LEFT)

        # boto per mostrar la lletra del test i activar el timer
        b2 = tk.Button(tabsFrame, text='Comença',
                       command=self.startTestENsc, font=('Helvetica', fontSizeC1))
        b2.pack(side=tk.LEFT)
        """
        # boto per aturar el test si no veu la lletra
        b3 = tk.Button(tabsFrame, text='Atura',
                       command=self.stopTestENsc, font=('Helvetica', fontSizeC1))
        b3.pack(side=tk.LEFT)
        """
        # etiquetes amb estat del test de SC
        l0 = tk.Label(self.controlsFrame, text="_____________________",
                      font=('Helvetica', fontSizeC1))
        l0.pack(side=tk.TOP)
        self.vResultatTestENsc = []
        self.vResultatTestENsc.append(tk.StringVar())
        self.vResultatTestENsc[0].set("Resultat ENsc (log): ?")
        l1 = tk.Label(self.controlsFrame, textvariable=self.vResultatTestENsc[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.TOP)
        l0b = tk.Label(self.controlsFrame, text="_____________________",
                      font=('Helvetica', fontSizeC1))
        l0b.pack(side=tk.TOP)
        self.vResultatTestENsc.append(tk.StringVar())
        self.vResultatTestENsc[1].set("Resultat ENsc Filtre (log): ?")
        l2 = tk.Label(self.controlsFrame, textvariable=self.vResultatTestENsc[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.TOP)

        # test --------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # scrollbar
        scrollB = tk.Scrollbar(self.testFrame)
        scrollB.pack(side=tk.RIGHT, fill=tk.Y)
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg="white",
                                    scrollregion=(0,0,
                                        self.canvas_width,self.canvas_height))
        self.testCanvas.pack()
        # scrollbar
        scrollB.config(command=self.testCanvas.yview)
        self.testCanvas.config(yscrollcommand=scrollB.set)
        # text mida AV determinada en test AV
        lettersTestENsc, resultMapTestSC = insertTextSC(self.testCanvas,
                                    int(listFontSize[self.indexAVtestENSC]),
                                    self.canvas_width,self.canvas_height )

    def testENt(self):
        if gEnable[indexENT] == 0:
            return
        response = messagebox.askyesno("Movilab", "Iniciar el test ENt esborra els resultats anteriors ENt. Vols continuar?")
        if response == False:
            return

        # ini variables test
        self.resetTestEN()

        # left frame -------------------------------------------------------
        self.guiTest(False)
        # controls -------------------------------
        self.updateControlsFrame()

        # canvas video
        self.videoFinestra = False
        heightVideo = gCamera[indexHeight]        
        widthVideo = gCamera[indexWidth]
        if (self.videoFinestra == True):
            heightVideo = 1
            widthVideo = 1
        self.testVideo = tk.Canvas(self.controlsFrame,
                                width=widthVideo,
                                height=heightVideo,
                                bg=self.backgroundColor)
        self.testVideo.pack()
        print(widthVideo,heightVideo)
        # start video
        self.startVideo()
        # etiqueta amb AV del pacient (escollida en el test AV) o fixe en funció settings de Enlluernament
        self.AV_SC_EN = self.currentAV
        if gEnlluernament[indexUsarAVFixe]==1:
            self.AV_SC_EN = gEnlluernament[indexAVFixe]
        tAux = "AV LogMAR test Ent: " + strAVLogMAR(listAVLogMAR[self.AV_SC_EN])
        lAV = tk.Label(self.controlsFrame, text=tAux, padx=10, pady=10,
                       font=('Helvetica', fontSizeC1))
        lAV.pack(side=tk.TOP)
        # etiqueta amb SC del pacient
        tAux = "Resultat SC (log): %.2f" % self.resultatSC
        lSC = tk.Label(self.controlsFrame, text=tAux, padx=10, pady=10,
                       font=('Helvetica', fontSizeC1))
        lSC.pack(side=tk.TOP)
        # checkbox per escollir si pacient porta filtres
        #self.vCheckboxFilters = tk.IntVar()
        #self.vCheckboxFilters.set(0)
        #c1 = tk.Checkbutton(self.controlsFrame, text="Filtres",
        #                    variable=self.vCheckboxFilters,
        #                    onvalue=1, offvalue=0,
        #                    font=('Helvetica', fontSizeC1))
        #c1.pack()
        # radiobutton quin test dins de ENt
        self.vQuinTestEN = tk.IntVar()
        # frame per agrupar radio button en dos columnes
        rbFrame = tk.Frame(self.controlsFrame)
        rbFrame.pack(side=tk.TOP)
        # frame per agrupar radio button left
        rbLeftFrame = tk.Frame(rbFrame)
        rbLeftFrame.pack(side=tk.LEFT)
        tk.Radiobutton (rbLeftFrame,text="Sense filtre",
                variable=self.vQuinTestEN,value=0,
                command=self.updateTestEN,  
                font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)
        for i in range (0,2):
            strAux = "Filtre #%d" % (i+1)
            tk.Radiobutton (rbLeftFrame,text=strAux,
                    variable=self.vQuinTestEN,value=i+1,
                    command=self.updateTestEN,  
                    font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)
        # frame per agrupar radio button dreta
        rbRightFrame = tk.Frame(rbFrame)
        rbRightFrame.pack(side=tk.LEFT)
        for i in range (2,4):
            strAux = "Filtre #%d" % (i+1)
            tk.Radiobutton (rbRightFrame,text=strAux,
                    variable=self.vQuinTestEN,value=i+1,
                    command=self.updateTestEN,  
                    font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)

        # frame per agrupar botons tipus tab
        tabsFrame = tk.Frame(self.controlsFrame)
        tabsFrame.pack(side=tk.TOP)
        # boto per esborrar la lletra visible d'entrada
        b1 = tk.Button(tabsFrame, text='Esborra',
                       command=self.cleanTestEN, font=('Helvetica', fontSizeC1))
        b1.pack(side=tk.LEFT)

        # boto per mostrar la lletra del test i activar el timer
        b2 = tk.Button(tabsFrame, text='Comença',
                       command=self.startTestEN, font=('Helvetica', fontSizeC1))
        b2.pack(side=tk.LEFT)
        # boto per aturar el test si no veu la lletra
        b3 = tk.Button(tabsFrame, text='Atura',
                       command=self.stopTestEN, font=('Helvetica', fontSizeC1))
        b3.pack(side=tk.LEFT)
        # etiquetes estat del test sense filtres
        l0 = tk.Label(self.controlsFrame, text="_____________________",
                      font=('Helvetica', fontSizeC1))
        l0.pack(side=tk.TOP)
  
        self.vEstatTestEN = []
        self.vResultatTestEN = []
        
        # frame per agrupar info resultats
        res1Frame = tk.Frame(self.controlsFrame)
        res1Frame.pack(side=tk.TOP)
        # labels
        self.vEstatTestEN.append(tk.StringVar())
        self.vEstatTestEN[0].set("Num resp.: %d" % (self.numLettersEN[0]))
        l1 = tk.Label(res1Frame, textvariable=self.vEstatTestEN[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        self.vResultatTestEN.append(tk.StringVar())
        self.vResultatTestEN[0].set("Temps rec.: ?")
        l2 = tk.Label(res1Frame, textvariable=self.vResultatTestEN[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        # frame per agrupar info resultats
        res2Frame = tk.Frame(self.controlsFrame)
        res2Frame.pack(side=tk.TOP)
        # labels
        self.vEstatTestEN.append(tk.StringVar())
        tAux = "Num resp. Filtre 1: %d" % (self.numLettersEN[1])
        self.vEstatTestEN[1].set(tAux)
        l1 = tk.Label(res2Frame, textvariable=self.vEstatTestEN[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        self.vResultatTestEN.append(tk.StringVar())
        self.vResultatTestEN[1].set("Temps rec.: ?")
        l2 = tk.Label(res2Frame, textvariable=self.vResultatTestEN[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        # frame per agrupar info resultats
        res3Frame = tk.Frame(self.controlsFrame)
        res3Frame.pack(side=tk.TOP)
        # labels
        self.vEstatTestEN.append(tk.StringVar())
        tAux = "Num resp. Filtre 2: %d" % (self.numLettersEN[2])
        self.vEstatTestEN[2].set(tAux)
        l1 = tk.Label(res3Frame, textvariable=self.vEstatTestEN[2],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        self.vResultatTestEN.append(tk.StringVar())
        self.vResultatTestEN[2].set("Temps rec.: ?")
        l2 = tk.Label(res3Frame, textvariable=self.vResultatTestEN[2],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        # frame per agrupar info resultats
        res4Frame = tk.Frame(self.controlsFrame)
        res4Frame.pack(side=tk.TOP)
        # labels
        self.vEstatTestEN.append(tk.StringVar())
        tAux = "Num resp. Filtre 3: %d" % (self.numLettersEN[3])
        self.vEstatTestEN[3].set(tAux)
        l1 = tk.Label(res4Frame, textvariable=self.vEstatTestEN[3],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        self.vResultatTestEN.append(tk.StringVar())
        self.vResultatTestEN[3].set("Temps rec.: ?")
        l2 = tk.Label(res4Frame, textvariable=self.vResultatTestEN[3],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        # frame per agrupar info resultats
        res5Frame = tk.Frame(self.controlsFrame)
        res5Frame.pack(side=tk.TOP)
        # labels
        self.vEstatTestEN.append(tk.StringVar())
        tAux = "Num resp. Filtre 4: %d" % (self.numLettersEN[4])
        self.vEstatTestEN[4].set(tAux)
        l1 = tk.Label(res5Frame, textvariable=self.vEstatTestEN[4],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        self.vResultatTestEN.append(tk.StringVar())
        self.vResultatTestEN[4].set("Temps rec.: ?")
        l2 = tk.Label(res5Frame, textvariable=self.vResultatTestEN[4],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)

        # test --------------------------------------
        self.updateTestFrame()
        """
        # creo text
        self.wText = tk.Text(self.testFrame, height=3, width=34)
        self.wText.pack()
        """
        self.updateTestFrame()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()
        # text mida inicial depen test AV o mida fixe en funció dels settings enlluernament
        insertTextEN(self.testCanvas, self.currentND, self.AV_SC_EN,
                     self.canvas_width,self.canvas_height)

    def testCV(self):
        if gEnable[indexCV] == 0:
            return
        # left frame -------------------------------------------------------
        self.guiTest(True)
        # controls -------------------------------
        self.updateControlsFrame()

    def testMO(self):
        if gEnable[indexMO] == 0:
            return
        response = messagebox.askyesno("Movilab", "Iniciar el test B esborra els resultats anteriors B. Vols continuar?")
        if response == False:
            return

        # ini variables test
        self.resetTestMO()
        self.isDoingMO = False
        self.iTestMO = 0

        # left frame -------------------------------------------------------
        self.guiTest(True)
        # controls -------------------------------
        self.updateControlsFrame()

        # radiobutton quin test dins de MO
        self.vQuinTestMO = tk.IntVar()
        # frame per agrupar radio button en dos columnes
        rbFrame = tk.Frame(self.controlsFrame)
        rbFrame.pack(side=tk.TOP)
        # frame per agrupar radio button left
        rbLeftFrame = tk.Frame(rbFrame)
        rbLeftFrame.pack(side=tk.LEFT)
        for i in range (0,3):
            strAux = "Test #%d" % (i+1)
            tk.Radiobutton (rbLeftFrame,text=strAux,
                    variable=self.vQuinTestMO,value=i,
                    command=self.updateTestMO,  
                    font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)
        # frame per agrupar radio button left
        rbRightFrame = tk.Frame(rbFrame)
        rbRightFrame.pack(side=tk.LEFT)
        for i in range (3,6):
            strAux = "Test Mentonera #%d" % (i+1)
            tk.Radiobutton (rbRightFrame,text=strAux,
                    variable=self.vQuinTestMO,value=i,
                    command=self.updateTestMO,  
                    font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)

        # etiqueta amb AV del pacient (escollida en el test AV)
        tAux = "AV LogMAR test: " + strAVLogMAR(listAVLogMAR[self.currentAV])
        lAV = tk.Label(self.controlsFrame, text=tAux, padx=10, pady=10,
                       font=('Helvetica', fontSizeC1))
        lAV.pack(side=tk.TOP)

        # frame per agrupar botons tipus tab
        tabsFrame = tk.Frame(self.controlsFrame)
        tabsFrame.pack(side=tk.TOP)
        # boto per esborrar lletres visible d'entrada
        b1 = tk.Button(tabsFrame, text='Esborra',
                       command=self.cleanTestMO, font=('Helvetica', fontSizeC1))
        b1.pack(side=tk.LEFT)

        # boto per mostrar lletres del test i activar el timer
        b2 = tk.Button(tabsFrame, text='Comença',
                       command=self.startTestMO, font=('Helvetica', fontSizeC1))
        b2.pack(side=tk.LEFT)
        # boto per mostrar lletres del test i activar el timer
        b2b = tk.Button(tabsFrame, text='Aleatori',
                       command=self.updateTestMO, font=('Helvetica', fontSizeC1))
        b2b.pack(side=tk.LEFT)
        # boto per aturar el test si no dona resposta
        b3 = tk.Button(tabsFrame, text='Atura',
                       command=self.stopTestMO, font=('Helvetica', fontSizeC1))
        b3.pack(side=tk.LEFT)
        
        self.vResMO = []
        self.vTempsMO = []
        
        """
        l0a = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0a.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res1Frame = tk.Frame(self.controlsFrame)
        res1Frame.pack(side=tk.TOP)
        # etiqueta amb resultat num 'C'
        self.vResMO.append(tk.StringVar())
        self.vResMO[0].set("Test #1: ?" )
        l1 = tk.Label(res1Frame,
                      textvariable=self.vResMO[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsMO.append(tk.StringVar())
        self.vTempsMO[0].set("temps: ?")
        l2 = tk.Label(res1Frame, textvariable=self.vTempsMO[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        """
        l0b = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0b.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res2Frame = tk.Frame(self.controlsFrame)
        res2Frame.pack(side=tk.TOP)
        # etiqueta amb resultat num 'C'
        self.vResMO.append(tk.StringVar())
        self.vResMO[1].set("Test #2: ?" )
        l3 = tk.Label(res2Frame,
                      textvariable=self.vResMO[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l3.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsMO.append(tk.StringVar())
        self.vTempsMO[1].set("temps: ?")
        l4 = tk.Label(res2Frame, textvariable=self.vTempsMO[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l4.pack(side=tk.LEFT)
        """
        l0c = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0c.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res3Frame = tk.Frame(self.controlsFrame)
        res3Frame.pack(side=tk.TOP)
        # etiqueta amb resultat linies
        self.vResMO.append(tk.StringVar())
        self.vResMO[2].set("Test #3: ?" )
        l5 = tk.Label(res3Frame,
                      textvariable=self.vResMO[2],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l5.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsMO.append(tk.StringVar())
        self.vTempsMO[2].set("temps: ?")
        l6 = tk.Label(res3Frame, textvariable=self.vTempsMO[2],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l6.pack(side=tk.LEFT)
        """
        l0a = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0a.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res4Frame = tk.Frame(self.controlsFrame)
        res4Frame.pack(side=tk.TOP)
        # etiqueta amb resultat num 'C'
        self.vResMO.append(tk.StringVar())
        self.vResMO[3].set("Test #4: ?" )
        l1 = tk.Label(res4Frame,
                      textvariable=self.vResMO[3],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsMO.append(tk.StringVar())
        self.vTempsMO[3].set("temps: ?")
        l2 = tk.Label(res4Frame, textvariable=self.vTempsMO[3],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        """
        l0b = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0b.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res5Frame = tk.Frame(self.controlsFrame)
        res5Frame.pack(side=tk.TOP)
        # etiqueta amb resultat num 'C'
        self.vResMO.append(tk.StringVar())
        self.vResMO[4].set("Test #5: ?" )
        l3 = tk.Label(res5Frame,
                      textvariable=self.vResMO[4],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l3.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsMO.append(tk.StringVar())
        self.vTempsMO[4].set("temps: ?")
        l4 = tk.Label(res5Frame, textvariable=self.vTempsMO[4],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l4.pack(side=tk.LEFT)
        """
        l0c = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0c.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res6Frame = tk.Frame(self.controlsFrame)
        res6Frame.pack(side=tk.TOP)
        # etiqueta amb resultat linies
        self.vResMO.append(tk.StringVar())
        self.vResMO[5].set("Test #6: ?" )
        l5 = tk.Label(res6Frame,
                      textvariable=self.vResMO[5],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l5.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsMO.append(tk.StringVar())
        self.vTempsMO[5].set("temps: ?")
        l6 = tk.Label(res6Frame, textvariable=self.vTempsMO[5],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l6.pack(side=tk.LEFT)

        # test --------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        print(self.canvas_height)
        print(self.canvas_width)
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()
        self.drawTestMO()
        
    def testPV(self):
        if gEnable[indexPV] == 0:
            return
        response = messagebox.askyesno("Movilab", "Iniciar el test PV esborra els resultats anteriors PV. Vols continuar?")
        if response == False:
            return
        
        # ini variables test
        self.resetTestPV()
        self.isDoingPV = False
        self.iTestPV = 0

        # left frame -------------------------------------------------------
        self.guiTest(True)
        # controls -------------------------------
        self.updateControlsFrame()

        # tipus test
        l0 = tk.Label(self.controlsFrame,
                      text="Làmines TVPS4",
                      padx=10, pady=10, font=('Helvetica', fontSizeC2))
        l0.pack(side=tk.TOP)

        # radiobutton quin test dins de PV
        self.vQuinTestPV = tk.IntVar()
        # frame per agrupar radio button en 1 columna
        rbFrame = tk.Frame(self.controlsFrame)
        rbFrame.pack(side=tk.TOP)
        tk.Radiobutton (rbFrame,text=self.vNameTestPV[0],
                variable=self.vQuinTestPV,value=0,
                command=self.updateTestPV,  
                font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)
        tk.Radiobutton (rbFrame,text=self.vNameTestPV[1],
                variable=self.vQuinTestPV,value=1,
                command=self.updateTestPV,  
                font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)
        tk.Radiobutton (rbFrame,text=self.vNameTestPV[2],
                variable=self.vQuinTestPV,value=2,
                command=self.updateTestPV,  
                font=('Helvetica', fontSizeC1)).pack(anchor=tk.W)


        # frame per agrupar botons tipus tab
        tabsFrame = tk.Frame(self.controlsFrame)
        tabsFrame.pack(side=tk.TOP)
        # boto per esborrar lletres visible d'entrada
        b1 = tk.Button(tabsFrame, text='Exemples',
                       command=self.examplesTestPV, font=('Helvetica', fontSizeC1))
        b1.pack(side=tk.LEFT)

        # boto per mostrar lletres del test i activar el timer
        b2 = tk.Button(tabsFrame, text='Comença',
                       command=self.startTestPV, font=('Helvetica', fontSizeC1))
        b2.pack(side=tk.LEFT)
        # boto per aturar el test si no dona resposta
        b3 = tk.Button(tabsFrame, text='Atura',
                       command=self.stopTestPV, font=('Helvetica', fontSizeC1))
        b3.pack(side=tk.LEFT)
        
        self.vResPV = []
        self.vTempsPV = []
        
        """
        l0a = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0a.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res1Frame = tk.Frame(self.controlsFrame)
        res1Frame.pack(side=tk.TOP)
        # etiqueta amb resultat num 'C'
        self.vResPV.append(tk.StringVar())
        self.vResPV[0].set("Memòria Visual: ?" )
        l1 = tk.Label(res1Frame,
                      textvariable=self.vResPV[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l1.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsPV.append(tk.StringVar())
        self.vTempsPV[0].set("temps: ?")
        l2 = tk.Label(res1Frame, textvariable=self.vTempsPV[0],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l2.pack(side=tk.LEFT)
        """
        l0b = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0b.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res2Frame = tk.Frame(self.controlsFrame)
        res2Frame.pack(side=tk.TOP)
        # etiqueta amb resultat num 'C'
        self.vResPV.append(tk.StringVar())
        self.vResPV[1].set("Figura Fondo: ?" )
        l3 = tk.Label(res2Frame,
                      textvariable=self.vResPV[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l3.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsPV.append(tk.StringVar())
        self.vTempsPV[1].set("temps: ?")
        l4 = tk.Label(res2Frame, textvariable=self.vTempsPV[1],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l4.pack(side=tk.LEFT)
        """
        l0c = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0c.pack(side = tk.TOP)     
        """
        # frame per agrupar info resultats
        res3Frame = tk.Frame(self.controlsFrame)
        res3Frame.pack(side=tk.TOP)
        # etiqueta amb resultat linies
        self.vResPV.append(tk.StringVar())
        self.vResPV[2].set("Cierre Visual: ?" )
        l5 = tk.Label(res3Frame,
                      textvariable=self.vResPV[2],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l5.pack(side=tk.LEFT)
        # etiqueta amb resultats de temps de resposta
        self.vTempsPV.append(tk.StringVar())
        self.vTempsPV[2].set("temps: ?")
        l6 = tk.Label(res3Frame, textvariable=self.vTempsPV[2],
                      padx=10, pady=10, font=('Helvetica', fontSizeC1))
        l6.pack(side=tk.LEFT)
        """
        l0a = tk.Label(self.controlsFrame,
                      text="________________", font=('Helvetica', fontSizeC1))
        l0a.pack(side = tk.TOP)     
        """

        # test --------------------------------------
        self.updateTestFrame()
        self.testFrame.update()
        # quan faig aquest get la mida es 1 si no poso el update abans
        self.canvas_width = self.testFrame.winfo_width()
        self.canvas_height = self.testFrame.winfo_height()
        self.testCanvas = tk.Canvas(self.testFrame,
                                    width=self.canvas_width,
                                    height=self.canvas_height,
                                    bg=self.backgroundColor)
        self.testCanvas.pack()
        self.drawTestPV()
        

# Generem GUI
master = tk.Tk()

master.title('Movilab / Experiments')
master.bind_all('<KeyPress>', kp)
master.protocol("WM_DELETE_WINDOW", on_closing)

# mostra imatge a pantalla completa, sense barra meu
# master.attributes('-fullscreen',True)
# mostra a una mida fixe
master.geometry('%dx%d' % (wMonitorRes, hMonitorRes*0.9))
# mostra a una mida maxima / depen de la mida de la pantalla
# no es el mateix que maximitzar des del botó de windows però casi
# m = master.maxsize()
# master.geometry('{}x{}+0+0'.format(*m))


# w = Label(master,text="Hello, wold!")
# w.pack()

iAV = tk.IntVar()

app = App(master)

master.mainloop()
# master.destroy()
