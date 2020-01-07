#!/usr/bin/env python3.7
# coding: utf8

"""
    Bibliothèque pour représenter les Réseaux de Pétri (RdP) classiques.
    TODO :
    - gérer les arcs hinibiteurs
"""
import pprint
import numpy as np
import random


class PeNet(object):
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
        self.v_count = np.zeros(self.nbt, dtype=int)

        self.init()

    def init(self):
        self.Mi = self.M0.copy()
        self.v_count = np.zeros(len(self.T), dtype=int)
        self.setU()

    def setMi(self, m):
        assert isinstance(m, np.ndarray), "[setMi] Pb m (1)"
        v = np.shape(m)
        assert len(v) == 1, "[setMi] Pb m (2)"
        assert v[0] == len(self.P), "[setMi] Pb m (3)"

        self.Mi = m

    def estDeclanchable(self, t):
        ok = True
        for p in range(self.nbp):
            ok = ok and (self.UeT[t][p] <= self.Mi[p])
        return ok

    def declancher(self, t):
        self.v_count[t] += 1
        for p in range(self.nbp):
            self.Mi[p] += self.UT[t][p]

    def next(self):
        lDeclanchables = list()
        for t in range(self.nbt):
            if self.estDeclanchable(t):
                lDeclanchables.append(t)
                
        if len(lDeclanchables) > 0:
            t = random.choice(lDeclanchables)
            self.declancher(t)

            assert (self.Mi == self.EquationEtat(
                self.v_count)).all(), "[next] pb d'exécution"
            return t
        else:
            return None


# ==================================================
# ==================================================
# ==================================================
if __name__ == '__main__':
    print('main de pyPeNet.py')
    pp = pprint.PrettyPrinter(indent=4)

    rdp2 = PeNet()
    rdp2.load(("p1", "p2"), ("t1", "t2"), (("p1", "t1"), ("t1", "p2"),
                                           ("p2", "t2"), ("t2", "p1")), (1, 1, 1, 1),  (1, 1))

    print(rdp2.Mi)
    print(rdp2.Ue)
    print(rdp2.Us)
    print(rdp2.U)
    for i in range(15):
        rdp2.next()
        print(rdp2.Mi)
    print("Comptage:" + str(rdp2.v_count))
