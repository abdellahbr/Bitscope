from Acquisition import*
from pylab import*

Acq = Acquisition("A",5000)
Acq.setRate(1000000)
Acq.setMode("FAST")
Acq.Enregistrer()

Acq.Infos()
plot(Acq.TIME, Acq.DATA)
show()

