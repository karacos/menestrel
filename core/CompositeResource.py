'''
Created on 27 nov. 2010

@author: nico
'''

import sys
import karacos

class CompositeResource(karacos.db['Resource']):
    """
    Multi_content resource
    """
    
    def __init__(self,parent=None,base=None,data=None):
        karacos.db['Resource'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None):
        return karacos.db['Resource'].create(parent=parent,base=base,data=data)
    
    def __get_content__(self,cid=None):
        """
        param cid is content id in object
        """
        content_id = "content"
        if cid != None:
            if 'content_%s' % cid in self:
                return self['content_%s' % cid]
        return "<p>No content found</p>"
    
    def _get_edit_content_form(self):
        form={'title':  _("Edit content multi"),
              'submit':'modifier',
                'fields':[
                    {'name':'title', 'title':_('title'), 'dataType': 'TEXT', 'value': user['CUSTOM_SITE_SKIN']},
                    {'name':'CUSTOM_SITE_BASE', 'title':_('Skin de site'), 'dataType': 'TEXT', 'value': user['CUSTOM_SITE_BASE']}
                        ]
                }
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,*args, **kw):
        """
        """
        for k,v in kw:
            if k in self:
                self[k] = v
        self.save()
    
    