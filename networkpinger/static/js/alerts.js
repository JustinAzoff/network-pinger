var fetching_down = false;
var fetching_up = false;

var log_message = function(s,d){
    if(!d)d=3000;
    $("#msg").text(s).show().fadeOut(d);
}

var load_alerts = function(){
    log_message("Loading...");
    load_down();
    load_up();
    $("#time_remaining").text(15); //try again in 15 seconds
}

var load_down = function() {
    if(fetching_down)
        return;
    fetching_down = true;
    $("#down").load("/alerts/down", function(){
        var num = $("#num_alerts").text();
        document.title = "Alerts - " + num;
        fetching_down = false;
    });
}
var load_up = function(){
    if(fetching_up)
        return;
    fetching_up = true;
    $("#up").load("/alerts/up", function(){
        fetching_up = false;
    });
}

var update_time = function(){
    t = $("#time_remaining");
    t.text(t.text() - 1);
    if (t.text() == 1)
        load_alerts();
}

$(function(){
    setInterval("update_time()", 1 * 1000);
    load_alerts();
});

