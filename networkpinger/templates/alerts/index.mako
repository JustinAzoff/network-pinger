<center>
<h2>Down</h2>
<table border=1>
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Ok</th> <th>Reason</th> <th>Note</th>
</thead>
<tbody>
%if c.down:
%   for a in c.down:
<tr>
    <td> ${h.link_to(a.addr, url(controller="alerts",action="addr",id=a.addr))} </td>
    <td> ${a.name} </td>
    <td> ${a.time.strftime("%X %x")} </td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${h.link_to(a.cur_note or '[no note]', url(controller="alerts",action="notes",id=a.id)) }</td>
</tr>
%   endfor
%else:
    <tr><td colspan=6>Nothing is down</td></tr>
%endif
</tbody>
</table>

<h2>Up</h2>
<table border=1>
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Uptime</th> <th>Ok</th> <th>Reason</th> <th>Note</th> <th>Count</th>
</thead>
<tbody>
%if c.down:
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
</center>
