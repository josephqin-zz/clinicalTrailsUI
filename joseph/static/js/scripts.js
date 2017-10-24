(function() {

    var remember = [];
    var transitionEnd = transitionEndEventName();
    var db = [];
    var backuphtml;
    var ContentWidth = 1100;
    var sassReference = {
        'ContentPaddingTop': 32,
        'RequestFormBottom': 36,
        'lineHeight': 24
    };

    //fake database: db
    $('.RequestForm .inputs input, .RequestForm .inputs select').each(function(i) {
        var item = {};
        item['name'] = this.name;
        item['index'] = i;
        item['selectedValue'] = null;
        item['confirmedValue'] = null;
        item['type'] = this.type;
        item['tagName'] = this.tagName.toLowerCase();
        db.push(item);
    });

    //record the height
    var RequestHeight = $('.Requestwrapper').height();
    var collapsedRequestHeight = sassReference.ContentPaddingTop/2 + sassReference.RequestFormBottom/2 + Math.ceil(db.length / 4) * sassReference.lineHeight;
    // $('.Requestwrapper').css('transform',function(){return 'translateY('+ RequestHeight +')'})
    //check whether the form canbe submitted -> whether the submit button is clickable
    check_btn_state();

    $('.Resultwrapper').css('transform','translateY('+ RequestHeight +'px)');
    /////////////change the select style/////////////////
    $('select').on('change', function() {
        var selectedVal = this.value;
        var selectedText = this.options[this.selectedIndex].text;
        var selectedItem;
        for (x in db) {
            if (db[x].name == this.name) {

                selectedItem = db[x];
                if (this.selectedIndex > 0) {
                    db[x].selectedValue = selectedVal;
                } else db[x].selectedValue = null;
            }
        }

        if (this.selectedIndex > 0) {
            if ($(this).hasClass('selectedValue')) return;
            else {
                $(this).addClass('selectedValue');
            }
        } else {
            if ($(this).hasClass('selectedValue')) {
                $(this).removeClass('selectedValue');
            } else return;
        }

        check_btn_state();

    });


    $('input').on('change', function() {
        var selectedVal = this.value;
        var selectedName = this.name;
        var selectedItem;
        for (x in db) {
            if (db[x].name == selectedName) {

                selectedItem = db[x];
                if (selectedVal == "") {
                    selectedVal = null;
                }
                db[x].selectedValue = selectedVal;

            }
        }
        check_btn_state();
    });

////////////////////submit/////////////////////////////
    $('.RequestForm').submit(function(e) {
        if ($('.Submit').hasClass('freeze') == false) {

            e.preventDefault();

            var filledArray = [];
            var newForm;
            var showAll;
            for (x in db) {
                if ((db[x].selectedValue !== null)) {
                    filledArray.push(db[x]);
                }
                db[x].confirmedValue = db[x].selectedValue;
            }
            backuphtml = $.extend(true, [], $('.RequestForm .inputs input, .RequestForm .inputs select'));


            $('.Requestwrapper').addClass('collapsed');
            $('.Resultwrapper').addClass('collapsed');
            $('.Resultwrapper').css('transform',function(){return 'translateY('+ collapsedRequestHeight + 'px)'});
            // $('.collapsed.Resultwrapper').css('transform', 'translateY(-204px)');
            $('.selectedfilters').one(transitionEnd, function() {

                $('.Requestwrapper .RequestForm').addClass('visuallyhidden');
                $('.Requestwrapper .RequestForm').addClass('hidden');

            });

            // $(".Requestwrapper.collapsed").css('max-height',100* Math.ceil(filledArray.length/3));
            filledArray.map(function(d) {
                var ele = document.createElement('p');
                $(ele).text(backuphtml[d.index].value);
                $(ele).addClass('shrinked');
                $(ele).appendTo($('.selectedfilters'));
            });
            $(".Requestwrapper.collapsed form input.shrinked").css('width', Math.min(900 / 4 - 20, (900 / filledArray.length) - 12));

            showAll = document.createElement('a');
            $(showAll).text('Show All');
            $(showAll).addClass('showAll');
            $(showAll).addClass('clearfix right');
            $(showAll).prependTo($('.selectedfilters'));

            $(".Result").css('display', 'block');
            showTab('Level1', $('[data-level-type="Level1"]'));
        }
    });


    $('body').on('click', 'a.showAll', function(e) {

        $('#Match').removeClass('collapsed');
        $('.selectedfilters').empty();
        $('.Requestwrapper .RequestForm').removeClass('hidden');
        setTimeout(function() {
            $('.Requestwrapper .RequestForm').removeClass('visuallyhidden');
        }, 200);

    });
 




    $('.Leveltab li a').on('click', function(evt) {


        var level = $(this).data('level-type');
        showTab(level, evt);

        $('.Resultwrapper').css('transform',function(){return 'translateY('+ RequestHeight + 'px)'})
        $('.Resultwrapper').removeClass('collapsed');
        // $('.Resultwrapper').css('transform',function(){return 'translateY('+ RequestHeight + 'px)'});




    });






    //////////////////////////////////
    ////          backyards       ////
    //////////////////////////////////
    function showTab(level, evt) {

        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(level).style.display = "block";
        if (evt.currentTarget) {
            evt.currentTarget.className += " active";
        } else {
            evt.addClass('active');
        }

    }



    function check_btn_state() {
        var ele = $('.Submit');
        var freeze = ele.hasClass('freeze');
        var selected = false;
        for (x in db) {
            if (db[x].selectedValue) {
                if (db[x].selectedValue.length > 0) {
                    selected = true;
                }
            }
        }
        if ((freeze == true) && (selected == true)) {
            ele.removeClass('freeze');
        } else if ((freeze == false) && (selected == false)) {
            ele.addClass('freeze');
        }
    }

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
