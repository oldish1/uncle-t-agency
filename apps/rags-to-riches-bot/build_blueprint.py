import json, itertools, re
SID="1v1Detux-M4oUkbdx82Oa1KXDasSfH7S1AG3dkzw28gk"; CONN=5535950
CAL="742ce44765f86d99b594b724e348e02648375a53eb0d973430e1ec8faaedd738@group.calendar.google.com"
M="1.entry[].changes[].value.messages[]"
TOK="PASTE_ACCESS_TOKEN"; AKEY="PASTE_ANTHROPIC_KEY"; TPL="PASTE_TEMPLATE_NAME"
ids=itertools.count(30)
Y=[0]
def pos():
    Y[0]+=150; return {"designer":{"x":0,"y":Y[0]}}
def mini(js):
    out=[]
    for line in js.split("\n"):
        t=line.strip()
        if not t or t.startswith("//"): continue
        t=re.sub(r"\s+//[^\"']*$","",t)
        out.append(t)
    return "\n".join(out)
def code(src, inputs, name):
    return {"id":next(ids),"module":"code:ExecuteCode","version":1,"parameters":{},
      "mapper":{"input":[{"name":k,"value":v} for k,v in inputs.items()],"language":"javascript","inputFormat":"editor","dependencies":[],"codeEditorJavascript":mini(open("code/"+src).read())},
      "metadata":{"designer":{"x":0,"y":0,"name":name}}}
def withfilter(mod, name, conds):
    mod["filter"]={"name":name,"conditions":conds}; return mod
TOKF=[[{"a":"{{3.wa_token}}","o":"text:notequal","b":TOK}]]
def wa(name, body, extra=None):
    m={"id":next(ids),"module":"http:MakeRequest","version":4,"parameters":{"tlsType":"","authenticationType":"noAuth"},
     "mapper":{"url":"https://graph.facebook.com/{{3.graph_version}}/{{3.wa_phone_id}}/messages","method":"post",
      "headers":[{"name":"Authorization","value":"Bearer {{3.wa_token}}"},{"name":"Content-Type","value":"application/json"}],
      "contentType":"json","inputMethod":"jsonString","jsonStringBodyContent":body,"shareCookies":False,"parseResponse":True,
      "allowRedirects":True,"stopOnHttpError":True,"requestCompressedContent":True},"metadata":{"designer":{"x":0,"y":0,"name":name}}}
    conds=[TOKF[0]+(extra or [])]
    m["filter"]={"name":"Token pasted in","conditions":conds}
    return m
def router(branches, name=None, conds=None, fallback=None):
    r={"id":next(ids),"module":"builtin:BasicRouter","version":1,"parameters":({"else":fallback} if fallback is not None else {}),"mapper":None,
       "metadata":{"designer":{"x":0,"y":0}},"routes":[{"flow":b} for b in branches]}
    if conds: r["filter"]={"name":name,"conditions":conds}
    return r
def upd(values, name, rownum="{{4.`__ROW_NUMBER__`}}"):
    return {"id":next(ids),"module":"google-sheets:updateRow","version":2,"parameters":{"__IMTCONN__":CONN},
     "mapper":{"select":"map","spreadsheetId":SID,"sheetId":"BookingSession","rowNumber":rownum,"valueInputOption":"RAW","values":dict(values,**{"16":"{{now}}"})},
     "metadata":{"designer":{"x":0,"y":0,"name":name}}}
def gcal(url, method, qs=None, body=None, name=""):
    mp={"url":url,"method":method,"headers":[{"key":"Content-Type","value":"application/json"}] if body else []}
    if qs: mp["qs"]=[{"key":k,"value":v} for k,v in qs]
    if body: mp["body"]=body
    return {"id":next(ids),"module":"google-calendar:makeApiCall","version":5,"parameters":{"__IMTCONN__":CONN},"mapper":mp,"metadata":{"designer":{"x":0,"y":0,"name":name}}}
def cdb_search():
    return {"id":next(ids),"module":"google-sheets:filterRows","version":2,"parameters":{"__IMTCONN__":CONN},
     "mapper":{"from":"share","spreadsheetId":SID,"sheetId":"ClientDatabase","includesHeaders":True,"tableFirstRow":"A1:Z1","limit":"1","sortOrder":"asc",
      "valueRenderOption":"FORMATTED_VALUE","dateTimeRenderOption":"FORMATTED_STRING","filter":[[{"a":"A","b":"{{3.wa_id}}","o":"text:equal"}]]},
     "metadata":{"designer":{"x":0,"y":0,"name":"ClientDatabase lookup"}}}
