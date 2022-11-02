#!/usr/bin/env python 
# -*- coding: cp1252 -*-
#   Edited by LKolding
import tkinter as tk

BOX_WIDTH = 36

class ScrollBox(tk.Frame): 
    def __init__(self, elements: list = None, master: tk.Tk = None, x= True, y=True):
        '''frame with a scrollable listbox'''
        tk.Frame.__init__(self, master)
        self.elements: list = elements
        self.grid()
        self.createWidgets(x = x, y= y)
        
    def createWidgets(self, x=True, y=True):
        if y:
            self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
            self.yScroll.grid(row=0, column=1, sticky=tk.NW+tk.S)
        if x:
            self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
            self.xScroll.grid(row=1, column=0, sticky=tk.E+tk.W)
            
        if x and y: self.listbox = tk.Listbox(self, width=BOX_WIDTH,yscrollcommand=self.yScroll.set, xscrollcommand=self.xScroll.set)
        elif y: self.listbox = tk.Listbox(self, width=BOX_WIDTH,yscrollcommand=self.yScroll.set)
        elif x: self.listbox = tk.Listbox(self, width=BOX_WIDTH,xscrollcommand=self.xScroll.set)
        
        if self.elements is None: self.listbox.insert(tk.END,"NO DOINKS")
        else: self.listbox.insert(tk.END,*self.elements)
        
        self.listbox.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        if x: self.xScroll['command'] = self.listbox.xview
        if y: self.yScroll['command'] = self.listbox.yview