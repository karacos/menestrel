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
(function ResourceSubMenu(submenu){
	var 
		item,
		actionwindow = KaraCos.actionWindow;
	if (auth.hasAction('publish_node')) {
		item = $('<li><button>Publier</button></li>');
		item.find('button').button().click(actionsMenu.getActionButtonHandler("${instance._get_action_url()}",'publish_node'));
		submenu.append(item);
	}
})(submenu);

<%include file="/includes/actionmenu/WebNode.js"/>
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