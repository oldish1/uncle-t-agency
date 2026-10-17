const fs=require('fs');const run=(f,i)=>new Function('input',fs.readFileSync(f,'utf8'))(i);const a=require('assert');
const H="2026-12-16,2026-12-25";
let r=run('A.js',{now_iso:'2026-09-28T04:00:00Z',holidays:H}); // Mon 06:00 SAST, before 07:00
let rows=JSON.parse(r.sections_json)[0].rows; console.log(rows.map(x=>x.id+' '+x.title+' | '+x.description).join('\n'));
a.equal(rows[0].id,'day_2026-09-28'); a(rows.find(x=>x.title.startsWith('Sun')).description.includes('+R50')); a.equal(rows[rows.length-1].id,'day_multi'); a.equal(rows[rows.length-2].id,'day_later'); a(rows.length<=10);
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
{ // Later date -> weeks -> days (Kobie books weeks ahead)
const now='2026-10-17T08:00:00Z'; // Sat 10:00 SAST
let w=JSON.parse(run('A.js',{now_iso:now,mode:'weeks'}).sections_json)[0].rows;
a.equal(w.length,8); a.equal(w[0].id,'day_wk_2026-10-25'); a.equal(w[0].title,'25 Oct – 31 Oct'); a(w.every(r=>r.title.length<=24));
let d=JSON.parse(run('A.js',{now_iso:now,week_id:'day_wk_2026-10-25'}).sections_json)[0].rows;
a.equal(d[0].id,'day_2026-10-25'); a(d.some(r=>r.id=='day_2026-10-30')); a.equal(d[d.length-1].id,'day_later'); a(d.length<=10);
let m=JSON.parse(run('A.js',{now_iso:now}).sections_json)[0].rows; a.equal(m[m.length-1].id,'day_multi'); a.equal(m[m.length-2].id,'day_later'); a.equal(m[m.length-3].id,'day_2026-10-24'); a(m.length<=10);
let b=run('B.js',{day_id:'day_2026-10-30',slot_id:'slot_0800',service_id:'svc_basic',now_iso:now}); a.equal(b.ok,true);
}
console.log('ALL PASS');
// Nita's day capacity (28 Sept answers)
{
const S='2026-09-29T12:00:00+02:00',E='2026-09-29T14:00:00+02:00';
const ad=(t)=>({status:'confirmed',summary:t,start:{date:'2026-09-29'},end:{date:'2026-09-30'}});
const bot=(svc,s)=>({status:'confirmed',summary:'x',start:{dateTime:s},end:{dateTime:s},extendedProperties:{private:{service:svc}}});
const c=(items,svc,extra={})=>run('C.js',Object.assign({events_json:{items},start_iso:S,end_iso:E,service_id:svc},extra));
a.equal(c([], 'svc_deep').slot_full,false);
a.equal(c([ad('117')],'svc_basic').slot_full,false);        // 1 basic + 1 basic = 2
a.equal(c([ad('117')],'svc_deep').slot_full,true);          // deep needs the whole day
a.equal(c([ad('117 & 210')],'svc_basic').slot_full,true);   // day already has 2
a.equal(c([ad('603 deep')],'svc_basic').slot_full,true);    // her deep entry fills the day
a.equal(c([ad('Off')],'svc_deep').slot_full,false);         // Off = only Nita off
a.equal(c([ad('Off')],'svc_deep',{off_blocks_day:'yes'}).slot_full,true);
a.equal(c([ad('Cassie 501')],'svc_basic').slot_full,false);
a.equal(c([bot('svc_deep','2026-09-29T08:00:00+02:00')],'svc_basic').slot_full,true);
a.equal(c([bot('svc_basic','2026-09-29T08:00:00+02:00')],'svc_basic').slot_full,false);
a.equal(c([bot('svc_basic','2026-09-28T22:30:00Z')],'svc_deep').slot_full,true);  // 00:30 SAST on the 29th counts
a.equal(c([{status:'confirmed',summary:'615',start:{date:'2026-09-28'},end:{date:'2026-09-29'}}],'svc_deep').slot_full,false); // yesterday
const tm=(t)=>({status:'confirmed',summary:t,start:{dateTime:'2026-09-29T08:30:00+02:00'},end:{dateTime:'2026-09-29T09:30:00+02:00'}});
a.equal(c([tm('Off'),ad('117')],'svc_basic').slot_full,false); // her timed "Off" isn't a job
a.equal(c([tm('2910'),ad('409')],'svc_basic').slot_full,true);  // timed job still counts
let b2=run('B.js',{day_id:'day_2026-09-29',slot_id:'slot_1200',service_id:'svc_deep',now_iso:'2026-09-27T10:00:00Z'}); a.equal(b2.day_start,'2026-09-29T00:00:00+02:00');
console.log('DAY CAPACITY TESTS PASS');
}
