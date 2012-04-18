/*! Copyright (c) 2012 Nicolas Karageuzian (http://nico.karageuzian.com)
 * Dual licensed under the MIT (http://www.opensource.org/licenses/mit-license.php)
 * and GPL (http://www.opensource.org/licenses/gpl-license.php) licenses.
 * Code base borrowed from PADICILIOUS (http://padilicious.com/code/touchevents/swipesensejs.html)
 *
 * Version: 0.0.1
 * 
 */

(function($) {
	
var 
	types = ['touchstart','touchend','touchmove','touchcancel'],
	triggerdElement = null,
	curX = 0,
	curY = 0,
	fingerCount = 0,
	handleswipe=false,
	swipedata = {
		startX: 0,
		startY: 0,
		deltaX: 0,
		deltaY: 0,
		horzDiff: 0,
		vertDiff: 0,
		swipeLength: 0,
		swipeAngle: null,
		swipeDirection: null,
	},
	minLength = 72,
	handlers = {
		'touchstart': function(event) {
			// get the total number of fingers touching the screen
			fingerCount = event.touches.length;
			// since we're looking for a swipe (single finger) and not a gesture (multiple fingers),
			// check that only one finger was used
			if ( fingerCount == 1 ) {
				handleswipe = true;
				// disable the standard ability to select the touched object
				event.preventDefault();
				// get the coordinates of the touch
				swipedata.startX = event.touches[0].pageX;
				swipedata.startY = event.touches[0].pageY;
				// store the triggering element ID
				triggerdElement = event.target;
			} else {
				// more than one finger touched so cancel
				handlers.touchCancel(event);
			}
		},
		'touchend': function(event) {
			// check to see if more than one finger was used and that there is an ending coordinate
			if ( fingerCount == 1 && curX != 0 && handleswipe) {
				event.preventDefault();
				// use the Distance Formula to determine the length of the swipe
				swipedata.swipeLength = Math.round(Math.sqrt(Math.pow(curX - swipedata.startX,2) + Math.pow(curY - swipedata.startY,2)));
				// if the user swiped more than the minimum length, perform the appropriate action
				if ( swipedata.swipeLength >= minLength ) {
					caluculateAngle();
					determineSwipeDirection();
					$(this).trigger('touchswipe',[swipedata])
					touchCancel(event); // reset the variables
				} else {
					touchCancel(event);
				}	
			} else {
				touchCancel(event);
			}
		},
		'touchmove': function(event) {
			if ( event.touches.length == 1 && handleswipe) {
				event.preventDefault();
				curX = event.touches[0].pageX;
				curY = event.touches[0].pageY;
			} else {
				touchCancel(event);
			}
		},
		'touchcancel': function(event) {
			handleswipe = false;
			triggerdElement = null;
			fingerCount = 0;
			curX = 0,
			curY = 0,
			swipedata = {
				startX: 0,
				startY: 0,
				deltaX: 0,
				deltaY: 0,
				horzDiff: 0,
				vertDiff: 0,
				swipeLength: 0,
				swipeAngle: null,
				swipeDirection: null,
			};
		}
	};
function caluculateAngle() {
	var X = swipedata.startX-curX;
	var Y = curY-swipedata.startY;
	var Z = Math.round(Math.sqrt(Math.pow(X,2)+Math.pow(Y,2))); //the distance - rounded - in pixels
	var r = Math.atan2(Y,X); //angle in radians (Cartesian system)
	swipedata.swipeAngle = Math.round(r*180/Math.PI); //angle in degrees
	if ( swipedata.swipeAngle < 0 ) { swipedata.swipeAngle =  360 - Math.abs(swipedata.swipeAngle); }
}

function determineSwipeDirection() {
	if ( (swipedata.swipeAngle <= 45) && (swipedata.swipeAngle >= 0) ) {
		swipedata.swipeDirection = 'left';
	} else if ( (swipedata.swipeAngle <= 360) && (swipedata.swipeAngle >= 315) ) {
		swipedata.swipeDirection = 'left';
	} else if ( (swipedata.swipeAngle >= 135) && (swipedata.swipeAngle <= 225) ) {
		swipedata.swipeDirection = 'right';
	} else if ( (swipedata.swipeAngle > 45) && (swipedata.swipeAngle < 135) ) {
		swipedata.swipeDirection = 'down';
	} else {
		swipedata.swipeDirection = 'up';
	}
}
$.event.special.touchswipe = {
		setup: function() {
				for ( var i=types.length; i; )
					if ( this.addEventListener )
						this.addEventListener( types[--i], handler[types[i]], false );
					else
						this['on' + types[--i]] = handler[types[i]];
		},
		
		teardown: function() {
				for ( var i=types.length; i; )
					if ( this.removeEventListener )
						this.removeEventListener(  types[--i], handler[types[i]], false );
					else
						this['on' + types[--i]] = handler[types[i]];
		}
	};
$.fn.extend({
	touchswipe: function(fn) {
		return fn ? this.bind("touchswipe", fn) : this.trigger("touchswipe");
	},
	
	untouchswipe: function(fn) {
		return this.unbind("touchswipe", fn);
	}
});
})(jQuery);