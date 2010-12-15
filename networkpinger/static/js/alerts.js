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

var setup_socket_io = function(){
    var s = new io.Socket(document.location.hostname, {port: 8888});
    s.connect();
    
    s.addEvent('connect', function() {
        //s.send('New participant joined');
        log_message("Connected to socket!");
    });
    
    s.addEvent('message', function(data) {
        //log_message(data);
        load_alerts();
        msg = $.parseJSON(data);
        if(msg.down) {
            if(console.log) console.log("Playing alarm");
            play_alarm();
        }
    });

    s.addEvent('disconnect', function(){
        log_message("disconnected:(");
        setTimeout("setup_socket_io()", 2*1000);
    });

    //send the message when submit is clicked
    //$('#chatform').submit(function (evt) {
    //    var line = $('#chatform [type=text]').val()
    //    $('#chatform [type=text]').val('')
    //    s.send(line);
    //    return false;
    //});
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
    setup_socket_io()
});
