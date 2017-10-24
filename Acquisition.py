
from bitlib import *

MODES = ("FAST","DUAL","MIXED","LOGIC","STREAM") # défini les mode de capture
SOURCES = ("POD","BNC","X10","X20","X50","ALT","GND") # défini les sources du bitscope


class Acquisition:
    """ Classe Acquisition : elle défini un objet permettant d'acquérir un signal
avec le bitscoepe. elle prend comme attribut de classe :
        - une voie d'acquisition
        - un nombre de points à capturer"""

    def __init__(self, NbPoints, Voie):
        self.MY_SIZE = NbPoints
        if Voie != "A" and Voie!= "B":
             print("ERREUR DE SAISIE DE VOIX: ENTRER A OU B") # gestion d'erreur
        self.MY_CHANNEL = Voie
        self.CONNECT = BL_Open("",0) # si 1 : connecté
                                    # si 0 : pas connecté

    def __del__(self):
        """ destructeur de la classe """
        self.CONNECT = BL_Close()
        

    def Infos(self):
        """ Information sur la session d'acquisition """
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


    def Enregistrer():
        """ Méthode permettant d'enregistrer suivant les paramètre de l'instance
en cour"""   
