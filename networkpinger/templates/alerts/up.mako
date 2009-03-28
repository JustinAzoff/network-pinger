<h2>Hosts that were down and came back up</h2>
%if c.up:
<table border=1 class="alert">
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Uptime</th> <th>Downtime</th> <th>Ok</th> <th>Reason</th> <th>Note</th> <th>Count</th>
</tr>
</thead>
<tbody>
%   for a in c.up:
<tr class="up ${["notok","ok"][a.ok]}">
    <td> ${h.link_to(a.addr, url(controller="alerts",action="addr",id=a.addr))} </td>
    <td> ${a.name} </td>
    <td> ${a.time.strftime("%Y-%m-%d %H:%M:%S")} </td>
    <td> ${a.uptime.strftime("%Y-%m-%d %H:%M:%S")} </td>
    <td> ${h.distance_of_time_in_words(a.time,a.uptime)}</td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${h.link_to(a.cur_note or '[no note]', url(controller="alerts",action="notes",id=a.id)) }</td>
    <td> ${a.count} </td>
</tr>
%   endfor
</tbody>
</table>
%else:
    <p>Nothing was down</p>
%endif
