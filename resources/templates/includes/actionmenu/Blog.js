<% import karacos %>
<% import sys, traceback %>
% try:
<% request = karacos.serving.get_request() %>
<% session = karacos.serving.get_session() %>
<% response = karacos.serving.get_response() %>
<% instance = None %>
%try:
	<% instance = response.__instance__ %>
%except:
	
%endtry
% if 'instance_id' in request.str_params and 'base_id' in request.str_params:
<% instance = karacos.base.db[request.str_params['base_id']].db[request.str_params['instance_id']] %>
% endif

% if instance != None:
<% node_actions = instance._get_actions() %>

(function BlogSubMenu(submenu){
//	require(['menestrel/BlogMenu.toolkit-jquery-ui'], function(Blog) {
//		if (typeof KaraCos.blog === "undefined") {
//			KaraCos.blog = new Blog({
//				blogContainer: "#main",
//				blogUrl: "${instance._get_action_url()}",
//				menuContainer: submenu,
//				actionwindow: KaraCos.actionWindow
//			});
//		}
//	})
//	var 
//		item,
//		actionwindow = KaraCos.actionWindow, 
//		entryTemplate = '<div name="unpublished_entry" typeof="karacos:Entry" about="urn:uuid:${instance.id}/new_entry"> \
//							<h2 property="title">Nouveau message</h2> \
//							<span class="updated">Last Updated: <a href="#">.</a></span> \
//							<div class="paragraphblock" property="content"><p>Texte</p></div> \
//						</div>';
//	/* {"method": "view_unpublic_entries",
//		"id": 1,
//		"params":{"number": 5, "first":0}} */
//	if (auth.hasAction('view_unpublic_entries')) {
//		item = KaraCos('<li><button>Brouillons</button></li>');
//		item.find('button').button().click( //actionsMenu.getActionFormButtonHandler("${instance._get_action_url()}",'create_child_node'));
//			function() {
//				KaraCos.action({ method: "view_unpublic_entries",
//					url: "${instance._get_action_url()}",
//					async: false,
//					params: {"number": 5, "first":0},
//					callback: function(data) {
//						if (data.success) {
//							actionwindow.empty();
//							// displays a control box with a lost of unpublished entries
//							$.each(data.data,function(i, entry) {
//								var 
//									entryItem = $('<li><a href="'+entry.name+'">'+entry.title+'</a></li>');
//								entryItem.find('a').data("entry",entry);
//								actionwindow.append(entryItem);
//							});
//							actionwindow.find('a').click(function modifyEntry(e) {
//								var
//									$this = $(this),
//									entry = $('[name="unpublished_entry"]'),
//									entryData = $this.data("entry"),
//									publishButton = $('<button class="publish_button">Publier</button>').button(),
//									saveButton = $('<button class="save_button">Sauvegarder</button>').button();
//								e.preventDefault();
//
//								e.stopImmediatePropagation();
//								if (entry.length === 0) {
//									entry = $(entryTemplate);
//									$("#main").prepend(entry);
//								}
//								entry.css({
//									"border": "1px solid purple",
//									"background-color": "#202020"
//								});
//								entry.find('button').remove();
//								entry.attr("about", "urn:uuid:" + entryData._id);
//								entry.find('[property="title"]').empty().text(entryData.title);
//								entry.find('[property="content"]').empty().text(entryData.content);
//								entry.find('a').attr("href", "${instance._get_action_url()}/"+entryData.name).text(entryData._id);
//								if (entry.find(".publish_button").length === 0) {
//									
//									entry.append(publishButton);
//								}
//								saveButton.click(function(){
//									var params = {};
//									entry.find('[property]').each(function(i,e){
//										var $e = $(e);
//										params[$e.attr("property")] = $e.text();
//										
//									});
//									KaraCos.action({ method: "_update",
//										url: "${instance._get_action_url()}/" + entryData.name,
//										params: params,
//										callback: function(data) {
//											entry.find('[property]').mahalo();
//											publishButton.button("enable");
//											saveButton.button("disable");
//										}
//									});
//								});
//								entry.append(saveButton);
//								KaraCos.activate_aloha(function() {
//									Aloha.bind('aloha-ready',function(){
//										entry.find('[property]').aloha();
//										publishButton.button("disable");
//									});
//								});
//							});
//							actionwindow.dialog({
//								width: '400px',
//								modal: false});
//						}
//					},
//					error: function(data) {
//						
//					}
//				}); // POST form
//			}
//		);
//		submenu.append(item);
//	}
//	if (auth.hasAction('create_entry')) {
//		//TODO: extract method, parameters : item,action_url, action_name, form_template_url
//		// voir MDomain.js
//		item = KaraCos('<li><button>Cr&eacute;er Billet</button></li>');
//		item.find('button').button().click( //actionsMenu.getActionFormButtonHandler("${instance._get_action_url()}",'create_child_node'));
//			function() {
//				var 
//					entry = $(entryTemplate),
//					saveButton = $('<button class="save_button">Sauvegarder</button>').button().click(function(){
//						var params = {};
//						entry.find('[property]').each(function(i,e){
//							var $e = $(e);
//							params[$e.attr("property")] = $e.text();
//						});
//						KaraCos.action({ method: "create_entry",
//							url: "${instance._get_action_url()}",
//							async: false,
//							params: params,
//							callback: function(data) {
//								if (data.success) {
//									entry.find('a').attr("href", "${instance._get_action_url()}/"+data.data.name).text(data.data.id);
//									if (entry.find(".publish_button").length === 0) {
//										publishButton.click(function(e) {
//											actionsMenu.getActionButtonHandler("${instance._get_action_url()}/"+data.data.name,'publish_node')();
//											entry.attr("name","");
//										});
//										entry.append(publishButton);
//										publishButton.button("enable");
//									}
//								}
//							},
//							error: function(data) {
//								
//							}
//						}); // POST form
//					}),
//					publishButton = $('<button class="publish_button">Publier</button>').button();
//				entry.css({
//					"border": "1px solid purple",
//					"background-color": "#202020"
//				});
//				entry.find('button').remove();
//				entry.attr("about", "urn:uuid:${instance.id}/new_entry");
//				entry.append(saveButton);
//				$('#main').prepend(entry);
//				KaraCos.activate_aloha(function() {
//					Aloha.bind('aloha-ready',function(){
//						entry.find('[property]').aloha();
//						publishButton.button("disable");
//					});
//				});
//			}	
//		);
//
//		submenu.append(item);
//		
//	}
	
})(submenu);
<%include file="/includes/actionmenu/Resource.js"/>
% endif
% except:
	some errors :
	<pre>
		${sys.exc_info()}
		---
		%for line in traceback.format_exc().splitlines():
			${line}
		%endfor
	</pre>
% endtry
