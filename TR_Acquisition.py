from bitlib import *
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
import threading

TRUE = 1

class TR_Acquisition:

    # Constructeur
    def __init__(self, Voie,NbPoints,Rate): 

        print "Recherche de votre materiel ... "
	BL_Open("",1)
	self.SELECT = BL_Select(BL_SELECT_DEVICE,0)
        self.MY_SIZE = NbPoints
        self.MY_MODE = BL_MODE_FAST
        self.DATA = [0]*self.MY_SIZE
	if Voie == "A" or Voie=="a" or Voie==0:
            self.MY_CHANNEL =0
	if Voie=="B" or Voie=="b" or Voie==1:
	    self.MY_CHANNEL=1
        self.MY_RATE = Rate
        print "Materiel detecte ! (%s)" %BL_Name(0)

    #Destructeur
    def __del__(self):

        BL_Close()

    # Obtenir donnees

    def Acquisition(self):

        BL_Mode(self.MY_MODE)
	BL_Intro(BL_ZERO)
	BL_Delay(BL_ZERO)
	BL_Rate(self.MY_RATE)
	BL_Size(self.MY_SIZE)
	BL_Select(self.MY_CHANNEL, self.MY_SIZE)
	BL_Trigger(BL_ZERO,BL_TRIG_RISE)
	BL_Select(BL_SELECT_SOURCE,BL_SOURCE_POD)
	BL_Range(BL_Count(BL_COUNT_RANGE))
	BL_Offset(BL_ZERO)
        BL_Enable(TRUE)
        BL_Trace()
        self.DATA = BL_Acquire()

    # Boucle Acquisition temps reel
    def tr_plot(self):

        if BL_State()== BL_STATE_DONE:
            
            # Definition du graphe
            fig = plt.figure()
            ax = fig.add_subplot(111)
            # Premiere Acquisition
            self.Acquisition()
            x = np.arange(-self.MY_SIZE,0)
            y = self.DATA
            li, = ax.plot(x, y)
            ax.relim() 
            ax.autoscale_view(True,True,True)
            fig.canvas.draw()
            plt.show(block=False)

            # Boucle temps reel
            while True:
                try:
                    if BL_State()== BL_STATE_DONE:
                        self.Acquisition
                        y[:-self.MY_SIZE] = y[self.MY_SIZE:]
                        y[-self.MY_SIZE:] = self.DATA

                        # Inserer nouvelles donnees
                        li.set_ydata(y)
                        fig.canvas.draw()
                        time.sleep(0.01)
                except KeyboardInterrupt:
                    break
        # Gestion de multithreading
    def run(self):
        acquisition_thread = threading.Thread(target = self.tr_plot)
        acquisition_thread.daemon = True
        acquisition_thread.start()
        print 'Acquisition en cours...'
        # Arreter thread
        while True:
            if raw_input() == 'stop':
                print 'Acquisition terrminee'
                sys.exit()
