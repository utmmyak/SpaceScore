$( document ).ready(function() {
    var ec = new evercookie();
    function setCookie(cname, cvalue, exdays) {
        var d = new Date();
        d.setTime(d.getTime() + (exdays*24*60*60*1000));
        var expires = "expires="+d.toUTCString();
        document.cookie = cname + "=" + cvalue + "; " + expires;
    };
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = $('[name="csrfmiddlewaretoken"]').val();
    setCookie('csrftoken', $('[name="csrfmiddlewaretoken"]').val(), 1);
    //var csrftoken = getCookie('csrftoken');
    
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {

            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }

        }
    });
    var chartElement = $("#official-perspective-chart");
    var chartData = {
        labels: ["Human", "Public", "Unmanned", "Private"],
        datasets: [
            {
                label: "Score",
                fillColor: "rgba(120,120,120,0.2)",
                strokeColor: "rgba(220,220,220,0.9)",
                pointColor: "#7dd2e4",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(180,180,180,0.5)",
                data: [chartElement.attr("data-hsfscore"), chartElement.attr("data-pubscore"),
                    chartElement.attr("data-usfscore"), chartElement.attr("data-privscore")]
            }
        ]
    };
    var chartOptions = {
        scaleOverride: true, //
        // -> The number of steps in a hard coded scale
        scaleSteps: 100,
        // ->  The value jump in the hard coded scale
        scaleStepWidth: 1,
        // - > The scale starting value
        scaleStartValue: 0,
        //scaleShowLine : false,
        pointLabelFontFamily : "'Arial'",
        pointLabelFontStyle : "bold",
        pointLabelFontColor : "#111",
        pointDotRadius : 4,
        pointLabelFontSize : 14,
        // String - Template string for single tooltips
        tooltipTemplate: "<%if (label){%><%=label %>: <%}%><%= value + '%' %>",
        // String - Template string for multiple tooltips
        multiTooltipTemplate: "<%= value + '%' %>",
    };
    var ctx = chartElement.get(0).getContext("2d");
    var myChart = new Chart(ctx)
    var myRadarChart = myChart.Radar(chartData, chartOptions); // options is second param

    var alreadyVoted = function(){
        $("#vote-alert").css("display", "block").removeClass("alert-success").addClass("alert-danger");
        $('#vote-msg').text("You have already voted on this official.");
        $("#alert-glyph").removeClass("glyphicon-ok-sign").addClass("glyphicon-exclamation-sign");
        $("#usr-vote-form > table > tbody > tr > td > input").prop("disabled", "true");
        //$("#alert-glyph")
        //$("#vote-alert").removeClass("alert-success");
        //$("#vote-alert").addClass("alert-danger");
        $('#vote-go').prop("disabled", "true").css("display", "none");
        //$('#vote-go')
        $('#voteModal > div > div > div.modal-footer > button.btn.btn-default').text("Continue");
    }
    ec.get(document.URL + "vote/",
        function(res) {
            if (res == "true") {
                alreadyVoted();
            }
        }
    );

    $("#usr-vote-form").submit(function(e) {
        e.preventDefault();

        $('html').addClass('waiting');  // set waiting
        ec.get(document.URL + "vote/",
            function(res){
                if (res != "true") {
                    var usrScore = $('#usr-vote-form input[name=vote-options]:checked').attr("data-send");
                    
                    $.ajax({
                        type: "POST",
                        //headers: {"X-CSRFToken": getCookie('csrftoken')},
                        url: document.URL + "vote/",
                        data: {userScore: usrScore, csrftoken: csrftoken}
                    })
                    .done(function(){
                        //$("#content > div:nth-child(1) > div.col-xs-7 > button").css("display", "block");
                        $('html').removeClass('waiting');  // set waiting
                        $('#vote-go').prop("disabled", true);
                        $('#vote-go').css("display", "none");
                        $('#vote-alert').css("display", "block");
                        $('#usr-vote-form > div.modal-footer > button.btn.btn-default').text("Continue");
                        setTimeout(function(){
                            $("#voteModal").modal('hide');
                            ec.set(document.URL + "vote/", "true");
                            return false;
                        }, 2500);
                    });
                }
                else {
                    alreadyVoted();
                    return false;
                }
            }
        );
    });
    $("#basescore-display").knob({
        'format' : function(val) {
            return val + '%';
        },
        width: 170, height: 170, readOnly: true, min: 0, max: 100, displayInput: true});
    $("#peoples-score-display").knob({
            'format' : function(val) {
                if (isNaN(val)) {
                    return "N/A";
                }
                else if (val != "N/A") {
                    return val + '%';
                }
            },
        width: 130, height: 130, readOnly: true, min: 0, max: 100, displayInput: true});
    $(".tooltipster-icon.basescore-tooltip.popover").popover({
        html: true,
        content: "<span>The Base Score reflects our editorial opinion of how closely this official aligns with the needs of space in general as outlined <a href=\"/methodology.html#base\">here</a>.</span>",
        trigger: 'manual',
        placement: 'bottom',
        container: $(this).attr('id')
    }).on("mouseenter", function () {
        var _this = this;
        $(this).popover("show");
        $(this).siblings(".popover").on("mouseleave", function () {
            $(_this).popover('hide');
        });
    }).on("mouseleave", function () {
        var _this = this;
        setTimeout(function () {
            if (!$(".popover:hover").length) {
                $(_this).popover("hide")
            }
        }, 100);
    });
});
