from Acquisition import*

Acq = Acquisition("A",20)
Acq.setDuration(0.02)
Acq.Enregistrer()

Acq.Infos()
Acq.DisplayAcq()
Acq.DisplayTime()
