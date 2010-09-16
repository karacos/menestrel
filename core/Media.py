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
        if '__media_name__' in self:
            self.parent.db.delete_attachment(self,self.__media_name__)
        result = self._add_attachment(att_file)
        self['media'] = att_file.filename
        self.save()
        self.__media_name__ = self['media']
        #return result
    
    @karacos._db.isaction
    def _media(self):
        if '__media_name__' not in self.__dict__:
            if 'media' not in self:
                raise karacos.http.NotFound(message=_("Ressource introuvable"))
            else:
                self.__media_name__ = self['media']
        if '_attachments' in self:
            if self.__media_name__ in self['_attachments']:
                res = self.__parent__.db.get_attachment(self.id, self.__media_name__)
                response = karacos.serving.get_response()
                response.headers['Content-Type'] = self['_attachments'][self.__media_name__]['content_type']
                response.headers['Content-Length'] = self['_attachments'][self.__media_name__]['length']
                response.body = "%s" % res.read()
                return
        raise karacos.http.NotFound(message=_("Ressource introuvable"))
        
        
    add_media_file.form = {'title': _("Add media file"),
         'submit': _('Upload'),
         'fields': [{'name':'att_file', 'title':'Fichier','dataType': 'FILE'}]}