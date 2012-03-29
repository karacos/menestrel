define("menestrel/BlogMenu.toolkit-jquery-ui",
		['jquery',
		 'menestrel/libs/div-carousel-nka',
		 'menestrel/libs/jquery.mousewheel'],
			function($,topbar, shoppingCart) {
				$(function() {
					var menu = $("#carousel1"),
						imgs = menu.find("img.cloudcarousel"),
						countimg = 0,
						spires = $("#Spires"),
						$body = $("body")
						setSize = function(elem) {
							var $elem = $(elem), ratio;
							if (typeof $elem.data("origSize") === "undefined") {
								$elem.data("origSize", {width: $elem.width(), height: $elem.height()})
							}
							// reset to original size
							
							//$elem.attr("width", "");//$elem.attr("height", "");
							//$elem.css("width","");//$elem.css("height", "");
							//$elem.css("max-width","");
							//menu.height(Math.ceil(menu.width()/1.42))
							ratio = menu.width() / $elem.innerWidth();
							$elem.css("max-width",menu.width() / 4 );
							$elem.css("max-height",menu.width() / 8 );
							//$elem.width(Math.ceil(menu.width() / 2) );
							//menu.css("margin-top", (window.screen.availHeight - menu.outerHeight()) / 2);
							//$elem.height(Math.ceil($elem.innerHeight() * ratio));
						},
						setBodySizes = function(){
							var top_container_additional_margin = window.screen.availHeight - $('#Spires').outerHeight();
							if (top_container_additional_margin < 0) {
								top_container_additional_margin = 0;
							}
							top_container_additional_margin = top_container_additional_margin / 6;
							$body.css("font-size", Math.ceil($("body").width()/100));
							//$("#carousel_alt_text_wrap").css("margin-top",($("body").width() * 0.8 / 1141 * 64));
							$("#carousel_alt_text_wrap").css("top", "15%");
							$('.carousel_wrap').css({"height": window.screen.availHeight/100 * 60 + "px"});
							$(".top_container").css("margin-top", ($("body").width() * 0.8 / 1141 * 64) + top_container_additional_margin );
//							
						},
						loadCarousel = function() {
							var topMargin, carouselControls;
							countimg = countimg + 1;
							if (countimg >= imgs.length) {
								//menu.height(Math.ceil(menu.width()/1.42));
								topMargin = $(".top_container").css("margin-top");
								topMargin = Number(topMargin.substr(0,topMargin.length - 2));
								
								menu.CloudCarousel(		
										{			
											xPos: Math.ceil(menu.width()/2),
											yPos: Math.ceil((menu.width()/9.6) + topMargin),
											yRadius: Math.ceil(menu.width()/18),
											buttonLeft: $("#left-but img"),
											buttonRight: $("#right-but img"),
											altBox: $("#carousel_alt_text"),
											titleBox: $("#carousel_title_text"),
											mouseWheel: true,
											//reflHeight: Math.ceil(menu.width()/15.36),
											bringToFront: true
										}
								);
								carouselControls = $("#carouselControls");
								carouselControls.find("div.carouselControl .pressed").hide();
								carouselControls.find("div.carouselControl").bind("mousedown", function(e){
									var $this = $(this);
									carouselControls.find("div.carouselControl .pressed").hide();
									carouselControls.find("div.carouselControl .unpressed").show();
									$this.find(".unpressed").hide();
									$this.find(".pressed").show();
									window.setTimeout(function(){
										$this.find(".pressed").hide();
										$this.find(".unpressed").show();
									}, 1000);
								});
								
								menu.bind("rotateStop", function(e, item){
									try {
										$("#carousel_alt_text").empty().append($(item.image).attr("alt"));
									} catch (e) {}
								});
							}
						};
					
						$body.css('background-color', "black");
					
					setBodySizes();
					$(window).resize(function () {
						topbar.resize();
						var controler = menu.data("cloudcarousel"), topMargin,
							imgs = menu.find("img.cloudcarousel"), item, ratio,
							itemsLen, $img, orig;
						topMargin = $(".top_container").css("margin-top");
						topMargin = Number(topMargin.substr(0,topMargin.length - 2));
						setBodySizes();
						imgs.each(function(i, e) {
//								setSize(e);
							});
						if (typeof controler !== "undefined") {
							topMargin = $(".top_container").css("margin-top");
							topMargin = Number(topMargin.substr(0,topMargin.length - 2));
							controler.xRadius = Math.ceil(menu.width()/2.3);
							controler.yRadius = Math.ceil(menu.width()/18);
							controler.xCentre = Math.ceil(menu.width()/2);
							controler.yCentre = Math.ceil((menu.width()/9.6) + topMargin);
							for (var i = 0; i<controler.items.length ;i++)
				            {
				                item = controler.items[i];
				                $img=$(item.image);
				                orig = $img.data("origSize");
				                
//				                if (orig.width >= orig.height) {
//				                	item.orgWidth = menu.width() / 8;
//				                	ratio = orig.width / item.orgWidth;
//				                	item.orgHeight = orig.height / ratio;
//				                } else {
				                	item.orgHeight = menu.width() / 8;
				                	ratio = orig.height / item.orgHeight;
				                	item.orgWidth = orig.width / ratio;
//				                }
				                $img.css("max-width",item.orgWidth);
				                $img.css("max-height",item.orgHeight);
//				                $elem.css("max-width",menu.width() / 4 );
//								$elem.css("max-height",menu.width() / 8 );
				                 
				            }
							controler.updateAll();
						}
					});
					if (imgs.length === 0) {
						loadCarousel();
					}
					imgs.each(function(i, e) {
						setSize(e);
						if (e.complete !== undefined && e.complete === true) {
							$(e).data("complete", true);
							loadCarousel();
						}
						e.onloadend = function() {
								setSize(e);
								$(e).data("complete", true);
								loadCarousel();
							};
					});
					
				});
			});