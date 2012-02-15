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
import re, datetime
#from anydbm import result
json = karacos.json
class Blog(karacos.db['EntriesHolder']):
    '''
    Blog resource
    '''
    
    def __init__(self,parent=None,base=None,data=None):
        #assert isinstance(domain,karacos.db['Domain']), "domain in not type Domain"
        karacos.db['WebNode'].__init__(self,parent=parent,base=base,data=data)

    @staticmethod
    def create(parent=None, base=None,data=None):
        assert isinstance(data,dict)
        if 'WebType' not in data:
            data['WebType'] = 'Blog'
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
    def _get_create_entry_form(self):
        form = {'title': _("Creer un message"),
         'submit': _('Ajouter'),
         'fields': [{'name':'name', 'title':_('Nom'),'dataType': 'TEXT'},
                    {'name':'title', 'title':_('Titre'),'dataType': 'TEXT'},
                    {'name':'content', 'title':_('Message'),'dataType': 'TEXT', 'formType': 'TEXTAREA'},
                 ] }
        return form
    
    @karacos._db.isaction
    def create_entry(self,*args,**kw):
        """
        Create a blog entry
        """
        rx = re.compile('\W+')
        name = rx.sub('', kw['title']).strip()
        kw['name'] = "%s-%s" % (datetime.datetime.now().strftime('%Y%m%dT%H%M'),name)
        entry = self._create_child_node(data=kw,type='Entry',base=False)
        return {"success": True,
                "data": {
                         "name": kw['name'],
                         "id": entry.id}
                }
    create_entry.get_form = _get_create_entry_form
    create_entry.label = _("Creer message")
    
    
    def _entry_publish(self,entry):
        """
        Triggered action by Entries when published
        """
            
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_public_entries__(self):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (doc.status == "published" && doc.publish_date) {
                  emit(doc.publish_date, doc._id);
                  }
            }
        """
    
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_public_entries_values__(self,*args,**kw):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (doc.status == "published" && doc.publish_date) {
                  emit(doc.publish_date, doc);
                  }
            }
        """
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_unpublic_entries__(self,*args,**kw):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (!(doc.status == "published" && doc.publish_date)) {
                  emit(doc.creation_date, doc._id);
                  }
            }
        """
    @karacos._db.ViewsProcessor.isview('self','javascript')
    def __get_unpublic_entries_values__(self,*args,**kw):
        """
        //
            function(doc) {
             if (doc.parent_id == "%s" && !("_deleted" in doc && doc._deleted == true))
              if (!(doc.status == "published" && doc.publish_date)) {
                  emit(doc.creation_date, doc);
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
    
    def _get_public_entries(self,*args, **kw):
        result = {}
        for item in self.__get_public_entries_values__(*(), **{'descending':True, "limit": 2}):
            result[item.value['publish_date']] = self.db[item.value['_id']]
        return result
    
    def _get_editing_entries(self):
        result = {}
        for item in self.__get_editing_entries__():
            result[item.value['publish_date']] = self.db[item.value['_id']]
        return result
    
    def _get_unpublic_entries(self,number=5, first=0):
        result = []
        for item in self.__get_unpublic_entries__(*(), **{'descending':True, "limit": number,"skip": first}):
            if len(result) <= number:
                result.append(self.db[item.value])
        return result
    
    def _view_last_entries(self,number=5, first=0):
        result = []
        for item in self.__get_public_entries__(*(), **{'descending':True, "limit": number,"skip": first}):
            if len(result) <= number:
                result.append(self.db[item.value])
        return result
    
    @karacos._db.isaction
    def view_last_entries(self,number=5, first=0):
        """
        Return a list of newsletter subscribers
        """
        return {"success": True, 'data':self._view_last_entries(number=int(number),first=int(first))}

    @karacos._db.isaction
    def view_unpublic_entries(self,number=5, first=0):
        """
        List of non-public items
        """
        return {"success": True, 'data':self._get_unpublic_entries(number=int(number),first=int(first))}
    
    @karacos._db.isaction
    def view_unpublic_entries_values(self,number=5, first=0):
        """
        List of non-public items
        """
        return {"success": True, 'data':self._get_unpublic_entries(number=int(number),first=int(first))}
    
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
        return {"success": True, 'message':_("Contenu modifi&eacute;"),'data':{}}
    edit_content.get_form = _get_edit_resource_content_form
    edit_content.label = _('Modifier la page')
    
