
from bitlib import *

MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM") # défini les mode de capture
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND") # défini les sources du bitscope
TRUE = 1 

class Acquisition:
    """ Classe Acquisition : elle défini un objet permettant d'acquérir un signal
avec le bitscoepe. elle prend comme attribut de classe :
        - une voie d'acquisition
        - un nombre de points à capturer"""

    def __init__(self, NbPoints, Voie):
        print "Recherche de votre matériel ... "
        self.MY_SIZE = NbPoints
	self.DATA = [0]*self.MY_SIZE
        if Voie != "A" and Voie!= "B":
             print("ERREUR DE SAISIE DE VOIX: ENTRER A OU B") # gestion d'erreur
	if Voie == "A":
		self.MY_CHANNEL =0
	if Voie=="B":
		self.MY_CHANNEL=1
        self.CONNECT = BL_Open("",0) # si 1 : connecté
                                    # si 0 : pas connecté
	self.MY_MODE = BL_MODE_FAST
	self.MY_RATE = 1000000
	BL_Mode(self.MY_MODE)
	BL_Intro(BL_ZERO)
	BL_Delay(BL_ZERO)
	BL_Rate(self.MY_RATE)
	BL_Size(self.MY_SIZE)
	BL_Select(BL_SELECT_CHANNEL, self.MY_SIZE)
	BL_Trigger(BL_ZERO,BL_TRIG_RISE)
	BL_Select(BL_SELECT_SOURCE,BL_SOURCE_POD)
	BL_Range(BL_Count(BL_COUNT_RANGE))
	BL_Offset(BL_ZERO)
        BL_Enable(TRUE)
        print "Matériel détecté ! (%s)" %BL_Name(0)

    def __del__(self):
        """ destructeur de la classe """
        self.CONNECT = BL_Close()
        

    def Infos(self):
        """ Information sur la session d'acquisition """
        print "-------------- INFOS -------------\n"
        print "Port de connection : %s" %BL_Name(0)
        print "version du Bitscope : %s (%s)" %(BL_Version(BL_VERSION_DEVICE),BL_ID())
        print "Canales : %d (%d analogiques(s) + %d logique(s))" %(BL_Count(
            BL_COUNT_ANALOG)+BL_Count(BL_COUNT_LOGIC),
            BL_Count(BL_COUNT_ANALOG),BL_Count(BL_COUNT_LOGIC))
        print " Capture: %d @ %.0fHz = %fs (%s)" % (
            BL_Size(),BL_Rate(),
            BL_Time(),MODES[BL_Mode()])
        BL_Range(BL_Count(BL_COUNT_RANGE));
        if BL_Offset(-1000) != BL_Offset(1000):
            print "  Offset: %+.4gV to %+.4gV" % (
                BL_Offset(1000), BL_Offset(-1000))
        print "\n--------------------------------"

    def Enregistrer(self):
        """ Méthode permettant d'enregistrer suivant les paramètre de l'instance
en cour"""   
	BL_Trace()
	self.DATA = BL_Acquire()

    def DisplayAcq(self):
        """Renvoi les valeur aquise par l'instance de la classe en cours """
        print "------------- DATA --------------\n\n"
        print "\t" .join(["%f" % self.DATA[i] for i in range (len(self.DATA))])
        print "\n--------------------------------"

