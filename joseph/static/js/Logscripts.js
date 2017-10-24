(function() {

    $('svg').hide();
    $('.error_message').hide();
    var transitionEnd = transitionEndEventName();

    $('input[name ="password"]').on('change', function(e) {

        $(this).addClass('error');
        $('.error_message').show();

        $('svg').show();
        setTimeout(function() {
            $('svg').addClass('error');
            $('.error_message').addClass('error');
        }, 20);
    });

    $('svg').click(function(e) {
        if ($('.error_message').hasClass('hidden')) {
          $('.error_message').removeClass('hidden');
          setTimeout(function() {
            $('.error_message').removeClass('visuallyhidden');
          }, 200);
        }else{
          $('.error_message').addClass('visuallyhidden');
          $('.error_message').one(transitionEnd, function(e) {
              $('.error_message').addClass('hidden');
          });
        }
    });

    /////javascript detect heights

    function transitionEndEventName() {
        var i,
            undefined,
            el = document.createElement('div'),
            transitions = {
                'transition': 'transitionend',
                'OTransition': 'otransitionend', // oTransitionEnd in very old Opera
                'MozTransition': 'transitionend',
                'WebkitTransition': 'webkitTransitionEnd'
            };

        for (i in transitions) {
            if (transitions.hasOwnProperty(i) && el.style[i] !== undefined) {
                return transitions[i];
            }
        }
    }
})();
