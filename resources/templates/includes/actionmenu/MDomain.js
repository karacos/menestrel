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
<% node_actions = instance.__domain__._get_actions() %>
(function mDomainSubMenu(submenu){
	var 
		item,
		actionwindow = KaraCos.actionMenu.actionWindow;
	% if '_settings' in node_actions:
		item = KaraCos('<li><button>Parametrage</button></li>');
	item.find('button').button().click(actionsMenu.getActionFormButtonHandler("${instance.__domain__._get_action_url()}",'_settings'));
//			function(){
//				KaraCos.getForm({
//					url: "${instance.__domain__._get_action_url()}",
//					form: "_settings",
//					callback: function(data, form) {
//						var create_child_node_template = jsontemplate.Template(form, KaraCos.jst_options);
//						actionwindow.empty().append(create_child_node_template.expand(data));
//						actionwindow.dialog({width: '600px', modal:true,buttons: [{
//							'text': data.form.submit,
//							'click': function() {
//								var params = {},
//									method = '_settings';
//								$.each(actionwindow.find('form').serializeArray(), function(i, field) {
//									if (field.name === "method") {
//										method = field.value;
//									} else {
//										params[field.name] = field.value;
//									}
//								}); // each
//								KaraCos.action({ url: "${instance.__domain__._get_action_url()}",
//									method: method,
//									async: false,
//									params: params,
//									callback: function(data) {
//										if (data.success) {
//											
//											actionwindow.dialog('close');
//											
//										}
//									},
//									error: function(data) {
//										
//									}
//								}); // POST login form
//							}
//						}]}).show();
//					}
//				});
//			});
	submenu.append(item);
	%endif
})(submenu);
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
<%include file="/includes/actionmenu/Domain.js"/>