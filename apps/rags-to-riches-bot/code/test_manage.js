const fs=require('fs');const run=(f,i)=>new Function('input',fs.readFileSync(f,'utf8'))(i);const a=require('assert');
const now='2026-10-28T08:00:00Z'; // Wed 10:00 SAST
const ev=(id,start,summary,svc)=>({id,status:'confirmed',summary,start:{dateTime:start},end:{dateTime:start},description:'Client: Fancy',extendedProperties:{private:{service:svc,wa_id:'27836561976'}}});
const fancy=[ev('e2','2026-11-03T08:00:00+02:00','🧹 Basic Clean · VC · Fancy','svc_basic'), ev('e1','2026-10-29T08:00:00+02:00','🧹 Basic Clean · Bree Street, Unit 2910 · Fancy','svc_basic'),
  ev('e3','2026-11-05T08:00:00+02:00','❌ CANCELLED · Basic Clean · VC · Fancy','svc_basic')];
// X1 lists upcoming, sorted, skips cancelled
let x1=run('X1.js',{events_json:{items:fancy}}); let rows=JSON.parse(x1.sections_json)[0].rows;
a.equal(x1.count,2); a.equal(rows[0].id,'bk_e1'); a.equal(rows[0].title,'Thu 29 Oct, 08:00'); a(rows[0].description.includes('Bree Street, Unit 2910')); a(rows.every(r=>r.title.length<=24));
a.equal(run('X1.js',{events_json:{items:[]}}).count,0);
// X2: 29 Oct 08:00 is 22h away -> late
let x2=run('X2.js',{event_json:fancy[1],now_iso:now}); a.equal(x2.late,'yes'); a(JSON.parse(x2.text_json).includes('R150'));
let x2b=run('X2.js',{event_json:fancy[0],now_iso:now}); a.equal(x2b.late,'no'); a(!JSON.parse(x2b.text_json).includes('R150'));
a.equal(run('X2.js',{event_json:fancy[2],now_iso:now}).ok,false);
// X3 cancel: late -> fee in calendar title and message
let x3=run('X3.js',{booking_json:x2.booking_json,now_iso:now}); let p3=JSON.parse(x3.patch_json);
a(p3.summary.startsWith('❌ CANCELLED · R150 LATE FEE · Basic Clean')); a(p3.description.includes('R150 fee applies')); a(JSON.parse(x3.text_json).includes('R150'));
let x3b=JSON.parse(run('X3.js',{booking_json:x2b.booking_json,now_iso:now}).patch_json); a(x3b.summary.startsWith('❌ CANCELLED · Basic Clean')); a(x3b.description.includes('no fee'));
// cancelled event no longer counts for the day (C.js)
const S='2026-11-05T12:00:00+02:00',E='2026-11-05T15:00:00+02:00';
a.equal(run('C.js',{events_json:{items:[fancy[2],ev('x','2026-11-05T08:00:00+02:00','🧹 Deep Clean · 409 · Megan','svc_deep')]},start_iso:S,end_iso:E,service_id:'svc_basic'}).slot_full,true);
a.equal(run('C.js',{events_json:{items:[fancy[2]]},start_iso:S,end_iso:E,service_id:'svc_deep'}).slot_full,false);
// X4 move: to 6 Nov 12:00, day has one basic -> fits
let x4=run('X4.js',{booking_json:x2b.booking_json,day_id:'rs_day_2026-11-06',slot_id:'rsl_1200',events_json:{items:[ev('o','2026-11-06T08:00:00+02:00','🧹 Basic Clean · 117 · Joy','svc_basic')]},now_iso:now});
a.equal(x4.ok,true); let p4=JSON.parse(x4.patch_json); a.equal(p4.start.dateTime,'2026-11-06T12:00:00+02:00'); a.equal(p4.end.dateTime,'2026-11-06T15:00:00+02:00'); a(p4.description.startsWith('MOVED')); a(!p4.summary);
a(JSON.parse(x4.text_json).includes('Fri 6 Nov, 12:00'));
// X4: moving within its own day doesn't count itself
a.equal(run('X4.js',{booking_json:x2b.booking_json,day_id:'rs_day_2026-11-03',slot_id:'rsl_1500',events_json:{items:[fancy[0],ev('o','2026-11-03T08:00:00+02:00','🧹 Basic Clean · 117 · Joy','svc_basic')]},now_iso:now}).ok,true);
// X4: full day refused
let x4f=run('X4.js',{booking_json:x2b.booking_json,day_id:'rs_day_2026-11-06',slot_id:'rsl_0800',events_json:{items:[{status:'confirmed',summary:'117 & 210',start:{date:'2026-11-06'},end:{date:'2026-11-07'}}]},now_iso:now});
a.equal(x4f.ok,false); a.equal(x4f.full,true); a(JSON.parse(x4f.text_json).includes('stays as it is'));
// X4 late move -> fee flagged
let x4l=JSON.parse(run('X4.js',{booking_json:x2.booking_json,day_id:'rs_day_2026-11-06',slot_id:'rsl_1200',events_json:{items:[]},now_iso:now}).patch_json); a(x4l.summary.endsWith('R150 LATE CHANGE'));
// X5 typed dates
a.equal(run('X5.js',{text:'14 Nov',now_iso:now}).day_id,'rs_day_2026-11-14');
a.equal(run('X5.js',{text:'Friday 14th of November please',now_iso:now}).day_id,'rs_day_2026-11-14');
a.equal(run('X5.js',{text:'14/11',now_iso:now}).day_id,'rs_day_2026-11-14');
a.equal(run('X5.js',{text:'Nov 14',now_iso:now}).day_id,'rs_day_2026-11-14');
a.equal(run('X5.js',{text:'3 Jan',now_iso:now}).day_id,'rs_day_2027-01-03');
a.equal(run('X5.js',{text:'whenever',now_iso:now}).ok,false);
a.equal(run('X5.js',{text:'31 Nov',now_iso:now}).ok,false);
// A.js resched list
let rs=JSON.parse(run('A.js',{now_iso:now,mode:'resched'}).sections_json)[0].rows; a(rs[0].id.startsWith('rs_day_')); a.equal(rs[rs.length-1].id,'rs_other'); a(rs.length<=10);
console.log('CHANGE/CANCEL TESTS PASS');
