<script>
  import { onMount } from 'svelte';
  import { gsap, reduced } from '$lib/motion.js';

  const ridge = [[0, 0.8], [0.06, 0.78], [0.12, 0.79], [0.18, 0.74], [0.23, 0.66], [0.27, 0.62], [0.31, 0.66], [0.35, 0.7], [0.4, 0.69], [0.45, 0.64], [0.5, 0.56], [0.545, 0.5], [0.57, 0.485], [0.8, 0.485], [0.83, 0.5], [0.86, 0.55], [0.9, 0.62], [0.95, 0.68], [1, 0.7]];
  const W = 1440, H = 800;
  function path(off = 0, scaleY = 1, wob = 0) {
    const pts = [];
    for (let x = 0; x <= W; x += 12) {
      const n = x / W;
      let k = 1;
      while (k < ridge.length - 1 && n > ridge[k][0]) k++;
      const [x0, y0] = ridge[k - 1], [x1, y1] = ridge[k];
      const t = (n - x0) / (x1 - x0), e = t * t * (3 - 2 * t);
      const y = (y0 + (y1 - y0) * e) * H * scaleY + off + Math.sin(x * 0.011) * wob;
      pts.push(`${x},${y.toFixed(1)}`);
    }
    return `M0 ${H}L` + pts.join('L') + `L${W} ${H}Z`;
  }
  const mtn = path(0, 1);
  const far = path(-40, 0.93, 6);
  const near = `M0 ${H}V690C240 664 420 704 640 684C860 662 1060 700 1240 676C1340 664 1400 672 1440 668V${H}Z`;
  const stars = Array.from({ length: 46 }, (_, i) => [(i * 193) % W, (i * 71) % 330 + 20, i % 3 === 0 ? 2 : 1.3]);
  const lights = Array.from({ length: 30 }, (_, i) => [60 + i * 46 + ((i * 17) % 20), 730 + ((i * 13) % 40)]);

  const msgs = [
    [0.04, '6:10 am', 'Booked: blow-dry, Saturday 09:00. I will remind you on Friday.'],
    [0.38, '12:40 pm', 'Blocked drain quote: Thursday 14:00 is free. Shall I book it?'],
    [0.7, '9:05 pm', 'Thursday 11:30 is yours. Confirmed, with a reminder on Wednesday.']
  ];

  let sec, topStop, botStop, sun, moon, starsEl, lightsEl, layerFar, layerNear, clock, farEl, midEl, nearEl;
  const els = [];
  let msgEls = [];

  function render(v) {
    const L = (a) => gsap.utils.interpolate(a, v);
    topStop.setAttribute('stop-color', L(['#2b2f63', '#3f8fc8', '#2a2850', '#04070f']));
    botStop.setAttribute('stop-color', L(['#e9a27a', '#a8d6ee', '#df7a52', '#142040']));
    farEl.setAttribute('fill', L(['#0f4a3d', '#14614f', '#0c3b34', '#071a17']));
    midEl.setAttribute('fill', L(['#0a3b30', '#0e5444', '#082d27', '#04120f']));
    nearEl.setAttribute('fill', L(['#052a21', '#073b30', '#041f1a', '#020b09']));
    const sp = Math.min(1, v / 0.76);
    const sx = 150 + sp * 1140, sy = 560 - Math.sin(Math.PI * sp) * 470;
    sun.setAttribute('cx', sx); sun.setAttribute('cy', sy);
    sun.setAttribute('fill', L(['#f8dcae', '#fff6d6', '#ffb27a', '#ffb27a']));
    sun.style.opacity = v > 0.8 ? 0 : 1;
    const night = Math.max(0, (v - 0.68) / 0.3);
    moon.style.opacity = night;
    moon.setAttribute('transform', `translate(${1120 - night * 160} ${210 + (1 - night) * 120})`);
    starsEl.style.opacity = night;
    lightsEl.style.opacity = Math.max(0, (v - 0.55) / 0.4);
    layerFar.style.transform = `translate3d(${(-v * 30).toFixed(1)}px,0,0)`;
    layerNear.style.transform = `translate3d(${(v * 50).toFixed(1)}px,0,0)`;
    const mins = Math.round(6 * 60 + 10 + v * (22 * 60 - 6 * 60 - 10));
    clock.textContent = String(Math.floor(mins / 60)).padStart(2, '0') + ':' + String(mins % 60).padStart(2, '0');
    msgEls.forEach((el, i) => { const at = msgs[i][0]; el.classList.toggle('on', v >= at && v < at + 0.26); });
  }

  onMount(() => {
    msgEls = [...sec.querySelectorAll('.msg')];
    if (reduced()) { render(0.74); msgEls.forEach((m) => m.classList.add('on')); return; }
    render(0);
    const proxy = { v: 0 };
    const ctx = gsap.context(() => {
      gsap.to(proxy, {
        v: 1, ease: 'none', onUpdate: () => render(proxy.v),
        scrollTrigger: { trigger: sec, start: 'top top', end: '+=2800', pin: true, scrub: 0.6, anticipatePin: 1 }
      });
    }, sec);
    return () => ctx.revert();
  });
