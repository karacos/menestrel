//////////////////////////////////////////////////////////////////////////////////
// Carousel Menu enhanced by nka
// (c) 2012 by N Karageuzian <http://nka.menestrel.net/>
// MIT License
// base code : CloudCarousel V1.0.5
// CloudCarousel (c) 2011 by R Cecco. <http://www.professorcloud.com>
// Reflection code based on plugin by Christophe Beyls <http://www.digitalia.be>
//
// Please retain this copyright header in all versions of the software
//////////////////////////////////////////////////////////////////////////////////
define("menestrel/libs/div-carousel-nka",
		['jquery'], function($) {	
	
	// START Reflection object.
	// Creates a reflection for underneath an image.
	// IE uses an image with IE specific filter properties, other browsers use the Canvas tag.	
	// The position and size of the reflection gets updated by updateAll() in Controller.
	function Reflection(img, reflHeight, opacity) {				
		
		var	reflection, cntx, imageWidth = img.width, imageHeight = img.width, gradient, parent;
	
		parent = $(img.parentNode);
		this.element = reflection = parent.append("<canvas class='reflection' style='position:absolute'/>").find(':last')[0];
        if ( !reflection.getContext &&  $.browser.msie) {
			this.element = reflection = parent.append("<img class='reflection' style='position:absolute'/>").find(':last')[0];					
			reflection.src = img.src;			
			reflection.style.filter = "flipv progid:DXImageTransform.Microsoft.Alpha(opacity=" + (opacity * 100) + ", style=1, finishOpacity=0, startx=0, starty=0, finishx=0, finishy=" + (reflHeight / imageHeight * 100) + ")";	
			
        } else {							
			cntx = reflection.getContext("2d");
			try {
				
				
				$(reflection).attr({width: imageWidth, height: reflHeight});
				cntx.save();
				cntx.translate(0, imageHeight-1);
				cntx.scale(1, -1);				
				cntx.drawImage(img, 0, 0, imageWidth, imageHeight);				
				cntx.restore();
				cntx.globalCompositeOperation = "destination-out";
				gradient = cntx.createLinearGradient(0, 0, 0, reflHeight);
				gradient.addColorStop(0, "rgba(255, 255, 255, " + (1 - opacity) + ")");
				gradient.addColorStop(1, "rgba(255, 255, 255, 1.0)");
				cntx.fillStyle = gradient;
				cntx.fillRect(0, 0, imageWidth, reflHeight);				
			} catch(e) {			
				return;
			}		
		}
		// Store a copy of the alt and title attrs into the reflection
		$(reflection).attr({ 'alt': $(img).attr('alt'), title: $(img).attr('title')} );	
				
	}	//END Reflection object

	// START Item object.
	// A wrapper object for items within the carousel.
	var	Item = function(elemIn, options)
	{
		elemIn.data("carouselItem", this);
		this.orgWidth = elemIn.outerWidth();			
		this.orgHeight = elemIn.outerHeight();	
		this.orgFtSz = parseFloat(elemIn.css("font-size"));
		this.elem = elemIn;
		this.reflection = null;					
		this.alt = "";//elemIn.alt;
		this.title = "";//elemIn.title;
		this.options = options;				
		this.isOK = true;				
		
//		if (this.options.reflHeight > 0)
//		{													
//			this.reflection = new Reflection(this.image, this.options.reflHeight, this.options.reflOpacity);					
//		}
		this.elem.css('position','absolute');	// Bizarre. This seems to reset image width to 0 on webkit!		
		
		this.move = function(x, y, scale) {
			var 
				item = this,
				px = 'px',
				options = {
						"width": this.orgWidth * scale,
						"height": this.orgHeight * scale,
						"left": x + px,
						"top": y + px,
						"zIndex": "" + (scale * 100)>>0, // >>0 = Math.foor(). Firefox doesn't like fractional decimals in z-index.
						'font-size': this.orgFtSz * scale
					};
			
			this.elem.css(options);
			if (this.elem.attr("item") === "1") {
				//console.log(scale + " | " + this.orgFtSz + " | " + this.orgFtSz * scale);
			}
			return;
		}
		
	};// END Item object
	
	// Controller object.
	// This handles moving all the items, dealing with mouse clicks etc.	
	var Controller = function(container, elements, options)
	{
		var	funcSin = Math.sin, funcCos = Math.cos, ctx=this, $container = $(container);
		this.items = [];
		this.controlTimer = 0;
		this.stopped = false;
		//this.imagesLoaded = 0;
		this.container = container;
		this.xRadius = options.xRadius;
		this.yRadius = options.yRadius;
		this.showFrontTextTimer = 0;
		this.autoRotateTimer = 0;
		if (options.xRadius === 0)
		{
			this.xRadius = ($container.width()/2.3);
		}
		if (options.yRadius === 0)
		{
			this.yRadius = ($container.height()/6);
		}

		this.xCentre = options.xPos;
		this.yCentre = options.yPos;
		this.frontIndex = 0;	// Index of the item at the front
		
		// Start with the first item at the front.
		this.rotation = this.destRotation = Math.PI/2;
		this.timeDelay = 1000/options.FPS;
								
		// Turn on the infoBox
		if(options.altBox !== null)
		{
			$(options.altBox).css('display','block');	
			$(options.titleBox).css('display','block');	
		}
		// Turn on relative position for container to allow absolutely positioned elements
		// within it to work.
		$container.css({ position:'relative', overflow:'hidden'} );
	
		$(options.buttonLeft).css('display','inline');
		$(options.buttonRight).css('display','inline');
		
		// Setup the buttons.
		$(options.buttonLeft).bind('mouseup',this,function(event){
			event.data.rotate(-1);	
			return false;
		});
		$(options.buttonRight).bind('mouseup',this,function(event){															
			event.data.rotate(1);	
			return false;
		});
		
		// You will need this plugin for the mousewheel to work: http://plugins.jquery.com/project/mousewheel
		if (options.mouseWheel)
		{
			$container.bind('mousewheel',this,function(event, delta) {					 
					 event.data.rotate(delta);
					 return false;
				 });
		}
		elements.bind('touchswipe',function(e,args) {
			
		});
		elements.bind('mouseover click',this,function(event){
			
			clearInterval(event.data.autoRotateTimer);		// Stop auto rotation if mouse over.
			var	$target = $(event.target),
				text = $target.attr('alt'),
				carouselItem;	
			if ($target.hasClass('divcarousel')) {
				carouselItem = $target;
			} else {
				carouselItem = $target.closest('.divcarousel');
			}
			// If we have moved over a carousel item, then show the alt and title text.
		
			if ( text !== undefined && text !== null )
			{
					
				clearTimeout(event.data.showFrontTextTimer);			
				$(options.altBox).html( ($(event.target).attr('alt') ));
				$(options.titleBox).html( ($(event.target).attr('title') ));							
				
			}
			if ( options.bringToFront && event.type == 'click' ){
				
				var	idx = carouselItem.data('itemIndex');	
				var	frontIndex = event.data.frontIndex;
				//var	diff = idx - frontIndex;                    
                var        diff = (idx - frontIndex) % elements.length;
                if (Math.abs(diff) > elements.length / 2) {
                    diff += (diff > 0 ? -elements.length : elements.length);
                }
                
				event.data.rotate(-diff);
			}
		});
		// If we have moved out of a carousel item (or the container itself),
		// restore the text of the front item in 1 second.
		$container.bind('mouseout',this,function(event){
				var	context = event.data;				
				clearTimeout(context.showFrontTextTimer);				
				context.showFrontTextTimer = setTimeout( function(){context.showFrontText();},1000);
				context.autoRotate();	// Start auto rotation.
		});

		// Prevent items from being selected as mouse is moved and clicked in the container.
		$container.bind('mousedown',this,function(event){	
			
			event.data.container.focus();
			//return false;
			// don't return false here, for allowing contenteditable to be selected and modified via aloha (for example)
		});
		//container.onselectstart = function () { return false; };		// For IE.

		this.innerWrapper = $container.wrapInner('<div style="position:absolute;width:100%;height:100%;"/>').children()[0];
	
		// Shows the text from the front most item.
		this.showFrontText = function()
		{	
			if ( ctx.items[this.frontIndex] === undefined ) { return; }	// Images might not have loaded yet.
			$(options.titleBox).html( $(ctx.items[this.frontIndex].image).attr('title'));
			$(options.altBox).html( $(ctx.items[this.frontIndex].image).attr('alt'));				
		};
						
		this.go = function()
		{		
			if(this.controlTimer !== 0) { return; }
			$container.trigger("rotateStart", [this.direction]);
			var	context = this;
			this.controlTimer = setTimeout( function(){context.updateAll();},this.timeDelay);					
		};
		
		this.stop = function(item)
		{
			clearTimeout(this.controlTimer);
			this.controlTimer = 0;
			if (this.frontIndex < 0) {
				this.frontIndex = ctx.items.length + this.frontIndex; 
 			}
			$container.trigger("rotateStop",[ctx.items[this.frontIndex]]);
		};
		
		
		// Starts the rotation of the carousel. Direction is the number (+-) of carousel items to rotate by.
		this.rotate = function(direction)
		{	
			this.direction = direction;
			this.frontIndex -= direction;
			this.frontIndex %= ctx.items.length;					 			
			this.destRotation += ( Math.PI / ctx.items.length ) * ( 2*direction );
			this.showFrontText();
			this.go();			
		};
		
		
		this.autoRotate = function()
		{			
			if ( options.autoRotate !== 'no' )
			{
				var	dir = (options.autoRotate === 'right')? 1 : -1;
				this.autoRotateTimer = setInterval( function(){ctx.rotate(dir); }, options.autoRotateDelay );
			}
		};
		
		/**
		 * This is the main loop function that moves everything.
		 * Revewed for handling div elements or images
		 * 
		 */ 
		this.updateAll = function()
		{											
			var	minScale = options.minScale;	// This is the smallest scale applied to the furthest item.
			var smallRange = (1-minScale) * 0.5;
			var	w,h,x,y,scale,item,sinVal;
			
			var	change = (this.destRotation - this.rotation);				
			var	absChange = Math.abs(change);
	
			this.rotation += change * options.speed;
			if ( absChange < 0.001 ) { this.rotation = this.destRotation; }			
			var	itemsLen = ctx.items.length;
			var	spacing = (Math.PI / itemsLen) * 2; 
			//var	wrapStyle = null;
			var	radians = this.rotation;
			var	isMSIE = $.browser.msie;
		
			// Turn off display. This can reduce repaints/reflows when making style and position changes in the loop.
			// See http://dev.opera.com/articles/view/efficient-javascript/?page=3			
			this.innerWrapper.style.display = 'none';		
			
			var	style;
			var	px = 'px', reflHeight;	
			var context = this;
			for (var i = 0; i<itemsLen ;i++)
			{
				item = ctx.items[i];
								
				sinVal = funcSin(radians);
				
				scale = ((sinVal+1) * smallRange) + minScale;
				
				x = this.xCentre + (( (funcCos(radians) * this.xRadius) - (item.orgWidth*0.5)) * scale);
				y = this.yCentre + (( (sinVal * this.yRadius)  ) * scale);		
		
				if (item.isOK)
				{
					// below, beyond the magic
					item.move(x,y,scale);
//					var	item = item.image;
//					
					// Reflexion don't apply to present reflexion
//					if (item.reflection !== null)
//					{																										
//						reflHeight = options.reflHeight * scale;						
//						style = item.reflection.element.style;
//						style.left = x + px;
//						style.top = y + h + options.reflGap * scale + px;
//						style.width = w + px;								
//						if (isMSIE)
//						{											
//							style.filter.finishy = (reflHeight / h * 100);				
//						}else
//						{								
//							style.height = reflHeight + px;															
//						}																													
//					}					
				}
				radians += spacing;
			}
			// Turn display back on.					
			this.innerWrapper.style.display = 'block';

			// If we have a preceptable change in rotation then loop again next frame.
			if ( absChange >= 0.001 )
			{				
				this.controlTimer = setTimeout( function(){context.updateAll();},this.timeDelay);		
			}else
			{
				
				// Otherwise just stop completely.				
				this.stop(ctx.items[this.frontIndex]);
			}
		}; // END updateAll		
		
		//initialize items index
		for(var i=0;i<elements.length;i++) {	
			var $elem = $(elements[i]);
			if ($elem.data("carouselItem") === undefined) {
				ctx.items.push( new Item( $elem, options ) );	
			}
			$elem.data('itemIndex',i);
		}
		this.autoRotate();	
		this.updateAll();
		//this.tt = setInterval( function(){ctx.checkImagesLoaded();},50);	
	}
	
	// The jQuery plugin part. Iterates through items specified in selector and inits a Controller class for each one.
	$.fn.DivCarousel = function(options) {
		var $this = $(this);
		$this.each( function() {			
			
			options = $.extend({}, {
							   reflHeight:0,
							   reflOpacity:0.5,
							   reflGap:0,
							   minScale:0.5,
							   xPos:0,
							   yPos:0,
							   xRadius:0,
							   yRadius:0,
							   altBox:null,
							   titleBox:null,
							   FPS: 30,
							   autoRotate: 'no',
							   autoRotateDelay: 1500,
							   speed:0.2,
							   mouseWheel: false,
							   bringToFront: false
			},options );									
			// Create a Controller for each carousel.
			if (typeof $this.data('divcarousel') === "undefined") {
				$this.data('divcarousel', new Controller( this, $this.find('.divcarousel'), options) );
			}
		});				
		return this;
	};
	
});