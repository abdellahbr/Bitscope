# -*- coding: utf-8 -*-

from bitlib import *

MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM") # défini les mode de capture
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND") # défini les sources du bitscope
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
    def Help(self,info = "g"):
        for i in range(len(info)):
            self.sub_Help(str(info[i]))
            
            
    def sub_Help(self,Cara):
        if Cara=="g":
            message = "La fonction d'aide prend plusieurs paramètre qu'il convient de passer en paramètre. "
            message = message + "Ces paramètres sont des lettres sensible à la casse. \n\n"
            message = message + "\"d\"\t-->\t Extrait de la dataSheet du btscope\n\n"
            message = message + "\"\""
            print message

        if Cara =="d":
            message = "Valeur critique extraite de la datasheet à ne pas dépasser :\n\n"
            message = message + "Fréquence d'échantillonnage max : 20 MHz\n"
            message = message + "Tension d'entrée max : 5 V\n"
            message = message + "Mémoire tampon : 12 Ko\n"
            message = message + "Impédence des entrées analogique : 1 MOhm (+- 1%) , 1pF\n"
            message = message + "Impédance des entrées logiques : 100 KOhm (+- 1%), 10pF\n"
            message = message + "Niveau des entrées logiques : 3.3 / 5 V CMOS (compatible TTL)\n"
            message = message + "Sensibilité maximal : 5 mV (<1 MHz)\n"
            message = message + "Sensibilité entré analogique : 20 mV (bande complète)\n"
            message = message + "Fréquence d'affichage : 50 Hz(20 ms)\n"
            message = message + "\n"
            print message
