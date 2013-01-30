// Center the login box vertically and horizontally on the page
// Don't center on page load, offload to Google Web Fonts script
$(document).ready(function(){
    $(window).resize(function(){
        items = $('#loginmaster');
        var topTemp = ($(window).height() - $('.abs-center').outerHeight()) / 2;
        topTemp = topTemp - topTemp % 2;
        items.css({
            position:'absolute',
            left: ($(window).width() - $('.abs-center').outerWidth()) / 2,
            top: topTemp
        });
        // fade in login box once it's rendered
        items.fadeIn('slow');
    });
});