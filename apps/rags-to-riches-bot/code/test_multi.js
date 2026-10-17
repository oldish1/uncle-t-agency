const fs=require('fs');const run=(f,i)=>new Function('input',fs.readFileSync(f,'utf8'))(i);const a=require('assert');
const now='2026-10-17T08:00:00Z'; // Sat 10:00 SAST
// M1 builds valid JSON with today's date in it
const m1=JSON.parse(run('M1.js',{client_text:'26 Oct 2910 Bree\n30 Oct 409 "deep"',now_iso:now}).body_json);
a(m1.system.includes('2026-10-17')); a.equal(m1.max_tokens,2000); a(m1.messages[0].content.includes('409 "deep"'));
// Claude's answer for Kobie's list (one date bad, one too far, one past)
const claude=(o)=>({type:'message',stop_reason:'end_turn',content:[{type:'text',text:JSON.stringify(o)}]});
const reply=claude({intent:'details',client_name:'',bookings:[
 {date:'2026-10-30',raw:'30 Oct Bree',unit_number:'2910',building_name:'Bree',access_code:'',service:''},
 {date:'2026-10-26',raw:'26 Oct Bree',unit_number:'2910',building_name:'Bree',access_code:'',service:''},
 {date:'2026-10-24',raw:'24 Oct 603 sea point deep',unit_number:'603',building_name:'Sea Point',access_code:'1234',service:'deep'},
 {date:'2026-10-18',raw:'18 Oct',unit_number:'',building_name:'',access_code:'',service:''},
 {date:'2027-03-01',raw:'1 March',unit_number:'',building_name:'',access_code:'',service:''},
 {date:'2026-10-10',raw:'10 Oct',unit_number:'',building_name:'',access_code:'',service:''},
 {date:'',raw:'sometime next month',unit_number:'',building_name:'',access_code:'',service:''}]});
const m2=run('M2.js',{claude_body:reply,default_service:'svc_basic',saved_name:'Kobie Smit',saved_unit:'2910',saved_building:'Bree',saved_code:'4471',now_iso:now});
const L=JSON.parse(m2.lines_json);
a.equal(m2.has_lines,true); a.equal(L.length,4); a.deepEqual(L.map(x=>x.day),['2026-10-18','2026-10-24','2026-10-26','2026-10-30']);
a.equal(L[0].unit,'2910'); a.equal(L[0].code,'4471');        // no place given -> her usual place + code
a.equal(L[1].service,'svc_deep'); a.equal(L[1].code,'1234');
a.equal(L[2].code,'4471');                                    // same unit as saved -> saved code
a(m2.problems_text.includes('2 months')); a(m2.problems_text.includes('too soon')); a(m2.problems_text.includes("couldn't read"));
a.equal(m2.min_day,'2026-10-18T00:00:00+02:00'); a.equal(m2.max_day,'2026-10-30T23:59:59+02:00');
// unknown client with no name -> asks for name
const m2b=run('M2.js',{claude_body:reply,default_service:'svc_basic',now_iso:now}); a.equal(m2b.has_lines,false); a(JSON.parse(m2b.reprompt_json).includes('name'));
// garbage -> reprompt
a.equal(run('M2.js',{claude_body:'nope',now_iso:now}).ok,false);
// M3 with Nita's real-style calendar: 18 Oct has "2910" all-day (1pt), 24 Oct has "603 sea point" (1pt) -> deep (2pt) doesn't fit
const ev={items:[
 {status:'confirmed',summary:'2910',start:{date:'2026-10-18'},end:{date:'2026-10-19'}},
 {status:'confirmed',summary:'603 sea point',start:{date:'2026-10-24'},end:{date:'2026-10-25'}},
 {status:'confirmed',summary:'Off',start:{date:'2026-10-26'},end:{date:'2026-10-27'}},
 {status:'confirmed',summary:'Off',start:{dateTime:'2026-10-30T08:30:00+02:00'},end:{dateTime:'2026-10-30T09:30:00+02:00'}}]};
const m3=run('M3.js',{events_json:ev,lines_json:m2.lines_json,problems_text:m2.problems_text});
const ok=JSON.parse(m3.ok_lines_json); const txt=JSON.parse(m3.text_json);
a.equal(m3.ok_count,3); a.deepEqual(ok.map(x=>x.day),['2026-10-18','2026-10-26','2026-10-30']);
a(txt.includes('❌ Sat 24 Oct')); a(txt.includes('✅ Sun 18 Oct')); a(txt.includes('Same time for all 3 dates')); a(txt.length<=1000);
// two of her own on one day count against each other (capacity 2): 3 basics on 20 Oct -> third rejected
const three=JSON.stringify([1,2,3].map(i=>({day:'2026-10-20',label:'Tue 20 Oct',service:'svc_basic',unit:String(i),building:'',code:'',raw:'x'})));
a.equal(run('M3.js',{events_json:{items:[]},lines_json:three}).ok_count,2);
// M4 builds events + confirmation
const m4=run('M4.js',{events_json:ev,lines_json:m3.ok_lines_json,slot_id:'slot_0800',client_name:'Kobie Smit',wa_id:'27820000000',now_iso:now});
a.equal(m4.ok,true); a.equal(m4.count,3); a(m4.event_json_3); a.equal(m4.event_json_4,'');
const e1=JSON.parse(m4.event_json_1); a.equal(e1.start.dateTime,'2026-10-18T08:00:00+02:00'); a.equal(e1.end.dateTime,'2026-10-18T11:00:00+02:00');
a(e1.summary.includes('Bree, Unit 2910')); a(e1.description.includes('Access code: 4471')); a(e1.description.includes('R50 Sunday'));
const c=JSON.parse(m4.confirm_json); a(c.includes('Bookings received, Kobie')); a(c.includes('Fri 30 Oct, 08:00'));
// M4: calendar filled meanwhile
const fullEv={items:[{status:'confirmed',summary:'117 & 210',start:{date:'2026-10-30'},end:{date:'2026-10-31'}}]};
const m4b=run('M4.js',{events_json:fullEv,lines_json:m3.ok_lines_json,slot_id:'slot_1200',client_name:'Kobie',wa_id:'27',now_iso:now});
a.equal(m4b.count,2); a(JSON.parse(m4b.confirm_json).includes('just got booked up'));
a.equal(run('M4.js',{lines_json:'[]',slot_id:'slot_0800'}).ok,false);
console.log('MULTI-DATE TESTS PASS');
console.log('---- sample messages ----\n'+txt+'\n----\n'+c);
