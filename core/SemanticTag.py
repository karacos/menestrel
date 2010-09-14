'''
Created on 18 août 2010

@author: nico
'''
import KaraCos
_ = KaraCos._

class SemanticTag(KaraCos.Db.Resource):
    """
    Represents a meaning keyword, ca be associated to any resource
    """
    
    def __init__(self,parent=None,base=None,data=None):
        KaraCos.Db.Resource.__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None,owner=None):
        if 'WebType' not in data:
            data['WebType'] = 'SemanticTag'
        return KaraCos.Db.Resource.create(parent=parent,base=base,data=data,owner=owner)