#!/usr/bin/env python3.6
# coding: utf8


class Place(object):
    def __init__(self, name):
        self.name = name


class Transition(object):
    def __init__(self, name):
        self.name = name


class Arc(object):
    def __init__(self, place, arc, poids=1):
        pass
