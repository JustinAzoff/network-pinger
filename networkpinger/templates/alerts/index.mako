<center>
<table border=1>
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Ok</th> <th>Reason</th> <th>Note</th>
</thead>
<tbody>
%if c.down:
%   for a in c.down:
<tr>
    <td> ${a.addr} </td>
    <td> ${a.name} </td>
    <td> ${a.time} </td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${h.link_to(a.cur_note, url(controller="alerts",action="notes",id=a.id)) }</td>
</tr>
%   endfor
%else:
    <tr><td colspan=6>Nothing is down</td></tr>
%endif
</tbody>
</center>
