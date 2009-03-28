<%inherit file="../base.mako"/>

<a onclick="load_alerts();return false;" href="/alerts/index">Refresh</a>
<span id="msg">
</span>

<div id="down">
Loading...
</div>

<div id="up">
Loading...
</div>

<script src="/js/orbited/Orbited.js"></script>
<script src="/js/orbited/stomp.js"></script>
<script src="/js/alerts.js"></script>
