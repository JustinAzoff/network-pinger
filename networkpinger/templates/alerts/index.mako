<%inherit file="../base.mako"/>

<div id="down">
Loading...
</div>

<div id="up">
Loading...
</div>

<script>

$("#down").load("/alerts/down", function(){
    var num = $("#num_alerts").text();
    document.title = "Alerts - " + num;
});
$("#up").load("/alerts/up");

</script>
