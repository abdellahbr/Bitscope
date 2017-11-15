from Acquisition import*
from pylab import*

Acq = Acquisition("A",5000)
Acq.setRate(1000000)
Acq.setMode("DUAL")
Acq.Enregistrer()

Acq.Infos()
plt.plot(Acq.TIME, Acq.DATA)
plt.show()
