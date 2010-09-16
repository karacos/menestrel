

import karacos
class CommentWfItem(karacos.db['WorkFlowItem']):
    """
    Handler for comment validation
    """
    
    def __init__(self,parent=None,base=None,data=None):
        karacos.db['WorkFlowItem'].__init__(self,parent=parent,base=base,data=data)
        base = karacos.db.sysdb[data['ref_db']]
        self.__comment__ = base.db[data['ref_id']]
        self.actions = {'validate': CommentWfItem.validate_comment,
               'moderate': CommentWfItem.moderate_comment,
               'delete': CommentWfItem.delete_comment}
        
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(parent.__domain__, karacos.db['MDomain'])
        assert isinstance(data,dict)
        assert 'ref_db' in data, "Workflow Item must ref item related container db"
        assert 'ref_id' in data, "Workflow Item must ref item related id"
        base = karacos.db.sysdb[data['ref_db']]
        comment = base.db[data['ref_id']]
        assert isinstance(comment,karacos.db['Comment'])
        
        if 'type' not in data:
            data['type'] = 'CommentWfItem'
        if 'status' not in data:
            data['status'] = 'unread'
        result = karacos.db['WorkFlowItem'].create(parent=parent,base=base,data=data)
        return result
    
    def validate_comment(self):
        """
        """
        self.__comment__._validate_comment()
    
    def moderate_comment(self):
        """
        """
        self.__comment__._moderate('moderate')
        
    def delete_comment(self):
        """
        """
        self.__comment__._delete()
        
    
    
    def _get_validation_action(self):
        result = {'title': _("Moderation des commentaires"),
         'submit': _('Envoyer'),
         'fields': [
                    {'name':'comment_action', 'title':'Action','dataType': 'TEXT',
                       'formType':'RADIO', 'values': self.actions.keys()}
                    
                    ]
                    }
        return result
    
    def _get_title(self):
        return "Par %s [%s] sur %s" % (self.__comment__['pseudo'],self.__comment__['ip'], self.__comment__.parent['name'])
    
    def _get_description(self):
        return self.__comment__['comment']
    
    
    def process_comment(self,*args,**kw):
        """
        """
        assert 'comment_action' in kw
        assert kw['comment_action'] in self.actions
        self.actions[kw['comment_action']](self)
    
    
    def _get_validation_method(self):
        """
        Returns the callable for validation
        """
        return CommentWfItem.process_comment