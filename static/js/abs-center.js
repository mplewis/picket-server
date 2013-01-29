// Center any element with .abs-center vertically and horizontally on the page

$(document).ready(function(){
	$(window).resize(function(){
		$('.abs-center').css({
			position:'absolute',
			left: ($(window).width() - $('.abs-center').outerWidth()) / 2,
			top: ($(window).height() - $('.abs-center').outerHeight()) / 2
		});
	});
	// Center on page load
	$(window).resize();
});