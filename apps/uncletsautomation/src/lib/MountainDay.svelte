<script>
  import { onMount } from 'svelte';
  import { gsap, reduced } from '$lib/motion.js';
  import { dayPhotos } from '$lib/content.js';
  const hasPhotos = dayPhotos.length > 0;

  import { ridgeY, buildings, stadium, cranes, base, lift } from '$lib/skyline.js';
  const W = 1440, H = 800;
  const Y = (y) => lift(y, 0.26) * H;
  function path(off = 0, scaleY = 1, wob = 0) {
    const pts = [];
    for (let x = 0; x <= W; x += 12) {
      const y = (Y(ridgeY(x / W)) - H * 0.8) * scaleY + H * 0.8 + off + Math.sin(x * 0.011) * wob;
      pts.push(`${x},${y.toFixed(1)}`);
    }
    return `M0 ${H}L` + pts.join('L') + `L${W} ${H}Z`;
  }
  const baseY = Y(base);
  const mtn = path(0, 1);
  const far = path(-34, 0.9, 5);
  const sea = `M0 ${baseY}H${W}V${H}H0Z`;
  const bld = buildings.map(([x, w, h]) => ({ x: x * W, w: w * W, y: Y(base - h), h: baseY - Y(base - h) }));
  const wins = [];
  bld.forEach((b, bi) => {
    for (let wx = b.x + 4; wx < b.x + b.w - 5; wx += 8)
      for (let wy = b.y + 6; wy < baseY - 6; wy += 9) if (((wx * 7 + wy * 13 + bi * 31) | 0) % 5 < 2) wins.push([wx, wy]);
  });
  const stad = { cx: (stadium.x + stadium.w / 2) * W, rx: (stadium.w * W) / 2, ry: stadium.h * H * 0.9, cy: baseY - stadium.h * H * 0.4 };
  const craneLines = cranes.map(([x, h]) => ({ x: x * W, y: Y(base - h) }));
  const stars = Array.from({ length: 46 }, (_, i) => [(i * 193) % W, (i * 71) % 300 + 18, i % 3 === 0 ? 2 : 1.3]);

  const msgs = [
    [0.04, '6:10 am', 'Booked: blow-dry, Saturday 09:00. I will remind you on Friday.'],
    [0.38, '12:40 pm', 'Blocked drain quote: Thursday 14:00 is free. Shall I book it?'],
    [0.7, '9:05 pm', 'Thursday 11:30 is yours. Confirmed, with a reminder on Wednesday.']
  ];

  let sec, svgEl, grade, topStop, botStop, sun, moon, starsEl, lightsEl, layerFar, layerNear, clock, farEl, midEl, cityEl, seaEl, stadEl;
  const els = [];
  let msgEls = [];
  let photoEls = [];

  function render(v) {
    const L = (a) => gsap.utils.interpolate(a, v);
    const topCol = L(['#2b2f63', '#3f8fc8', '#2a2850', '#04070f']);
    topStop.setAttribute('stop-color', topCol);
    sec.style.backgroundColor = topCol;
    botStop.setAttribute('stop-color', L(['#e9a27a', '#a8d6ee', '#df7a52', '#142040']));
    farEl.setAttribute('fill', L(['#0f4a3d', '#14614f', '#0c3b34', '#071a17']));
    midEl.setAttribute('fill', L(['#0a3b30', '#0e5444', '#082d27', '#04120f']));
    cityEl.setAttribute('fill', L(['#06251e', '#0a3a30', '#04201a', '#020a08']));
    seaEl.setAttribute('fill', L(['#35506f', '#3a86ad', '#37406a', '#0a1428']));
    stadEl.setAttribute('fill', L(['#cfd8d4', '#eef3f0', '#d6b3a0', '#2c3856']));
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
    layerNear.style.transform = `translate3d(${(v * 26).toFixed(1)}px,0,0)`;
    const mins = Math.round(6 * 60 + 10 + v * (22 * 60 - 6 * 60 - 10));
    clock.textContent = String(Math.floor(mins / 60)).padStart(2, '0') + ':' + String(mins % 60).padStart(2, '0');
    if (hasPhotos) {
      const n = dayPhotos.length;
      photoEls.forEach((el, i) => {
        const o = n === 1 ? 1 : Math.max(0, 1 - Math.abs(v * (n - 1) - i));
        el.style.opacity = o;
        el.style.transform = `scale(${(1.08 - v * 0.08).toFixed(3)}) translate3d(${(-v * 18).toFixed(1)}px,0,0)`;
      });
      grade.style.background = L(['rgba(255,150,90,0.22)', 'rgba(0,0,0,0)', 'rgba(255,110,60,0.30)', 'rgba(6,12,40,0.62)']);
      starsEl.style.opacity = n === 1 ? night : 0;
    }
    msgEls.forEach((el, i) => { const at = msgs[i][0]; el.classList.toggle('on', v >= at && v < at + 0.26); });
  }

  const fit = () => {
    const small = window.innerWidth < 720;
    svgEl?.setAttribute('preserveAspectRatio', small ? 'xMidYMax meet' : 'xMidYMax slice');
    svgEl?.setAttribute('viewBox', small ? '300 250 840 550' : `0 0 ${W} ${H}`);
  };

  onMount(() => {
    fit();
    window.addEventListener('resize', fit);
    msgEls = [...sec.querySelectorAll('.msg')];
    photoEls = [...sec.querySelectorAll('.photo')];
    if (reduced()) { render(0.74); msgEls.forEach((m) => m.classList.add('on')); return () => window.removeEventListener('resize', fit); }
    render(0);
    const proxy = { v: 0 };
    const ctx = gsap.context(() => {
      gsap.to(proxy, {
        v: 1, ease: 'none', onUpdate: () => render(proxy.v),
        scrollTrigger: { trigger: sec, start: 'top top', end: '+=2800', pin: true, scrub: 0.6, anticipatePin: 1 }
      });
    }, sec);
    return () => { ctx.revert(); window.removeEventListener('resize', fit); };
  });
