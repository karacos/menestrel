	GENTICS.Aloha.settings = {
	   'i18n' : {
	     'current' : 'fr'
	   },
	   'base' : 'http://${instance.__domain__['fqdn']}/_browser/aloha/',
	   'ribbon' : true,
	   'plugins': {
	   				"org.karacos.aloha.Plugin": { 
	   				instance_url : "http://${instance.__domain__['fqdn']}${instance._get_action_url()}",
	   				% if isstaff:
		   				edit_content_action : "edit_content",
		   			% endif
	   				idfieldsref : {
							resource_title	: "title",
							resource_content 	: "content"
					  	}},
					"com.gentics.aloha.plugins.Link": {
								config : [ 'a' ],
							  	editables : {
								'#resource_title'	: [  ]
							  	},
							  	targetregex : '^(?!.*${instance.__domain__['fqdn']}).*',
							  	target : '_blank',
							  	},
					"com.gentics.aloha.plugins.List": {
						editables : {
								'#resource_title'	: [  ]
							  	}
					},
					"com.gentics.aloha.plugins.Table": {
						editables : {
								'#resource_title'	: [  ]
							  	}
					},
		   			"com.gentics.aloha.plugins.Format": { 
						config : [ 'b', 'i','u','del','sub','sup', 'p', 'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'pre', 'removeFormat'],
					  	editables : {
							'#resource_title'	: [ ], // no formatting allowed
							'#resource_content' 	: [ 'b', 'i', 'u', 'del', 'sub', 'sup','removeFormat', 'h2','h3'  ] // just basic formattings, no headers, etc.
					  	}
					} // plugin
				} // plugins
				
		}; //Aloha.Settings
		
		$("#resource_title").aloha();
		$("#resource_content").aloha();