def J(o): return json.dumps(o,ensure_ascii=False)
def body_text(txt_expr_json):   # txt_expr_json is a JSON string literal or a mapping that yields one
    return '{"messaging_product":"whatsapp","to":"{{3.wa_id}}","type":"text","text":{"body":'+txt_expr_json+'}}'
def body_static(text): return body_text(J(text))
def body_buttons(text_json, buttons):
    return '{"messaging_product":"whatsapp","to":"{{3.wa_id}}","type":"interactive","interactive":{"type":"button","body":{"text":'+text_json+'},"action":{"buttons":'+J([{"type":"reply","reply":{"id":i,"title":t}} for i,t in buttons])+'}}}'
SVC=[("svc_basic","Basic Clean"),("svc_deep","Deep Clean"),("svc_moveout","Move Out / In")]
SLOT=[("slot_0800","08:00"),("slot_1200","12:00"),("slot_1500","15:00")]
PROP=[("prop_apartment","Apartment"),("prop_office","Office"),("prop_house","House")]
RET=[("ret_yes","Yes, same place"),("ret_no","No, different place")]
BUILD_ROWS=[("bld_mouille","Mouille Point",""),("bld_seapoint","Sea Point",""),("bld_cbd","Cape Town CBD",""),("bld_other","Other","Somewhere else")]
def body_list(text_json, button, sections_expr):
    return '{"messaging_product":"whatsapp","to":"{{3.wa_id}}","type":"interactive","interactive":{"type":"list","body":{"text":'+text_json+'},"action":{"button":'+J(button)+',"sections":'+sections_expr+'}}}'
svc_body=body_buttons(J("Hi! 👋 Welcome to *Rags to Riches Cleaning*.\nWhat kind of clean do you need?"),SVC)
def time_body(prefix):
    return body_buttons('"'+prefix+'What time should the team arrive on *{{4.`5`}}*?"',SLOT)
CLEAR={str(k):"{{emptystring}}" for k in list(range(2,16))+[17]}
def s(k): return "{{4.`%d`}}"%k
def cond(a,o,b=None):
    c={"a":a,"o":o}
    if b is not None: c["b"]=b
    return c
HAS=cond("{{4.`__ROW_NUMBER__`}}","exist")
def step_is(x): return cond(s(1),"text:equal",x)
def tap_has(x): return cond("{{3.tap_id}}","text:contain",x)
def tap_is(x): return cond("{{3.tap_id}}","text:equal",x)

