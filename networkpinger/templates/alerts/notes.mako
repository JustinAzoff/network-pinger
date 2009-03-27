<h2>Notes for ${c.alert.name} (${c.alert.addr})</h2>
<ol>
%for n in c.alert.notes:
<li> 
${ n.short} - ${n.added.strftime("%X %x")}
    <p> ${n.long}</p>
</li>
%endfor
</ol>

${h.form(url(controller="alerts",action="addnote",id=c.id))}

<label><b>Short</b> <br/>
${h.text("short",size=30)} <br/>

<label><b>long</b> <br/>
${h.textarea("long",rows=10,cols=80)} <br/>

${h.submit('add','add')}

</form>
