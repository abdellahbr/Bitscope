# -*- coding: utf-8 -*-

from bitlib import *

MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM") # défini les mode de capture
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND") # défini les sources du bitscope
METHODES = ("setDuration", "setVoie", "setMode", "Enregistrer", "Infos", "DisplayAcq", "DisplayTime")
TRUE = 1 

class Acquisition:
    """ Classe Acquisition : elle défini un objet permettant d'acquérir un signal
avec le bitscoepe. elle prend comme attribut de classe :
        - une voie d'acquisition
        - un nombre de points à capturer [OPTIONAL (default = 300)]
        - une fréquence d'échantillonnage [OPTIONAL (default = 10000 Hz)]"""

    def __init__(self, Voie,NbPoints=300,Rate=10000): 
        print "Recherche de votre matériel ... "
	BL_Open("",1)
	self.SELECT = BL_Select(BL_SELECT_DEVICE,0)
        self.MY_SIZE = NbPoints
        self.TIME= [0]*self.MY_SIZE
	self.DATA = [0]*self.MY_SIZE
        self.MY_MODE =BL_MODE_FAST # d'après la doc le mode fast doit être appeler avant de choisir la voie
        if Voie.upper() != "A" and Voie.upper()!= "B" and Voie!=0 and Voie!=1:
             print("ERREUR DE SAISIE DE VOIX: ENTRER A OU B") # gestion d'erreur
	if Voie.upper() == "A" or Voie==0:
		self.MY_CHANNEL =0
	if Voie.upper()=="B" or Voie==1:
		self.MY_CHANNEL=1
        
        self.MY_RATE = Rate
        
        # on récupère le temps d'acquisition pour l'objet courant
        self.MY_DURATION=BL_Time()
        print "Matériel détecté ! (%s)\n" %BL_Name(0)


    def __del__(self):
        """ destructeur de la classe """
        BL_Close()
        

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
        
        print "\n-------------------------------------\n"
        print "\n------------- software --------------\n"
        print "Nombre de points : %s" %(self.MY_SIZE)
        print "Fréquence d'échantillonage : %s Hz" %(self.MY_RATE)
        print "durée entre deux points : %s s" %(1./self.MY_RATE)
        print "Durée de l'acquisition : %s s" %(BL_Time())
        print "Mode d'acquisition : %s" %(MODES[self.MY_MODE])
        print "-------------------------------------\n"
        print "\n====================================="

    def Enregistrer(self):
        """ Méthode permettant d'enregistrer suivant les paramètre de l'instance
en cour"""
        # récupération des donnée de l'acquisition

       
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
        if BL_State()!= BL_STATE_DONE:
            print "ERREUR --> Le Bitscope n'est pas près pour l'acquisition"
        else:
	    self.DATA = BL_Acquire()

        # Affectation des valeurs du temps dans le tableau TIME
        time = 0.
        for i in range (self.MY_SIZE):
            self.TIME[i] = time
            time = time + (1./self.MY_RATE)

    def DisplayAcq(self):
        """Renvoi les valeur aquise par l'instance de la classe en cours """
        print "--------------- DATA ----------------\n\n"
        string =""  # initialisation de l'affichage
        string = str(self.DATA[0])
        while len(string)<9:
            string = string + "0"
        string = string + "\t"
        for i in range(1,self.MY_SIZE):
            ToAdd = str(self.DATA[i])
        # Si la chaine de caratère associé à la valeur du tableau est plus petite que 7 alors on ajoute
        # des 0 pour que la tabulation d'affichage réussise à faire un tableau propre
            while len(ToAdd) <9:       
                ToAdd = ToAdd + "0"
            string = string + ToAdd + "\t"
            if (i+1)%5==0:
                print string
                string = ""
        print string
        #print "" .join(["%f\t" % self.DATA[i] for i in range (len(self.DATA))])
        print "\n------------------------------------"


    # Mutateur du temps de d'acquisition
    def setDuration(self, NewDuration):
        # On redéfinira le nombre de point de l'acquisition en conséquence
        self.DURATION = NewDuration        
        if NewDuration/(1./self.MY_RATE)<1:
            print "ERREUR --> La durée d'acquisition est incompatible avec la fréquence d'échantillonnage choisie"
        self.MY_SIZE = int(NewDuration/(1./self.MY_RATE))
        self.DATA = [0] * self.MY_SIZE
        self.TIME = [0] * self.MY_SIZE
    
    # Mutateur du temps d'échantillonnage (les autres données d'acquisition reste inchanger)
    def setRate(self,NewRate):
        self.MY_RATE = NewRate

    
    # Affichage de la matrice des temps assicié à l'enregetristement de l'acquisition
    def DisplayTime(self):
        """Renvoi les valeur du temps d' aquisition par l'instance de la classe en cours """
        print "--------------- TIME ----------------\n\n"
        string =""  # initialisation de l'affichage
        string = str(self.TIME[0])
        while len(string)<9:
            string = string + "0"
        string = string + "\t"
        for i in range(1,self.MY_SIZE):
            ToAdd = str(self.TIME[i])
        # Si la chaine de caratère associé à la valeur du tableau est plus petite que 7 alors on ajoute
        # des 0 pour que la tabulation d'affichage réussise à faire un tableau propre
            while len(ToAdd) <9:       
                ToAdd = ToAdd + "0"
            string = string + ToAdd + "\t"
            if (i+1)%5==0:
                print string
                string = ""
        print string
        #print "" .join(["%f\t" % self.DATA[i] for i in range (len(self.DATA))])
        print "\n------------------------------------"

    # Mutateur du mode d'acquisition

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


    # Mutateur de la voie d'acquisition
    def setVoie(self,NewVoie):
        if NewVoie != "A" and NewVoie!= "B" and NewVoie!="a" and NewVoie!="b" and NewVoie !=0 and NewVoie!=1:
             print("ERREUR DE SAISIE DE VOIX: ENTRER A OU B") # gestion d'erreur
	if NewVoie == "A" or NewVoie == "a" or NewVoie == 0 :
		self.MY_CHANNEL =0
	if NewVoie=="B" or NewVoie=="b" or NewVoie==1:
		self.MY_CHANNEL=1

    
    # Remise à zéro de l'acuisition (donnée et flag)
    def RAZ(self):
        self.DATA = [0]*self.MY_SIZE
        self.TIME = [0]*self.MY_SIZE