# ---------- finalize chain (used by returning-yes and name-complete) ----------
def finalize(name_expr):
    g=gcal("/v3/calendars/"+CAL+"/events","GET",qs=[("timeMin","{{replace(4.`4`; \"day_\"; \"\")}}T00:00:00+02:00"),("timeMax","{{replace(4.`4`; \"day_\"; \"\")}}T23:59:59+02:00"),("singleEvents","true"),("maxResults","50")],name="Re-check slot (calendar)")
    c=code("C.js",{"events_json":"{{%d.body}}"%g["id"],"start_iso":s(7),"end_iso":s(8),"service_id":s(2),"day_capacity":"{{3.day_capacity}}","off_blocks_day":"{{3.off_blocks_day}}"},"Day capacity re-check")
    f=code("F.js",{"service_id":s(2),"service_label":s(3),"client_name":name_expr,"property_type":s(17),"unit_number":s(10),"building_name":s(11),
        "access_code":s(12),"access_note":s(13),"when_label":s(9),"start_iso":s(7),"end_iso":s(8),"wa_id":"{{3.wa_id}}",
        "holidays":"{{3.holidays}}","late_window":"{{3.late_window}}","bank_details":"{{3.bank_details}}"},"Build confirmation + event")
    ev=gcal("/v3/calendars/"+CAL+"/events","POST",body="{{%d.result.event_json}}"%f["id"],name="Create calendar event")
    cs=cdb_search()
    cdb_upd={"id":next(ids),"module":"google-sheets:updateRow","version":2,"parameters":{"__IMTCONN__":CONN},
      "filter":{"name":"Known client","conditions":[[cond("{{%d.`__ROW_NUMBER__`}}"%cs["id"],"exist")]]},
      "mapper":{"select":"map","spreadsheetId":SID,"sheetId":"ClientDatabase","rowNumber":"{{%d.`__ROW_NUMBER__`}}"%cs["id"],"valueInputOption":"RAW",
       "values":{"1":name_expr,"2":s(11),"4":s(10),"5":s(12),"6":s(13),"7":s(17),"10":"{{replace(4.`4`; \"day_\"; \"\")}}",
                 "11":"{{parseNumber(ifempty(%d.`11`; \"0\")) + 1}}"%cs["id"],"12":s(3)}},"metadata":{"designer":{"x":0,"y":0,"name":"Update client"}}}
    cdb_add={"id":next(ids),"module":"google-sheets:addRow","version":2,"parameters":{"__IMTCONN__":CONN},
      "filter":{"name":"New client","conditions":[[cond("{{%d.`__IMTLENGTH__`}}"%cs["id"],"number:equal","0")]]},
      "mapper":{"mode":"map","spreadsheetId":SID,"sheetId":"ClientDatabase","tableFirstRow":"A1:Z1","insertDataOption":"INSERT_ROWS","valueInputOption":"RAW","insertUnformatted":False,
       "values":{"0":"{{3.wa_id}}","1":name_expr,"2":s(11),"4":s(10),"5":s(12),"6":s(13),"7":s(17),"8":"New",
                 "9":"{{replace(4.`4`; \"day_\"; \"\")}}","10":"{{replace(4.`4`; \"day_\"; \"\")}}","11":"1","12":s(3),"13":"Bot"}},
      "metadata":{"designer":{"x":0,"y":0,"name":"Add client"}}}
    alert=wa("Alert Nita (template)",
      '{"messaging_product":"whatsapp","to":"{{3.nita_alert_number}}","type":"template","template":{"name":"{{3.alert_template}}","language":{"code":"en"},"components":[{"type":"body","parameters":{{%d.result.alert_params_json}}}]}}'%f["id"],
      [cond("{{3.alert_template}}","text:notequal",TPL)])
    free=[f, ev, router([
        [wa("Send confirmation",body_text("{{%d.result.confirm_json}}"%f["id"]))],
        [cs, router([[cdb_upd],[cdb_add]])],
        [upd({"1":"DONE","14":name_expr,"15":"{{%d.body.id}}"%ev["id"]},"Session: DONE")],
        [alert]])]
    free[0]["filter"]={"name":"Still free","conditions":[[cond("{{%d.result.slot_full}}"%c["id"],"text:notequal","true")]]}
    full=router([[wa("Send day just filled",body_static("Sorry, that day was just booked up by someone else 😕 Send *menu* to pick another day."))],
                 [upd({"1":"TIME","6":"{{emptystring}}","7":"{{emptystring}}","8":"{{emptystring}}","9":"{{emptystring}}"},"Session: back to TIME")]],
                name="Slot taken meanwhile",conds=[[cond("{{%d.result.slot_full}}"%c["id"],"text:equal","true")]])
    return [g,c,router([[full],free])]

