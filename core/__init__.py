"""
Core tools for Menestrel
abstraction layer for couchdb
"""

import karacos
from Resource import Resource
from MDomain import MDomain
from Person import Person
from Profile import Profile
from Comment import Comment
from EntriesHolder import EntriesHolder
from Newsletter import Newsletter
from Entry import Entry
from Tag import Tag
from Media import Media
from MDMessage import MDMessage
from CommentWfItem import CommentWfItem

#from wrapper import Server, Resource
#import couchdb
#from MenestrelObject import MenestrelObject
#from BaseObject import BaseObject
import sys
class MenestrelException(Exception):
    """
    Base exception class for Menestrel
    """
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)
    