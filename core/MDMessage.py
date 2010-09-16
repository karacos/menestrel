'''
Created on 25 aout 2010

@author: nico
'''
import karacos

class MDMessage(karacos.db['WorkFlowItem']):
    '''
    WorkFlow item for messages in MDomain.
    This implementation carries data of message on itself
    '''


    def __init__(self,parent=None,base=None,data=None):
        karacos.db['WorkFlowItem'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(parent.__domain__, karacos.db['MDomain'])
        assert isinstance(data,dict)
        assert 'subject' in data
        assert 'message' in data
        assert 'sender_email' in data
        if 'type' not in data:
            data['type'] = 'MDMessage'
        if 'status' not in data:
            data['status'] = 'unread'
        result = karacos.db['WorkFlowItem'].create(parent=parent,base=base,data=data)
        return result

    def _get_validation_action(self):
        result = {'title': _("Repondre"),
         'submit': _('Envoyer'),
         'fields': [
                    {'name':'message', 'title':'Votre message','dataType': 'TEXT', 'formType':'TEXTAREA'}
                    ]
                    }
        return result
    
    def _get_title(self):
        return "From %s : %s" % (self['sender_email'],self['subject'])
    
    def _get_description(self):
        return self['message']
    
    def _reply_to_sender(self,*args,**kw):
        """
        """
        assert 'message' in kw
        self.log.info("Reply action, message is : \n%s" % kw['message'])
        subject = "Re: %s" % self['subject']
        # TODO: implement reply
    
    def _get_validation_method(self):
        """
        Returns the callable for validation
        """
        return MDMessage._reply_to_sender