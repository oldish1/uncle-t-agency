/* Canvas drawings of the two machines. Pure functions: (ctx state, progress) -> pixels. */
export const C = {
  table: '#1c2228', slat: '#222a31', plate: '#a9b1b8', part: '#c9d0d6',
  kerf: '#0b0e11', laser: '#ff5a1f', hot: '#fff3e6', spark: '#ffb36b',
  die: '#323d46', punch: '#66737f', sheet: '#e2e6e9', frame: '#10151a', accent: '#ff5a1f'
};
export const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
export const ease = t => (t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);

function laserPaths(pw, ph) {
  const m = Math.min(pw, ph);
  const circ = (u, v, r, n = 36) => Array.from({ length: n + 1 }, (_, i) => {
    const a = (i / n) * Math.PI * 2; return [u * pw + Math.cos(a) * r * m, v * ph + Math.sin(a) * r * m];
  });
  const holes = [[.26, .34], [.74, .34], [.26, .66], [.74, .66]].map(([u, v]) => ({ pts: circ(u, v, .07), hole: true }));
  const sl = [], sr = .035 * m, x0 = .43 * pw, x1 = .57 * pw, cy = .5 * ph;
  for (let i = 0; i <= 12; i++) { const a = -Math.PI / 2 + (i / 12) * Math.PI; sl.push([x1 + Math.cos(a) * sr, cy + Math.sin(a) * sr]); }
  for (let i = 0; i <= 12; i++) { const a = Math.PI / 2 + (i / 12) * Math.PI; sl.push([x0 + Math.cos(a) * sr, cy + Math.sin(a) * sr]); }
  sl.push(sl[0]);
  const r = Math.min(.06 * m, 30), L = .14 * pw, R = .86 * pw, T = .17 * ph, B = .83 * ph, out = [];
  const arc = (cx, cy2, a0) => { for (let i = 0; i <= 8; i++) { const a = a0 + (i / 8) * Math.PI / 2; out.push([cx + Math.cos(a) * r, cy2 + Math.sin(a) * r]); } };
  arc(L + r, T + r, Math.PI); arc(R - r, T + r, Math.PI * 1.5); arc(R - r, B - r, 0); arc(L + r, B - r, Math.PI / 2); out.push(out[0]);
  return [...holes, { pts: sl, hole: true }, { pts: out, hole: false }];
}

const sparks = new Map();

export function drawLaser(o, lp, id, live) {
  const { ctx, w, h, dpr } = o;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.fillStyle = C.table; ctx.fillRect(0, 0, w, h);
  ctx.fillStyle = C.slat;
  const step = Math.max(14, h / 9);
  for (let x = -step * .25; x < w; x += step) ctx.fillRect(x, 0, step * .45, h);

  const px = w * .06, py = h * .1, pw = w * .88, ph = h * .8;
  ctx.save(); ctx.translate(px, py);
  ctx.fillStyle = C.plate; ctx.fillRect(0, 0, pw, ph);

  const subs = laserPaths(pw, ph);
  const seq = [], ends = []; let total = 0, last = null;
  subs.forEach((s, si) => {
    if (last) { const d = Math.hypot(s.pts[0][0] - last[0], s.pts[0][1] - last[1]) * .22; seq.push({ a: last, b: s.pts[0], len: d, on: false, si }); total += d; }
    for (let i = 1; i < s.pts.length; i++) {
      const a = s.pts[i - 1], b = s.pts[i], d = Math.hypot(b[0] - a[0], b[1] - a[1]);
      seq.push({ a, b, len: d, on: true, si }); total += d;
    }
    last = s.pts[s.pts.length - 1]; ends[si] = total;
  });
  const dist = clamp(lp) * total;
  let acc = 0, head = subs[0].pts[0], ang = 0, on = false;
  const partial = subs.map(() => []);
  for (const sg of seq) {
    if (acc + sg.len <= dist) { if (sg.on) partial[sg.si].push([sg.a, sg.b]); acc += sg.len; head = sg.b; ang = Math.atan2(sg.b[1] - sg.a[1], sg.b[0] - sg.a[0]); }
    else {
      const f = sg.len ? (dist - acc) / sg.len : 0;
      head = [sg.a[0] + (sg.b[0] - sg.a[0]) * f, sg.a[1] + (sg.b[1] - sg.a[1]) * f];
      ang = Math.atan2(sg.b[1] - sg.a[1], sg.b[0] - sg.a[0]);
      if (sg.on) partial[sg.si].push([sg.a, head]);
      on = sg.on && lp > 0 && lp < 1; acc = dist; break;
    }
  }
  const done = subs.map((_, si) => lp > 0 && dist >= ends[si] - 1e-6);
  const path = s => { ctx.beginPath(); s.pts.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y))); ctx.closePath(); };

  const outerDone = done[subs.length - 1];
  if (outerDone) {
    const s = subs[subs.length - 1];
    // the finished part, slightly lifted from the offcut
    ctx.save(); ctx.translate(0, -Math.min(w, h) * .006); path(s); ctx.fillStyle = C.part; ctx.fill(); ctx.restore();
  }
  subs.forEach((s, si) => { if (s.hole && done[si]) { path(s); ctx.fillStyle = C.table; ctx.fill(); } });

  ctx.strokeStyle = C.kerf; ctx.lineWidth = Math.max(2, Math.min(w, h) * .012); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  partial.forEach(list => {
    if (!list.length) return; ctx.beginPath();
    list.forEach(([a, b], i) => { if (i === 0 || list[i - 1][1] !== a) ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); });
    ctx.stroke();
  });

  // gantry bridge and carriage: the real machine moves like this
  if (lp > 0 && lp < 1) {
    const bh = Math.max(10, Math.min(w, h) * .05);
    ctx.fillStyle = C.frame; ctx.fillRect(-px, head[1] - bh / 2, w, bh);
    ctx.fillStyle = '#2c353d'; ctx.fillRect(-px, head[1] - bh / 2, w, bh * .28);
    ctx.fillStyle = '#46515b'; ctx.fillRect(head[0] - bh * 1.2, head[1] - bh * .9, bh * 2.4, bh * 1.8);
  }

  let arr = sparks.get(id); if (!arr) { arr = []; sparks.set(id, arr); }
  const dt = live ? 1 / 60 : 0;
  if (on && live) {
    const sc = Math.min(w, h) / 260;
    for (let i = 0; i < 4; i++) {
      const a = ang + Math.PI + (Math.random() - .5) * 1.7, sp = (80 + Math.random() * 240) * sc;
      arr.push({ x: head[0], y: head[1], vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: .25 + Math.random() * .4 });
    }
  }
  for (let i = arr.length - 1; i >= 0; i--) {
    const p = arr[i]; p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt;
    if (p.life <= 0) { arr.splice(i, 1); continue; }
    ctx.globalAlpha = clamp(p.life / .35); ctx.fillStyle = C.spark;
    const r = Math.max(1.3, Math.min(w, h) * .0065);
    ctx.fillRect(p.x - r / 2, p.y - r / 2, r, r);
  }
  ctx.globalAlpha = 1;

  const hr = Math.max(8, Math.min(w, h) * .05);
  if (lp > 0 && lp < 1) { ctx.fillStyle = 'rgba(255,90,31,.28)'; ctx.beginPath(); ctx.arc(head[0], head[1], hr * 1.5, 0, 7); ctx.fill(); ctx.shadowColor = C.laser; ctx.shadowBlur = hr * 2; }
  ctx.fillStyle = C.laser; ctx.beginPath(); ctx.arc(head[0], head[1], hr * .38, 0, 7); ctx.fill();
  ctx.shadowBlur = 0; ctx.fillStyle = C.hot; ctx.beginPath(); ctx.arc(head[0], head[1], hr * .16, 0, 7); ctx.fill();
  ctx.restore();
}

