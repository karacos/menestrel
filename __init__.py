'''
Created on 19 nov. 2009

@author: nico
'''
import os, sys
import core
import karacos
#Exception = core.MenestrelException

class Root():
    def __init__(self):
        self.menestrel = karacos.apps['menestrel']
        #KaraCos.Apps['menestrel'].core._init()