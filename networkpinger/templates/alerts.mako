<table border=1>
<thead>
<tr>
<th>Addr</th> <th>Name</th> <th>Time</th> <th>Ok</th> <th>Reason</th> <th>Note</th>
</thead>
<tbody>
%for a in c.down:
<tr>
    <td> ${a.addr} </td>
    <td> ${a.name} </td>
    <td> ${a.time} </td>
    <td> ${a.ok} </td>
    <td> ${a.reason} </td>
    <td> ${a.cur_note} </td>
</tr>
%else:
    <tr><td colspan=6>Nothing is down</td></tr>
%endfor
</tbody>
