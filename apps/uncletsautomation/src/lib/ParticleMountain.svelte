<script>
  import { onMount } from 'svelte';
  import { reduced } from '$lib/motion.js';

  let canvas;
  import { ridgeY, buildings, stadium, cranes, base, lift } from '$lib/skyline.js';

  onMount(() => {
    const ctx = canvas.getContext('2d');
    const still = reduced();
    let w = 0, h = 0, dpr = 1, dots = [], raf, t = 0;
    const mouse = { x: -9999, y: -9999 };

    function build() {
      const r = canvas.getBoundingClientRect();
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = r.width; h = r.height;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const step = w < 600 ? 12 : 11;
      dots = [];
      const baseY = lift(base) * h;
      const add = (x, y, a, kind, extra = {}) => dots.push({ ox: x, oy: y, x, y, vx: 0, vy: 0, a, ph: Math.random() * 6.28, kind, ...extra });
      /* mountains: dots from the ridge down to the water */
      for (let x = step / 2; x < w; x += step) {
        const top = lift(ridgeY(x / w)) * h;
        for (let y = top, k = 0; y < baseY; y += step, k++) {
          const depth = Math.min(1, (y - top) / (h * 0.3));
          add(x, y, 0.95 - depth * 0.8, k === 0 ? 'edge' : 'land');
        }
        /* sea: sparse rows that shimmer */
        for (let y = baseY + step, r = 0; y < h; y += step * 1.4, r++) {
          if ((Math.round(x / step) + r) % 3 === 0) add(x, y, 0.5 - Math.min(0.3, r * 0.05), 'sea');
        }
      }
      /* city: warmer, brighter, windows that flicker */
      for (const [bx, bw, bh] of buildings) {
        const x0 = bx * w, x1 = (bx + bw) * w, topY = lift(base - bh) * h;
        for (let x = x0; x < x1; x += step * 0.7) {
          for (let y = topY; y < baseY; y += step * 0.7) add(x, y, 1, 'city', { lit: Math.random() > 0.55 });
        }
      }
      const sx0 = stadium.x * w, sx1 = (stadium.x + stadium.w) * w, sTop = lift(base - stadium.h) * h;
      for (let x = sx0; x < sx1; x += step * 0.8) for (let y = sTop; y < baseY; y += step * 0.8) add(x, y, 0.9, 'city', { lit: true });
      for (const [cx, ch] of cranes) {
        const x = cx * w;
        for (let y = lift(base - ch) * h; y < baseY; y += step * 0.8) add(x, y, 0.8, 'city', { lit: false });
      }
      draw();
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      const groups = { land: [[], [], [], []], city: [[], []], sea: [] };
      for (const d of dots) {
        if (d.kind === 'city') groups.city[d.lit ? 1 : 0].push(d);
        else if (d.kind === 'sea') groups.sea.push(d);
        else groups.land[Math.min(3, Math.floor(d.a * 4))].push(d);
      }
      groups.land.forEach((list, i) => {
        ctx.fillStyle = `rgba(37,211,102,${0.16 + i * 0.26})`;
        for (const d of list) ctx.fillRect(d.x - 1, d.y - 1, d.kind === 'edge' ? 2.6 : 2, d.kind === 'edge' ? 2.6 : 2);
      });
      ctx.fillStyle = 'rgba(120,200,255,0.28)';
      for (const d of groups.sea) ctx.fillRect(d.x - 1, d.y - 1, 2, 2);
      ctx.fillStyle = 'rgba(190,255,215,0.55)';
      for (const d of groups.city[0]) ctx.fillRect(d.x - 1, d.y - 1, 2, 2);
      ctx.fillStyle = `rgba(255,222,150,${0.75 + Math.sin(t * 2) * 0.12})`;
      for (const d of groups.city[1]) ctx.fillRect(d.x - 1, d.y - 1, 2.2, 2.2);
    }

    function tick() {
      t += 0.016;
      const R = 120;
      for (const d of dots) {
        const amp = d.kind === 'sea' ? 2.2 : 0.8;
        const wx = d.ox + Math.sin(t * 0.9 + d.ph) * amp;
        const wy = d.oy + Math.cos(t * 0.7 + d.ph) * (d.kind === 'sea' ? 0.6 : 0.8);
        const dx = d.x - mouse.x, dy = d.y - mouse.y, dist = Math.hypot(dx, dy);
        if (dist < R) {
          const f = (1 - dist / R) * 5.5;
          d.vx += (dx / (dist || 1)) * f;
          d.vy += (dy / (dist || 1)) * f;
        }
        d.vx += (wx - d.x) * 0.055; d.vy += (wy - d.y) * 0.055;
        d.vx *= 0.86; d.vy *= 0.86;
        d.x += d.vx; d.y += d.vy;
      }
      draw();
      raf = requestAnimationFrame(tick);
    }

    const move = (e) => {
      const r = canvas.getBoundingClientRect();
      mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    };
    const leave = () => { mouse.x = mouse.y = -9999; };
    const vis = () => { cancelAnimationFrame(raf); if (!document.hidden && !still) raf = requestAnimationFrame(tick); };

    build();
    const ro = new ResizeObserver(build);
    ro.observe(canvas);
    if (!still) {
      window.addEventListener('pointermove', move, { passive: true });
      window.addEventListener('pointerleave', leave);
      document.addEventListener('visibilitychange', vis);
      raf = requestAnimationFrame(tick);
    }
    return () => {
      cancelAnimationFrame(raf); ro.disconnect();
      window.removeEventListener('pointermove', move);
      window.removeEventListener('pointerleave', leave);
      document.removeEventListener('visibilitychange', vis);
    };
  });
</script>

<canvas bind:this={canvas} aria-hidden="true"></canvas>

<style>
  canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block; }
</style>