</script>

<section class="day" bind:this={sec} aria-label="Lexi over a day in Cape Town">
  {#if hasPhotos}
    <div class="photos">
      {#each dayPhotos as p, i}
        <img class="photo" src={p.src} alt={i === 0 ? p.alt : ''} style="opacity:{i === 0 ? 1 : 0}" loading={i === 0 ? 'eager' : 'lazy'} />
      {/each}
      <div class="grade" bind:this={grade}></div>
      <div class="scrim"></div>
    </div>
  {/if}
  <svg bind:this={svgEl} class:off={hasPhotos} viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
    <defs>
      <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" bind:this={topStop} stop-color="#2b2f63" />
        <stop offset="1" bind:this={botStop} stop-color="#e9a27a" />
      </linearGradient>
    </defs>
    <rect class="sky" width={W} height={H} fill="url(#sky)" />
    <g bind:this={starsEl} style="opacity:0">
      {#each stars as [x, y, r]}<circle cx={x} cy={y} {r} fill="#f2f4f1" opacity="0.85" />{/each}
    </g>
    <circle class="scn" bind:this={sun} r="46" cx="150" cy="560" fill="#f8dcae" />
    <g class="scn" bind:this={moon} style="opacity:0"><circle r="34" fill="#eef0e8" /><circle r="30" cx="12" cy="-6" fill="#0a1226" opacity="0.28" /></g>
    <g class="scn" bind:this={layerFar}><path bind:this={farEl} d={far} fill="#0f4a3d" /></g>
    <path class="scn" bind:this={midEl} d={mtn} fill="#0a3b30" />
    <path class="scn" bind:this={seaEl} d={sea} fill="#35506f" />
    <g class="scn" bind:this={layerNear}>
      <ellipse bind:this={stadEl} cx={stad.cx} cy={stad.cy} rx={stad.rx} ry={stad.ry} fill="#cfd8d4" />
      <g bind:this={cityEl} fill="#06251e">
        {#each bld as b}<rect x={b.x} y={b.y} width={b.w} height={b.h} />{/each}
        {#each craneLines as c}<rect x={c.x} y={c.y} width="3" height={baseY - c.y} /><rect x={c.x - 22} y={c.y} width="30" height="3" />{/each}
      </g>
    </g>
    <g class="scn" bind:this={lightsEl} style="opacity:0">
      {#each wins as [x, y]}<rect {x} {y} width="3" height="4" fill="#ffd98a" />{/each}
      <ellipse cx={stad.cx} cy={stad.cy} rx={stad.rx * 0.8} ry={stad.ry * 0.5} fill="#fff3c8" opacity="0.7" />
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
  svg.off { pointer-events: none; }
  svg.off :global(.sky), svg.off :global(.scn) { display: none; }
  .photos { position: absolute; inset: 0; overflow: hidden; background: #0a1226; }
  .photo { position: absolute; inset: -2%; width: 104%; height: 104%; object-fit: cover; will-change: transform, opacity; }
  .grade { position: absolute; inset: 0; }
  .scrim { position: absolute; inset: 0; background: linear-gradient(90deg, rgba(4, 8, 12, 0.55), rgba(4, 8, 12, 0.05) 60%), linear-gradient(0deg, rgba(4, 8, 12, 0.5), transparent 35%); }
  .over { position: absolute; inset: 0; padding: 110px var(--margin) 48px; display: flex; flex-direction: column; justify-content: space-between; max-width: 1360px; margin-inline: auto; }
  .top { display: flex; justify-content: space-between; gap: 32px; align-items: flex-start; }
  .top .h1 { max-width: 15ch; text-shadow: 0 2px 30px rgba(0, 0, 0, 0.35); }
  .top .lead { margin-top: 16px; color: rgba(245, 247, 244, 0.85); max-width: 40ch; text-shadow: 0 1px 14px rgba(0, 0, 0, 0.4); }
  .clock { font: 500 clamp(2.4rem, 1.4rem + 3.4vw, 4.6rem) / 1 var(--font-sans); letter-spacing: -0.05em; font-variant-numeric: tabular-nums; text-shadow: 0 2px 24px rgba(0, 0, 0, 0.4); }
  .msgs { position: relative; height: 120px; display: flex; justify-content: flex-end; }
  .msg { position: absolute; right: 0; bottom: 0; margin: 0; max-width: min(440px, 100%); background: #fff; color: #111; padding: 12px 16px; border-radius: 16px; border-bottom-right-radius: 3px; font-size: 0.95rem; line-height: 1.4; opacity: 0; transform: translateY(14px); transition: opacity 0.5s, transform 0.5s var(--ease); }
  :global(.msg.on) { opacity: 1; transform: none; }
  .msg b { display: block; font: 600 0.78rem var(--font-sans); color: #075e54; margin-bottom: 2px; }
  @media (max-width: 720px) {
    .over { padding-top: 124px; padding-bottom: 28px; justify-content: flex-start; gap: 22px; }
    .msgs { height: 96px; justify-content: flex-start; }
    .msg { right: auto; left: 0; border-bottom-right-radius: 16px; border-bottom-left-radius: 3px; }
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
