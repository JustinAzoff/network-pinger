<%inherit file="../base.mako"/>

Seconds to refresh: <b id="time_remaining">15</b>.
<a onclick="load_alerts();return false;" href="/alerts/index">Refresh</a>

<span id="msg">
</span>

<div id="down">
Loading initial alerts...
</div>

<div id="up">
</div>

<script src="${h.url_for("alerts_js")}"></script>