</script>

<section class="day" bind:this={sec} aria-label="Lexi over a day in Cape Town">
  <svg viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs>
      <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" bind:this={topStop} stop-color="#2b2f63" />
        <stop offset="1" bind:this={botStop} stop-color="#e9a27a" />
      </linearGradient>
    </defs>
    <rect width={W} height={H} fill="url(#sky)" />
    <g bind:this={starsEl} style="opacity:0">
      {#each stars as [x, y, r]}<circle cx={x} cy={y} {r} fill="#f2f4f1" opacity="0.85" />{/each}
    </g>
    <circle bind:this={sun} r="46" cx="150" cy="560" fill="#f8dcae" />
    <g bind:this={moon} style="opacity:0"><circle r="34" fill="#eef0e8" /><circle r="30" cx="12" cy="-6" fill="#0a1226" opacity="0.28" /></g>
    <g bind:this={layerFar}><path bind:this={farEl} d={far} fill="#0f4a3d" /></g>
    <path bind:this={midEl} d={mtn} fill="#0a3b30" />
    <g bind:this={layerNear}><path bind:this={nearEl} d={near} fill="#052a21" /></g>
    <g bind:this={lightsEl} style="opacity:0">
      {#each lights as [x, y]}<circle cx={x} cy={y} r="2" fill="#ffd98a" />{/each}
    </g>
  </svg>

  <div class="over">
    <div class="top">
      <div>
        <h1 class="h1">She works the hours <em>you</em> can't.</h1>
        <p class="lead">Early mornings, lunch rush, late nights. Customers message when it suits them, and Lexi answers every time, books the slot and sends the reminder.</p>
      </div>
      <p class="clock" bind:this={clock} aria-hidden="true">06:10</p>
    </div>
    <div class="msgs">
      {#each msgs as [, time, text]}
        <p class="msg"><b>{time}</b>{text}</p>
      {/each}
    </div>
  </div>
</section>

<style>
  .day { position: relative; height: 100svh; overflow: hidden; color: #f5f7f4; background: #0a1226; }
  svg { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
  .over { position: absolute; inset: 0; padding: 110px var(--margin) 48px; display: flex; flex-direction: column; justify-content: space-between; max-width: 1360px; margin-inline: auto; }
  .top { display: flex; justify-content: space-between; gap: 32px; align-items: flex-start; }
  .top .h1 { max-width: 15ch; text-shadow: 0 2px 30px rgba(0, 0, 0, 0.35); }
  .top .lead { margin-top: 16px; color: rgba(245, 247, 244, 0.85); max-width: 40ch; text-shadow: 0 1px 14px rgba(0, 0, 0, 0.4); }
  .clock { font: 500 clamp(2.4rem, 1.4rem + 3.4vw, 4.6rem) / 1 var(--font-sans); letter-spacing: -0.05em; font-variant-numeric: tabular-nums; text-shadow: 0 2px 24px rgba(0, 0, 0, 0.4); }
  .msgs { position: relative; height: 120px; }
  .msg { position: absolute; left: 0; bottom: 0; margin: 0; max-width: min(440px, 100%); background: #fff; color: #111; padding: 12px 16px; border-radius: 16px; border-bottom-left-radius: 3px; font-size: 0.95rem; line-height: 1.4; opacity: 0; transform: translateY(14px); transition: opacity 0.5s, transform 0.5s var(--ease); }
  :global(.msg.on) { opacity: 1; transform: none; }
  .msg b { display: block; font: 600 0.78rem var(--font-sans); color: #075e54; margin-bottom: 2px; }
  @media (max-width: 720px) {
    .over { padding-top: 124px; padding-bottom: 28px; }
    .top { flex-direction: column; gap: 14px; }
    .clock { order: -1; font-size: 2.4rem; }
    .top .lead { display: none; }
  }
  @media (prefers-reduced-motion: reduce) {
    .day { height: auto; min-height: 100svh; }
    .msgs { height: auto; display: grid; gap: 10px; }
    .msg { position: static; opacity: 1; transform: none; }
  }
</style>
