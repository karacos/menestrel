function createCommentsObject(){
	KaraCos.comments = {
		'initialize': function(res_url,container) {
			if (KaraCos.auth.hasAction('get_comments')) {
				KaraCos.action({
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
		}
	}
}
require(["karacos/jquery"],function($){
	$('body').bind('karacosCoreLoaded', function(){
		KaraCos(function(){
			if (typeof KaraCos.comments === "undefined") {
				createCommentsObject();
			}
		})
	});
});