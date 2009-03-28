<h2>Hosts that are down(<span id="num_alerts">${len(c.down)}</span>)</h2>
<table border=1 class="alert">
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Ok</th> <th>Reason</th> <th>Note</th>
</tr>
</thead>
<tbody>
%if c.down:
%   for a in c.down:
<tr class="down ${["notok","ok"][a.ok]}">
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