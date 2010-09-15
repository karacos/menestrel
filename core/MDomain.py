'''
Created on 13 janv. 2010

@author: nico
'''

__author__="Nicolas Karageuzian"
__contributors__ = []

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import os, sys
import karacos
from mako.template import Template
from uuid import uuid4

class MDomain(karacos.db['Domain']):
    '''
    WebApp oriented Domain
    '''


    def __init__(self,*args, **kw):
        karacos.db['Domain'].__init__(self,*args, **kw)
        if 'KC_M_user_profiles_node_name' not in self:
            self['KC_M_user_profiles_node_name'] = 'users'
        self.save()
        m_templatesdir = os.path.join(karacos.apps['menestrel'].__path__[0],'resources','templates')
        if 'templatesdirs' not in self:
            self['templatesdirs'] = [m_templatesdir]
        if m_templatesdir not in self['templatesdirs']:
            self['templatesdirs'].append(self['templatesdirs'])
        self.save()
        if 'register' not in self['ACL']['user.anonymous@%s'%self['name']]:
            self['ACL']['user.anonymous@%s'%self['name']].append('register')
        if 'validate_user' not in self['ACL']['user.anonymous@%s'%self['name']]:
            self['ACL']['user.anonymous@%s'%self['name']].append('validate_user')
        if 'group.everyone@%s' % self['name'] in self['ACL']:
            if 'modify_person_data' not in self['ACL']['group.everyone@%s' % self['name']]:
                self['ACL']['group.everyone@%s' % self['name']].append('modify_person_data')
            if 'create_password' not in self['ACL']['group.everyone@%s' % self['name']]:
                self['ACL']['group.everyone@%s' % self['name']].append('create_password')
        else:
            self['ACL']['group.everyone@%s' % self['name']] = ['modify_person_data','create_password']
        if u'group.registered@%s' % self['name'] in self['ACL']:
            if 'create_user_profile' not in self['ACL'][u'group.registered@%s' % self['name']]:
                self['ACL'][u'group.registered@%s' % self['name']].append('create_user_profile')
            if 'create_password' not in self['ACL'][u'group.registered@%s' % self['name']]:
                self['ACL'][u'group.registered@%s' % self['name']].append('create_password')
        self.save()
        """ SAME as in Domains
        if '_attachments' not in self:
            tidyzip = file(os.path.join(KaraCos.Apps['menestrel'].__path__[0],'interfaces','target','multiflex37.zip'))
            KaraCos.Db.sysdb.put_attachment(self, tidyzip.read(), 'multiflex37.zip')
        self._update_item()
        if 'multiflex37.zip' not in self['_attachments']:
                tidyzip = file(os.path.join(KaraCos.Apps['menestrel'].__path__[0],'interfaces','target','multiflex37.zip'))
                KaraCos.Db.sysdb.put_attachment(self, tidyzip.read(), 'multiflex37.zip')#, 'image/png')
        self._update_item()
        """ 
        
    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        templatepath = os.path.join(karacos.apps['menestrel'].__path__[0],'resources','templates')
        if 'templatesdirs' in data:
            data['templatesdirs'].append(templatepath)
        data['templatesdirs'] = [templatepath]
        if 'WebType' not in data:
            data['WebType'] = 'MDomain'
        result = karacos.db['Domain'].create(base=base,data=data)
        result.log.info("create domain : %s" % result)
        return result

    
    def _get_user_profiles_node(self):
        if '__user_profiles__' not in dir(self):
            self._update_item()
            if self['KC_M_user_profiles_node_name'] not in self.__childrens__:
                profiles = karacos.db['Resource'].create(base=None, parent=self,data={'name':self['KC_M_user_profiles_node_name']})
                profiles['ACL']['groups.everyone@%s' % self['name']] = ['index','get_user_actions_forms','w_browse']
                profiles['ACL']['user.admin@%s' % self['name']].remove('rename')
            
            self.__user_profiles__ = self.__childrens__[self['KC_M_user_profiles_node_name']]
        return self.__user_profiles__
    
    def _get_login_form(self):
        """
        """
        result = [{'title': _("Connexion"),
         'submit': _('Valider'),
         'fields': [{'name':'email', 'title':'Addresse email','dataType': 'TEXT'},
                    {'name':'password', 'title':'Mot de passe','dataType': 'PASSWORD'}]
        },
        {'title': _("Pas encore inscrit ?"),
         'submit': _("S'enregistrer"),
         'fields': [{'name':'register', 'title':"Creez votre identifiant",'dataType': 'HIDDEN', 'value': 'register'}]
        },]
        return result
    
    @karacos._db.isaction
    def login(self,*wargs, **kw):
        """
        """
        if 'register' in kw:
            raise karacos.http.Redirect('/register',301)
        assert 'email' in kw
        assert 'password' in kw
        user = None
        if True: # KaraCos._Core.mail.valid_email(email):
            try:
                user = self.authenticate(kw['email'],kw['password'])
            except karacos._db.Exception, e:
                
                return {'status':'failure', 'message' : '%s' % e.parameter,
                        'errors': None }
        else:
            return {'status':'failure', 'message':_('Adresse email invalide'),
                    'errors':{'email':_('This is not a valid mail address')}}
            
        return {'status':'success', 'message':_("Authentification r&eacute;ussie"),'data':user}
    login.get_form = _get_login_form
    login.label = _('S\'authentifier')
    
    
    
    @karacos._db.isaction
    def register(self,email=None):
        """
        """
        result = self._register(email=email)
        if result['status'] =='success':
            ""
        return karacos.json.dumps(result)
    register.form = {'title': _("S'enregister"),
         'submit': _('Valider'),
         'fields': [{'name':'email', 'title':'Addresse email','dataType': 'TEXT'}]
        }
    register.label = _('S\'inscrire')
    
    #@KaraCos.expose()      ##### IDEE Ce decorator est a reecrire, il faut pouvoir ecrire comme un isaction dedans, c'est le decorator qui devra appeler le processor de templates en fnct de la requete
    @karacos._db.isaction
    def validate_user(self,email=None,validation=None):
        """
        Validate user account
        """
        
        result =  self._validate_user(email,validation)
        if result['status'] != 'failure':
            user = self.get_user_by_name(email)
            karacos.serving.get_session().set_user(user)
            raise karacos.http.DataRequired(self,self.create_password)
            
        else: #result['status'] == 'failure'
            
            return result

    @karacos._db.isaction
    def _unregister(self,email,validation):
        """
        """
        result =  self._unregister_user(email,validation)
        template = self.__domain__.lookup.get_template('/default/system')
        return template.render(instance=self,result=result['message'])

    @karacos._db.isaction
    def create_password(self,password,confirmation):
        """
        Creates user password
        """
        assert isinstance(password,basestring)
        assert password == confirmation, _("Erreur, les motes de passe ne correspondent pas")
        user = self.get_user_auth()
        #assert 'password' not in user
        passwordhash = "%s" % KaraCos.Db.User.hash_pwd(password)
        user['password'] = passwordhash
        user.save()
        result = {'status':'success', 'message':_("Mot de passe modifi&eacute;"),'data':{}}
        return result
    create_password.form = {'title': _("Saisissez votre mot de passe"),
         'submit': _('Valider'),
         'fields': [{'name':'password', 'title':'Mot de passe','dataType': 'PASSWORD'},
                    {'name':'confirmation', 'title':'Confirmez le mot de passe','dataType': 'PASSWORD'}]
        }
    create_password.label = _('Creation du mot de passe')
    @karacos._db.isaction
    def modify_person_data(self):
        """
        """
        pass
    
    @karacos._db.isaction
    def user_profile_exist(self,name):
        profilesParent = self.get_child_by_name('users')
        if profilesParent.child_exist(name):
            return {'status':'success', 'message' : _('Profile existe avec ce nom'),
                        'data': None }
        else:
            return {'status':'failure', 'message' : _("Profile n'existe pas"),
                        'errors': None }
    
    @karacos._db.isaction
    def rename_user_profiles_node(self,name):
        """
        """
        assert name not in self.__dict__, "error,reserved name"
        self._get_user_profiles_node()._rename(name)
        self['KC_M_user_profiles_node_name'] = name
        self.save()
    #rename_user_profiles_node.form = forms._forms['rename']
    rename_user_profiles_node.label = _("rename_user_profiles_node")
    
    @karacos._db.isaction
    def create_user_profile(self,type='Profile',name=None):
        """
        """
        assert isinstance(name,basestring), "ArgumentError : name should be baseString"
        
        person = self._get_person_data()
        data = { 'name': name,
                    }
        profile = KaraCos.Db.Profile.create(parent=self._get_user_profiles_node(),data=data, person=person)
        profile['ACL']['group.everyone@%s' % self['name']] = ['get_comment_form','add_comment','w_browse','__get_actions']
        profile.save()
    #create_user_profile.form = forms._forms['create_profile']
    create_user_profile.label = _("Creer un profil")
    
    def _get_person_data(self):
        user = self.__domain__.get_user_auth()
        assert user['name'] != self.__domain__._get_anonymous_user()['name']
        if 'personData' not in user.__childrens__:
            personData = {'name':'personData'}
            KaraCos.Db.Person.create(user=user, base=None,data=personData)
        return user.__childrens__['personData']
        

    def _register(self,email=None,password=None):
        """
        """
        user = None
        if karacos.core.mail.valid_email(email):
            try:
                user = None
                if not self.user_exist(email):
                    self._create_user(email,password)
                    user = self.get_user_by_name(email)
                    self._get_registered_group().add_user(user)
                    self._get_everyone_group().add_user(user)
                    user = self.get_user_by_name(email)
                    personData = {'name':'personData'}
                    karacos.db['Person'].create(user=user, base=None,data=personData)
                    self.send_validation(user)
                    return {'status':'success',
                            'message' : _('Enregistrement reussi'), 'data': user }
                    
                user = self.get_user_by_name(email)
                if password != None:
                    passwordhash = "%s" % karacos.db['User'].hash_pwd(password)
                    if not user['password'] == passwordhash:
                        return {'status':'failure',
                                'message' : _('Erreur, email connue mais mot de passe incorrect'),
                            'errors': None }
                if user.belongs_to(self._get_confirmed_group()):
                    ""
                    return {'status':'success',
                            'message' : _('Email/mot de passe connus, user deja valid&eacute;'),
                         'data': user }
                else:
                    #resend validation
                    ""
                    self.send_validation(user)
                    return {'status':'success',
                            'message' : _('Email/mot de passe connus, user non valid&eacute, renvoi validation'),
                         'data': user }
            except karacos._db.Exception, e:
                
                return {'status':'failure', 'message' : '%s' % e.parameter,
                        'errors': None }
        else:
            return {'status':'failure', 'message':_('Adresse email invalide'),
                    'errors':{'email':_('This is not a valid mail address')}}
            
        return {'status':'success', 'message':_("Enregistrement reussi"),'data':user}


    def send_validation(self,user):
        """
        send the validation mail to user
        """
        if not karacos.core.mail.valid_email(user['name']):
            return False
        if 'validation' not in user:
            user['validation'] = "%s" % uuid4().hex
        user.save()
        self.log.info("Sending validation to : %s with validation '%s'" % (user['name'], user['validation']))
        message = MIMEMultipart()
        message['From'] = self['mail_register_from_addr']
        message['To'] = user['name']
        message['Subject'] = _("Confirmation d'inscription")
        
        
        if 'mail_confirm_template' not in self.__dict__:
            if 'mail_confirm_template' not in self:
                try:
                    self.mail_confirm_template = self.lookup.get_template('%s/mail_confirmation' % self.get_site_theme_base())
                except:
                    self.mail_confirm_template = self.lookup.get_template('/default/mail_confirmation')
            else:
                self.mail_confirm_template = Template(self['mail_confirm_template'])
            
        self.log.info("Using main confirm template : %s" % self.mail_confirm_template.uri)
        self.log.info("Using main confirm template : %s" % self.mail_confirm_template)
        body = self.mail_confirm_template.render(domain=self,user=user)
        
        if 'mail_confirm_attachements' in self:
            
            for img in self['mail_confirm_attachements'].keys():
                # 
                #images = {'TraiderZicLogo.png':"TzLogoPng@11111",
                #  'TraiderZicLogo.gif':"TzLogoGif@11112",
                #  'FondLogo.png':"TzFondLogoPng@11113>",
                #  'FondLogo.gif':"TzFondLogoGif@11114>",
                #  'fond_site_traderzic.png':"TzBackGroud@11115",
                #          }
                
                img_location = os.path.join(KaraCos.Apps['traderzic'].__path__[0],'interfaces','war','public',img)
                img_content=file(img_location, "rb").read()
                img_msg=MIMEImage(img_content)
                img_type, img_ext=img_msg["Content-Type"].split("/")
        
                del img_msg["MIME-Version"]
                del img_msg["Content-Type"]
                del img_msg["Content-Transfer-Encoding"]
        
                img_msg.add_header("Content-Type", "%s/%s; name=\"%s.%s\"" % (img_type, img_ext, self['mail_confirm_attachements'][img], img_ext))
                img_msg.add_header("Content-Transfer-Encoding", "base64")
                img_msg.add_header("Content-ID", "<%s>" % self['mail_confirm_attachements'][img])
                img_msg.add_header("Content-Disposition", "inline; filename=\"%s.%s\"" % (self['mail_confirm_attachements'][img], img_ext))
                message.attach(img_msg)

        message.attach(MIMEText(body, 'html'))
        self.log.debug("sending mail : %s,%s" % (user['name'],user['validation']))
        try:
            karacos.core.mail.send_mail(user['name'],message.as_string())
            self.log.info("mail successfully sent to %s" % user['name'])
        except:
            self.log.warn("error while sending mail to %s" % user['name'])
            self.log.log_exc( sys.exc_info(),'warn')
        return True
    
    
    def _unregister_user(self,email):
        """
        Newsletter unregister
        obsolete - see Newsletter Object
        """
        if self.user_exist(email):
            ""
            user = self.get_user_by_name(email)
            if user['validation'] == validation:
                user['newsletter'] = False
                user.save()
            
    @karacos._db.isaction
    def _simple_message(self,sender_name=None,sender_email=None,subject=None,message=None):
        """
        Creates a node in manager/messages
        """
        if len(self._get_child_by_name('manager')) == 0:
            karacos.db['Manager'].create(base=None, parent=self,
                                      data={'name':'manager'})
        manager = self.get_child_by_name('manager')
        data = {'ref_db': self.base.id,
                'ref_id': self.id,
                'sender_name' : sender_name,
                'sender_email': sender_email,
                'subject': subject,
                'message': message,
                'type': 'MDMessage'
                }
        manager._create_workflow_item(data)
        
    _simple_message.form = {'title': _("Envoyer un message"),
         'submit': _('Valider'),
         'fields': [{'name':'sender_name', 'title':'Votre nom','dataType': 'TEXT'},
                    {'name':'sender_email', 'title':'Votre adresse email','dataType': 'TEXT'},
                    {'name':'subject', 'title':'Sujet','dataType': 'TEXT'},
                    {'name':'message', 'title':'Votre message','dataType': 'TEXT', 'formType':'TEXTAREA'}]
        }
    def _validate_user(self,email,validation):
        if self.user_exist(email):
            ""
            user = self.get_user_by_name(email)
            if user['validation'] == validation:
                
                if user.belongs_to(self._get_confirmed_group()):
                    return {'status':'error', 'message': _("Email deja validee"), 'data':{}}
                else:
                    self._get_registered_group().remove_user(user)
                    self._get_confirmed_group().add_user(user)
                    return {'status':'success', 'message': _("Confirmation email reussie"), 'data':{}}
                    
        else:
            return {'status':'failure', 'message': _("Email inconnue dans le systeme"), 'data':{}}