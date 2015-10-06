//search-init.js

/*
var activateSelection = function(selection, container){
	console.log(selection);
	container.find("[data-url-signal=\"" + selection + "\"]").addClass("highlight-header");
}*/
/*
var activateSelections = function(){
	var url = decodeURIComponent(document.URL);
	var urlList = url.split("/");
	var filter = urlList[urlList.length-2]
	var sort;
	if (filter.substring(0, 5) == "sort:"){
		// just a sort
		sort = filter;
		console.log("sort: " + sort);
	}
	else if (filter.substring(0, 6) == "filter:") {
		// filter as well as sort
		sort = urlList[urlList.length-3];
		console.log("sort: " + sort);
		console.log("filter: " + filter);
		activateSelection(filter, $("#filter-container"));
	}
	else {
		sort = "";
		console.log("no special selection");
	}
	activateSelection(sort, $("#sort-container"));
}*/

/*var activateParameterSelection = function(parameter, data) {
	if (parameter.startsWith("sort_by")) {
		if (data.substr(0,1) == "-"){
			$("a[data-select-param=\"" + parameter + "__" + data.substr(1) + "\"]").addClass("active highlight").append('<span class="glyphicon glyphicon-triangle-bottom"></span>');
		}
		else {
			$("a[data-select-param=\"" + parameter + "__" + data + "\"]").addClass("active highlight").append('<span class="glyphicon glyphicon-triangle-top"></span>');
		}
	}
	else {
		$("a[data-select-param=\"" + parameter + "__" + data + "\"]").addClass("active highlight");
	}
};

var activateParameterSelections = function(get_data, callback){
	for (var parameter in get_data) {
		if ((parameter != "selected_facets") && (parameter != "sort_by")){
			continue;
		}
		if (get_data[parameter].constructor === Array) {
			for (var i = 0; i < get_data[parameter].length; i++) {
				activateParameterSelection(parameter, get_data[parameter][i]);
			}
		}
		else {
			activateParameterSelection(parameter, get_data[parameter]);
			
		}
	}
	if (!get_data.hasOwnProperty("sort_by")) {
		$("a[data-select-param=\"sort_by__lastName\"]").addClass("active highlight").append('<span class="glyphicon glyphicon-triangle-top"></span>');
	}
	if (callback !== undefined) {
		callback();
	}
};*/

var setFormAttr = function(name, value, overwrite) {
	console.log("removing inputs of name", name);
	/*$("input[name=" + name + "]").remove();
	$("#search-form").append("<input type=\"hidden\" name=\"" + name + "\" value=\"" + value + "\"/>");*/
	if (overwrite) {
		//console.log("removing inputs of name", name);
		$("input[name=" + name + "]").remove();
		$("#search-form").append("<input type=\"hidden\" name=\"" + name + "\" value=\"" + value + "\"/>");
	}
	else {
		console.log("removing inputs of name", name);
		if ($("input[name=" + name + "]").length == 0) {
			$("#search-form").append("<input type=\"hidden\" name=\"" + name + "\" value=\"" + value + "\"/>");
		}
		else if (name == "selected_facets" && ($("input[name=\"" + name + "\"][value=\"" + value + "\"]").length == 0)) {
			$("#search-form").append("<input type=\"hidden\" name=\"" + name + "\" value=\"" + value + "\"/>");
		}
	}

	/*if ($("#search-form input[name=" + name + "][value=" + value + "]").length <= 0) {
		$("#search-form").append("<input type=\"hidden\" name=\"" + name + "\" value=\"" + value + "\"/>");
	}
	else {
		console.log("not repeating ", name, value);
	}*/

};
var getCookie = function(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1);
        if (c.indexOf(name) != -1) return c.substring(name.length,c.length);
    }
    return "";
};


