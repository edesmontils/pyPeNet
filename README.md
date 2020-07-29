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
- MODE_MOINSPRIORITAIRE : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables les moins prioritaires ;
- MODE_PLUSPRIORITAIRE : la transition déclenchée est choisie aléatoirement parmi les transitions déclenchables les plus prioritaires.

## Récupérer un RdP construit avec PIPE 

Transformer le fichier XML PIPE (http://pipe2.sourceforge.net/) en CSV :
``
xsltproc PIPE2CSV.xsl ex_PIPEa.xml > ex_PIPEa.csv
``

On obtient alors :
```
name;type;v1;v2;v3
P0;place;10;;
P1;place;0;;
P2;place;0;;
P3;place;4;;
P4;place;0;;
T0;transition;1;;
T1;transition;1;;
T2;transition;1;;
T3;transition;1;;
T4;transition;1;;
P0 to T0;normal;P0;T0;1
P1 to T1;normal;P1;T1;1
P1 to T3;normal;P1;T3;1
P2 to T2;normal;P2;T2;1
P3 to T1;normal;P3;T1;1
P4 to T2;inhibitor;P4;T2;
P4 to T4;normal;P4;T4;2
T0 to P1;normal;T0;P1;1
T0 to P4;normal;T0;P4;1
T1 to P2;normal;T1;P2;1
T2 to P1;normal;T2;P1;1
T2 to P3;normal;T2;P3;1
T3 to P4;normal;T3;P4;1
T4 to P0;normal;T4;P0;1
```



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
