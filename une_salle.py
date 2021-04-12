from keyboardPeNet import *

rdp1 = DynaPeNet()
rdp1.loadPIPEFile('une_salle.csv')
rdp1.init(mode=PeNet.MODE_MOINSFREQUENT)
print(rdp1)

rdp1.setOutEvent("entrée", StdoutDisplayEvent("Un étudiant entre dans la salle"))
rdp1.setOutEvent("sortie", StdoutDisplayEvent("Un étudiant sort de la salle"))

rdp1.setOutEvent("T0", StdoutDisplayEvent("Un étudiant entre dans le forum"))
rdp1.setOutEvent("T1", StdoutDisplayEvent("Un étudiant sort du forum"))

rdp1.run()

