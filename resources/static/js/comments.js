define('menestrel/comments',['jquery', 'karacos/main'], function($,karacos) {
	var 
		auth,
		comments = {
				'initialize': function(res_url,container) {
					$('body').bind('kcauth', function() {
						auth = karacos.authManager;
						if (auth.hasAction('get_comments')) {
							karacos.action({
								url: 'res_url',
								action: 'get_comments',
								params: {},
								callback: function(data) {
									$.ajax({
										url: "/fragment/comments_list.jst",
										context: document.body,
										type: "GET",
										cache: false,
										success: function(tmpl) {
											var comments_list_template = jsontemplate.Template(tmpl, KaraCos.jst_options);
											container.empty().append(comments_list_template.expand(data));
										}
									});
								},
								error: function(data) {
									
								}
							});
						}
					});
				}
			};
	$('body').bind('kcready', function(){
		karacos = KaraCos;
		if (typeof karacos.comments === "undefined") {
			karacos.comments = comments;
		}
	});
	return comments;
});