var log_message = function(s){
    $("#msg").text(s).show().fadeOut('slow');
}

var load_alerts = function(){
    log_message("Loading...");
    load_down();
    load_up();
}

var load_down = function() {
    $("#down").load("/alerts/down", function(){
        var num = $("#num_alerts").text();
        document.title = "Alerts - " + num;
    });
}
var load_up = function(){
    $("#up").load("/alerts/up");
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
});
