<h2>Alerts for ${c.host.name} (${c.host.addr})</h2>
<table border=1 class="alert">
<thead>
<tr>
<th>Time</th> <th>Uptime</th> <th>Ok</th> <th>Reason</th> <th>Note</th>
</tr>
</thead>
<tbody>
%if c.alerts:
%   for a in c.alerts:
<tr>
    <td> ${a.time.strftime("%X %x")} </td>
    <td> ${a.uptime and a.uptime.strftime("%X %x")} </td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${h.link_to(a.cur_note or '[no note]', url(controller="alerts",action="notes",id=a.id)) }</td>
</tr>
%   endfor
%else:
    <tr><td colspan=4>No alert history</td></tr>
%endif
</tbody>