###############################################################################

    """ Fonction d'aide permet d'avoir tout les infos sur le bitscope """
    def Help(self,info = "0"):
        if (info in METHODES) == True:
            self.sub_Help(info)
        else:
            for i in range(len(info)):
                self.sub_Help(str(info[i]))

            
    def sub_Help(self,Cara):
        if Cara=="0":
            message = "La fonction d'aide vous permet d'obtenir des informations sur l 'utilisation de votre "
            message = message + "bitscope en ligne de commande. Il vous suffit de passer en paramètre de la "
            message = message + "fonction Help une chaine de caractère contenant l'un ou un ensemble concaténé des caratères suivants :\n\n"
            message = message + "\"d\"\t-->\t Totalité de la dataSheet du btscope\n\n"
            message = message + "\"i\"\t--> Documentation sur les Inputs\n\n"
            message = message + "\"a\"\t--> Documentation sur les Acquisitions\n\n"
            message = message + "\"t\"\t--> Documentation sur les triggers\n\n"
            message = message + "\"g\"\t--> Documentation général sur le bitscope\n\n"
            message = message + "Pour obtenir de l'aide sur une méthode taper "
            message = message + "son nom en paramètre de la fonction help. LA liste des méthodes est données si dessous :\n\n"
            message = message + "SetMode, setVoie, setDuration, Enregistrer, DisplayAcq, DisplayTime, Infos"
            print message

        if Cara =="d":
            self.sub_Help("g")
            self.sub_Help("i")
            self.sub_Help("a")
            self.sub_Help("t")

        if Cara =="i":
            message = "---------- INPUTS ----------\n\n"
            message = message + "Analog Bandwith : 20 MHz\n"
            message = message + "Capture channels : 2 analog + 8 logic\n"
            message = message + "Input Ranges : 1.1 V ~ 11 V\n"
            message = message + "Vertical Scalling : 20 mV/Div ~ 2 V/div\n"
            message = message + "Vertical Acuracy : +- 4% (full scale)\n"
            message = message + "Analog sensitivity : 20 mV (full bandwith)\n"
            message = message + "Maximum sensitivity : 5 mV(<1 MHz)\n"
            message = message + "Protocole capture : UART, SPI and I2C\n"
            message = message + "Input Offsets : Yes (manual only)\n"
            message = message + "Input Sensing : Yes\n"
            message = message + "Adjustable Switching : Yes (D6 and D7)\n"
            message = message + "Analog Input Impedence : 1 MOhms +- 1%, 10 pF\n"
            message = message + "Logic Input Impedence : 100 KOhms +- 1%, 10 pF (logic)\n"
            message = message + "Logic Input levels : 3.3/5 V CMOS (TTL Compatible)\n"
            print message

        if Cara == "a":
            message = "---------- ACQUISITION ----------\n\n"
            message = message + "Real-Time Mixed Signal : Yes\n"
            message = message + "Mixed Signal Streaming : Yes\n"
            message = message + "Macro High Resolution : Yes\n"
            message = message + "Sub-Sampled Analog : No\n"
            message = message + "Protocol Streaming : No\n"
            message = message + "Digital Sample Rate (Max) : 40 MSps (per frame)\n"
            message = message + "Analog Sample Rate (Max) : 20 MSps (per frame)\n"
            message = message + "Streaming Rate (Max) : 200 KSps (continous)\n"
            message = message + "Native Resolution : 8/12 bits(switchable)\n"
            message = message + "12 ENOB (<1 MHz)\n"
            message = message + "Display Frame Rate : 50Hz (20 ms)\n"
            message = message + "Capture Buffers : 12 KS, 6 KS x 2, 6 KS x 9 or 3 KS x 2 + 6 KS x 8\n"
            message = message + "Timerbase Range : 1us/Div ~ 100 ms/Div\n"
            message = message + "Timebase Accuracy : 0.01% (100 ppm)\n"
            print message

        if Cara =="t":
            message = "---------- TRIGGERS ----------\n\n"
            message = message + "Trigger Modes : Edge (Rise/Fall), Level/State & Logic\n"
            message = message + "Hysteresis / Sensitivity : +- 2%\n"
            message = message + "Trigger Filter : Fast, Normal & Delay\n"
            message = message + "Cross-Trigger Ops : Logic trigger analog & vice versa\n"
            message = message + "trigger Delay Timebase : 100 us to 10 s (programmable)\n"
            message = message + "Trigger Hold-Off : 1 ms ~ 100 ms\n"
            print message

        if Cara == "g":
            message = "---------- GENERAL ----------\n\n"
            message = message + "Power requierement : 5 V USB powered\n"
            message = message + "Operating Temperature : -40°C ~ +40°C\n"
            message = message + "Water Resistant : Yes\n"
            message = message + "Dimensions (WxDxH) : 20 x 110 x 8 mm\n"
            message = message + "Weight : 12 g\n"
            print message

        if Cara == "setMode":
            message = "Permet la selection du mode d'aqcuisition de la sonde :\n\n"
            message = message + "FAST --> Acquisition rapide d'une seul voie\n"
            message = message + "DUAL --> Acquisition des deux voie simultanément\n"
            message = message + "MIXED --> Acquisition de sur voie analogique et logique simultanément\n"
            message = message + "LOGIC --> Acquisition sur les voie logiques\n"
            message = message + "STREAM --> Mode pour l'utilisation du logiciel de visualisation fourni avec le Bitscope\n"
            message = message + "\nExemple d'utilisation : Acquisition.setMode(\"FAST\")"
            print message

        if Cara == "setDuration":
            message = "Permet de réglé la durée d'acquisition en seconde. le changement du temps d'acquisition induit un changement automatique du nombre de point (conservation de la fréquence d'échantillonnage)\n"
            print message

        if Cara == "setVoie":
            message = "Permet de choisir la voie d'acquisition si l'aqcuisition n'est pas une acquisition sur voie logique.\n"
            message = message + "\nExemple d'utilisation : Acquisition.setVoie(\"A\")"
            print message

        if Cara == "Enregistrer":
            message = "Permet de lancer l'acquisition préalablement paramétré.\n"
            print message

        if Cara == "DisplayAcq":
            message = "Permet d'afficher le tableau des valeurs acquise dans la console. Si l'acquisition n'a pas été lancée avec Enregistrer, le tableau est initialement rempli de 0\n"
            print message

        if Cara == "DisplayTime":
            message = "Permet d'afficher le tableau des temps d'acquisition dans la console. Si l'acquisition n'a pas été lancée avec Enregistrer, le tableau est initialement rempli de 0\n"
            print message

        if Cara == "Infos":
            message = "Permet d'afficher les informations de configuration de votre Bitscope et de l'acquisition en cours\n"
            print message
