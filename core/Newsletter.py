'''
Created on 13 janv. 2010

@author: nico
'''
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from uuid import uuid4
import sys
import karacos
#from anydbm import result
json = karacos.json
class Newsletter(karacos.db['EntriesHolder']):
    '''
    Newsletter resource
    '''
    
    def __init__(self,parent=None,base=None,data=None):
        #assert isinstance(domain,karacos.db['Domain']), "domain in not type Domain"
        karacos.db['WebNode'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'Newsletter'
        if 'mail_register_from_addr' not in data:
            data['mail_register_from_addr'] = ''
        return karacos.db['WebNode'].create(parent=parent,base=base,data=data)
    
    @karacos._db.isaction
    def publish_node(self):
        """
        overrides WebNode default
        """
        self['ACL']['group.everyone@%s' % self.__domain__['name']] = ["get_user_actions_forms","w_browse","index","subscribe","view_last_entries"]
        self.save()
    
    def _get_subscribers_node(self):
        if 'subscribers' not in self.__childrens__:
            subscribers = {'name': 'subscribers'}
            self._create_child_node(data=subscribers,type='Node',base=True)
        if '__subscribers__' not in self.__dict__:
            self.__subscribers__ = self.__childrens__['subscribers']
        return self.__subscribers__
    
    def _subscribe(self,email=None):
        if karacos.core.mail.valid_email(email):
            if email not in self._get_subscribers_node().__childrens__:
                subscriber = {'name': email,
                              'newsletter': False,
                              'validation': "%s" % uuid4().hex }
                self._get_subscribers_node()._create_child_node(data=subscriber,type='Node',base=True)
                try:
                    self.send_message(subscriber,'confirm')
                except:
                    self.log.log_exc( sys.exc_info(),'error')
                return {'status':'success',
                            'message' : _('Enregistrement reussi'), 'data': subscriber }
            else:
                subscriber = self._get_subscribers_node().__childrens__[email]
                if 'newsletter' not in subscriber or not subscriber['newsletter']:
                    try:
                        subscriber['validation'] = "%s" % uuid4().hex
                        self.send_message(subscriber,'confirm')
                    except:
                        self.log.log_exc( sys.exc_info(),'error')
                    return {'status':'success',
                                'message' : _('Merci de votre inscription'),
                             'data': subscriber }
                else:
                    return {'status':'success',
                            'message' : _('Votre adresse est deja inscrite'),
                             'data': subscriber }
        else:
            return {'status':'failure', 'message':_('Adresse invalide'),
                    'errors':{'email':_('This is not a valid mail address')}}
    
    @karacos._db.isaction
    def subscribe(self,email=None):
        """
        #TODO : si user connecte, argument outionnel
        """
        result = self._subscribe(email=email)
        if result['status'] =='success':
            ""
        return result
    subscribe.form = {'title': _("S'inscrire"),
         'submit': _('Valider'),
         'fields': [{'name':'email', 'title':'Addresse email','dataType': 'TEXT'}]
        }
    subscribe.label = _('S\'inscrire a la Newsletter')


    @karacos._db.isaction
    def _validate(self,email=None,validation=None):
        """
        Validate email for newsletter
        """
        result =  self._validate_email(email,validation)
        template = self.__domain__.lookup.get_template('/system')
        return template.render(instance=self,result=result['message'])
    
    def _validate_email(self,email,validation):
        """
        Newsletter only validation
        """
        if karacos.core.mail.valid_email(email):
            if email in self._get_subscribers_node().__childrens__:
                user = self._get_subscribers_node().__childrens__[email]
                if 'validation' in user and user['validation'] == validation:
                    user['newsletter'] = True
                    user.save()
                    return {'status':'success', 'message': _("Inscription newsletter confirmee"), 'data':{}}
                return {'status':'failure',
                        'message': _("Code validation incorrect"),
                        'errors':{'validation':_('Code validation incorrect')}}
            return {'status':'failure',
                        'message': _("Email invalide"),
                        'errors':{'email':_('Adresse inconnue')}}
        return {'status':'failure',
                        'message': _("Email invalide"),
                        'errors':{'email':_('Adresse invalide')}}
    
    def _get_create_message_form(self):
        form = {'title': _("Creer un message"),
         'submit': _('Ajouter'),
         'fields': [{'name':'name', 'title':_('Nom'),'dataType': 'TEXT'},
                    {'name':'title', 'title':_('Titre'),'dataType': 'TEXT'},
                    {'name':'message', 'title':_('Message'),'dataType': 'TEXT', 'formType': 'WYSIWYG'},
                 ] }
        return form
    
    @karacos._db.isaction
    def create_message(self,*args,**kw):
        """
        Create a newsletter message
        """
        self._create_child_node(data=kw,type='Entry',base=False)
    
    create_message.get_form = _get_create_message_form
    create_message.label = _("Creer message")
    
    
    def _entry_publish(self,entry):
        """
        Triggered action by Entries when published
        """
        
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_subscribers_list__(self,subscribers_id):
        """
        // %s
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              emit(doc.name, doc.newsletter);
            }
        """
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_public_entries__(self):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (doc.status == "published") {
                  emit(doc.name, doc._id);
                  }
            }
        """
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_public_entries_values__(self):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (doc.status == "published") {
                  emit(doc.name, doc);
                  }
            }
        """
        
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_editing_entries__(self):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (doc.status == "edition") {
                  
                      emit(doc.name, doc);
                  
                  }
            }
        """
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_entries__(self):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              emit(doc.name, doc._id);
            }
        """
    
    @karacos._db.isaction
    def view_subscribers(self):
        """
        Return a list of newsletter subscribers
        """
        result = []
        for item in self.__get_subscribers_list__(self._get_subscribers_node().id):
            result.append({item.key:item.value})
        return result
    
    def _get_public_entries(self,number=5):
        result = {}
        for item in self.__get_public_entries_values__():
            result[item.value['creation_date']] = self.db[item.value['_id']]
        return result
    
    def _get_editing_entries(self):
        result = {}
        for item in self.__get_editing_entries__():
            result[item.value['creation_date']] = self.db[item.value['_id']]
        return result
    
    def _view_last_entries(self,number=5):
        result = []
        for item in self.__get_public_entries__():
            if len(result) <= number:
                result.append(self.db[item.value])
        return result
    
    @karacos._db.isaction
    def view_last_entries(self,number=5):
        """
        Return a list of newsletter subscribers
        """
        return {'status':'success', 'data':self._get_public_entries(number)}
    
    def _get_subscribers(self):
        """
        """
    
    def _entry_publish(self,entry):
        """
        Callback when a message is published
        send mail to all subscribers
        """
    
    def _get_options_form(self):
        if 'mail_register_from_addr' not in self:
            self['mail_register_from_addr'] = ''
        if 'confirm_first_block' not in self:
            self['confirm_first_block'] = ''
        if 'confirm_subject' not in self:
            self['confirm_subject'] = ''
        if 'unregister_first_block' not in self:
            self['unregister_first_block'] = ''
        if 'unregister_subject' not in self:
            self['unregister_subject'] = ''
        self.save()
        return {'title': _("Option de la newsletter"),
         'submit': _('Sauver la configuration'),
         'fields': [{'name':'mail_register_from_addr', 'title':_("Adresse expediteur"),'dataType': 'TEXT', 'value': self['mail_register_from_addr']},
                    {'name':'confirm_subject', 'title':_('CONFIRM sujet'),'dataType': 'TEXT', 'value': self['confirm_subject']},
                    {'name':'confirm_first_block', 'title':_('CONFIRM message premier bloc'),'dataType': 'TEXT','formType': 'WYSIWYG', 'value': self['confirm_first_block']},
                    {'name':'unregister_subject', 'title':_('UNREGISTER sujet'),'dataType': 'TEXT', 'value': self['unregister_subject']},
                    {'name':'unregister_first_block', 'title':_('UNREGISTER message premier bloc'),'dataType': 'TEXT','formType': 'WYSIWYG', 'value': self['unregister_first_block']},
                 ] }
    
    @karacos._db.isaction
    def _options(self,*args,**kwds):
        assert 'mail_register_from_addr' in kwds
        assert 'confirm_first_block' in kwds
        assert 'confirm_subject' in kwds
        assert 'unregister_subject' in kwds
        assert 'unregister_first_block' in kwds
        self['mail_register_from_addr'] = kwds['mail_register_from_addr']
        self['confirm_first_block'] = kwds['confirm_first_block']
        self['confirm_subject'] = kwds['confirm_subject']
        self['unregister_subject'] = kwds['unregister_subject']
        self['unregister_first_block'] = kwds['unregister_first_block']
        self.save()
        return
    _options.get_form = _get_options_form
    
    def send_message(self,user,message_name):
        """
        send given mail message to given user
        """
        if not karacos.core.mail.valid_email(user['name']):
            return False
        if 'validation' not in user:
            user['validation'] = "%s" % uuid4().hex
        user.save()
        message = MIMEMultipart()
        message['From'] = self['mail_register_from_addr']
        message['To'] = user['name']
        if '%s_subject' % message_name not in self:
            message['Subject'] = _("Email de confirmation")
        else:
            message['Subject'] = self['%s_subject' % message_name]
        template = None
        if 'mail_template_%s' % message_name not in self:
            try:
                template = self.__domain__.lookup.get_template('%s/nl_templates/%s' % (self.__domain__.get_site_theme_base(),message_name))
            except:
                try:
                    template = self.__domain__.lookup.get_template('/menestrel/nl_templates/%s' % message_name)
                except:
                    self.log.log_exc(sys.exc_info(),'error')
                    self.log.error("Mail template '%s' not found, mail not sent" % message_name)
        else:
            template = Template(self['mail_template_%s' % message_name])
        body = template.render(instance=self,user=user)
        #if 'mail_confirm_attachements' in self:
            #for img in self['mail_confirm_attachements'].keys():
                # 
                #images = {'TraiderZicLogo.png':"TzLogoPng@11111",
                #  'TraiderZicLogo.gif':"TzLogoGif@11112",
                #  'FondLogo.png':"TzFondLogoPng@11113>",
                #  'FondLogo.gif':"TzFondLogoGif@11114>",
                #  'fond_site_traderzic.png':"TzBackGroud@11115",
                #          }
                
                #img_location = os.path.join(karacos.apps['traderzic'].__path__[0],'interfaces','war','public',img)
                #img_content=file(img_location, "rb").read()
                #img_msg=MIMEImage(img_content)
                #img_type, img_ext=img_msg["Content-Type"].split("/")
        
                #del img_msg["MIME-Version"]
                #del img_msg["Content-Type"]
                #del img_msg["Content-Transfer-Encoding"]
        
                #img_msg.add_header("Content-Type", "%s/%s; name=\"%s.%s\"" % (img_type, img_ext, self['mail_confirm_attachements'][img], img_ext))
                #img_msg.add_header("Content-Transfer-Encoding", "base64")
                #img_msg.add_header("Content-ID", "<%s>" % self['mail_confirm_attachements'][img])
                #img_msg.add_header("Content-Disposition", "inline; filename=\"%s.%s\"" % (self['mail_confirm_attachements'][img], img_ext))
                #message.attach(img_msg)

        
        message.attach(MIMEText(body, 'html'))
        self.log.debug("sending mail : %s,%s" % (user['name'],user['validation']))
        try:
            karacos.core.mail.send_mail(user['name'],message.as_string())
            self.log.info("mail successfully sent to %s" % user['name'])
        except:
            self.log.warn("error while sending mail to %s" % user['name'])
            self.log.log_exc( sys.exc_info(),'warn')
        return True
    
    @karacos._db.isaction
    def _unregister(self,email=None,validation=None):
        """
        Validate email for newsletter
        """
        self.log.info("unregister %s" % email)
        result =  self._unregister_user(email=email,validation=validation)
        template = self.__domain__.lookup.get_template('/system')
        return template.render(instance=self,result=result['message'])
    
    def _unregister_user(self,email=None, validation=None):
        """
        Unregister from newsletter
        """
        if karacos.core.mail.valid_email(email):
            if email in self._get_subscribers_node().__childrens__:
                subscriber = self._get_subscribers_node().__childrens__[email]
                if validation == None: # S'il n'y a pas de chaine de validation, on envoie un mail pour la desinscription
                    subscriber['validation'] = "%s" % uuid4().hex
                    try:
                        self.send_message(subscriber,'unregister')
                        return {'status':'success', 'message':'Message de desinscription envoye'}
                    except:
                        return {'status':'failure', 'message':'Erreur de traitement', 'errors':{'system':'Erreur de traitement'}}
                else:
                    if 'validation' in subscriber and subscriber['validation'] == validation:
                        subscriber['newsletter'] = False
                        subscriber.save()
                        return {'status':'success', 'message':'Desinscription reussie'}
                    else:
                        return {'status':'success', 'message':'Probleme lors de la desinscription'}
            else:
                return {'status':'failure', 'message':'Adresse inconnue', 'errors':{'email':'Adresse inconnue'}}
        else:
            return {'status':'failure', 'message':'Adresse invalide', 'errors':{'email':'Adresse invalide'}}