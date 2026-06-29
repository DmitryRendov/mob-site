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


    var containerEl = document.querySelector('.mob-projects');
    if (containerEl) {
        var mixer = mixitup(containerEl, {
                classNames: {
                    block: 'mob-projects',
                    elementFilter: 'controls',
                },
                load: {
                    sort: 'published-date:desc'
                },
                animation: {
                    effects: 'fade translateZ(-100px)'
                }
            });
    }

    // cookies consent
    if (!sessionStorage.getItem('cookieConsentGDPR')) {
        $('#cookieConsentGDPR').show();
    }

    $('#cookieConsentNecessary').on('click', function() {
        sessionStorage.setItem('cookieConsentGDPR', JSON.stringify({necessary: true, analytics: false, marketing: false}));
        $('#cookieConsentGDPR').alert('close');
    });

    $('#cookieConsentAcceptAll').on('click', function() {
        sessionStorage.setItem('cookieConsentGDPR', JSON.stringify({necessary: true, analytics: true, marketing: true}));
        $('#cookieConsentGDPR').alert('close');
    });

    $('#cookieConsentSettings').on('click', function() {
        $('#cookieSettingsModal').modal('show');
    });

    $('#saveCookieSettings').on('click', function() {
        var analytics = $('#analyticsCookies').is(':checked');
        var marketing = $('#marketingCookies').is(':checked');
        sessionStorage.setItem('cookieConsentGDPR', JSON.stringify({necessary: true, analytics: analytics, marketing: marketing}));
        $('#cookieConsentGDPR').alert('close');
    });

}); 