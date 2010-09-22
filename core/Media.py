'''
Created on 13 janv. 2010

@author: nico
'''
import karacos

class Media(karacos.db['Resource']):
    '''
    Basic resource
    '''
    def __init__(self,parent=None,base=None,data=None):
        assert isinstance(parent.__domain__,karacos.db['MDomain']), "domain in not type TzDomain"
        karacos.db['Resource'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'Media'
        return karacos.db['Resource'].create(parent=parent,base=base,data=data)
    
    @karacos._db.isaction
    def add_media_file(self, att_file=None):
        #att_file.filename = "media"
        result = self._add_attachment(att_file)
        self['media'] = att_file.filename
        self.save()
        self.__media_name__ = self['media']
        #return result
    
    @karacos._db.isaction
    def _media(self):
        if '__media_name__' not in dir(self):
            if 'media' not in self:
                raise karacos.http.NotFound(message=_("Ressource 'Media' introuvable"))
            else:
                self.__media_name__ = self['media']
        self._serve_att(self.__media_name__)
        
    add_media_file.form = {'title': _("Add media file"),
         'submit': _('Upload'),
         'fields': [{'name':'att_file', 'title':'Fichier','dataType': 'FILE'}]}