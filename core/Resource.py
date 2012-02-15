'''
Created on 13 janv. 2010

@author: nico
'''
import sys
import karacos
import re

class Resource(karacos.db['WebNode']):
    '''
    Basic resource,
    Features :
        is commentable
        RDF resource
    '''
    def __init__(self,parent=None,base=None,data=None):
        karacos.db['WebNode'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        assert isinstance(parent.__domain__,karacos.db['MDomain'])
        # some code... avoid bad url name...
        # data['name'] = re.sub('[^a-z0-9]','_',data['name'].lower())
        if 'WebType' not in data:
            data['WebType'] = 'Resource'
        return karacos.db['WebNode'].create(parent=parent,base=base,data=data)
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_comments__(self):
        """
        function(doc) {
            if (doc.parent_id == "%s" && doc.WebType == "Comment" && !("_deleted" in doc && doc._deleted == true)) {
                if (doc.status == "public")
                    emit(doc._id,doc)
                }
            }
        """
    
    def _get_comments(self):
        """
        """
        result = {}
        try:
            childs = self.__get_comments__()
            for child in childs:
                    
                result[child.value['creation_date']] = {'name':child.value['name'],
                                     'pseudo':child.value['pseudo'],
                                     'comment':child.value['comment'],
                                     'creation_date':child.value['creation_date']}
                if 'ip' in child.value :
                    result[child.value['creation_date']]['ip'] = child.value['ip']
                if 'website' in child.value :
                    result[child.value['creation_date']]['website'] = child.value['website']
                if 'email' in child.value :
                    result[child.value['creation_date']]['email'] = child.value['email']
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'warn')
        return result
    
    @karacos._db.isaction
    def get_comments(self):
        """
        Returns all comments of resource
        """
        
        return self._get_comments()
    
    @karacos._db.isaction
    def get_comment_action(self):
        return {'label': _("Commenter"), 'action':'add_comment', 'acturl':self.get_relative_uri(),
          'form': self._add_comment_form() }
    
    
    @karacos._db.isaction
    def create_resource(self,name=None):
        # TODO: String encoding (for utf-8 problems)
        data = {'name': name}
        result = self._create_child_node(data=data,type='Resource',base=False)
    create_resource.label = _("Creer une resource")
    create_resource.form = {'submit': _('Commenter'), 'title': _("Ajouter un commentaire"),
                            'fields':  [{'name':'name', 'title':_('Nom de la resource'), 'dataType': 'TEXT'}] }
    @karacos._db.isaction
    def add_comment(self,*args,**kw):   
        self.__domain__._update_item()
        try:
            message = ""
            if self.__domain__.get_user_auth()['name'] == self.__domain__._get_anonymous_user()['name']:
                assert len(kw) == 4, "Invalid argument count"
                assert 'email' in kw
                if not karacos.core.mail.valid_email(kw['email']):
                    return {'status': 'error','message': 'Email incorrect', 'error': {'email':'Incorrect'}}
                # TODO: validation du email quand comment
                kw['status'] = "to_validate" # Anonymous comment is moderated "a priori"
                message = "Commentaire enregistre, il sera valide par l'administrateur"
            else: # user is authenticated
                message = "Commentaire enregistre, et publie"
                assert len(kw) == 1
            self.log.debug("add_comment keywords : %s" % len(kw))
            assert 'comment' in kw
            #assert 'title' in kw
            kw['name'] = 'CMT%s' % len(self.__childrens__.keys())
            kw['ip'] = karacos.serving.get_request().remote_addr
            if 'pseudo' not in kw:
                user = self.__domain__.get_user_auth()
                if 'pseudo' not in user:
                    kw['pseudo'] = user['name'].split('@')[0]
            if 'website' in kw:
                # TODO: better url verification hint
                if not kw['website'].startswith("http://"):
                    del kw['website']
            result = self._create_child_node(data=kw,type='Comment',base=False)
            if result['status'] != 'public':
                data = {'ref_db': self.base.id,
                    'ref_id': result.id,
                    'type': 'CommentWfItem'
                    }
                manager = self.__domain__.get_manager_node()
                manager._create_workflow_item(data)
            
            return {'status': 'success', 'data': result, 'message': message}
        except Exception, e:
            self.log.log_exc(sys.exc_info(),'warn')
    add_comment.label = _("Commenter")
    
    def _add_comment_form(self):
        fieldlist = []
        if not karacos.serving.get_session().is_authenticated():
            fieldlist.append({'name':'pseudo', 'title':_('Pseudonyme'), 'dataType': 'TEXT'})
            fieldlist.append({'name':'email', 'title':_("Email (ne sera pas publiee)"), 'dataType': 'TEXT'})
            fieldlist.append({'name':'website', 'title':_('Site web (facultatif)'), 'dataType': 'TEXT'})
        fieldlist.append({'name':'comment', 'title':_('Commentaire'), 'dataType': 'TEXT', 'formType': 'TEXTAREA'})
        return {'fields': fieldlist, 'submit': _('Commenter'), 'title': _("Ajouter un commentaire") }
        
    add_comment.get_form = _add_comment_form      
    
    def set_editor_form(self):
        if 'editor' not in self:
            self['editor'] = 'WYSIWYG'
            self.save()
        form = {'title':'Modifier le contenu de la page',
                       'submit':'Modifier',
                       'fields':[
                      {'name':'editor', 'title':_('Editeur'), 'dataType': 'TEXT', 'value': self['editor']},
                        ]}
        return form
    
    @karacos._db.isaction
    def set_editor(self, editor=None):
        """
        """
        assert editor in ['WYSIWYG','WYSIWYM','TEXTAREA']
        self['editor'] = editor
        self.save()
    set_editor.get_form = set_editor_form 
           
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
                    {'name':'content', 'title':_('Contenu'), 'dataType': 'TEXT', 'formType': self['editor'], 'value': self['content']}
                        ]}
        
        return form
    
    @karacos._db.isaction
    def edit_content(self,title=None,content=None,stylesheets=None, description=None, keywords=None):
        """
        Basic content modification for Resource
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
    
    def _publish_node(self):
        karacos.db['WebNode']._publish_node(self)
        self['ACL']['group.everyone@%s' % self.__domain__['name']].append("add_comment")
        self['ACL']['group.everyone@%s' % self.__domain__['name']].append("get_comments")
        self.save()
    
    @karacos._db.isaction
    def publish_node(self):
        self._publish_node()
    
    def get_instance_template_uri(self):
        try:
            if 'resource_template' in self:
                template = self.__domain__.lookup.get_template(self['resource_template'])
                return self['resource_template']
        except:
            self.log.info("Template %s for resource %s[%s] doesn't exist" % (self['resource_template'],
                                                        self['name'], self.id) )
            pass
        return karacos.db['WebNode'].get_instance_template_uri(self)
    
    def _get_set_instance_template_uri_form(self):
        uri = ""
        if 'resource_template' in self:
            uri = self['resource_template']
        return {'title':_('Modify page template'),
                'submit':_('Modify'),
                'fields':[
                    {'name': 'template_uri','title':_('Template URI'),'dataType': 'TEXT', 'value': uri},
                    ]}
         
    @karacos._db.isaction
    def set_instance_template_uri(self,template_uri=None):
        try:
            template = self.__domain__.lookup.get_template(template_uri)
            self['resource_template'] = template_uri
            self.save()
            return {"status": "success", "message":_("Template changed successfully")}
        except:
            return {"status": "failure", "message":_("Template doesn't exist")}
    set_instance_template_uri.label = _("Set instance template")
    set_instance_template_uri.get_form = _get_set_instance_template_uri_form
    
    @karacos._db.isaction
    def _update(self,*args, **kw):
        if 'title' not in self and 'title' in kw:
            self['title'] = ""
        if 'content' not in self and 'content' in kw:
            self['content'] = ""
        return self._update_(*args, **kw)
    
    def _add_semantic_tag(self,tag_name=None):
        """
        Semantic Tags for resource, it's meaning
        """
        assert isinstance(tag_name,basestring)
        data = {'name':tag_name}
        tag = self._create_child_node(data=data,type='SemanticTag',base=False)