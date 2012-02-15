define('menestrel/BlogMenu.toolkit-jquery-ui',
		['jquery'], function($) {
	var 
		auth,
		karacos,
		blog,
		Blog = function(options) {
			this.options = $.extend({},{
				blogContainer: "#main",
				blogUrl: "/blog",
				menuContainer: "#blogMenu",
				template: '<div class="unpublished_entry" typeof="karacos:Entry" \
									about="" name=""> \
					<h2 property="title">Nouveau message</h2> \
					<span class="updated">Last Updated: <a href="#">.</a></span> \
					<div class="paragraphblock" property="content"><p>Texte</p></div> \
					<div class="comments_bloc" comments_allowed="false"></div> \
				</div>',
				actionwindow: undefined
			},options);
			
			this.initContainers();
			this.initButtons();
			this.initEntries();
			
			this.blogContainer.prepend(this.createEntryButton);
			this.blogContainer.prepend(this.draftsButton);
		};
	$.extend(Blog.prototype, {
		/**
		 * Init menuContainer and BlogContainer
		 */
		'initContainers': function() {
			if (typeof this.options.menuContainer === "string") {
				this.menuContainer = $(this.options.menuContainer);
			} else {
				// check for jQuery object...
				this.menuContainer = this.options.menuContainer;
			}
			
			if (typeof this.options.blogContainer === "string") {
				this.blogContainer = $(this.options.blogContainer);
			} else {
				// check for jQuery object...
				this.blogContainer = this.options.blogContainer;
			}
		},
		/**
		 * Init default buttons
		 */
		'initButtons': function() {
			this.createEntryButton = $('<button class="create_entry_button">Cr&eacute;er Billet</button>');
			this.publishButton = $('<button class="publish_button">Publier</button>');
			this.unpublishButton = $('<button class="unpublish_button">Retirer</button>');
			this.saveButton = $('<button class="save_button">Sauvegarder</button>');
			this.editButton = $('<button class="edit_button">Modifier</button>');
			this.deleteButton = $('<button class="delete_button">Supprimer</button>');
			this.draftsButton =  $('<button class="drafts_button">Brouillons</button>');
			this.allowCommentsButton =  $('<button class="drafts_button">Activer les commentaires</button>');
			this.disallowCommentsButton =  $('<button class="drafts_button">Désactiver les commentaires</button>');
			this.editButton.button({
				text: false,
				icons: {
					primary: "ui-icon-pencil"
				}
			}).click(this.getEditClikHandler());
			this.saveButton.button({
				text: false,
				icons: {
					primary: "ui-icon-disk"
				}
			}).click(this.getSaveClickHandler());
			this.publishButton.button().click(this.getPublishClickHandler());
			this.unpublishButton.button().click(this.getUnpublishClickHandler());
			this.createEntryButton.button().click(this.getcreateClickHandler());
			this.draftsButton.button().click(this.getDraftsClickHandler());
			this.allowCommentsButton.button().click(this.getAllowCommentsClickHandler());
			this.disallowCommentsButton.button().click(this.getDisallowCommentsClickHandler());
			this.deleteButton.button({
				text: false,
				icons: {
					primary: "ui-icon-trash"
				}
			}).click(this.getDeleteClickHandler());;
		},
		/**
		 * Add entry to toolbar
		 */
		'addEntryToolbar': function(entry) {
			var
				toolbar = $('<span style="float:right;padding: 3px 4px;" class="entry_toolbar ui-widget-header ui-corner-all" ></span>'),
				tbContainer = $('<div style="font-size:10px; float:right;width: 100%;"></div>');
			tbContainer.append(toolbar);
			entry.append(tbContainer);
			toolbar.editButton = this.editButton.clone(true);
			toolbar.append(toolbar.editButton);
			toolbar.saveButton = this.saveButton.clone(true);
			toolbar.append(toolbar.saveButton);
			toolbar.deleteButton = this.deleteButton.clone(true);
			toolbar.append(toolbar.deleteButton);
			toolbar.allowCommentsButton = this.allowCommentsButton.clone(true);
			toolbar.append(toolbar.allowCommentsButton);
			toolbar.disallowCommentsButton = this.disallowCommentsButton.clone(true);
			toolbar.append(toolbar.disallowCommentsButton);
			toolbar.unpublishButton = this.unpublishButton.clone(true);
			toolbar.append(toolbar.unpublishButton);
			
			if (entry.find("div.comments_bloc").attr("comments_allowed") === "true") {
				toolbar.disallowCommentsButton.show();
				toolbar.allowCommentsButton.hide();
			} else {
				toolbar.disallowCommentsButton.hide();
				toolbar.allowCommentsButton.show();
			}
			toolbar.editButton.show();
			toolbar.saveButton.hide();
			entry.data("toolbar", toolbar);
			return toolbar;
			
		},
		/**
		 * Init blog entries
		 */
		'initEntries': function() {
			
			var blog = this;
			blog.blogContainer.find('[typeof="karacos:Entry"]').each(function(i,e) {
				blog.addEntryToolbar($(e));
			});
		},
		/**
		 * Init Blog actions
		 */
		'initActions': function() {
			if (auth.hasAction('view_unpublic_entries')) {
				
			}
		},
		/**
		 * 
		 */
		'getViewUnpublicEntries': function() {
			//TODO : prevent multiple instances
			var item = KaraCos('<li><button>Brouillons</button></li>');
			item.find('button').button().click(function() {
					
			});
		},
		/**
		 * 
		 */
		'enableEntryEdit': function(entry) {
			karacos.activate_aloha(function() {
				var toolbar = entry.data("toolbar");
				Aloha.bind('aloha-ready',function(){				
					entry.find('[property]').aloha();
				});
				try {
					toolbar.editButton.hide();
					toolbar.saveButton.show();
					if (typeof toolbar.publishButton !== "undefined") {
						toolbar.publishButton.button("disable");
					}
				} catch(e) {}
				
			});
		},
		'prependEditEntry': function(entry) {
			this.blogContainer.prepend(entry);
			this.blogContainer.prepend(this.draftsButton);
			this.blogContainer.prepend(this.createEntryButton);
			this.enableEntryEdit(entry);
		},
		'findEntry': function(name) {
			return this.blogContainer.find('[name="'+name+'"]');
		},
		'getEditClikHandler': function(callback) {
			var blog = this;
			return function(e) {
					blog.enableEntryEdit($(this).closest('[typeof="karacos:Entry"]'));
			}
		},
		'getcreateClickHandler': function(callback) {
			var
				blog = this;
			return function(e) {
				var
					entry = $(blog.options.template), 
					toolbar;
				entry.attr("about", "urn:uuid:new_entry");
				toolbar = blog.addEntryToolbar(entry);
				toolbar.publishButton = blog.publishButton.clone(true);
				toolbar.append(toolbar.publishButton);
				toolbar.unpublishButton.hide();
				blog.prependEditEntry(entry);
			}
		},
		'getUnpublishClickHandler': function(){
			var
				blog = this;
			return function(e) {
				var
					$this = $(this),
					entry = $this.closest('[typeof="karacos:Entry"]'),
					toolbar = entry.data("toolbar");
				karacos.action({ method: "unpublish",
					url: blog.options.blogUrl + "/" + entry.attr('name'),
					params: {},
					callback: function(data) {
						toolbar.unpublishButton.hide();
						toolbar.publishButton = blog.publishButton.clone(true);
						toolbar.append(toolbar.publishButton);
						entry.addClass('unpublished_entry');
					}
				});
			}
		},
		/**
		 * Disable comments add feature for an entry
		 */
		'getDisallowCommentsClickHandler': function(){
			var
				blog = this;
			return function(e) {
				var
					$this = $(this),
					entry = $this.closest('[typeof="karacos:Entry"]'),
					toolbar = entry.data("toolbar");
				karacos.action({ method: "disallow_comments",
					url: blog.options.blogUrl + "/" + entry.attr('name'),
					params: {},
					callback: function(data) {
						toolbar.disallowCommentsButton.hide();
						toolbar.allowCommentsButton.show();
					}
				});
			}
		},
		/**
		 * Disable comments add feature for an entry
		 */
		'getDeleteClickHandler': function(){
			var
				blog = this;
			return function(e) {
				var
					$this = $(this),
					entry = $this.closest('[typeof="karacos:Entry"]');
				karacos.action({ method: "delete",
					url: blog.options.blogUrl + "/" + entry.attr('name'),
					params: {},
					callback: function(data) {
						if (data.success) {
							entry.remove();
						}
					}
				});
			}
		},
		/**
		 * Allow everyone to post comments
		 */
		'getAllowCommentsClickHandler': function(){
			var
				blog = this;
			return function(e) {
				var
					$this = $(this),
					entry = $this.closest('[typeof="karacos:Entry"]'),
					toolbar = entry.data("toolbar");
				karacos.action({ method: "allow_comments",
					url: blog.options.blogUrl + "/" + entry.attr('name'),
					params: {},
					callback: function(data) {
						toolbar.disallowCommentsButton.show();
						toolbar.allowCommentsButton.hide();
					}
				});
			}
		},
		'getDraftsClickHandler': function() {
			var
				blog = this,
				actionwindow = blog.options.actionwindow;
			return function(e) {
				KaraCos.action({
					method: "view_unpublic_entries",
					url: blog.options.blogUrl,
					async: false,
					params: {"number": 5, "first":0},
					callback: function(data) {
						if (data.success) {
							if (typeof actionwindow === 'undefined' || (typeof actionwindow !== 'undefined' && actionwindow.length === 0)) {
								actionwindow = $('<div></div>');
								$('body').append(actionwindow);
							}
							actionwindow.empty();
//							// displays a control box with a lost of unpublished entries
							$.each(data.data,function(i, entry) {
								var 
									entryItem = $('<li><a href="'+entry.name+'">'+entry.title+'</a></li>');
								entryItem.find('a').data("entry",entry);
								actionwindow.append(entryItem);
							});
							actionwindow.find('a').click(function modifyEntry(e) {
								var
									$this = $(this),
									entry, toolbar,
									entryData = $this.data("entry");
								e.preventDefault();
								e.stopImmediatePropagation();
								if (blog.findEntry(entryData.name).length > 0) {return;}
								entry = $(blog.options.template);
								entry.attr("name", entryData.name);
								entry.attr("about", "urn:uuid:" + entryData._id);
								entry.find('[property="title"]').empty().append(entryData.title);
								entry.find('[property="content"]').empty().append(entryData.content);
								entry.find('a').attr("href", blog.options.blogUrl + "/"+entryData.name).text(entryData._id);
								
								toolbar = blog.addEntryToolbar(entry);
								toolbar.publishButton = blog.publishButton.clone(true);
								toolbar.append(toolbar.publishButton);
								toolbar.publishButton.button("disable");
								toolbar.unpublishButton.hide();
								blog.prependEditEntry(entry);
							});
							actionwindow.dialog({
							width: '400px',
							modal: false,
							position: ['left','top']});
						}
					}
				});
			}
		},
		/**
		 * 
		 */
		'getPublishClickHandler': function(callback) {
			var blog = this;
			return function(e) {
				var 
					$this = $(this),
					entry = $this.closest('[typeof="karacos:Entry"]'),
					toolbar = entry.data("toolbar");
				karacos.action({ method: "publish",
					url: blog.options.blogUrl + "/" + entry.attr('name'),
					params: {},
					callback: function(data) {
						//
						entry.removeClass("unpublished_entry");
//						entry.css({
//							"border": "",
//							"background-color": ""
//						});
						toolbar.publishButton.hide();
						toolbar.unpublishButton.show();
						if (typeof callback === "function") {
							callback(data);
						}
					}
				});
			};
		}, 
		'getSaveClickHandler': function(callback) {
			var blog = this;
			return function(e) {
				var 
					$this = $(this),
					entry = $this.closest('[typeof="karacos:Entry"]'),
					toolbar = entry.data("toolbar"),
					createEntry = (entry.attr('name') === ""),
					handleSaveResponse = function(data) {
						entry.find('[property]').mahalo();
						if (createEntry) {
							entry.find('a').attr("href", blog.options.blogUrl +  "/"+data.data.name).text(data.data._id);
							entry.attr('name', data.data.name);
						}
						if (typeof toolbar.publishButton !== "undefined") {
							toolbar.publishButton.button("enable");
						}
						toolbar.editButton.show();
						toolbar.saveButton.hide();
						if (typeof callback === "function") {
							callback(data);
						}
					},
					options = {'callback': handleSaveResponse};
				if (createEntry) {
					options['method'] = "create_entry";
					options['url'] = blog.options.blogUrl;
				} else {
					options['method'] = "_update";
					options['url'] = blog.options.blogUrl + "/" + entry.attr('name');
				}
				options['params'] = {};
				entry.find('[property]').each(function(i,e){
					var $e = $(e);
					options['params'][$e.attr("property")] = $e.html();
				});
				
				karacos.action(options);
			};
		}
	});
	$('body').bind('kcauth', function(){
		karacos = KaraCos;
		auth = karacos.authManager;
	});
	
	return Blog;
});
