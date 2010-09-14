'''
Created on 13 janv. 2010

@author: nico
'''


'''
Created on 13 janv. 2010

@author: nico
'''

import KaraCos
_ = KaraCos._
class Person(KaraCos.Db.Node):
    '''
    Object used to store person relative data (personal info, address, etc...)
    '''


    def __init__(self,parent=None,base=None,data=None):
        assert isinstance(parent,KaraCos.Db.User), "parent must be of type User"
        KaraCos.Db.Node.__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(user=None, base=None,data=None,owner=None):
        assert isinstance(data,dict)
        assert isinstance(user, KaraCos.Db.User)
        if 'WebType' not in data:
            data['WebType'] = 'Person'
        if 'type' not in data:
            data['type'] = 'Person'
        return KaraCos.Db.WebNode.create(parent=user,base=base,data=data,owner=user)