export function drawBrake(o, bp) {
  const { ctx, w, h, dpr } = o;
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.fillStyle = C.table; ctx.fillRect(0, 0, w, h);
  const cx = w / 2, y0 = h * .66, s = Math.min(h * .28, w * .2), th = Math.max(6, Math.min(h * .045, 22));
  const L = Math.min(w * .4, h * .85);
  const theta = clamp(bp) * Math.PI / 4, d = s * Math.tan(theta);
  const yc = y0 - th / 2 + d;

  // machine side frames
  ctx.fillStyle = C.frame; ctx.fillRect(0, 0, w * .045, h); ctx.fillRect(w * .955, 0, w * .045, h);
  ctx.fillStyle = '#1a2128'; ctx.fillRect(w * .045, 0, w * .02, h); ctx.fillRect(w * .935, 0, w * .02, h);

  // bed and V die
  ctx.fillStyle = C.die;
  ctx.beginPath(); ctx.moveTo(w * .065, h); ctx.lineTo(w * .065, y0); ctx.lineTo(cx - s, y0); ctx.lineTo(cx, y0 + s); ctx.lineTo(cx + s, y0); ctx.lineTo(w * .935, y0); ctx.lineTo(w * .935, h); ctx.closePath(); ctx.fill();
  ctx.fillStyle = C.accent; ctx.fillRect(w * .065, h - Math.max(6, h * .022), w * .87, Math.max(6, h * .022));

  // sheet
  ctx.strokeStyle = C.sheet; ctx.lineWidth = th; ctx.lineJoin = 'miter'; ctx.lineCap = 'butt';
  ctx.beginPath(); ctx.moveTo(cx - Math.cos(theta) * L, yc - Math.sin(theta) * L); ctx.lineTo(cx, yc); ctx.lineTo(cx + Math.cos(theta) * L, yc - Math.sin(theta) * L); ctx.stroke();

  // ram and punch
  const tipY = yc - th / 2, ph = Math.min(h * .3, w * .3), half = ph * Math.tan(35 * Math.PI / 180);
  ctx.fillStyle = '#2c353d'; ctx.fillRect(w * .065, -h, w * .87, h + tipY - ph - h * .02);
  ctx.fillStyle = C.punch;
  ctx.beginPath(); ctx.moveTo(cx, tipY); ctx.lineTo(cx - half, tipY - ph); ctx.lineTo(cx - half * 1.25, tipY - ph); ctx.lineTo(cx - half * 1.25, tipY - ph - h * .02); ctx.lineTo(cx + half * 1.25, tipY - ph - h * .02); ctx.lineTo(cx + half * 1.25, tipY - ph); ctx.lineTo(cx + half, tipY - ph); ctx.closePath(); ctx.fill();
  ctx.fillStyle = C.accent; ctx.beginPath(); ctx.moveTo(cx, tipY); ctx.lineTo(cx - half * .28, tipY - ph * .28); ctx.lineTo(cx + half * .28, tipY - ph * .28); ctx.closePath(); ctx.fill();
}
