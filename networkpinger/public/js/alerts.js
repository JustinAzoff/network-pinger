var fetching_down = false;
var fetching_up = false;

var log_message = function(s){
    $("#msg").text(s).show().fadeOut(3000);
}

var load_alerts = function(){
    log_message("Loading...");
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
        fething_up = false;
    });
}

var fix_downtime = function(){
    var now = new Date().getTime()/1000;
    $("tr.down").each(function(){
        var downtime = $(this).attr("seconds");
        var cur = parseInt(downtime);
        var res = now - cur;
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
       log_message("Lost Connection, Code: " + c + " Reconnecting in 3 seconds...");
       setTimeout(connect, 3000);
   };
   stomp.onerror = function(error) {
       log_message("Error: " + error);
   };
   stomp.onerrorframe = function(frame) {
       log_message("Error: " + frame.body);
   };
   stomp.onconnectedframe = function() {
       stomp.subscribe("/topic/alert_msgs");
   };
   stomp.onmessageframe = function(frame) {
       load_alerts();
   };
   var connect = function(){
       stomp.connect('localhost', 61613);
   }
   load_alerts();
   connect();
   fix_downtime();
});
