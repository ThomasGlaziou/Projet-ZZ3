# -*- coding: utf-8 -*-

import copy

class Element(object):
    """ element in the list """
    def __init__(self,v):
        """ """
        self.__val = v
        self.next = None
        self.prec = None

    @property
    def value(self): return self.__val
    @value.setter
    def value(self,v):
        self.__val = v

        
from tkinter import *
from PIL import Image

class History(object):
    
    """ create doubly linked list """

    compteur = 0

    def __init__(self):

        self.first = None
        self.last = None
        self.__class__.compteur += 0

    def add(self,val):
        """add an element"""
        cell=Element(copy.deepcopy(val))
        if self.first is None:    
            self.first = self.last = cell
        else:
            self.last.next = cell
            cell.prec = self.last 
            self.last=cell


    def empty(self):
        """ clear the history """
        self.first=self.last = None

    def undo(self):
        """ """
        val = None
        if not self.isEmpty() and self.last.prec is not None:
            self.last = self.last.prec
            val = copy.deepcopy(self.last.value)
            
        return val
    
    def redo(self):
        """ """
        val = None
        print(self.last.next)
        if not self.isEmpty() and self.last.next is not None:
            self.last = self.last.next
            val = copy.deepcopy(self.last.value)
        return val
    
    def isEmpty(self):
        return self.last is None
            
        
