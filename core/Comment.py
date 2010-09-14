'''
Created on 13 janv. 2010

@author: nico
'''

import karacos

class Comment(karacos.db['Resource']):
    '''
    Basic resource
    '''


    def __init__(self,parent=None,base=None,data=None):
        assert isinstance(parent,karacos.db['Resource'])
        karacos.db['Resource'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None,owner=None):
        assert isinstance(data,dict)
        if 'status' not in data:
            data['status'] = 'public'
        if 'WebType' not in data:
            data['WebType'] = 'Comment'
        result = karacos.db['Resource'].create(parent=parent,base=base,data=data,owner=owner)
        staffgrpname = 'group.staff@%s' % result.__domain__['name']
        if staffgrpname not in result['ACL']:
            result['ACL'][staffgrpname] = []
        if "index" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("index")
        if "w_browse" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("w_browse")
        if "get_user_actions_forms" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("get_user_actions_forms")
        if "moderate" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("moderate")
        if "edit_content" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("edit_content")
        if "add_comment" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("add_comment")
        if "validate_comment" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("validate_comment")
        if "delete_comment" not in result['ACL'][staffgrpname]:
            result['ACL'][staffgrpname].append("delete")
        #anonid = 'user.anonymous@%s' % result.__domain__['name']
        #result['ACL'][anonid].append("add_comment")
        result.save()
        return result
    
    def __get_workflow_item__(self):
        """
        """
        result = False
        manager = self.__domain__.get_manager_node()
        if manager.workflow_exist_for_node(self.base.id,self.id):
            result = manager.get_workflow_item_for_node(self.base.id,self.id)
        return result
    
    def _delete(self):
        wfitem = self.__get_workflow_item__()
        if wfitem:
            assert isinstance(wfitem,karacos.db['CommentWfItem'])
            wfitem._delete()
        karacos.db['Node']._delete(self)
        
    @karacos._db.isaction
    def delete(self):
        self._delete()
        
    def _moderate(self,status=''):
        wfitem = self.__get_workflow_item__()
        wfitem._update_item()
        if wfitem:
            assert isinstance(wfitem,KaraCos.Db.CommentWfItem)
            wfitem['status'] = 'read'
            wfitem['active'] = False
            if 'log' not in wfitem:
                wfitem['log'] = []
            wfitem['log'].append(("moderate",status))
            wfitem.save()
        self['status'] = status
        self.save()
        
    @karacos._db.isaction
    def moderate(self,status=''):
        """
        Moderate comment, giving status other than public hides public display of this resource.
        """
        self._moderate(status)
        return {'status':'success', 'message':_("Contenu modere"),'data':{}}
    
    def _validate_comment(self):
        self._publish_node()
        self['status'] = "public"
        self.save()
        self.__domain__._update_item()
        
        wfitem = self.__get_workflow_item__()
        if wfitem:
            assert isinstance(wfitem,karacos.db['CommentWfItem'])
            wfitem['status'] = 'read'
            wfitem['active'] = False
            if 'log' not in wfitem:
                wfitem['log'] = []
            wfitem['log'].append("Validate comment")
            wfitem.save()
            
    @karacos._db.isaction
    def validate_comment(self):
        self._validate_comment()
        return {'status':'success', 'message':_("Contenu valide"),'data':{}}

    def _get_edit_content_form(self):
        self._update_item()
        if 'comment' not in self:
            self['comment'] = ''
        self.save()
        form = {'title':'Modifier le commentaire',
                'submit':'Modifier',
                'fields':[
                    {'name':'comment', 'title':_('Commentaire'), 'dataType': 'TEXT', 'formType': 'WYSIWYG', 'value': self['comment']}
                        ]}
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,comment=None):
        """
        Basic content modification for Resource
        """
        self._update_item()
        self['comment'] = comment
        self.save()
        return {'status':'success', 'message':_("Contenu modifi&eacute;"),'data':{}}
    edit_content.get_form = _get_edit_content_form
    edit_content.label = _('Modifier la page')