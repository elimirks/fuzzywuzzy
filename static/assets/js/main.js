/*
	Overflow by HTML5 UP
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var settings = {

		// Full screen header?
			fullScreenHeader: true,

		// Parallax background effect?
			parallax: true,

		// Parallax factor (lower = more intense, higher = less intense).
			parallaxFactor: 10

	};

	skel.breakpoints({
		wide: '(max-width: 1680px)',
		normal: '(max-width: 1080px)',
		narrow: '(max-width: 840px)',
		mobile: '(max-width: 736px)'
	});

	$(function() {
        
        //FUZZY
        var waiting = false
        var matches = {"matches": []}       
        var text = "";
        
        setInterval(function(){
            if (!waiting && !$('#input-box').val().equals("")) {
                waiting = true
                request()
                console.log('request')
            }
        }, 1000)
        
        $('#search-form').submit(function(e) {
            e.preventDefault()
        })
        
        $('#search-box').keypress(function(e) {
            if (!waiting) {
                waiting = true
                request()
            }
        });
        
        $('#input-form').submit(function(e) {
            e.preventDefault()
            post_text()
        })
        
        $('#post_button').click(function(e){
            //e.preventDefault()
            post_text()
            //$('#input-box').css('visibility','hidden')
        });
        
        function post_text() {
            text = $('#input-box').val()
            $('#input-box').val("")
            var request = $.ajax({
              url: "/add/",
              type: "POST",
              data: text,
              dataType: "json"
            });
            request.done(function(data) {
                
            });   
        }
        
        function request() {
            setTimeout(function(){ 
                $.get( "/search/"+$('#search-box').val()+"/", function( data ) {
                    html = ""
                    parsed = JSON.parse(data)['matches']
                    //console.log(parsed)
                    for (i in parsed) {
                        html += highlight(parsed[i])
                    }
                    $('#text-results').html(html)
                    waiting = false
                  
                }); }, 200);
        }
        
        function highlight(data) {
            //console.log('D',data)
            text = data['text']
            break_points = []
            //record all break points
            for (j in data['matchRanges']) {
                range= data['matchRanges'][j]
                break_points.push(parseInt(range['start']))
                break_points.push(parseInt(range['end']))
            }
            //break text into tokens
            break_points = break_points.sort(function(a, b) { return a - b;})
            highlighted = text.substring(0,break_points[0])
            span_open = false
            
            for (var i = 0; i < break_points.length; i++) {
                if (!span_open) {
                    span_open = true
                    highlighted += '<span id="highlighted">' + text.substring(break_points[i],break_points[i+1])
                } else {
                    span_open = false
                    highlighted += '</span>' + text.substring(break_points[i],break_points[i+1])
                }
            }
            return highlighted + "<br>"
        }

		var	$window = $(window),
			$body = $('body');

		if (skel.vars.touch) {

			settings.parallax = false;
			$body.addClass('is-scroll');

		}

		// Disable animations/transitions until the page has loaded.
			$body.addClass('is-loading');

			$window.on('load', function() {
				$body.removeClass('is-loading');
			});

		// CSS polyfills (IE<9).
			if (skel.vars.IEVersion < 9)
				$(':last-child').addClass('last-child');

		// Fix: Placeholder polyfill.
			$('form').placeholder();

		// Prioritize "important" elements on mobile.
			skel.on('+mobile -mobile', function() {
				$.prioritize(
					'.important\\28 mobile\\29',
					skel.breakpoint('mobile').active
				);
			});

		// Scrolly links.
			$('.scrolly-middle').click(function(){
                console.log($(document.body).height())
                $(document.body).animate({
                    scrollTop: $(document.body).height()
                }, 800);
            })


		// Full screen header.
			if (settings.fullScreenHeader) {

				var $header = $('#header');

				if ($header.length > 0) {

					var $header_header = $header.find('header');

					$window
						.on('resize.overflow_fsh', function() {

							if (skel.breakpoint('mobile').active)
								$header.css('padding', '');
							else {

								var p = Math.max(192, ($window.height() - $header_header.outerHeight()) / 2);
								$header.css('padding', p + 'px 0 ' + p + 'px 0');

							}

						})
						.trigger('resize.overflow_fsh');

					$window.load(function() {
						$window.trigger('resize.overflow_fsh');
					});

				}

			}

		// Parallax background.

			// Disable parallax on IE (smooth scrolling is jerky), and on mobile platforms (= better performance).
				if (skel.vars.browser == 'ie'
				||	skel.vars.mobile)
					settings.parallax = false;

			if (settings.parallax) {

				var $dummy = $(), $bg;

				$window
					.on('scroll.overflow_parallax', function() {

						// Adjust background position.
							$bg.css('background-position', 'center ' + (-1 * (parseInt($window.scrollTop()) / settings.parallaxFactor)) + 'px');

					})
					.on('resize.overflow_parallax', function() {

						// If we're in a situation where we need to temporarily disable parallax, do so.
							if (!skel.breakpoint('wide').active
							||	skel.breakpoint('narrow').active) {

								$body.css('background-position', '');
								$bg = $dummy;

							}

						// Otherwise, continue as normal.
							else
								$bg = $body;

						// Trigger scroll handler.
							$window.triggerHandler('scroll.overflow_parallax');

					})
					.trigger('resize.overflow_parallax');

			}

		// Poptrox.
			$('.gallery').poptrox({
				useBodyOverflow: false,
				usePopupEasyClose: false,
				overlayColor: '#0a1919',
				overlayOpacity: (skel.vars.IEVersion < 9 ? 0 : 0.75),
				usePopupDefaultStyling: false,
				usePopupCaption: true,
				popupLoaderText: '',
				windowMargin: 10,
				usePopupNav: true
			});

	});

})(jQuery);