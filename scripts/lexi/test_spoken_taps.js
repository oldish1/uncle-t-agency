// Run: python3 build_spoken_taps.py <blueprint> /tmp/out.json <hook> && node test_spoken_taps.js /tmp/out.json.js
const JS = require('fs').readFileSync(process.argv[2], 'utf8');
const run = new Function('input', JS);
// Friday 25 Sept 2026, 20:00 SAST (18:00 UTC)
const realNow = Date.now; Date.now = () => Date.UTC(2026, 8, 25, 18, 0);
const base = { entryId:'E', displayPhone:'1', phoneId:'2', name:'N', waId:'3', from:'3', msgId:'m', ts:'1' };
const cases = [
 ['day','', 'Saturday please','day_1 Saturday 26 September'],
 ['day','', 'saterdag asseblief','day_1 Saturday 26 September'],
 ['day','', 'tomorrow','Saturday 26 September'],
 ['day','', 'Friday','Friday 2 October'],
 ['day','', 'the 30th','Wednesday 30 September'],
 ['day','', 'Wednesday 1 October','-'], ['day','', 'Thursday 1 October','Thursday 1 October'],
 ['day','', 'Sunday','-'], ['day','', 'Monday?','-'],
 ['day','', 'how much is a wash and blowdry','-'],
 ['day','', 'not Saturday, Friday','-'],
 ['time','Saturday 27 September','10 o clock','10:00 AM'],
 ['time','Saturday 27 September','half past two','02:30 PM'],
 ['time','Saturday 27 September','half tien','09:30 AM'],
 ['time','Friday 26 September','2pm','02:00 PM'],
 ['time','Friday 26 September','14:00','02:00 PM'],
 ['time','Friday 26 September','10h30','-'],          // weekdays are hourly
 ['time','Saturday 27 September','10h30','10:30 AM'],
 ['time','Friday 26 September','9','09:00 AM'],
 ['time','Friday 26 September','nine in the morning','09:00 AM'],
 ['time','Friday 26 September','I will bring 2 friends with me','-'],
 ['time','Friday 26 September','6pm','-'],
 ['time','Friday 26 September','noon','12:00 PM'],
];
let bad = 0;
for (const [stage, day, text, exp] of cases) {
  const r = run({ ...base, text, day });
  const p = JSON.parse(r.payload).entry[0].changes[0].value.messages[0];
  const got = r.matched === 'yes' ? (p.interactive.list_reply.id + ' ' + p.interactive.list_reply.title) : '-';
  const ok = exp === '-' ? got === '-' : got.includes(exp);
  if (!ok) bad++;
  console.log(ok ? 'ok ' : 'BAD', stage.padEnd(4), JSON.stringify(text).padEnd(38), '->', got, r.matched === 'no' ? '(to AI: ' + p.lexi_passthrough + ')' : '');
}
console.log('failures', bad);
