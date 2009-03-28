<%inherit file="../base.mako"/>

<div id="down">
Loading...
</div>

<div id="up">
Loading...
</div>

<script>

$("#down").load("/alerts/down");
$("#up").load("/alerts/up");

</script>
