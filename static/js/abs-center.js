// Center the login box vertically and horizontally on the page
// Don't center on page load, offload to Google Web Fonts script
$(document).ready(function(){
	$(window).resize(function(){
		items = $('#loginmaster');
		items.css({
			position:'absolute',
			left: ($(window).width() - $('.abs-center').outerWidth()) / 2,
			top: ($(window).height() - $('.abs-center').outerHeight()) / 2
		});
		// fade in login box once it's rendered
		items.fadeIn('slow');
	});
});