# ---------- Claude text steps ----------
def claude_step(step, complete_flow):
    d=code("D.js",{"step":step,"client_text":"{{3.text}}","saved_unit":s(10),"saved_code":s(12),"property_type":s(17),"system_prompt":"{{3.system_prompt}}"},"Build Claude request")
    h={"id":next(ids),"module":"http:MakeRequest","version":4,"parameters":{"tlsType":"","authenticationType":"noAuth"},
       "mapper":{"url":"https://api.anthropic.com/v1/messages","method":"post",
        "headers":[{"name":"x-api-key","value":"{{3.anthropic_key}}"},{"name":"anthropic-version","value":"2023-06-01"},{"name":"content-type","value":"application/json"}],
        "contentType":"json","inputMethod":"jsonString","jsonStringBodyContent":"{{%d.result.body_json}}"%d["id"],"shareCookies":False,"parseResponse":True,
        "allowRedirects":True,"stopOnHttpError":False,"requestCompressedContent":True,"timeout":"30"},"metadata":{"designer":{"x":0,"y":0,"name":"Claude API"}}}
    e=code("E.js",{"claude_body":"{{%d.data}}"%h["id"],"step":step,"saved_unit":s(10),"saved_code":s(12)},"Parse Claude (immediately)")
    E=e["id"]
    ok=cond("{{%d.result.is_complete}}"%E,"text:equal","true")
    notok=cond("{{%d.result.is_complete}}"%E,"text:notequal","true")
    i_is=lambda x: cond("{{%d.result.intent}}"%E,"text:equal",x)
    i_not=lambda x: cond("{{%d.result.intent}}"%E,"text:notequal",x)
    partial={"10":"{{%d.result.unit_number}}"%E,"12":"{{%d.result.access_code}}"%E} if step=="UNIT_ACCESS" else {}
    r=router([
      [router(complete_flow,name="Complete",conds=[[ok]])],
      [router([[wa("Send reprompt",body_text("{{%d.result.reprompt_json}}"%E))]]+([[upd(partial,"Save partial unit/code")]] if partial else []),
              name="Incomplete",conds=[[notok,i_not("restart"),i_not("cancel")]])],
      [router([[wa("Send service buttons (restart)",svc_body)],[upd(dict(CLEAR,**{"1":"SERVICE"}),"Session: restart")]],name="Restart",conds=[[i_is("restart")]])],
      [router([[wa("Send cancelled",body_static("No problem, I've stopped this booking. Send *hi* any time to book."))],[upd(dict(CLEAR,**{"1":"CANCELLED"}),"Session: cancelled")]],name="Cancel",conds=[[i_is("cancel")]])]])
    return d,h,e,r,E

# ---------- routes ----------
A=router([
  [wa("Send service buttons",svc_body)],
  [withfilter(upd(dict(CLEAR,**{"1":"SERVICE"}),"Reset session row"),"Has session: reset it",[[HAS]])],
  [{"id":next(ids),"module":"google-sheets:addRow","version":2,"parameters":{"__IMTCONN__":CONN},
    "filter":{"name":"No session: create it","conditions":[[cond("{{4.`__IMTLENGTH__`}}","number:equal","0")]]},
    "mapper":{"mode":"map","spreadsheetId":SID,"sheetId":"BookingSession","tableFirstRow":"A1:Z1","insertDataOption":"INSERT_ROWS","valueInputOption":"RAW","insertUnformatted":False,
     "values":{"0":"{{3.wa_id}}","1":"SERVICE","16":"{{now}}"}},"metadata":{"designer":{"x":0,"y":0,"name":"Create session row"}}}]],
  name="A: Greeting Interceptor",conds=[[cond("{{4.`__IMTLENGTH__`}}","number:equal","0")],[cond("{{3.is_reset}}","text:equal","yes")],
    [cond("{{3.is_hello}}","text:equal","yes"),cond(s(1),"text:notequal","UNIT_ACCESS"),cond(s(1),"text:notequal","NAME")]])

dp=code("A.js",{"holidays":"{{3.holidays}}","same_day_cutoff":"{{3.same_day_cutoff}}","window_days":"7"},"Day picker")
dp["filter"]={"name":"B: Service tapped","conditions":[[HAS,tap_has("svc_")]]}
B=[dp, router([
  [wa("Send day list",body_list(J("Which day suits you?"),"Choose a day","{{%d.result.sections_json}}"%dp["id"]))],
  [upd(dict(CLEAR,**{"1":"DAY","2":"{{3.tap_id}}"}),"Session: DAY")]])]

C=router([
  [router([[wa("Send time buttons",body_buttons('"What time should the team arrive on *{{3.tap_title}}*?\\n\\n_Guests usually check out at 10 or 11 and new guests arrive at 15:00._"',SLOT))],
           [upd({"1":"TIME","4":"{{3.tap_id}}","5":"{{3.tap_title}}"},"Session: TIME")]],name="Normal day",conds=[[cond("{{3.tap_id}}","text:notequal","day_later")]])],
  [router([[wa("Send later-date note",body_static("For dates more than a week away, please message Nita directly and she'll book you in 🙂"))]],name="Later date",conds=[[tap_is("day_later")]])]],
  name="C: Day tapped",conds=[[tap_has("day_"),step_is("DAY")],[tap_has("day_"),step_is("TIME")]])

