var fetching_down = false;
var fetching_up = false;

var log_message = function(s,d){
    var m = $("#msg").text(s).show()
    if(d)
        m.fadeOut(d);
}

var load_alerts = function(){
    //log_message("Loading...");
    load_down();
    load_up();
    $("#time_remaining").text(9); //try again in 9 seconds
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

var alarm_timers = {}
var disconnected = false;

var setup_websocket = function(){
    var s = new WebSocket("ws://" + document.location.hostname + ":8888/websocket");
    
    s.onopen = function() {
        //s.send('New participant joined');
        log_message("Connected to socket!",3000);
        /* assume the application was updated and reload */
        if(disconnected)
            window.location.reload(true);
    }
    
    s.onmessage = function(evt) {
        //log_message(data);
        load_alerts();
        var msg = $.parseJSON(evt.data);
        if(msg.down) {
            maybe_play_alarm(msg.down);
        } else if(msg.up) {
            cancel_alarm(msg.up);
        }
    }

    s.onclose = function () {
        log_message("disconnected:(");
        disconnected = true;
        setTimeout("setup_websocket()", 2*1000);
    }
};

var maybe_play_alarm = function(node)
{
    console.log("Maybe playing alarm for " + node.name);
    alarm_timers[node.name] = setTimeout(play_alarm, 10*1000);
}

var cancel_alarm = function(node)
{
    console.log("Back up, not playing alarm for " + node.name);
    var t = alarm_timers[node.name];
    if(t) clearTimeout(t);
    delete(alarm_timers[node.name]);
}

var play_alarm = function(){
    var s = $("#sound").get(0);
    //FIXME, should not need to do this:
    s.src = s.src;
    s.play();
}

$(function(){
    setInterval("update_time()", 1 * 1000);
    load_alerts();
    setup_websocket()
});
