'''
Created on 13 janv. 2010

@author: nico
'''


'''
Created on 13 janv. 2010

@author: nico
'''

import KaraCos

class Tag(KaraCos.Db.Resource):
    '''
    Basic resource
    '''


    def __init__(self,parent=None,base=None,data=None,domain=None):
        assert isinstance(domain,KaraCos.Db.Domain), "domain in not type Domain"
        KaraCos.Db.Resource.__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None,owner=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'Tag'
        return KaraCos.Db.Resource.create(parent=parent,base=base,data=data,owner=owner)
    
    