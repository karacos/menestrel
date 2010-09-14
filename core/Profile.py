'''
Created on 13 janv. 2010

@author: nico
'''

import KaraCos

class Profile(KaraCos.Db.Resource):
    '''
    Basic profile for lambda user
    '''


    def __init__(self,parent=None,base=None,data=None):
        KaraCos.Db.Resource.__init__(self,parent=parent,base=base,data=data)
        

    @staticmethod
    def create(parent=None, base=None,data=None, owner=None):
        assert isinstance(data,dict)
        assert isinstance(parent.__domain__, KaraCos.Db.MDomain)
        #assert isinstance(person, KaraCos.Db.Person)
        if 'WebType' not in data:
            data['WebType'] = 'Profile'
        #data['person_id'] = person.id
        #data['person_db'] = person.parent.base.id
        return KaraCos.Db.Resource.create(parent=parent,base=base,data=data,owner=owner)#person.parent)
    
