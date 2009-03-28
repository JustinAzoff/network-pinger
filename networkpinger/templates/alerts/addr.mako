<%inherit file="../base.mako"/>

<h2>Alerts for ${c.host.name} (${c.host.addr})</h2>
%if c.alerts:
<table border=1 class="alert">
<thead>
<tr>
<th>Time</th> <th>Uptime</th> <th>Downtime</th> <th>Ok</th> <th>Reason</th> <th>Note</th>
</tr>
</thead>
<tbody>
%   for a in c.alerts:
<tr class="${["down","up"][bool(a.uptime)]} ${["notok","ok"][a.ok]}">
    <td> ${a.time.strftime("%Y-%m-%d %H:%M:%S")} </td>
    <td> ${a.uptime and a.uptime.strftime("%Y-%m-%d %H:%M:%S")} </td>
    <td>
    %if a.uptime:
    ${h.distance_of_time_in_words(a.time,a.uptime)}
    %else:
    ${h.time_ago_in_words(a.time)}
    %endif
    </td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${h.link_to(a.cur_note or '[no note]', url(controller="alerts",action="notes",id=a.id)) }</td>
</tr>
%   endfor
</tbody>
%else:
<p>No alert history :-)</p>
%endif
