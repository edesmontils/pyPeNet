#!/usr/bin/env python3.7
# coding: utf8

""" Bibliothèque pour représenter les Réseaux de Pétri (RdP) à exécuter. """

from pyPeNet import *
import argparse

import time


# ==================================================
# ==================================================
# ==================================================


class Event(object):
    """ Classe type pour les évnements produits ou récupérés par le RdP. """
    def __init__(self):
        super(Event, self).__init__()

    def declencher(self) :
        """ Méthode appelée lorsque l'événement est exécuté. """
        pass
# ==================================================
# OUT
# ==================================================


class OutEvent(Event):
    """ Classe représentant un événement "produit" par une transition. """
    def __init__(self):
        super(OutEvent, self).__init__()

# ==================================================

class DisplayEvent(OutEvent):
    """ Classe permettant l'affichage d'informations """
    def __init__(self):
        super(DisplayEvent, self).__init__()


class StdoutDisplayEvent(DisplayEvent):
    """
        Classe permettant l'affichage d'un texte sur la sortie standard.

        Parameters
        ----------
        cdc : str
            La chaine à afficher (None par défaut)
    """
    def __init__(self, cdc=None):
        super(StdoutDisplayEvent, self).__init__()
        self.cdc = cdc
        """ Chaine de caractères à afficher : str """

    def declencher(self) :
        """ Affiche la chaine sur la sortie standard """
        print(self.cdc)

# ==================================================
# IN
# ==================================================


class InEvent(Event):
    """ Classe représentant un événement "en entrée", permettant de déclencher une transition. """
    def __init__(self):
        super(InEvent, self).__init__()

    def estDeclenchable(self) :
        """
            Méthode permettant de déterminer si un événement est arrivé.

            Returns
            -------
            boolean 
                True si l'événement est arrivé, False sinon
        """
        return False

# ==================================================
# ==================================================
# ==================================================


class DynaPeNet(PeNet_I):
    """ Classe permettant d'exécuter un RdP """
    def __init__(self):
        PeNet_I.__init__(self)
        self.F_In = [list() for i in range(self.nbt)]
        """ Liste des événements en entrée associés à chaque transition : list(`InEvent`) """
        self.F_Out = [list() for i in range(self.nbt)]
        """ Liste des événements en sortie associés à chaque transition : list(`OutEvent`) """

    def _eventsBuilding(self, FI = None, FO = None):
        if FI == None :
            self.F_In = [list() for i in range(self.nbt)]
        else:
            self.F_In = FI
        assert self.nbt == len(self.F_In), "[load] incohérence entre F_In et T"
        if FO == None :
            self.F_Out = [list() for i in range(self.nbt)]
        else:
            self.F_Out = FO
        assert self.nbt == len(self.F_Out), "[load] incohérence entre F_Out et T"

    def load(self, P, T, A, W, M0, FI = None, FO = None):
        super().load(P, T, A, W, M0)
        self._eventsBuilding()

    def loadCSVFile(self, f) :
        ok = super().loadCSVFile(f)
        print(ok)
        if ok :
            self._eventsBuilding()
            return True
        else: 
            print('pb')
            return False

    def setInEvent(self, t, inEvt) :
        """ 
            Attribue un événement en entrée à une transition 

            Parameters
            ----------
            t : int
                La transition à laquelle l'événement est rattaché
            inEvt : InEvent
                L'événement rattaché
        """
        assert isinstance(inEvt, InEvent), "[setInEvent] mauvais type d'event"
        if t in self.T:
            i = self.T.index(t)
            self.F_In[i].append(inEvt)
        else:
            pass

    def setOutEvent(self, t, outEvt):
        """ 
            Attribue un événement en entrée à une transition 

            Parameters
            ----------
            t : int
                La transition à laquelle l'événement est rattaché
            outEvt : OutEvent
                L'événement rattaché
        """
        assert isinstance(outEvt, OutEvent), "[setOutEvent] mauvais type d'event"
        if t in self.T:
            i = self.T.index(t)
            self.F_Out[i].append(outEvt)
        else:
            pass

    def _estDeclenchable(self, t):
        dec = super()._estDeclenchable(t)
        la = self.F_In[t]
        if dec and (la != []) :
            for a in la :
                if isinstance(a, InEvent) :
                    dec = dec and a.estDeclenchable()            
        return dec

    def _declencher(self, t):
        super()._declencher(t)
        la = self.F_In[t]
        if la != None :
            for a in la :
                if isinstance(a, InEvent) :
                    a.declencher()
        la = self.F_Out[t]
        if la != None :
            for a in la :
                if isinstance(a, OutEvent) :
                    a.declencher()

    def run(self,delay=1):
        """
            Lance l'exécution du RdP. L'arrêt s'effectue par un Ctrl-C

            Parameters
            ----------
            delay : int
                temporisation entre deux déclenchement de transition (en secondes)
        """
        t = -1
        try:
            while(1):
                t = self.next()
                time.sleep(delay)
        except KeyboardInterrupt:
            print("Fin du RdP par interruption clavier")
        finally:
            print(self.Mi)
            print(self.v_count)


# ==================================================
# ==================================================
# ==================================================


if __name__ == '__main__':

    # rdp2 = DynaPeNet()
    # rdp2.load(("p0","p1", "p2"), ("t0","t1", "t2"), 
    #           (("t0","p0"),("p0","t1"), ("p1", "t1"), ("t1", "p2"), ("p2", "t2")),
    #           (1, 1, 1, 1, 1),
    #           (0, 2, 0))
    # rdp2.setOutEvent("t0", StdoutDisplayEvent("====> new c !"))
    # rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 go !"))
    # rdp2.setOutEvent("t1", StdoutDisplayEvent("T1 gone !"))
    # rdp2.setOutEvent("t2", StdoutDisplayEvent("T2 go !"))
    # rdp2.run()

    parser = argparse.ArgumentParser(description='pyDynaPeNet')
    parser.add_argument("-f", "--file", default='', dest="file", help="Nom du fichier CSV contenant le RdP")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("-a", "--aleatoire", action="store_true")
    group.add_argument("-pf", "--plusfrequent", action="store_true")
    group.add_argument("-mf", "--moinsfrequent", action="store_true")
    group.add_argument("-pr", "--plusrecent", action="store_true")
    group.add_argument("-mr", "--moinsrecent", action="store_true")
    group.add_argument("-pp", "--plusprioritaire", action="store_true")
    group.add_argument("-mp", "--moinsprioritaire", action="store_true")

    args = parser.parse_args()

    rdp1 = DynaPeNet()
    if rdp1.loadCSVFile(args.file) :

        if args.aleatoire :
            rdp1.init(mode=PeNet.ALEATOIRE)
        elif args.plusfrequent :
            rdp1.init(mode=PeNet.MODE_PLUSFREQUENT)
        elif args.moinsfrequent :
            rdp1.init(mode=PeNet.MODE_MOINSFREQUENT)
        elif args.plusrecent :
            rdp1.init(mode=PeNet.MODE_PLUSRECENT)
        elif args.moinsrecent :
            rdp1.init(mode=PeNet.MODE_MOINSRECENT)
        elif args.plusprioritaire :
            rdp1.init(mode=PeNet.MODE_PLUSPRIORITAIRE)
        elif args.moinsprioritaire :
            rdp1.init(mode=PeNet.MODE_MOINSPRIORITAIRE)
        else:
            rdp1.init()


        print(rdp1)
        rdp1.run()