sb=code("B.js",{"day_id":s(4),"slot_id":"{{3.tap_id}}","service_id":s(2)},"Date + duration builder")
sb["filter"]={"name":"D: Time tapped","conditions":[[tap_has("slot_"),step_is("TIME")]]}
g=gcal("/v3/calendars/"+CAL+"/events","GET",qs=[("timeMin","{{%d.result.day_start}}"%sb["id"]),("timeMax","{{%d.result.day_end}}"%sb["id"]),("singleEvents","true"),("maxResults","50")],name="Calendar: jobs in that window")
g["filter"]={"name":"Slot valid","conditions":[[cond("{{%d.result.ok}}"%sb["id"],"text:equal","true")]]}
cc=code("C.js",{"events_json":"{{%d.body}}"%g["id"],"start_iso":"{{%d.result.start_iso}}"%sb["id"],"end_iso":"{{%d.result.end_iso}}"%sb["id"],"service_id":s(2),"day_capacity":"{{3.day_capacity}}","off_blocks_day":"{{3.off_blocks_day}}"},"Day capacity check")
cs=cdb_search(); cs["filter"]={"name":"Slot free","conditions":[[cond("{{%d.result.slot_full}}"%cc["id"],"text:notequal","true")]]}
CS=cs["id"]
slotvals={"3":"{{%d.result.service_label}}"%sb["id"],"6":"{{3.tap_id}}","7":"{{%d.result.start_iso}}"%sb["id"],"8":"{{%d.result.end_iso}}"%sb["id"],"9":"{{%d.result.when_label}}"%sb["id"]}
known=[[cond("{{%d.`__ROW_NUMBER__`}}"%CS,"exist"),cond("{{%d.`4`}}"%CS,"exist"),cond("{{%d.`5`}}"%CS,"exist")]]
D=[sb, router([
  [router([[wa("Send slot error",body_text("{{%d.result.error_text_json}}"%sb["id"]))]],name="Slot invalid",conds=[[cond("{{%d.result.ok}}"%sb["id"],"text:notequal","true")]])],
  [g, cc, router([
     [router([[wa("Send day full",body_text('"Sorry, we can\'t fit a {{%d.result.service_label}} on *{{%d.result.day_label}}*, the team is fully booked that day 😕\\n\\nSend *menu* to pick another day."'%(sb["id"],sb["id"])))]],
             name="Slot full",conds=[[cond("{{%d.result.slot_full}}"%cc["id"],"text:equal","true")]])],
     [cs, router([
        [router([[wa("Send same place?",body_buttons('"{{%d.result.when_label}} is available ✅\\n\\nWelcome back, {{first(split(%d.`1`; " "))}}! Same place as last time?\\n🏢 {{%d.`2`}} Unit {{%d.`4`}}"'%(sb["id"],CS,CS,CS),RET))],
                 [upd(dict(slotvals,**{"1":"RETURNING","10":"{{%d.`4`}}"%CS,"11":"{{%d.`2`}}"%CS,"12":"{{%d.`5`}}"%CS,"13":"{{%d.`6`}}"%CS,"14":"{{%d.`1`}}"%CS,"17":"{{%d.`7`}}"%CS}),"Session: RETURNING")]],
                name="Known client",conds=known)],
        [router([[wa("Send property buttons",body_buttons('"{{%d.result.when_label}} is available ✅\\n\\nWhat kind of place is it?"'%sb["id"],PROP))],
                 [upd(dict(slotvals,**{"1":"PROPERTY"}),"Session: PROPERTY")]],
                name="New client",conds=[[cond("{{%d.`__ROW_NUMBER__`}}"%CS,"notexist")],[cond("{{%d.`4`}}"%CS,"notexist")],[cond("{{%d.`5`}}"%CS,"notexist")]])]])]])]])]

E=router([
  [router([finalize(s(14))],name="Same place: yes",conds=[[tap_is("ret_yes")]])],
  [router([[wa("Send property buttons (different place)",body_buttons(J("No problem. What kind of place is it?"),PROP))],
           [upd({"1":"PROPERTY","10":"{{emptystring}}","11":"{{emptystring}}","12":"{{emptystring}}","13":"{{emptystring}}","17":"{{emptystring}}"},"Session: PROPERTY")]],
          name="Same place: no",conds=[[tap_is("ret_no")]])]],
  name="E: Same place? tapped",conds=[[tap_has("ret_"),step_is("RETURNING")]])

