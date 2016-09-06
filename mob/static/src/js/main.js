$(function() {

    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });

    $('img').error(function(){
		$(this).attr('src', '/static/img/image-not-found.png');
	});

    var e = "info";
    var t = "minecraft";
    var n = ".of.by";
    var r = e + '@' + t + n;
    $(".hide-email").attr('href','mailto:' + r).html(r);

}); 