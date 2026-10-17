<script>
  import { onMount } from 'svelte';
  import { reduced } from '$lib/motion.js';

  let canvas;
  /* Table Mountain ridge, x across 0..1, y down 0..1 */
  const ridge = [[0, 0.8], [0.06, 0.78], [0.12, 0.79], [0.18, 0.74], [0.23, 0.66], [0.27, 0.62], [0.31, 0.66], [0.35, 0.7], [0.4, 0.69], [0.45, 0.64], [0.5, 0.56], [0.545, 0.5], [0.57, 0.485], [0.8, 0.485], [0.83, 0.5], [0.86, 0.55], [0.9, 0.62], [0.95, 0.68], [1, 0.7]];
  const yAt = (x) => {
    for (let i = 1; i < ridge.length; i++) {
      if (x <= ridge[i][0]) {
        const [x0, y0] = ridge[i - 1], [x1, y1] = ridge[i];
        return y0 + ((y1 - y0) * (x - x0)) / (x1 - x0);
      }
    }
    return ridge[ridge.length - 1][1];
  };

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
      for (let x = step / 2; x < w; x += step) {
        const top = yAt(x / w) * h;
        for (let y = top, k = 0; y < h; y += step, k++) {
          const depth = Math.min(1, (y - top) / (h * 0.42));
          dots.push({ ox: x, oy: y, x, y, vx: 0, vy: 0, a: 0.95 - depth * 0.85, ph: Math.random() * 6.28, edge: k === 0 });
        }
      }
      draw();
    }

    function draw() {
      ctx.clearRect(0, 0, w, h);
      const buckets = [[], [], [], []];
      for (const d of dots) buckets[Math.min(3, Math.floor(d.a * 4))].push(d);
      buckets.forEach((list, i) => {
        ctx.fillStyle = `rgba(37,211,102,${0.16 + i * 0.26})`;
        for (const d of list) ctx.fillRect(d.x - 1, d.y - 1, d.edge ? 2.6 : 2, d.edge ? 2.6 : 2);
      });
    }

    function tick() {
      t += 0.016;
      const R = 120;
      for (const d of dots) {
        const wx = d.ox + Math.sin(t * 0.9 + d.ph) * 0.8;
        const wy = d.oy + Math.cos(t * 0.7 + d.ph) * 0.8;
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
