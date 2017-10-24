from Acquisition import *

aqc = Acquisition(300,"A")
aqc.Enregistrer()
for i in range(len(aqc.DATA)):
	print DATA[i] + " ; "

