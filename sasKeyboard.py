from keyboardPeNet import *

rdp1 = DynaPeNet()
rdp1.loadPIPEFile('sas.pipe.csv')
print(rdp1)

rdp1.setInEvent("Arrivée d", KeyboardEvent('d'))
rdp1.setInEvent("Arrivée g", KeyboardEvent('g'))
rdp1.setInEvent("Validation", KeyboardEvent('v'))

rdp1.setOutEvent("Entrée SAS d->g", StdoutDisplayEvent("Entrée dans SAS d->g"))
rdp1.setOutEvent("Entrée SAS g->d", StdoutDisplayEvent("Entrée dans SAS g->d"))

rdp1.setOutEvent("Permut d-g", StdoutDisplayEvent("Permutation sens d->g"))
rdp1.setOutEvent("Permut g-d", StdoutDisplayEvent("Permutation sens SAS g->d"))

rdp1.setOutEvent("Validation", StdoutDisplayEvent("Validation faite !"))

rdp1.setOutEvent("sortie SAS d->g", StdoutDisplayEvent("Sortie du SAS d->g"))
rdp1.setOutEvent("sortie SAS g->d", StdoutDisplayEvent("Sortie du SAS g->d"))

l = Listener(on_press=on_press, on_release=on_release)
l.start()
rdp1.run()
l.stop()

