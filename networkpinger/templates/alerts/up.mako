<h2>Hosts that were down and came back up</h2>
<table border=1>
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Uptime</th> <th>Ok</th> <th>Reason</th> <th>Note</th> <th>Count</th>
</tr>
</thead>
<tbody>
%if c.up:
%   for a in c.up:
<tr>
    <td> ${h.link_to(a.addr, url(controller="alerts",action="addr",id=a.addr))} </td>
    <td> ${a.name} </td>
    <td> ${a.time.strftime("%X %x")} </td>
    <td> ${a.uptime.strftime("%X %x")} </td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${h.link_to(a.cur_note or '[no note]', url(controller="alerts",action="notes",id=a.id)) }</td>
    <td> ${a.count} </td>
</tr>
%   endfor
%else:
    <tr><td colspan=8>Nothing was down</td></tr>
%endif
</tbody>
</table>
