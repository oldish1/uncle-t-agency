const fs=require('fs');const run=(f,i)=>new Function('input',fs.readFileSync(f,'utf8'))(i);const a=require('assert');
const H="2026-12-16,2026-12-25";
let r=run('A.js',{now_iso:'2026-09-28T04:00:00Z',holidays:H}); // Mon 06:00 SAST, before 07:00
let rows=JSON.parse(r.sections_json)[0].rows; console.log(rows.map(x=>x.id+' '+x.title+' | '+x.description).join('\n'));
a.equal(rows[0].id,'day_2026-09-28'); a(rows.find(x=>x.title.startsWith('Sun')).description.includes('+R50')); a.equal(rows[rows.length-1].id,'day_later');
r=run('A.js',{now_iso:'2026-09-28T06:00:00Z'}); a.equal(JSON.parse(r.sections_json)[0].rows[0].id,'day_2026-09-29');
r=run('A.js',{now_iso:'2026-12-14T08:00:00Z',holidays:H}); a(JSON.parse(r.sections_json)[0].rows.find(x=>x.id=='day_2026-12-16').description.includes('R60'));
let b=run('B.js',{day_id:'day_2026-09-28',slot_id:'slot_0800',service_id:'svc_basic',now_iso:'2026-09-28T05:30:00Z'}); a.equal(b.ok,false); a.equal(b.error,'too_soon');
b=run('B.js',{day_id:'day_2026-09-28',slot_id:'slot_1200',service_id:'svc_moveout',now_iso:'2026-09-28T05:30:00Z'}); a.equal(b.end_iso,'2026-09-28T16:00:00+02:00');
let d=JSON.parse(run('D.js',{step:'UNIT_ACCESS',property_type:'House',client_text:'12 Beach Rd "gate" 1234',system_prompt:fs.readFileSync('../system-prompt.txt','utf8')}).body_json); a(d.system.includes('PROPERTY line')); a(d.messages[0].content.includes('PROPERTY: House'));
let f=run('F.js',{service_id:'svc_moveout',service_label:'Move Out / Move In Clean',client_name:'Kobie Classen',property_type:'Apartment',unit_number:'1204',building_name:'Sea Point',access_code:'NONE',when_label:'Wed 16 Dec, 08:00 (about 4 hrs)',start_iso:'2026-12-16T08:00:00+02:00',end_iso:'2026-12-16T12:00:00+02:00',holidays:H,wa_id:'27000000002'});
let m=JSON.parse(f.confirm_json); console.log(m); a(m.includes('R1,500 + R60')); a(m.includes('50% deposit')); a(m.includes('reception')); a(m.includes('Nita will send you the banking'));
let fb=JSON.parse(run('F.js',{service_id:'svc_basic',service_label:'Basic Clean',client_name:'Joy',property_type:'House',unit_number:'3 Main Rd',access_code:'55',when_label:'x',start_iso:'2026-10-01T08:00:00+02:00',bank_details:'FNB 123'}).confirm_json); a(fb.includes('3 Main Rd')); a(!fb.includes('Unit')); a(!fb.includes('FNB'));
a.equal(JSON.parse(f.alert_params_json).length,5);
let fs2=JSON.parse(run('F.js',{service_id:'svc_basic',service_label:'Basic Clean',client_name:'Joy',property_type:'Apartment',unit_number:'117',access_code:'NONE',when_label:'x',start_iso:'2026-10-04T08:00:00+02:00'}).confirm_json); a(fs2.includes('R420 to R520 + R50 Sunday rate'));
console.log('ALL PASS');
// Nita's all-day entries
{
const S='2026-09-29T12:00:00+02:00',E='2026-09-29T15:30:00+02:00';
const ad=(t,d1,d2)=>({status:'confirmed',summary:t,start:{date:d1},end:{date:d2}});
const tm=(s,e)=>({status:'confirmed',summary:'bot',start:{dateTime:s},end:{dateTime:e}});
let r=run('C.js',{events_json:{items:[ad('117','2026-09-29','2026-09-30')]},start_iso:S,end_iso:E}); a.equal(r.slot_full,false); a.equal(r.places_left,1);
r=run('C.js',{events_json:{items:[ad('117 & 210','2026-09-29','2026-09-30')]},start_iso:S,end_iso:E}); a.equal(r.slot_full,true); a.equal(r.all_day_jobs,2);
r=run('C.js',{events_json:{items:[ad('Off','2026-09-29','2026-09-30')]},start_iso:S,end_iso:E}); a.equal(r.slot_full,true); a.equal(r.day_off,true);
r=run('C.js',{events_json:{items:[ad('Nita off','2026-09-29','2026-09-30')]},start_iso:S,end_iso:E}); a.equal(r.day_off,true);
r=run('C.js',{events_json:{items:[ad('Off','2026-09-29','2026-09-30')]},start_iso:S,end_iso:E,off_blocks_day:'no'}); a.equal(r.slot_full,false);
r=run('C.js',{events_json:{items:[ad('Cassie 50','2026-09-29','2026-09-30'),tm('2026-09-29T12:00:00+02:00','2026-09-29T14:00:00+02:00')]},start_iso:S,end_iso:E}); a.equal(r.slot_full,true); a.equal(r.peak_busy,2);
r=run('C.js',{events_json:{items:[ad('615','2026-09-28','2026-09-29')]},start_iso:S,end_iso:E}); a.equal(r.slot_full,false); a.equal(r.all_day_jobs,0); // yesterday's entry doesn't count
console.log('ALL-DAY TESTS PASS');
}