F=router([
  [router([[wa("Send building list",body_list(J("Which area or building is it in?"),"Choose",J([{"title":"Buildings","rows":[dict({"id":i,"title":t},**({"description":dd} if dd else {})) for i,t,dd in BUILD_ROWS]}])))],
           [upd({"1":"BUILDING","17":"Apartment"},"Session: BUILDING")]],name="Apartment",conds=[[tap_is("prop_apartment")]])],
  [router([[wa("Send address + code question",body_static("Please send the *street address* and the *gate or access code*, e.g. _12 Beach Road, Mouille Point, gate code 4471_\n\nNo code? Just tell me how the team gets in."))],
           [upd({"1":"UNIT_ACCESS","11":"{{emptystring}}","17":"{{3.tap_title}}"},"Session: UNIT_ACCESS")]],name="Office or house",conds=[[tap_is("prop_office")],[tap_is("prop_house")]])]],
  name="F: Property tapped",conds=[[tap_has("prop_"),step_is("PROPERTY")]])

G=router([
  [wa("Send unit + code question",body_static("Please send your *apartment number* and the *lockbox or gate code*, e.g. _Unit 1204, code 4471_\n\nNo lockbox? Just say so, e.g. _keys at reception_."))],
  [upd({"1":"UNIT_ACCESS","11":"{{if(3.tap_id = \"bld_other\"; emptystring; 3.tap_title)}}"},"Session: UNIT_ACCESS")]],
  name="G: Building tapped",conds=[[tap_has("bld_"),step_is("BUILDING")]])

hd,hh,he,hr,HE=claude_step("UNIT_ACCESS",[
  [wa("Send name question",body_static("Got it, thanks! Last thing: what name should Nita put the booking under?"))],
  [upd({"1":"NAME","10":"{{%d.result.unit_number}}"%0,"11":"x","12":"x","13":"x"},"tmp")]])
# fix the placeholder session update now that we know the parse id
hr["routes"][0]["flow"][0]["routes"][1]["flow"][0]["mapper"]["values"]={"1":"NAME","10":"{{%d.result.unit_number}}"%HE,
   "11":"{{ifempty(%d.result.building_name; 4.`11`)}}"%HE,"12":"{{%d.result.access_code}}"%HE,"13":"{{%d.result.access_note}}"%HE,"16":"{{now}}"}
hr["routes"][0]["flow"][0]["routes"][1]["flow"][0]["metadata"]["designer"]["name"]="Session: NAME + unit/code"
hd["filter"]={"name":"H: Unit + code typed","conditions":[[cond("{{3.msg_type}}","text:equal","text"),step_is("UNIT_ACCESS"),cond("{{3.is_reset}}","text:equal","no")]]}
H=[hd,hh,he,hr]

nd,nh,ne,nr,NE=claude_step("NAME",[])
nr["routes"][0]["flow"][0]["routes"]=[{"flow":b} for b in [finalize("{{%d.result.client_name}}"%NE)]]
nd["filter"]={"name":"I: Name typed","conditions":[[cond("{{3.msg_type}}","text:equal","text"),step_is("NAME"),cond("{{3.is_reset}}","text:equal","no")]]}
I=[nd,nh,ne,nr]

Z=router([[wa("Send nudge",body_static("Sorry, I can only read typed messages and button taps 🙂 Please tap an option above, type your reply, or send *hi* to start a booking."))]])

main={"id":5,"module":"builtin:BasicRouter","version":1,"parameters":{"else":9},"mapper":None,"metadata":{"designer":{"x":900,"y":0}},
  "routes":[{"flow":[A]},{"flow":B},{"flow":[C]},{"flow":D},{"flow":[E]},{"flow":[F]},{"flow":[G]},{"flow":H},{"flow":I},{"flow":[Z]}]}
