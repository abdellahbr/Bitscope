# -*- coding: utf-8 -*-

from bitlib import*
from pylab import*

MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM") # défini les mode de capture
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND") # défini les sources du bitscope
TRUE = 1

class RTAcquisition:

    """ Classe RTAcquisition : elle défini un objet permettant de réaliser des acquisition de signaux
en temps réel. Elle prendra comme attribut de classe :
            - Une voie d'acquisition
            - Un mode [OPTIONAL (default = "FAST")]
            - Fréquence de rafraichissment [OPTIONAL (default = max)]"""

    def __init__(self,voie,Mode="FAST",Percistant = false, Refresh = 20000000):
        BL_Open("",1)
        self.SELECT = BL_Select(BLSELECT_SELECT_DEVICE,0)
        self.REFRESH_TIME = 1/Refresh
        self.REFRESH_FREQ = Refresh
        self.DATA = 0
        self.MY_MODE = BL_MODE_FAST # on initialise la variable
        if Mode!="FAST":
            self.setMode(Mode) # on défini le mode sur le mode rentré
        if Voie.upper() != "A" and Voie.upper()!= "B" and Voie!=0 and Voie!=1:
             print("ERREUR DE SAISIE DE VOIX: ENTRER A OU B") # gestion d'erreur
	if Voie.upper() == "A" or Voie==0:
		self.MY_CHANNEL =0
	if Voie.upper()=="B" or Voie==1:
		self.MY_CHANNEL=1
        

    def setMode(self,NewMode):
        NewMode=NewMode.upper()
        if NewMode!="FAST" and NewMode!="DUAL" and NewMode!="MIXED" and NewMode!="LOGIC" and NewMode!="STREAM":
            print "ERREUR ---> mode innexistant ou non pris en charge"
        else:
            if NewMode=="FAST":
                self.MY_MODE = BL_MODE_FAST
            if NewMode=="DUAL":
                self.MY_MODE = BL_MODE_DUAL
            if NewMode=="MIXED":
                self.MY_MODE = BL_MODE_MIXED
            if NewMode=="LOGIC":
                self.MY_MODE = BL_MODE_LOGIC
            if NewMode=="STREAM":
                self.MY_MODE = BL_MODE_STREAM

    def Infos(self):
        """ Information sur la session d'acquisition """
        print "=============== INFOS ===============\n\n"
        print "-------------- hardware -------------\n"
        print "Port de connection : %s" %BL_Name(0)
        print "version du Bitscope : %s (%s)" %(BL_Version(BL_VERSION_DEVICE),BL_ID())
        print "Canaux : %d (%d analogiques(s) + %d logique(s))" %(BL_Count(
            BL_COUNT_ANALOG)+BL_Count(BL_COUNT_LOGIC),
            BL_Count(BL_COUNT_ANALOG),BL_Count(BL_COUNT_LOGIC))       
        if BL_Offset(-1000) != BL_Offset(1000):
            print "Offset: %+.4gV to %+.4gV" % (
                BL_Offset(1000), BL_Offset(-1000))
        
        print "\n-------------------------------------\n"0Méch/s
        print "\n------------- software --------------\n"
        print "Nombre de points : %s" %(self.MY_SIZE)
        print "Fréquence d'échantillonage : %s Hz" %(self.MY_RATE)
        print "durée entre deux points : %s s" %(1./self.MY_RATE)
        print "Durée de l'acquisition : %s s" %(BL_Time())
        print "Mode d'acquisition : %s" %(MODES[self.MY_MODE])
        print "-------------------------------------\n"
        print "\n====================================="


    def Start(self):
        """ déclaration des variable de l'aqcuisition, création des Thread
et lancement de ce dernier pour la visualisation en continu"""

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

        # TODO création des thread et lancement affichage

    def Enregistrer(self):
        BL_Trace()
        if BL_State()!=BL_STATE_DONE:  # on regarde si le bitscope est près
            break
        else:
            
