# pyPeNet
Petri's Net for education 

## Construire un RdP et l'exécuter pas à pas

Avec pyPeNet :
```
rdp2 = PeNet_I()
rdp2.load(("p1", "p2"), ("t1", "t2", "t3"), 
          (("p1", "t1"), ("t1", "p2"), ("p2", "t2"), ("t2", "p1"), ("p1",  "t2"), ("t3", "p2")),
          (1, 1, 1, 1, 0, 1),
          (1, 1))

print(rdp2.M0)
print(rdp2.Ue)
print(rdp2.Us)
print(rdp2.U)
print(rdp2.I)
rdp2.init(mode=PeNet.MODE_MOINSFREQUENT)
for i in range(15):
    rdp2.next()
    print(rdp2.lastT, '->', rdp2.Mi)
print("Comptage:" + str(rdp2.v_count))
```

Il est possible de modifier le comportement du moteur d'exécution :
- MODE_ALEATOIRE (par défaut) : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables ;
- MODE_MOINSFREQUENT : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables les moins souvent utilisées ;
- MODE_PLUSFREQUENT : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables les plus souvent utilisées ;
- MODE_PLUSRECENT : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables les plus récemment utilisées ;
- MODE_MOINSRECENT : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables les plus anciennement utilisées ;

## Récupérer un RdP construit avec PIPE 

Transformer le fichier XML en CSV :
``
xsltproc PIPE2CSV.xsl ex_PIPEa.xml > ex_PIPEa.csv
``

Puis, avec pyPeNet, le charger :
```
rdp2 = PeNet_I()
rdp2.loadPIPEFile('ex_PIPEa.csv')
print(rdp2.M0)
print(rdp2.Ue)
print(rdp2.Us)
print(rdp2.U)
print(rdp2.I)
```

## Jouer un RdP avec des sorties écran

Avec pyDynaPeNet, Ctrl-C pour arrêter :
```
rdp2 = DynaPeNet()
rdp2.load(("p0","p1", "p2"), ("t0","t1", "t2"), 
            (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"), ("p2", "t2")),
            (1, 1, 1, 1, 1),
            (0, 2, 0))
rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
rdp2.run()
```

## Jouer un RdP avec des entrées clavier

Avec keyboardPeNet :
```
rdp2 = DynaPeNet()
rdp2.load(("p0","p1", "p2"), ("t0","t1", "t2"), 
            (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"), ("p2", "t2")),
            (1, 1, 1, 1, 1),  (0, 2, 0))
rdp2.setInEvent("t0", KeyboardEvent('c'))
rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
l = Listener(on_press=on_press, on_release=on_release)
l.start()
rdp2.run()
l.stop()
```


[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/edesmontils/pyPeNet.git/master)
