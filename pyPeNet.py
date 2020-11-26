#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) classiques.
"""

import random

#from lxml import etree
#from xml.dom.minidom import Node, Element, parse, parseString

import os
import csv

#==================================================
#============ Tools ===============================
#==================================================

def _existFile(f):
    return os.path.isfile(f)

def _existDir(d):
    return os.path.exists(d)

# pour ne pas utiliser numpy...

def _setIntMatrix(l,c):
    return [ [0] * c for i in range(l) ]

def _transposeIntMatrix(m) :
    l = len(m)
    c = len(m[0])
    n = _setIntMatrix(c,l)
    for i in range(l) :
        for j in range(c) :
            n[j][i] = m[i][j]
    return n

def _diffIntMatrix(m,n) :
    l = len(m)
    c = len(m[0])
    d = _setIntMatrix(l, c)
    for i in range(l):
        for j in range(c) :
            d[i][j] = m[i][j]-n[i][j]
    return d

def _setIntVector(n):
    return [0]*n

def _copyIntVector(v):
    l = len(v)
    w = [0]*l
    for i in range(l):
        w[i] = v[i]
    return v

def _addVector(v,w) :
    l = len(v)
    z = [0]*l
    for i in range(l):
        z[i] = v[i] + w[i]
    return z


# ==================================================
# ==================================================
# ==================================================

def _choixAleatoire(lde, cpt, seq, pr) :
    #print('--> aleatoire :',lde)
    if len(lde) == 1 :
        return lde[0]
    else :
        return random.choice(lde)

def _choixPFreq(lde, cpt, seq, pr) :
    c = [ lde[0] ]
    nb = cpt[lde[0]]
    for t in lde[1:] :
        if nb < cpt[t]:
            nb = cpt[t]
            c = [t]
        elif nb == cpt[t]:
            c.append(t)
    return _choixAleatoire(c, cpt, seq, pr)

def _choixMFreq(lde, cpt, seq, pr) :
    c = [ lde[0] ]
    nb = cpt[lde[0]]
    for t in lde[1:] :
        if nb > cpt[t]:
            nb = cpt[t]
            c = [t]
        elif nb == cpt[t]:
            c.append(t)
    return _choixAleatoire(c, cpt, seq, pr)

def _choixPPrio(lde, cpt, seq, pr) :
    c = [ lde[0] ]
    nb = pr[lde[0]]
    for t in lde[1:] :
        if nb < pr[t]:
            nb = pr[t]
            c = [t]
        elif nb == pr[t]:
            c.append(t)
    return _choixAleatoire(c, cpt, seq, pr)

def _choixMPrio(lde, cpt, seq, pr) :
    c = [ lde[0] ]
    nb = pr[lde[0]]
    for t in lde[1:] :
        if nb > pr[t]:
            nb = pr[t]
            c = [t]
        elif nb == pr[t]:
            c.append(t)
    return __choixAleatoire(c, cpt, seq, pr)

def _choixPRecent(lde, cpt, seq, pr) :
    l = len(seq)
    if l ==0 :
        return _choixAleatoire(lde, cpt, seq, pr)
    else :
        seqR = seq[::-1]
        t = lde[0]
        c = [ t ]
        #print('c:',c)
        if t in seqR: 
            nb = seqR.index(t)
        else: nb = l

        for t in lde[1:] :
            if t in seqR:
                i = seqR.index(t)
            else: i = l
            if nb > i:
                nb = i
                c = [t]
            elif  nb == i: 
                c.append(t) 
        return _choixAleatoire(c, cpt, seq, pr) 

def _choixMRecent(lde, cpt, seq, pr) :
    l = len(seq)
    if l == 0 :
        return _choixAleatoire(lde, cpt, seq, pr)
    else :
        seqR = seq[::-1]

        t = lde[0]
        c = [t]
        if t in seqR: 
            nb = seqR.index(t)
        else: nb = l
        for t in lde[1:] :
            if t in seqR:
                i = seqR.index(t)
            else: i = l
            if nb < i:
                nb = i
                c = [t]
            else : 
                if nb == i:
                    c.append(t)    
        return _choixAleatoire(c, cpt, seq, pr) 

# ==================================================
# ==================================================
# ==================================================

class PeNet(object):
    """ 
        Description d'un RdP de base 

        Attributes
        ----------
        P : list(str)
            Liste des places
        T : list(str)
            Liste des transitions
        Pr : list(int)
            Priorité des transitions
        A : list(str)
            Liste des arcs
        W : list(str)
            poids des arcs
        M0 : list(int)
            Marquage initial
        Mi : list(int)
            Marquage courant
    """

    MODE_ALEATOIRE = _choixAleatoire
    MODE_PLUSFREQUENT = _choixPFreq
    MODE_MOINSFREQUENT = _choixMFreq
    MODE_PLUSRECENT = _choixPRecent
    MODE_MOINSRECENT = _choixMRecent
    MODE_PLUSPRIORITAIRE = _choixPPrio
    MODE_MOINSPRIORITAIRE = _choixMPrio

    def __init__(self):
        self.P = list() # liste des places
        self.nbp = 0 # nombre de places
        self.T = list() # liste des transitions
        self.nbt = 0 # nombre de transitions
        self.A = list() # liste des arcs
        self.nba = 0 # nombre d'arcs
        self.W = list() # poids des arcs
        self.M0 = None # marquage initial
        self.Mi = None # marquage courant
        self.Us = None  # U+
        self.Ue = None  # U-
        self.U = None  # U
        self.v_count = None # vecteur de comptage
        self.lastT = None # dernière transition empruntée
        self.Pr = None # priorité des transitions

        self._choix = self.MODE_ALEATOIRE
        self.sequence=list()

    def __str__(self):
        return "\n".join([ ", ".join([str(i)+'/'+str(p)+'/'+str(self.M0[i]) for (i,p) in enumerate(self.P)]), 
                           ", ".join([str(i)+'/'+str(t)+'/'+str(self.Pr[i]) for (i,t) in enumerate(self.T)]),
                           ", ".join([str(i)+'/'+str(a)+'/'+str(self.W[i])  for (i,a) in enumerate(self.A)]) ])

    def _setU(self):
        self.Us = _setIntMatrix(self.nbp,self.nbt) 
        self.Ue = _setIntMatrix(self.nbp,self.nbt)

        for (i,p) in enumerate(self.P):
            for (j,t) in enumerate(self.T):
                ws = 0
                we = 0
                for (k, (source, cible)) in enumerate(self.A):
                    if cible == p and source == t:
                        ws = self.W[k]
                    elif cible == t and source == p:
                        we = self.W[k]
                self.Us[i][j]=ws
                self.Ue[i][j]=we

        self.U = _diffIntMatrix(self.Us, self.Ue)  # U = U+ - U-

        self.UeT = _transposeIntMatrix(self.Ue)
        self.UsT = _transposeIntMatrix(self.Us)
        self.UT = _transposeIntMatrix(self.U)

    def load(self, P, T, A, W, M0):
        """
            Chargement d'un RdP décrit par ses différents ensembles

            Parameters
            ----------
            P : list(str)
                Liste des places
            T : list(str)
                Liste des transitions
            A : list(str)
                Liste des arcs
            W : list(str)
                poids des arcs
            M0 : list(int)
                Marquage initial
        """
        self.nbp = len(P)
        self.P = list(P)
        self.nbt = len(T)
        self.T = list(T)
        self.nba = len(A)
        self.A = list(A)
        self.Pr = [1]*self.nbt
        assert self.nba == len(W), "[load] incohérence entre A et W"
        assert self.nbp == len(M0), "[load] incohérence entre P et M0"

        self.W = list(W)
        self.M0 = list(M0)
        self.init()

    def loadPIPEFile(self, f) :
        """
            Chargement d'un RdP décrit dans un fichier CSV

            Parameters
            ----------
            f : str
                Nom du fichier CSV

            .. warning:: Méthode dépréciée -> utiliser `PeNet.loadCSVFile`
        """
        self.loadCSVFile(f)

    def loadCSVFile(self, f) :
        """
            Chargement d'un RdP décrit dans un fichier CSV

            Parameters
            ----------
            f : str
                Nom du fichier CSV

            Notes
            -----
            CSV exemple :  \n
            name;type;v1;v2;v3 \n
            P0;place;10;; \n
            P1;place;0;; \n
            P2;place;0;; \n
            P3;place;4;; \n
            P4;place;0;; \n
            T0;transition;1;; \n
            T1;transition;1;; \n
            T2;transition;1;; \n
            T3;transition;1;; \n
            T4;transition;1;; \n
            P0 to T0;normal;P0;T0;1 \n
            P1 to T1;normal;P1;T1;1 \n
            P1 to T3;normal;P1;T3;1 \n
            P2 to T2;normal;P2;T2;1 \n
            P3 to T1;normal;P3;T1;1 \n
            P4 to T4;normal;P4;T4;2 \n
            T0 to P1;normal;T0;P1;1 \n
            T0 to P4;normal;T0;P4;1 \n
            T1 to P2;normal;T1;P2;1 \n
            T2 to P1;normal;T2;P1;1 \n
            T2 to P3;normal;T2;P3;1 \n
            T3 to P4;normal;T3;P4;1 \n
            T4 to P0;normal;T4;P0;1

        """
        if _existFile(f) :
            self.P = list()
            self.M0 = list()
            self.T = list()
            self.Pr = list()
            self.W = list()
            self.A = list()
            with open(f, newline='') as csvfile:
                rdp = csv.DictReader(csvfile, delimiter=';')
                for row in rdp:
                    typeNode = row['type']
                    if typeNode == 'place' :
                        self.P.append(row['name'])
                        self.M0.append(int(row['v1'])) # contenu de la place dans le marquage initial
                    
                    elif typeNode == 'transition' :
                        self.T.append(row['name'])
                        self.Pr.append(int(row['v1'])) # priorité de la transition

                    elif typeNode == 'normal' :
                        source = row['v1']
                        target = row['v2']
                        w = row['v3']
                        self.W.append(int(w))
                        self.A.append( (source,target) )

                    elif typeNode == 'inhibitor' :
                        source = row['v1']
                        target = row['v2']                        
                        self.W.append(0)
                        self.A.append( (source,target) )

                self.nbt = len(self.T)
                self.nba = len(self.A)
                self.nbp = len(self.P)
                self.init()
                print('File loaded')
                return True
        else :
            print('File ',f,' doesn''t exist')
            return False

    def loadXMLPIPEFile(self, f : str) -> None :
        """
            Chargement d'un RdP décrit dans un fichier XML au format de l'application PIPE.

            .. warning:: méthode à implémenter

            Parameters
            ----------
            f : str
                Nom du fichier XML
        """
        if _existFile(f) :
            pass
            # XMLparser = etree.XMLParser(recover=True, strip_cdata=True)
            # tree = etree.parse(f, XMLparser)
            # self.P = list()
            # M0 = list()
            # for p in tree.getroot().iter('place'):
            #     self.P.append(p.get('id'))
            #     contains = p[2][0].text.split(',')[1]
            #     M0.append(int(contains))
            # self.nbp = len(self.P)
            # self.M0 = list(M0)

            # self.T = list()
            # for t in tree.getroot().iter('transition'):
            #     self.T.append(t.get('id'))
            # self.nbt = len(self.T)

            # self.W = list()
            # self.A = list()
            # for a in tree.getroot().iter('arc'):
            #     source = a.get('source')
            #     target = a.get('target')
            #     w = a[1][0].text
            #     atype = a[-1].get('value')
            #     if (w is not None) and (atype == 'normal') :
            #         w = w.split(',')[1]
            #         self.W.append(int(w))
            #     elif (w is None) and (atype == 'inhibitor') :
            #         self.W.append(0)
            #     else :
            #         self.W.append(1)
            #     self.A.append( (source,target) )
            # self.nba = len(self.A)

            # self.init()
        else:
            pass

    def init(self, mode : int = MODE_ALEATOIRE) -> None :
        """
            Initialise le RdP pour une exécution. 
            Il est possible de spécifier la stratégie de choix des transitions déclenchables.

            Parameters
            ----------
            mode : {MODE_ALEATOIRE, MODE_PLUSFREQUENT, MODE_MOINSFREQUENT, MODE_PLUSRECENT, MODE_MOINSRECENT, MODE_PLUSPRIORITAIRE, MODE_MOINSPRIORITAIRE}, optional
                Mode de choix à sélectionner (MODE_ALEATOIRE par défaut)
        """
        self.Mi = _copyIntVector(self.M0)
        self.v_count = [0]*self.nbt
        self.sequence = list()
        self._choix = mode
        self.lastT = None
        self._setU()
        print('M0:',self.Mi, ' ; Pr:', self.Pr)


    def setM0(self, m : list ) -> None :
        """
            Modification du mrquage initial

            Parameters
            ----------
            m : list(int)
                Nouvelles valeurs pour les différentes places
        """
        assert isinstance(m, list), "[setM0] Pb m (1)"
        self.Mi = _copyIntVector(m)

    def _estDeclenchable(self, t):
        ok = True
        for p in range(self.nbp):
            if self.UeT[t][p] > 0 : ok = ok and (self.UeT[t][p] <= self.Mi[p])
        return ok

    def _declencher(self, t):
        self.v_count[t] += 1
        self.Mi = _addVector(self.Mi, self.UT[t])

    def next(self):
        """
            Permet d'avancer d'une étape dans l'exécution du RdP
        """
        lDeclenchables = list()
        for t in range(self.nbt):
            if self._estDeclenchable(t):
                lDeclenchables.append(t)

        if len(lDeclenchables) > 0:
            t = self._choix(lDeclenchables, self.v_count, self.sequence, self.Pr)
            self._declencher(t)
            self.sequence.append(t)
            self.lastT = t
            print(lDeclenchables,  ' -> ', t, '/',self.T[t], ' Mi:',self.Mi, ' count:', self.v_count)
            return t
        else:
            return None

# ==================================================
# ==================================================
# ==================================================


class PeNet_I(PeNet):
    """ RdP avec arcs inhibiteurs possibles. Les arcs inhibiteurs sont identifiés par un poids de 0. """

    def __init__(self):
        PeNet.__init__(self)
        self.I = list()

    def _setInhibitorMatrix(self) :
        self.I = _setIntMatrix(self.nbp,self.nbt)
        for (i,p) in enumerate(self.P):
            for (j,t) in enumerate(self.T):
                w = 0
                for (k, (source, cible)) in enumerate(self.A):
                    if cible == t and source == p and self.W[k] == 0:
                        w = 1
                        break
                self.I[i][j] = w

        self.IT = _transposeIntMatrix(self.I)
        print('I:',self.I)


    def load(self, P, T, A, W, M0):
        super().load(P, T, A, W, M0)
        self._setInhibitorMatrix()

    def loadPIPEFile(self, f) :
        ok = super().loadPIPEFile(f)
        if ok :
            self._setInhibitorMatrix()
        return ok

    def loadXMLPIPEFile(self, f) :
        ok = super().loadXMLPIPEFile(f)
        if ok :
            self._setInhibitorMatrix()
        return ok

    def _estDeclenchable(self, t):
        ok = True
        for p in range(self.nbp):
            if self.IT[t][p] == 0:
                if self.UeT[t][p] > 0 : ok = ok and (self.UeT[t][p] <= self.Mi[p])
            else:
                ok = ok and (self.Mi[p] == 0)

        return ok


# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    rdp2 = PeNet_I()
    rdp2.load(("p1", "p2"), ("t1", "t2", "t3"), (("p1", "t1"), ("t1", "p2"),
                                                 ("p2", "t2"), ("t2", "p1"), ("p1", "t2"), ("t3", "p2")),
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
   

    rdp2.loadPIPEFile('ex_PIPEa.csv')
    print(rdp2.M0)
    print(rdp2.Ue)
    print(rdp2.Us)
    print(rdp2.U)
    print(rdp2.I)
    print(rdp2)