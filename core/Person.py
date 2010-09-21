'''
Created on 13 janv. 2010

@author: nico
'''


'''
Created on 13 janv. 2010

@author: nico
'''

import karacos

class Person(karacos.db['Node']):
    '''
    Object used to store person relative data (personal info, address, etc...)
    '''


    def __init__(self,parent=None,base=None,data=None):
        assert isinstance(parent,karacos.db['User']), "parent must be of type User"
        karacos.db['Node'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(user=None, base=None,data=None):
        assert isinstance(data,dict)
        assert isinstance(user, karacos.db['User'])
        if 'type' not in data:
            data['type'] = 'Person'
        return karacos.db['Node'].create(parent=user,base=base,data=data)