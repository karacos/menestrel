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
        if 'staticdirs' not in self:
            self['staticdirs'] = {}
        staticdirname = os.path.join(karacos.apps['menestrel'].__path__[0],'resources','static')
        self['staticdirs']['m_design'] = staticdirname
        m_templatesdir = os.path.join(karacos.apps['menestrel'].__path__[0],'resources','templates')
        if 'templatesdirs' not in self:
            self['templatesdirs'] = [m_templatesdir]
        if m_templatesdir not in self['templatesdirs']:
            self['templatesdirs'].append(m_templatesdir)
        self.save()
        if 'register' not in self['ACL']['user.anonymous@%s'%self['name']]:
            self['ACL']['user.anonymous@%s'%self['name']].append('register')
        if '_process_facebook_cookie' not in self['ACL']['user.anonymous@%s'%self['name']]:
            self['ACL']['user.anonymous@%s'%self['name']].append('_process_facebook_cookie')
        
        if 'validate_user' not in self['ACL']['user.anonymous@%s'%self['name']]:
            self['ACL']['user.anonymous@%s'%self['name']].append('validate_user')
        if 'group.everyone@%s' % self['name'] in self['ACL']:
            if 'modify_person_data' not in self['ACL']['group.everyone@%s' % self['name']]:
                self['ACL']['group.everyone@%s' % self['name']].append('modify_person_data')
            if 'create_password' not in self['ACL']['group.everyone@%s' % self['name']]:
                self['ACL']['group.everyone@%s' % self['name']].append('create_password')
            if '_process_facebook_cookie' not in self['ACL']['group.everyone@%s'%self['name']]:
                self['ACL']['group.everyone@%s'%self['name']].append('_process_facebook_cookie')
            if 'fragment' not in self['ACL']['group.everyone@%s'%self['name']]:
                self['ACL']['group.everyone@%s'%self['name']].append('fragment')
            if 'set_user_email' not in self['ACL'][u'group.everyone@%s' % self['name']]:
                self['ACL'][u'group.everyone@%s' % self['name']].append('set_user_email')
        else:
            self['ACL']['group.everyone@%s' % self['name']] = ['modify_person_data','create_password','_process_facebook_cookie','set_user_email']
        if u'group.registered@%s' % self['name'] in self['ACL']:
            if 'create_user_profile' not in self['ACL'][u'group.registered@%s' % self['name']]:
                self['ACL'][u'group.registered@%s' % self['name']].append('create_user_profile')
            if 'create_password' not in self['ACL'][u'group.registered@%s' % self['name']]:
                self['ACL'][u'group.registered@%s' % self['name']].append('create_password')
        else:
            self['ACL'][u'group.registered@%s' % self['name']] = ['create_user_profile', 'create_password']
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
        result = [{'title': _("Vous connecter directement au site (Connexion)"),
         'submit': _('Valider'),
         'fields': [{'name':'email', 'title':'Addresse email','dataType': 'TEXT'},
                    {'name':'password', 'title':'Mot de passe','dataType': 'PASSWORD'}]
        },
        {'title': _("Cr&eacute;er un compte (Pas encore inscrit ?)"),
         'submit': _("S'enregistrer"),
         'fields': [{'name':'email', 'title':'Addresse email','dataType': 'TEXT'},
                    {'name':'register', 'title':"Creez votre identifiant",'dataType': 'HIDDEN', 'value': 'register'}]
        },]
        return result
    
    @karacos._db.isaction
    def login(self,*wargs, **kw):
        """
        """
        if 'register' in kw:
            assert 'email' in kw
            return self._register(kw['email'])
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
            
        return {'status':'success', 'message':_("Authentification r&eacute;ussie"),'data':self._get_user_actions_forms(),'success': True}
    login.get_form = _get_login_form
    login.label = _('S\'authentifier')
    
    
    
    @karacos._db.isaction
    def register(self,email=None):
        """
        """
        result = self._register(email=email)
        if result['status'] =='success':
            ""
        return result
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
    def _process_facebook_cookie(self):
        """
        """
        import facebook
        cookie = facebook.get_user_from_cookie(
                karacos.serving.get_request().cookies, self['fb_appId'], self['fb_appKey'])
        graph = facebook.GraphAPI(cookie['access_token'])
        fbuser = graph.get_object("me")
        user = self.get_user_by_name(fbuser['name'])
        if user == None:
            user = self._create_user(username=fbuser['name'])
        user.update(fbuser)
        user['name'] = fbuser['name']
        user['full_name'] = fbuser['name']
        if 'group.registered@%s' % self['name'] not in user['groups']:
            user['groups'].append('group.registered@%s' % self['name'])
        user.save()
        karacos.serving.get_session()._set_user_auth_(user)
        return self._get_user_actions_forms()
    
    @karacos._db.isaction
    def _unregister(self,email,validation):
        """
        """
        result =  self._unregister_user(email,validation)
        template = self.__domain__.lookup.get_template('/default/system')
        return template.render(instance=self,result=result['message'])

    @karacos._db.isaction
    def create_password(self,password=None,confirmation=None):
        """
        Creates user password
        """
        assert isinstance(password,basestring)
        assert password == confirmation, _("Erreur, les motes de passe ne correspondent pas")
        user = self.get_user_auth()
        #assert 'password' not in user
        passwordhash = "%s" % karacos.db['User'].hash_pwd(password)
        user['password'] = passwordhash
        user.save()
        result = {'status':'success', 'message':_("Mot de passe modifi&eacute;"),'data':{}}
        return result
    create_password.form = {'title': _("Saisissez votre mot de passe"),
         'submit': _('Valider'),
         'fields': [{'name':'password', 'title':'Mot de passe','dataType': 'PASSWORD'},
                    {'name':'confirmation', 'title':'Confirmez le mot de passe','dataType': 'PASSWORD'}]
        }
    
    @karacos._db.isaction
    def modify_person_data(self,*args,**kw):
        """
        """
        user = self.__domain__.get_user_auth()
        userdata = self._get_person_data_user(user)
        for k in kw:
            userdata[k] = kw[k]
            userdata.save()
        return {'success': True, 'message': "Userdata modified", 'data': userdata}
    
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
    def _settings(self,*args,**kw):
        if 'require_login_mail' in kw:
            if kw['require_login_mail'] != '':
                if kw['require_login_mail'].lower() == 'true':
                    self['require_login_mail'] = True
                else:
                    self['require_login_mail'] = False
        if 'description' in kw:
            if kw['description'] != '':
                self['description'] = kw['description']
        if 'keywords' in kw:
            if kw['keywords'] != '':
                self['keywords'] = kw['keywords']
        if 'head_bloc' in kw:
            if kw['head_bloc'] != '':
                self['head_bloc'] = kw['head_bloc']
        if 'fb_appId' in kw:
            if kw['fb_appId'] != '':
                self['fb_appId'] = kw['fb_appId']
        if 'fb_appKey' in kw:
            if kw['fb_appKey'] != '':
                self['fb_appKey'] = kw['fb_appKey']
        if 'site_email_from' in kw:
            if kw['site_email_from'] != '':
                self['site_email_from'] = kw['site_email_from']
        if 'site_email_service_host' in kw:
            if kw['site_email_service_host'] != '':
                self['site_email_service_host'] = kw['site_email_service_host']
        if 'site_email_service_port' in kw:
            if kw['site_email_service_port'] != '':
                self['site_email_service_port'] = int(kw['site_email_service_port'])
        if 'site_email_service_username' in kw:
            if kw['site_email_service_username'] != '':
                self['site_email_service_username'] = str(kw['site_email_service_username'])
        if 'site_email_service_password' in kw:
            if kw['site_email_service_password'] != '':
                self['site_email_service_password'] =str( kw['site_email_service_password'])
        if 'site_email_service_secure' in kw:
            if kw['site_email_service_secure'] != '':
                self['site_email_service_secure'] = kw['site_email_service_secure']
        self.save()
        return {'status': 'success', 'success': True, 'message': _('Domain settings updated')}
    
    def get_settings_form(self):
        fb_appId = ''
        if 'fb_appId' in self:
            fb_appId = self['fb_appId']
        fb_appKey = ''
        if 'fb_appKey' in self:
            fb_appKey = self['fb_appKey']
        site_email_from = ''
        if 'site_email_from' in self:
            site_email_from = self['site_email_from']
        description = ''
        if 'description' in self:
            description = self['description']
        keywords = ''
        if 'keywords' in self:
            keywords = self['keywords']
        head_bloc = ''
        if 'head_bloc' in self:
            head_bloc = self['head_bloc']
        site_email_service_host = ''
        if 'site_email_service_host' in self:
            site_email_service_host = self['site_email_service_host']
        site_email_service_port = ''
        if 'site_email_service_port' in self:
            site_email_service_port = self['site_email_service_port']
        site_email_service_username = ''
        if 'site_email_service_username' in self:
            site_email_service_username = self['site_email_service_username']
        site_email_service_password = ''
        if 'site_email_service_password' in self:
            site_email_service_password = self['site_email_service_password']
        site_email_service_secure = ''
        if 'site_email_service_secure' in self:
            site_email_service_secure = self['site_email_service_secure']
        require_login_mail = 'true'
        if 'require_login_mail' in self:
            if self['require_login_mail']:
                require_login_mail = 'true'
            else:
                require_login_mail = 'false'
                
        return {'title': _("Domain settings"),
         'submit': _('Appliquer'),
         'fields': [{'name':'description', 'title':'Description','dataType': 'TEXT','formType':'TEXTAREA', 'value':description},
                    {'name':'keywords', 'title':'Mots clef','dataType': 'TEXT', 'value':keywords},
                    {'name':'head_bloc', 'title':'Additional head bloc','dataType': 'TEXT','formType':'TEXTAREA', 'value':head_bloc},
                    {'name':'fb_appId', 'title':'Id app Facebook','dataType': 'TEXT', 'value':fb_appId},
                    {'name':'fb_appKey', 'title':'Clef app Facebook','dataType': 'TEXT', 'value':fb_appKey},
                    {'name':'site_email_from', 'title':'Expediteur email','dataType': 'TEXT', 'value':site_email_from},
                    {'name':'site_email_service_host', 'title':'Serveur service mail','dataType': 'TEXT', 'value':site_email_service_host},
                    {'name':'site_email_service_port', 'title':'Port service mail','dataType': 'TEXT', 'value':site_email_service_port},
                    {'name':'site_email_service_username', 'title':'User service mail','dataType': 'TEXT', 'value':site_email_service_username},
                    {'name':'site_email_service_password', 'title':'User service password','dataType': 'PASSWORD', 'value':site_email_service_password},
                    {'name':'site_email_service_secure', 'title':'Use secure','dataType': 'TEXT', 'value':site_email_service_secure},
                    {'name':'require_login_mail', 'title':'Require mail login','dataType': 'TEXT', 'value':require_login_mail},
                    ]}
    _settings.get_form = get_settings_form
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
        return self._get_person_data_user(user)
        
    def _get_person_data_user(self, user):
        assert user['name'] != self.__domain__._get_anonymous_user()['name']
        if 'personData' not in user.__childrens__:
            personData = {'name':'personData'}
            karacos.db['Person'].create(user=user, base=None,data=personData)
        return user.db[user['childrens']['personData']]
    
    def _register_user(self, email=None, password=None):
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
                return {'status':'success', 'success': True,
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
                return {'status':'success', 'success': True,
                        'message' : _('Email/mot de passe connus, user deja valid&eacute;'),
                     'data': user }
            else:
                #resend validation
                ""
                self.send_validation(user)
                return {'status':'success', 'success': True,
                        'message' : _('Email/mot de passe connus, user non valid&eacute, renvoi validation'),
                     'data': user }
        except karacos._db.Exception, e:
            
            return {'status':'failure', 'message' : '%s' % e.parameter,
                    'errors': None }
            
    def _register(self,email=None,password=None):
        """
        """
        user = None
        
        if 'require_login_mail' not in self:
            self['require_login_mail'] = False
        if bool(self['require_login_mail']):
            if karacos.core.mail.valid_email(email):
                return self._register_user(email, password)
            else:
                return {'status':'failure', 'message':_('Adresse email invalide'),
                        'errors':{'email':_('This is not a valid mail address')}}
        else:
            return self._register_user(email, password)
                
        
    @karacos._db.isaction
    def set_user_email(self, email=None):
        assert self.__domain__.is_user_authenticated() , _("Unavailable to anonymous user")
        user = self.__domain__.get_user_auth()
        user._set_email(email)
        return {'success': True}
        

    def send_validation(self,user):
        """
        send the validation mail to user
        """
        if 'validation' not in user:
            user['validation'] = "%s" % uuid4().hex
        user.save()
        self.log.error("Validation for %s : '%s'" % (user['name'], user['validation']))
        self.log.error("Validation url: /?method=validate_user&email=%s&validation=%s" % (user['name'], user['validation']))
        if not karacos.core.mail.valid_email(user['name']):
            return False
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
            karacos.core.mail.send_domain_mail(self,user['name'],message.as_string())
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
        """
        if 'manager' not in self.__childrens__:
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
        """
        msg = MIMEMultipart()
        msg['From'] = self['site_email_service_username']
        msg['To'] = self['site_email_service_username']
        msg['Subject'] = _("Message du site")
        msg.attach(MIMEText(""" <h2>Message envoye par %s (%s)</h2>
        <h3>subject: %s</h3>
        <p>message: %s</p>
        """ % (sender_name, sender_email, subject, message), 'html'));
        karacos.core.mail.send_domain_mail(self, self['site_email_service_username'], msg.as_string())
        
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
                    user._set_email(email)
                    return {'status':'success', 'message': _("Confirmation email reussie"), 'data':{}}
                    
        else:
            return {'status':'failure', 'message': _("Email inconnue dans le systeme"), 'data':{}}
    
    def _get_edit_resource_content_form(self):
        self._update_item()
        if 'content' not in self:
            self['content'] = '<p>No content found.</p>'
        if 'title' not in self:
            self['title'] = 'no title'
        if 'stylesheets' not in self:
            self['stylesheets'] = ['']
        if 'editor' not in self:
            self['editor'] = 'WYSIWYG'
        if 'keywords' not in self:
            self['keywords'] = ''
        if 'description' not in self:
            self['description'] = ''
        self.save()
        form = {'title':'Modifier le contenu de la page',
                'submit':'Modifier',
                'fields':[
                    {'name': 'stylesheets','title':_('Feuilles de style'),'dataType': 'TEXT', 'formType': 'TEXTAREA','value': karacos.json.dumps(self['stylesheets'])},
                    {'name':'title', 'title':_('Titre'), 'dataType': 'TEXT', 'value': self['title']},
                    {'name': 'keywords','title':_('Mots clef SEO'),'dataType': 'TEXT','value': self['keywords']},
                    {'name': 'description','title':_('Description SEO'),'dataType': 'TEXT', 'formType': 'TEXTAREA','value': self['description']},
                    {'name':'content', 'title':_('Contenu'), 'dataType': 'TEXT', 'formType': self['editor'], 'value': self['content']},
                    {'name':'lang', 'title':_('Langage'), 'dataType': 'TEXT', 'value': self.get_default_site_language()}
                    
                        ]}
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,title=None,content=None,stylesheets=None, description=None, keywords=None, lang=None):
        """
        Basic content modification for MDomain
        """
        self._update_item()
        self.log.info("EDIT CONTENT %s" % {title:content})
        self['content'] = content
        self['title'] = title
        self['description'] = description
        self['keywords'] = keywords
        assert isinstance(stylesheets,basestring)
        self['stylesheets'] = karacos.json.loads(stylesheets)
        self.save()
        return {'status':'success', 'message':_("Contenu modifi&eacute;"),'data':{}}
    edit_content.get_form = _get_edit_resource_content_form
    edit_content.label = _('Modifier la page')