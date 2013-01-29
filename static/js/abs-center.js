// Center the login box vertically and horizontally on the page
// Don't center on page load, offload to Google Web Fonts script
$(document).ready(function(){
	$(window).resize(function(){
		items = $('#loginmaster');
		// This modulo business fixes a problem with sub-pixel rendering: when
		// the window is an odd size, the Log In button doesn't line up with the
		// text boxes. This forces the window measured height to always be even.
		var topPos = ($(window).height() - $('.abs-center').outerHeight()) / 2;
		var topModulo = topPos % 2;
		var topPosFix = topPos - topModulo;
		items.css({
			position:'absolute',
			left: ($(window).width() - $('.abs-center').outerWidth()) / 2,
			top: topPosFix
		});
		// fade in login box once it's rendered
		items.fadeIn('slow');
	});
});