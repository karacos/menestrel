'''
Created on 13 janv. 2010

@author: nico
'''

import karacos
class Entry(karacos.db['Resource']):
    '''
    Basic Entry resource
    '''


    def __init__(self,parent=None,base=None,data=None,domain=None):
        assert isinstance(parent,karacos.db['EntriesHolder']), "parent in not type EntriesHolder"
        karacos.db['Resource'].__init__(self,parent=parent,base=base,data=data)
        if 'status' not in self:
            self['status'] = 'edition'
        
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'Entry'
        result = karacos.db['Resource'].create(parent=parent,base=base,data=data)
        result.log.info("Create for me ok")
        if 'group.staff@%s' % result.__domain__['name'] not in result['ACL']:
            result['ACL']['group.staff@%s' % result.__domain__['name']] = []
        result['ACL']['group.staff@%s' % result.__domain__['name']].append("edit_content")
        result['ACL']['group.staff@%s' % result.__domain__['name']].append("publish")
        result['ACL']['group.staff@%s' % result.__domain__['name']].append("delete")
        result.save()
        return result
    
    def _get_edit_content_form(self):
        self._update_item()
        if 'content' not in self:
            self['content'] = ''
        if 'title' not in self:
            self['title'] = ''
        self.save()
        form = {'title':'Modifier le message',
                'submit':'Modifier',
                'fields':[
                    {'name':'title', 'title':_('Titre'), 'dataType': 'TEXT', 'value': self['title']},
                    {'name':'message', 'title':_('Message'), 'dataType': 'TEXT', 'formType': 'WYSIWYG', 'value': self['message']}
                        ]}
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,title=None,message=None):
        """
        Basic content modification for entry
        """
        self._update_item()
        self['message'] = message
        self['title'] = title
        self.save()
        return {'status':'success', 'message':_("Contenu modifi&eacute;"),'data':{}}
    edit_content.get_form = _get_edit_content_form
    edit_content.label = _('Modifier le message')
    
    @karacos._db.isaction
    def publish(self):
        """
        """
        karacos.db['WebNode']._publish_node(self)
        self['status'] = "published"
        everyone = 'group.everyone@%s' % self.__domain__['name']
        self['ACL'][everyone] = ["get_user_actions_forms","w_browse","index","add_comment","get_comments"]
        self.save()
        self.__parent__._entry_publish(self)
        return {'status':'success', 'message':'Message publie'}
    