#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) classiques.
    TODO :
    - ...
"""
import numpy as np
import random
from lxml import etree
import os

#==================================================
#============ Tools ===============================
#==================================================

def existFile(f):
    return os.path.isfile(f)

def existDir(d):
    return os.path.exists(d)

# ==================================================
# ==================================================
# ==================================================


def choixAleatoire(lde, cpt, seq) :
    #print('--> aleatoire :',lde)
    if len(lde) == 1 :
        return lde[0]
    else :
        return random.choice(lde)

def choixPFreq(lde, cpt, seq) :
    c = [ lde[0] ]
    nb = cpt[lde[0]]
    for t in lde[1:] :
        if nb < cpt[t]:
            nb = cpt[t]
            c = [t]
        elif nb == cpt[t]:
            c.append(t)
    return choixAleatoire(c, cpt, seq)

def choixMFreq(lde, cpt, seq) :
    c = [ lde[0] ]
    nb = cpt[lde[0]]
    for t in lde[1:] :
        if nb > cpt[t]:
            nb = cpt[t]
            c = [t]
        elif nb == cpt[t]:
            c.append(t)
    return choixAleatoire(c, cpt, seq)

def choixPRecent(lde, cpt, seq) :
    l = len(seq)
    if l ==0 :
        return choixAleatoire(lde, cpt, seq)
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
        return choixAleatoire(c, cpt, seq) 

def choixMRecent(lde, cpt, seq) :
    l = len(seq)
    if l == 0 :
        return choixAleatoire(lde, cpt, seq)
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
        return choixAleatoire(c, cpt, seq) 

class PeNet(object):
    """ RdP de base """

    MODE_ALEATOIRE = choixAleatoire
    MODE_PLUSFREQUENT = choixPFreq
    MODE_MOINSFREQUENT = choixMFreq
    MODE_PLUSRECENT = choixPRecent
    MODE_MOINSRECENT = choixMRecent

    def __init__(self):
        self.P = list()
        self.nbp = 0
        self.T = list()
        self.nbt = 0
        self.A = list()
        self.nba = 0
        self.W = list()
        self.M0 = None
        self.Mi = None
        self.Us = None  # U+
        self.Ue = None  # U-
        self.U = None  # U
        self.v_count = None
        self.lastT = None

        self.choix = self.MODE_ALEATOIRE
        self.sequence=list()

    def __str__(self):
        return [str(p) for p in self.P]

    def setU(self):
        ls = list()
        le = list()
        for p in self.P:
            lps = list()
            lpe = list()
            for t in self.T:
                ws = 0
                we = 0
                for (i, (source, cible)) in enumerate(self.A):
                    if cible == p and source == t:
                        ws = self.W[i]
                    elif cible == t and source == p:
                        we = self.W[i]
                lps.append(ws)
                lpe.append(we)
            ls.append(lps)
            le.append(lpe)

        self.Us = np.array(ls, dtype=int)
        self.Ue = np.array(le, dtype=int)
        self.U = self.Us - self.Ue  # U = U+ - U-

        self.UeT = self.Ue.transpose()
        self.UsT = self.Us.transpose()
        self.UT = self.U.transpose()

    def EquationEtat(self, v):
        assert isinstance(v, np.ndarray), "[EquationEtat] Pb v (1)"
        n = np.shape(v)
        assert len(n) == 1, "[EquationEtat] Pb v (2)"
        assert n[0] == len(self.T), "[EquationEtat] Pb v (3)"

        M = self.M0.transpose() + self.U.dot(v.transpose())
        return M.transpose()

    def load(self, P, T, A, W, M0):
        self.nbp = len(P)
        self.P = list(P)
        self.nbt = len(T)
        self.T = list(T)
        self.nba = len(A)
        self.A = list(A)

        assert self.nba == len(W), "[load] incohérence entre A et W"
        assert self.nbp == len(M0), "[load] incohérence entre P et M0"

        self.W = list(W)
        self.M0 = np.array(list(M0))
        self.init()

    def loadPIPEFile(self, f : str) -> None :
        if existFile(f) :
            XMLparser = etree.XMLParser(recover=True, strip_cdata=True)
            tree = etree.parse(f, XMLparser)
            self.P = list()
            M0 = list()
            for p in tree.getroot().iter('place'):
                self.P.append(p.get('id'))
                contains = p[2][0].text.split(',')[1]
                M0.append(int(contains))
            self.nbp = len(self.P)
            self.M0 = np.array(list(M0))

            self.T = list()
            for t in tree.getroot().iter('transition'):
                self.T.append(t.get('id'))
            self.nbt = len(self.T)

            self.W = list()
            self.A = list()
            for a in tree.getroot().iter('arc'):
                source = a.get('source')
                target = a.get('target')
                w = a[1][0].text
                atype = a[-1].get('value')
                if (w is not None) and (atype == 'normal') :
                    w = w.split(',')[1]
                    self.W.append(int(w))
                elif (w is None) and (atype == 'inhibitor') :
                    self.W.append(0)
                else :
                    self.W.append(1)
                self.A.append( (source,target) )
            self.nba = len(self.A)

            self.init()
        else:
            pass

    def init(self, mode : int = MODE_ALEATOIRE) -> None :
        self.Mi = self.M0.copy()
        self.v_count = np.zeros(len(self.T), dtype=int)
        self.sequence = list()
        self.choix = mode
        self.lastT = None
        self.setU()

    def setMi(self, m : np.ndarray) -> None :
        assert isinstance(m, np.ndarray), "[setMi] Pb m (1)"
        v = np.shape(m)
        assert len(v) == 1, "[setMi] Pb m (2)"
        assert v[0] == len(self.P), "[setMi] Pb m (3)"

        self.Mi = m

    def estDeclanchable(self, t):
        return (self.UeT[t] <= self.Mi).all()

    def declancher(self, t):
        self.v_count[t] += 1
        self.Mi = self.Mi + self.UT[t]

    def next(self):
        lDeclanchables = list()
        for t in range(self.nbt):
            if self.estDeclanchable(t):
                lDeclanchables.append(t)

        if len(lDeclanchables) > 0:
            t = self.choix(lDeclanchables, self.v_count, self.sequence)
            print(lDeclanchables, self.v_count, self.sequence)
            self.declancher(t)
            self.sequence.append(t)

            assert (self.Mi == self.EquationEtat(
                self.v_count)).all(), "[next] pb d'exécution"
            self.lastT = t
            return t
        else:
            return None

# ==================================================
# ==================================================
# ==================================================


class PeNet_I(PeNet):
    """ RdP avec arcs inhibiteurs possibles """

    def __init__(self):
        #super(PeNet, self).__init__()
        PeNet.__init__(self)
        self.I = list()

    def setInhibitorMatrix(self) :
        self.I = list()
        li = list()
        for p in self.P:
            lpi = list()
            for t in self.T:
                w = 0
                for (i, (source, cible)) in enumerate(self.A):
                    if cible == t and source == p and self.W[i] == 0:
                        w = 1
                        break
                lpi.append(w)
            li.append(lpi)

        self.I = np.array(li, dtype=int)
        self.IT = self.I.transpose()


    def load(self, P, T, A, W, M0):
        super().load(P, T, A, W, M0)
        self.setInhibitorMatrix()

    def loadPIPEFile(self, f : str) -> None :
        super().loadPIPEFile(f)
        self.setInhibitorMatrix()

    def estDeclanchable(self, t):
        ok = True
        for p in range(self.nbp):
            if self.IT[t][p] == 0:
                ok = ok and (self.UeT[t][p] <= self.Mi[p])
            else:
                ok = ok and (self.Mi[p] == 0)

        return ok


# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    rdp2 = PeNet_I()
    rdp2.load(("p1", "p2"), ("t1", "t2", "t3"), (("p1", "t1"), ("t1", "p2"),
                                                 ("p2", "t2"), ("t2", "p1"), ("p1", "t2"), ("t3", "p2")), (1, 1, 1, 1, 0, 1),  (1, 1))

    print(rdp2.M0)
    print(rdp2.Ue)
    print(rdp2.Us)
    print(rdp2.U)
    rdp2.init(mode=PeNet.MODE_MOINSFREQUENT)
    for i in range(15):
        rdp2.next()
        print(rdp2.lastT, '->', rdp2.Mi)
    print("Comptage:" + str(rdp2.v_count))
    print(rdp2.I)

    rdp2.loadPIPEFile('ex_PIPEa.xml')
    print(rdp2.M0)
    print(rdp2.Ue)
    print(rdp2.Us)
    print(rdp2.U)
    print(rdp2.I)