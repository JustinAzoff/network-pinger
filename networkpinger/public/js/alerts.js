var fetching_down = false;
var fetching_up = false;

var log_message = function(s,d){
    if(!d)d=3000;
    $("#msg").text(s).show().fadeOut(d);
}

var load_alerts = function(){
    //log_message("Loading...");
    load_down();
    load_up();
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

var pretty_time = function(d){
    var r = "";
    var minute = 60;
    var hour   = 60 * minute;
    var day    = 24 * hour;
    var year   = 365 * day;

    var did_years = false;
    var did_days = false;
    var did_hours = false;

    if(d > year){
        r+= Math.floor(d/year) + " years";
        d %= year;
        did_years = true;
    }
    if(d > day){
        r+= " " + Math.floor(d/day) + " days";
        d %= day;
        did_days = true;
    }
    if(d > hour){
        r+= " " + Math.floor(d/hour) + " hours";
        d %= hour;
        did_hours = true;
    }

    if(did_years)
        return r

    if(d > minute){
        r+= " " + Math.floor(d/60) + " minutes";
        d %= minute;
    }
    
    if (did_hours)
        return r;

    r+= " " + Math.floor(d) + " seconds";
    return r;
}
        

var fix_downtime = function(){
    var now = new Date().getTime()/1000;
    $("tr.down").each(function(){
        var downtime = $(this).attr("seconds");
        var cur = parseInt(downtime);
        var res = now - cur;
        res = pretty_time(res);
        $(this).find(".downtime").text(res);
    });
    setTimeout(fix_downtime, 1000);
}

$(function(){
    TCPSocket = Orbited.TCPSocket;
    stomp = new STOMPClient();
    stomp.onopen = function() {
        //log_message("");
    };
    stomp.onclose = function(c) {
        log_message("Connection error, code: " + c + ". Reconnecting in 30 seconds... Automatically refreshing alerts",30000);
        setTimeout(connect, 30000);
        load_alerts();
    };
    stomp.onerror = function(error) {
        log_message("Error: " + error);
    };
    stomp.onerrorframe = function(frame) {
        log_message("Error: " + frame.body);
    };
    stomp.onconnectedframe = function() {
        stomp.subscribe("/topic/alert_msgs");
        load_alerts();
    };
    stomp.onmessageframe = function(frame) {
        load_alerts();
        body = JSON.parse(frame.body);
        if(body.up)
            log_message("Up: " +   body.up.addr);
        else(body.down)
            log_message("Down: " + body.down.addr);
    };
    var connect = function(){
        stomp.connect('localhost', 61613);
    }
    connect();
    fix_downtime();
});
