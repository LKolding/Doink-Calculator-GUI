#!/usr/bin/env python 
# -*- coding: cp1252 -*-
import tkinter as tk

class ScrollBox(tk.Frame): 
    def __init__(self, elements: list = None, master: tk.Tk = None):
        '''Literally just a frame with a scrollable listbox'''
        tk.Frame.__init__(self, master)
        self.elements: list = elements
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        self.yScroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yScroll.grid(row=0, column=1, sticky=tk.NW+tk.S)
        self.xScroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=1, column=0, sticky=tk.E+tk.W)
        
        self.listbox = tk.Listbox(self, width=32,xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set)
        self.listbox.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        if self.elements is None: self.listbox.insert(tk.END,"NO DOINKS")
        else: self.listbox.insert(tk.END,*self.elements)
        self.xScroll['command'] = self.listbox.xview
        self.yScroll['command'] = self.listbox.yview