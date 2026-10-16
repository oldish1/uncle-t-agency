/* T & T Engineering: machine animations (laser cutting, press brake) drawn in canvas.
   To use real footage later: put laser.mp4 / brake.mp4 in /media and swap the canvas
   for a <video muted loop playsinline autoplay> in index.html. */
(() => {
  'use strict';

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const C = {
    table: '#1c2228', slat: '#232b32', plate: '#a9b1b8', part: '#c3cad0',
    kerf: '#0d1114', laser: '#ff5a1f', hot: '#fff3e6', spark: '#ffb36b',
    die: '#323d46', punch: '#66737f', sheet: '#e2e6e9', accent: '#ff5a1f'
  };
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
  const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

  /* ---------- canvas plumbing ---------- */
  function setup(canvas) {
    const o = { canvas, ctx: canvas.getContext('2d'), w: 0, h: 0, dpr: 1 };
    const fit = () => {
      const r = canvas.getBoundingClientRect();
      o.dpr = Math.min(devicePixelRatio || 1, 2);
      o.w = Math.max(1, r.width); o.h = Math.max(1, r.height);
      canvas.width = Math.round(o.w * o.dpr); canvas.height = Math.round(o.h * o.dpr);
    };
    fit();
    new ResizeObserver(fit).observe(canvas);
    return o;
  }

  /* ---------- laser scene ---------- */
  const sparks = new Map();
  function laserPaths(pw, ph) {
    const m = Math.min(pw, ph), P = (u, v) => [u * pw, v * ph], circ = (u, v, r, n = 36) =>
      Array.from({ length: n + 1 }, (_, i) => { const a = i / n * Math.PI * 2; return [u * pw + Math.cos(a) * r * m, v * ph + Math.sin(a) * r * m]; });
    const holes = [[.26, .34], [.74, .34], [.26, .66], [.74, .66]].map(([u, v]) => ({ pts: circ(u, v, .07), hole: true }));
    const sl = []; const sr = .035 * m, x0 = .43 * pw, x1 = .57 * pw, cy = .5 * ph;
    for (let i = 0; i <= 12; i++) { const a = -Math.PI / 2 + i / 12 * Math.PI; sl.push([x1 + Math.cos(a) * sr, cy + Math.sin(a) * sr]); }
    for (let i = 0; i <= 12; i++) { const a = Math.PI / 2 + i / 12 * Math.PI; sl.push([x0 + Math.cos(a) * sr, cy + Math.sin(a) * sr]); }
    sl.push(sl[0]);
    const r = Math.min(.06 * m, 30), L = .14 * pw, R = .86 * pw, T = .17 * ph, B = .83 * ph, out = [];
    const arc = (cx, cy, a0) => { for (let i = 0; i <= 8; i++) { const a = a0 + i / 8 * Math.PI / 2; out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]); } };
    arc(L + r, T + r, Math.PI); arc(R - r, T + r, Math.PI * 1.5); arc(R - r, B - r, 0); arc(L + r, B - r, Math.PI / 2); out.push(out[0]);
    return [...holes, { pts: sl, hole: true }, { pts: out, hole: false }];
  }

  function drawLaser(o, lp, t, id, live) {
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
    // lengths with "jump" weights between sub-paths
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

    // holes
    subs.forEach((s, si) => {
      if (s.hole && done[si]) { ctx.beginPath(); s.pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.fillStyle = C.table; ctx.fill(); }
    });
    const outerDone = done[subs.length - 1];
    if (outerDone) {
      const s = subs[subs.length - 1]; ctx.beginPath(); s.pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath();
      ctx.fillStyle = C.part; ctx.fill();
      subs.forEach((q, qi) => { if (q.hole) { ctx.beginPath(); q.pts.forEach(([x, y], i) => i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)); ctx.closePath(); ctx.fillStyle = C.table; ctx.fill(); } });
    }
    // kerf
    ctx.strokeStyle = C.kerf; ctx.lineWidth = Math.max(2, Math.min(w, h) * .012); ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    partial.forEach(list => { if (!list.length) return; ctx.beginPath(); list.forEach(([a, b], i) => { if (i === 0 || list[i - 1][1] !== a) ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0], b[1]); }); ctx.stroke(); });

    // sparks
    let arr = sparks.get(id); if (!arr) { arr = []; sparks.set(id, arr); }
    const dt = live ? 1 / 60 : 0;
    if (on && live) {
      const sc = Math.min(w, h) / 260;
      for (let i = 0; i < 3; i++) {
        const a = ang + Math.PI + (Math.random() - .5) * 1.6, sp = (80 + Math.random() * 220) * sc;
        arr.push({ x: head[0], y: head[1], vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: .25 + Math.random() * .4, max: .65 });
      }
    }
    for (let i = arr.length - 1; i >= 0; i--) {
      const p = arr[i]; p.x += p.vx * dt; p.y += p.vy * dt; p.life -= dt;
      if (p.life <= 0) { arr.splice(i, 1); continue; }
      ctx.globalAlpha = clamp(p.life / .35); ctx.fillStyle = C.spark;
      const r = Math.max(1.2, Math.min(w, h) * .006);
      ctx.fillRect(p.x - r / 2, p.y - r / 2, r, r);
    }
    ctx.globalAlpha = 1;

    // cutting head
    const hr = Math.max(8, Math.min(w, h) * .05);
    ctx.fillStyle = 'rgba(255,90,31,.25)'; ctx.beginPath(); ctx.arc(head[0], head[1], hr * 1.4, 0, 7); ctx.fill();
    ctx.strokeStyle = C.die; ctx.lineWidth = Math.max(2, hr * .3); ctx.beginPath(); ctx.arc(head[0], head[1], hr, 0, 7); ctx.stroke();
    if (lp > 0 && lp < 1) { ctx.shadowColor = C.laser; ctx.shadowBlur = hr * 1.8; }
    ctx.fillStyle = C.laser; ctx.beginPath(); ctx.arc(head[0], head[1], hr * .38, 0, 7); ctx.fill();
    ctx.shadowBlur = 0; ctx.fillStyle = C.hot; ctx.beginPath(); ctx.arc(head[0], head[1], hr * .16, 0, 7); ctx.fill();
    ctx.restore();
  }

  /* ---------- press brake scene ---------- */
  function drawBrake(o, bp) {
    const { ctx, w, h, dpr } = o;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = C.table; ctx.fillRect(0, 0, w, h);
    const cx = w / 2, y0 = h * .66, s = Math.min(h * .28, w * .2), th = Math.max(6, Math.min(h * .045, 22));
    const L = Math.min(w * .4, h * .85);
    const theta = clamp(bp) * Math.PI / 4, d = s * Math.tan(theta);
    const yc = y0 - th / 2 + d;

    // die block with V notch
    ctx.fillStyle = C.die;
    ctx.beginPath(); ctx.moveTo(cx - w * .46, h); ctx.lineTo(cx - w * .46, y0); ctx.lineTo(cx - s, y0); ctx.lineTo(cx, y0 + s); ctx.lineTo(cx + s, y0); ctx.lineTo(cx + w * .46, y0); ctx.lineTo(cx + w * .46, h); ctx.closePath(); ctx.fill();

    // sheet
    ctx.strokeStyle = C.sheet; ctx.lineWidth = th; ctx.lineJoin = 'miter'; ctx.lineCap = 'butt';
    ctx.beginPath(); ctx.moveTo(cx - Math.cos(theta) * L, yc - Math.sin(theta) * L); ctx.lineTo(cx, yc); ctx.lineTo(cx + Math.cos(theta) * L, yc - Math.sin(theta) * L); ctx.stroke();

    // punch + ram
    const tipY = yc - th / 2, ph = Math.min(h * .3, w * .3), half = ph * Math.tan(35 * Math.PI / 180);
    ctx.fillStyle = C.punch;
    ctx.beginPath(); ctx.moveTo(cx, tipY); ctx.lineTo(cx - half, tipY - ph); ctx.lineTo(cx - half * 1.25, tipY - ph); ctx.lineTo(cx - half * 1.25, -h); ctx.lineTo(cx + half * 1.25, -h); ctx.lineTo(cx + half * 1.25, tipY - ph); ctx.lineTo(cx + half, tipY - ph); ctx.closePath(); ctx.fill();
    ctx.fillStyle = C.accent; ctx.beginPath(); ctx.moveTo(cx, tipY); ctx.lineTo(cx - half * .28, tipY - ph * .28); ctx.lineTo(cx + half * .28, tipY - ph * .28); ctx.closePath(); ctx.fill();
  }

  /* ---------- scene drivers ---------- */
  // hero slot: laser cuts, then the press brake bends, on a loop
  function heroLoop(o) {
    const T = { cut: 5.2, hold: .7, bend: 2.4, rest: 1.1 }, cyc = T.cut + T.hold + T.bend + T.rest;
    if (reduce) { drawLaser(o, .7, 0, 'hero', false); return; }
    const t0 = performance.now();
    const frame = now => {
      const t = ((now - t0) / 1000) % cyc;
      if (t < T.cut + T.hold) drawLaser(o, ease(clamp(t / T.cut)) * .98 + (t >= T.cut ? .02 : 0), t, 'hero', true);
      else {
        const b = t - T.cut - T.hold, k = b < T.bend ? ease(clamp(b / (T.bend * .6))) : 1 - ease(clamp((b - T.bend) / T.rest));
        drawBrake(o, b < T.bend ? ease(clamp(b / (T.bend * .7))) : 1 - ease(clamp((b - T.bend) / T.rest)));
      }
      requestAnimationFrame(frame);
    };
    requestAnimationFrame(frame);
  }

  // showcase: scroll position runs the machines
  function stageScene(o, section) {
    const caps = [...document.querySelectorAll('[data-cap]')], chaps = [...document.querySelectorAll('[data-chap]')];
    let target = 0, cur = 0, mode = ''; const h2 = document.getElementById('mach-h');
    const read = () => {
      const r = section.getBoundingClientRect(), span = section.offsetHeight - innerHeight;
      target = clamp(-r.top / Math.max(1, span));
    };
    const setMode = m => {
      if (m === mode) return; mode = m;
      caps.forEach(c => c.hidden = c.dataset.cap !== m);
      chaps.forEach(c => c.classList.toggle('is-on', c.dataset.chap === m));
      if (h2) h2.textContent = h2.dataset['h' + m[0].toUpperCase() + m.slice(1)];
    };
    const scene = p => {
      const SPLIT = .5;
      if (p < SPLIT) { setMode('laser'); drawLaser(o, clamp(p / .44), 0, 'stage', !reduce); }
      else { setMode('brake'); drawBrake(o, ease(clamp((p - .56) / .38))); }
    };
    const frame = () => {
      if (!reduce) read();
      cur += (target - cur) * .12; if (Math.abs(target - cur) < .0004) cur = target;
      scene(cur);
      requestAnimationFrame(frame);
    };
    chaps.forEach(b => b.addEventListener('click', () => {
      const brake = b.dataset.chap === 'brake';
      if (reduce) { target = brake ? 1 : .46; return; }
      const span = section.offsetHeight - innerHeight, top = section.getBoundingClientRect().top + scrollY;
      scrollTo({ top: top + span * (brake ? .98 : .02), behavior: 'smooth' });
    }));
    if (reduce) { target = .46; }
    requestAnimationFrame(frame);
  }

  document.querySelectorAll('canvas[data-scene]').forEach(cv => {
    const o = setup(cv);
    if (cv.dataset.scene === 'hero') heroLoop(o);
    else stageScene(o, document.getElementById('machines'));
  });

  /* ---------- entrance motion ---------- */
  const targets = [
    ['.stage h2', 0], ['.chapters', 90], ['.cap', 150],
    ['.about-facts', 0], ['.about .lead', 80], ['.about .body', 160],
    ['.work-head', 0], ['.row-text', 0], ['.art', 90], ['.work-more', 0],
    ['.statement', 0], ['.contact-line', 0], ['.contact-links', 120],
    ['.foot-top', 0], ['.foot-phone', 100], ['.foot-meta', 200], ['.hero-action', 700], ['.hero-sub', 820]
  ];
  const els = [];
  targets.forEach(([sel, d]) => document.querySelectorAll(sel).forEach(el => { el.classList.add('r'); el.style.setProperty('--d', d + 'ms'); els.push(el); }));
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { threshold: .12 });
    els.forEach(el => io.observe(el));
    setTimeout(() => els.filter(el => el.getBoundingClientRect().top < innerHeight).forEach(el => el.classList.add('in')), 50);
  } else els.forEach(el => el.classList.add('in'));
})();
