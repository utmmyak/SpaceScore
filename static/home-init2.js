function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function setCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; Domain=spacescore.com"+"; path=/";
}

function eraseCookie(name) {
    setCookie(name,"",-1);
}
$.fn.pressEnter = function(fn) {  
    return this.each(function() {  
        $(this).bind('enterPress', fn);
        $(this).keyup(function(e){
            if(e.keyCode == 13)
            {
              $(this).trigger("enterPress");
            }
        });
    });  
 }; 

$(document).ready(function() {
    var visit = getCookie("VISITED");
    if (visit === null) {
        $('#hoverNotification').fadeIn();

        //$("#home-stats > h2:nth-child(12)").popover("show");
        $("#comm-spaceflight-heading::before").popover(
            {
                //html : true, 
                content: "You can hover over dials to view the Legislators included in each statistic.",
                //title: "Hover",
                //container: 'body',
                placement: "top",
                trigger: "manual"
            }
        ).popover('show');
        $("#home-stats > div.popover.fade.top.in").css("margin-top", "250px");
        setCookie("VISITED", "true", 1000);
    }

    $("#get-started-btn").click(function(){
        $("#find-legislator-txt").addClass("flash");
        $("#find-legislator-box").addClass("flash");
        setTimeout(function(){
            $("#find-legislator-txt").removeClass("flash");
            $("#find-legislator-box").removeClass("flash");
        }, 1200);
        $('html,body').animate({
            scrollTop: $("#find-legislator-txt").offset().top - 25
        }, 800);
    });

    $('#science_officials_block').tooltipster({
        content: $('<span>We classify science experience as professional experience in experimental science, such as physics, microbiology, chemistry, etc. We do not count engineers or doctors in this metric.</span>'),
        maxWidth: 350,
        interactive: true,
        iconDesktop: true,
        icon: '?',
        position: 'right'
    });
    $('#priv_officials_block').tooltipster({
        content: $('<span>We classify "liking" the privatization of spaceflight as having a 80% or higher PrivatizationScore.</span>'),
        maxWidth: 350,
        interactive: true,
        iconDesktop: true,
        icon: '?',
        position: 'right'
    });
    $('#pub_officials_block').tooltipster({
        content: $('<span>We classify "liking" the nationalization of spaceflight as having a 80% or higher NationalizationScore.</span>'),
        maxWidth: 350,
        interactive: true,
        iconDesktop: true,
        icon: '?',
        position: 'right'
    });
    $('#hsf_officials_block').tooltipster({
        content: $('<span>We classify "liking" human spaceflight as having a 80% or higher HumanSpaceflightScore.</span>'),
        maxWidth: 350,
        interactive: true,
        iconDesktop: true,
        icon: '?',
        position: 'right'
    });
    $('#usf_officials_block').tooltipster({
        content: $('<span>We classify "liking" unmanned spaceflight as having a 80% or higher UnmannedSpaceflightScore.</span>'),
        maxWidth: 350,
        interactive: true,
        iconDesktop: true,
        icon: '?',
        position: 'right'
    });
    $('#high_basescore_officials_block').tooltipster({
        content: $('<span>We classify "loving" space as having a 90% or higher BaseScore.</span>'),
        maxWidth: 350,
        interactive: true,
        iconDesktop: true,
        icon: '?',
        position: 'right'
    });

    $( "#high_basescore_officials_block" ).hoverIntent({
    	over: function(){
		$( "#high_basescore_officials_cont" ).filter(':not(:animated)').hide();
		$( "#high_basescore_officials_cont" ).children("canvas").hide();
		$( "#high_basescore_officials_cont" ).promise().done(function(){
			$( "#bscore_offs" ).css('display', 'inline').hide().filter(':not(:animated)').show();
		});
    }, out: function(){
		$( "#bscore_offs" ).filter(':not(:animated)').hide();
    	$( "#bscore_offs" ).promise().done(function(){
            $( "#high_basescore_officials_cont" ).css({"display": "inline-block", "margin-top": "0"});
    		$( "#high_basescore_officials_cont" ).children("canvas").show();
    		$( "#high_basescore_officials_cont" ).filter(':not(:animated)').show();
    	});
	}, timeout: 500
    });

    $( "#usf_officials_block" ).hoverIntent({
    	over: function(){
		$( "#usf_officials_cont" ).filter(':not(:animated)').hide();
		$( "#usf_officials_cont" ).children("canvas").hide();
		$( "#usf_officials_cont" ).promise().done(function(){
			$( "#usfscore_offs" ).css('display', 'inline').hide().filter(':not(:animated)').show();
		});
    }, out: function(){
    	$( "#usfscore_offs" ).filter(':not(:animated)').hide();
    	$( "#usfscore_offs" ).promise().done(function(){
            $( "#usf_officials_cont" ).css({"display": "inline-block", "margin-top": "0"});
    		$( "#usf_officials_cont" ).children("canvas").show();
    		$( "#usf_officials_cont" ).filter(':not(:animated)').show();
    	});
    }, timeout: 500
    });

    $( "#hsf_officials_block" ).hoverIntent({
    	over: function(){
   		$( "#hsf_officials_cont" ).filter(':not(:animated)').hide();
		$( "#hsf_officials_cont" ).children("canvas").hide();
		$( "#hsf_officials_cont" ).promise().done(function(){
			$( "#hsfscore_offs" ).css('display', 'inline').hide().filter(':not(:animated)').show();
		});
    }, out: function(){
    	$( "#hsfscore_offs" ).filter(':not(:animated)').hide();
    	$( "#hsfscore_offs" ).promise().done(function(){
            $( "#hsf_officials_cont" ).css({"display": "inline-block", "margin-top": "0"});
    		$( "#hsf_officials_cont" ).children("canvas").show();
    		$( "#hsf_officials_cont" ).filter(':not(:animated)').show();
    	});
	}, timeout: 500
    });

    $( "#pub_officials_block" ).hoverIntent({
    	over: function(){
		$( "#pub_officials_cont" ).filter(':not(:animated)').hide();
		$( "#pub_officials_cont" );
		$( "#pub_officials_cont" ).promise().done(function(){
			$( "#pubscore_offs" ).css('display', 'inline').hide().filter(':not(:animated)').show();
		});
    }, out: function(){
	    $( "#pubscore_offs" ).filter(':not(:animated)').hide();
    	$( "#pubscore_offs" ).promise().done(function(){
            $( "#pub_officials_cont" ).css({"display": "inline-block", "margin-top": "0"});
    		$( "#pub_officials_cont" ).children("canvas").show();
    		$( "#pub_officials_cont" ).filter(':not(:animated)').show();
    	});
	}, timeout: 500
    });

    $( "#priv_officials_block" ).hoverIntent({
    	over: function(){
		$( "#priv_officials_cont" ).filter(':not(:animated)').hide().children("canvas").hide();
		$( "#priv_officials_cont" ).promise().done(function(){
			$( "#privscore_offs" ).css('display', 'inline').hide().filter(':not(:animated)').show();
		});
    }, out: function(){
	    $( "#privscore_offs" ).filter(':not(:animated)').hide();
	    $( "#privscore_offs" ).promise().done(function(){
            $( "#priv_officials_cont" ).css({"display": "inline-block", "margin-top": "0"});
	    	$( "#priv_officials_cont" ).children("canvas").show();
	    	$( "#priv_officials_cont" ).filter(':not(:animated)').show();
	    });
	}, timeout: 500
    });

    $( "#science_officials_block" ).hoverIntent({
    	over: function(){
    	$( "#science_officials_cont" ).filter(':not(:animated)').hide();
		$( "#science_officials_cont" ).children("canvas").hide();
		$( "#science_officials_cont" ).promise().done(function(){
			$( "#science_offs" ).css('display', 'inline').hide().filter(':not(:animated)').show();
		});
    }, out: function(){
		$( "#science_offs" ).filter(':not(:animated)').hide();
    	$( "#science_offs" ).promise().done(function(){
            $( "#science_officials_cont" ).css({"display": "inline-block", "margin-top": "0"});
    		$( "#science_officials_cont" ).children("canvas").show();
    		$( "#science_officials_cont" ).filter(':not(:animated)').show();
    	});
	}, timeout: 500
    });
    $("#zip_entry").pressEnter(function(){$("#zip_button").click();});
    $("#zip_button").click(function(){
        var zipCode = $("#zip_entry").val();
        var zipRegex = /^\d{5}$/;

        if (!zipRegex.test(zipCode))
        {
            $("#zip-error").text("Invalid zip code.");
            return false;
        }

        $.ajax({
            dataType: "json",
            url: "https://congress.api.sunlightfoundation.com/legislators/locate",
            data: "apikey=98d96d2b0f914284be93d3b600cc23be&zip=" + zipCode,
            success: function (json) {
                if (json.count === 0) {
                    $("#zip-error").text("Failure retrieving officials; zip code is likely invalid.");
                    return false;
                }
                var queryStr = "";
                if (json.results.length > 0) {
                    queryStr += "\"" + json.results[0].first_name + "+" + json.results[0].last_name + "\"";
                }
                for (var i = 1; i < json.results.length; i++ ) {
                    queryStr += "+OR+";
                    queryStr += "\"" + json.results[i].first_name + "+" + json.results[i].last_name + "\"";
                }
                if (getCookie("HOME_QUERY") !== "") {
                    eraseCookie("HOME_QUERY");
                }
                setCookie("HOME_QUERY", queryStr, 1000);
                window.location.href = "https://spacescore.com/CongressScore/MyLegislators/?q=" + queryStr;
            }
        });
    });

});