var get_data = {};
$(document).ready(function() {

	var postInit = function() {
		(function() { 
			for (var parameter in get_data) {
				if (parameter != "") {
					console.log(parameter + ": " + get_data[parameter]);
					if (get_data[parameter].constructor === Array) {
						for (var i = 0; i < get_data[parameter].length; i++) {
							console.log("param: " + parameter + "; item: " + get_data[parameter][i]);
							if (parameter == "page") {
								break;
							}

							setFormAttr(parameter, get_data[parameter][i]);
						}
					}
					else {
						if (parameter == "page") {
							continue;
						}
						setFormAttr(parameter, get_data[parameter]);
					}
				}
			}
		}());

		$("#content form div.table-responsive table tbody tr").click(function(){
			window.location = $(this).find("a").attr("href");
		});

		

		$(".facet-select").click(function(){
			console.log("facet-select lcik");
			console.log("facet is " + $(this).attr("data-facet"));
			if ($(this).attr("data-facet").startsWith("house")) {
				$("input[name=selected_facets][value*=house]").remove();
			}
			else {
				$("input[name=selected_facets][value*=party]").remove();
			}

			//TOFIX: Use facets to get pagination and no of pages
			$("form input[name=page]").remove(); // don't know the number of results ()
			setFormAttr("selected_facets", $(this).attr("data-facet"));
			$("form#search-form").submit();
		});
		$(".sort-select").click(function(){
			console.log("sopr-select lcik");
			var tosort = $(this).attr("data-sort");
			console.log("sort is " + tosort);
			console.log("get data[sort_by] is " + get_data.sort_by);

			if ((!get_data.hasOwnProperty("sort_by") && (tosort == "lastName")) || tosort == get_data.sort_by) {
				tosort = "-" + tosort;
			}
			setFormAttr("sort_by", tosort, true);
			$("form#search-form").submit();
		});
		$("#search-form > nav > ul > li > a[data-page]").click(function(){
			setFormAttr("page", $(this).attr("data-page"), true);
			$("form#search-form").submit();
		});
		$("#results-selector-container > a:not(.selected-results-no)").click(function(){
			if (! $(this).hasClass("selected-results-no")) {
				setFormAttr("results_no", $(this).attr("data-results-no"), true);
				$("form#search-form").submit();
			}
		});
		if (get_data.results_no) {
			$("#results-selector-container > a[data-results-no=" + get_data.results_no + "]").addClass("selected-results-no");
		}
		else {
			$("#results-selector-container > a[data-results-no=50]").addClass("selected-results-no");
		}
	};



	var init = function(){
		(function() { 
			// POST: URL Parameters in get_data hash table, identical ones are in further list
		    var sPageURL = window.location.search.substring(1);
		    var sURLVariables = sPageURL.split('&');
		    for (var i = 0; i < sURLVariables.length; i++)
		    {
		        var sParameterName = sURLVariables[i].split('=');
		        //console.log("sParameterName = " + sParameterName);
		        if (sParameterName[0] == "q"){ // unncessary
		        	continue;
		        }
		        val = decodeURIComponent(sParameterName[1]);
		        if (sParameterName[0] in get_data) {
		        	if (get_data[sParameterName[0]].constructor === Array) {
		        		get_data[sParameterName[0]].push(val);
		        	}
		        	else {
		        		get_data[sParameterName[0]] = [get_data[sParameterName[0]], val];
		        	}
		        }
		        else {
		        	get_data[sParameterName[0]] = val;
		        }
		    }
		}());
		//activateParameterSelections(get_data, postInit);
		postInit();
	};
	init();


// after document.ready is run
	(function() { 
		for (var parameter in get_data) {
			//console.log(parameter + ": " + get_data[parameter]);
			if (parameter != "") {
				if (get_data[parameter].constructor === Array) {
					for (var i = 0; i < get_data[parameter].length; i++) {
						//console.log("param: " + parameter + "; item: " + get_data[parameter][i]);
						setFormAttr(parameter, get_data[parameter][i]);
					}
				}
				else {
					setFormAttr(parameter, get_data[parameter]);
				}
			}
		}
	}());

	$("#content form div.table-responsive table tbody tr").click(function(){
		window.location = $(this).find("a").attr("href");
	});

	

	$(".facet-select").click(function(){
		console.log("facet-select lcik");
		console.log("facet is " + $(this).attr("data-facet"));
		if ($(this).attr("data-facet").startsWith("house")) {
			$("input[name=selected_facets][value*=house]").remove();
		}
		else {
			$("input[name=selected_facets][value*=party]").remove();
		}

		//TOFIX: Use facets to get pagination and no of pages
		$("form input[name=page]").remove(); // don't know the number of results ()
		setFormAttr("selected_facets", $(this).attr("data-facet"));
		$("form#search-form").submit();
	});
	$(".sort-select").click(function(){
		console.log("sopr-select lcik");
		var tosort = $(this).attr("data-sort");
		console.log("sort is " + tosort);
		console.log("get data[sort_by] is " + get_data.sort_by);

		if ((!get_data.hasOwnProperty("sort_by") && (tosort == "lastName")) || tosort == get_data.sort_by) {
			tosort = "-" + tosort;
		}
		setFormAttr("sort_by", tosort, true);
		$("form#search-form").submit();
	});
	$("#search-form > nav > ul > li > a[data-page]").click(function(){
		setFormAttr("page", $(this).attr("data-page"), true);
		$("form#search-form").submit();
	});
	$("#results-selector-container > a:not(.selected-results-no)").click(function(){
		if (! $(this).hasClass("selected-results-no")) {
			setFormAttr("results_no", $(this).attr("data-results-no"), true);
			$("form#search-form").submit();
		}
	});
	if (get_data.results_no) {
		$("#results-selector-container > a[data-results-no=" + get_data.results_no + "]").addClass("selected-results-no");
	}
	else {
		$("#results-selector-container > a[data-results-no=50]").addClass("selected-results-no");
	}
	

    $(".replace-link").attr('href', function(i, href) {
        //var url = window.location.href;
        //var getData = (url.split("?")[1] ? ('?' + url.split("?")[1]) : "");
        var url = href.split('?')[0];
        return url;
    });
    var queryStr = getCookie("HOME_QUERY");
    if (queryStr !== "") {
        $("#my-officials").css("display", "inline-block");
        $("#my-officials-link").attr('href',"https://spacescore.com/CongressScore/MyLegislators/?q=" + queryStr);
    }

});