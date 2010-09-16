'''
Created on 13 janv. 2010

@author: nico
'''

import karacos

class Profile(karacos.db['Resource']):
    '''
    Basic profile for lambda user
    '''


    def __init__(self,parent=None,base=None,data=None):
        karacos.db['Resource'].__init__(self,parent=parent,base=base,data=data)
        

    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        assert isinstance(parent.__domain__, karacos.db['MDomain'])
        #assert isinstance(person, KaraCos.Db.Person)
        if 'WebType' not in data:
            data['WebType'] = 'Profile'
        #data['person_id'] = person.id
        #data['person_db'] = person.parent.base.id
        return karacos.db['Resource'].create(parent=parent,base=base,data=data)#person.parent)
    
