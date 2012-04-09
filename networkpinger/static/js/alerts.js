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
    $("#time_remaining").text(30); //try again in 30 seconds
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

var setup_websocket = function(){
    var s = new WebSocket("ws://" + document.location.hostname + ":8888/websocket");
    
    s.onopen = function() {
        //s.send('New participant joined');
        log_message("Connected to socket!");
    }
    
    s.onmessage = function(evt) {
        //log_message(data);
        load_alerts();
        msg = $.parseJSON(evt.data);
        if(msg.down) {
            if(console.log) console.log("Playing alarm");
            play_alarm();
        }
    }

    s.onclose = function () {
        log_message("disconnected:(");
        setTimeout("setup_socket_io()", 2*1000);
    }
};

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