log={"id":6,"module":"google-sheets:addRow","version":2,"parameters":{"__IMTCONN__":CONN},
  "mapper":{"mode":"map","spreadsheetId":SID,"sheetId":"ChatMemory","tableFirstRow":"A1:Z1","insertDataOption":"INSERT_ROWS","valueInputOption":"RAW","insertUnformatted":False,
   "values":{"0":"{{now}}","1":"{{3.wa_id}}","2":"{{3.msg_id}}","3":"{{3.msg_type}}","4":"{{ifempty(4.`1`; \"NEW\")}}",
             "5":"{{if(4.`1` = \"UNIT_ACCESS\"; \"[unit/code reply]\"; ifempty(3.tap_id; 3.text))}}"}},
  "metadata":{"designer":{"x":900,"y":600,"name":"Log to ChatMemory (after reply)"}}}
top={"id":7,"module":"builtin:BasicRouter","version":1,"parameters":{},"mapper":None,"metadata":{"designer":{"x":750,"y":0}},"routes":[{"flow":[main]},{"flow":[log]}]}

old=json.load(open('base.json'))
m3=old["flow"][1]
for v in m3["mapper"]["variables"]:
    pass
m3["mapper"]["variables"]=[v for v in m3["mapper"]["variables"] if v["name"] not in ("wa_phone_id","wa_token","graph_version")]+[
  {"name":"wa_phone_id","value":"PASTE_PHONE_NUMBER_ID"},{"name":"wa_token","value":TOK},{"name":"graph_version","value":"v25.0"},
  {"name":"anthropic_key","value":AKEY},{"name":"system_prompt","value":open("system-prompt.txt").read()},
  {"name":"holidays","value":"2026-12-16,2026-12-25,2026-12-26,2027-01-01,2027-03-22,2027-03-26,2027-03-29,2027-04-27,2027-05-01,2027-06-16,2027-08-09,2027-09-24,2027-12-16,2027-12-25,2027-12-27"},
  {"name":"same_day_cutoff","value":"07:00"},{"name":"late_window","value":"24 hours"},{"name":"bank_details","value":(open("../../private/r2r-bank-details.txt").read() if __import__("os").path.exists("../../private/r2r-bank-details.txt") else "")},{"name":"day_capacity","value":"2"},{"name":"off_blocks_day","value":"no"},
  {"name":"alert_template","value":TPL},{"name":"nita_alert_number","value":"PASTE_NITA_NUMBER"}]
# VERIFY=1: adds the Meta webhook handshake (answers hub.challenge) and turns sequential off,
# because Make ignores Webhook response modules while sequential processing is on.
# Run once while Meta's Configuration screen is verifying, then rebuild without it.
VERIFY=__import__("os").environ.get("VERIFY")=="1"
if VERIFY:
    respond={"id":8,"module":"gateway:WebhookRespond","version":1,"parameters":{},
      "mapper":{"body":"{{1.hub_challenge}}","status":"200","headers":[]},
      "filter":{"name":"Meta verification","conditions":[[{"a":"{{1.hub_mode}}","b":"subscribe","o":"text:equal"}]]},
      "metadata":{"designer":{"x":0,"y":0,"name":"Answer Meta handshake"}}}
    vr={"id":9,"module":"builtin:BasicRouter","version":1,"parameters":{},"mapper":None,"metadata":{"designer":{"x":0,"y":0}},
        "routes":[{"flow":[respond]},{"flow":[m3,old["flow"][2],top]}]}
    flow=[old["flow"][0],vr]
    old["metadata"]["scenario"]["sequential"]=False
else:
    flow=[old["flow"][0],m3,old["flow"][2],top]
    old["metadata"]["scenario"]["sequential"]=True
bp={"name":"Rags to Riches - Booking Bot","flow":flow,"metadata":old["metadata"]}
# layout: spread designer coords
def lay(fl,x,y):
    for m in fl:
        m.setdefault("metadata",{}).setdefault("designer",{}); m["metadata"]["designer"]["x"]=x; m["metadata"]["designer"]["y"]=y[0]
        x+=300
        for r in m.get("routes",[]) or []:
            lay(r["flow"],x,y); y[0]+=300
lay(flow,0,[0])
json.dump(bp,open('full.json','w'),ensure_ascii=False,separators=(',',':'))
cnt=[0]
def c(fl):
    for m in fl:
        cnt[0]+=1
        for r in m.get("routes",[]) or []: c(r["flow"])
c(flow); print("modules",cnt[0],"bytes",len(json.dumps(bp,ensure_ascii=False)))
