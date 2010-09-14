'''
Created on 13 janv. 2010

@author: nico
'''
import cherrypy
import KaraCos
_ = KaraCos._
class Media(KaraCos.Db.Resource):
    '''
    Basic resource
    '''
    def __init__(self,parent=None,base=None,data=None):
        assert isinstance(parent.__domain__,KaraCos.Db.MDomain), "domain in not type TzDomain"
        KaraCos.Db.Resource.__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None,owner=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'Media'
        return KaraCos.Db.Resource.create(parent=parent,base=base,data=data,owner=owner)
    
    @KaraCos._Db.isaction
    def add_media_file(self, att_file=None):
        #att_file.filename = "media"
        if '__media_name__' in self:
            self.parent.db.delete_attachment(self,self.__media_name__)
        result = self._add_attachment(att_file)
        self['media'] = att_file.filename
        self.save()
        self.__media_name__ = self['media']
        #return result
    
    @KaraCos.expose
    def _media(self):
        if '__media_name__' not in self.__dict__:
            if 'media' not in self:
                raise cherrypy.HTTPError(status=404,message=_("Ressource introuvable"))
            else:
                self.__media_name__ = self['media']
        if '_attachments' in self:
            if self.__media_name__ in self['_attachments']:
                res = self.parent.db.get_attachment(self.id, self.__media_name__)
                response = cherrypy.response
                response.headers['Content-Type'] = self['_attachments'][self.__media_name__]['content_type']
                response.headers['Content-Length'] = self['_attachments'][self.__media_name__]['length']
                response.body = res
                return response.body
        raise cherrypy.HTTPError(status=404,message=_("Ressource introuvable"))
        
        
    add_media_file.form = {'title': _("Add media file"),
         'submit': _('Upload'),
         'fields': [{'name':'att_file', 'title':'Fichier','dataType': 'FILE'}]}