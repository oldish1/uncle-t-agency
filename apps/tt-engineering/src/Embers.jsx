import { useEffect, useRef } from 'react';
import { useInView, useReducedMotion } from 'framer-motion';

/* Ambient fallback while there is no footage: embers rising through a dark workshop.
   `cut` adds a glowing cut line that sweeps across the frame. */
export default function Embers({ cut = false, density = 1 }) {
  const ref = useRef(null);
  const inView = useInView(ref, { margin: '100px' });
  const reduce = useReducedMotion();

  useEffect(() => {
    const cv = ref.current; if (!cv) return;
    const ctx = cv.getContext('2d');
    let w = 1, h = 1, dpr = 1, raf = 0, t0 = performance.now();
    const fit = () => {
      const r = cv.getBoundingClientRect(); dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = Math.max(1, r.width); h = Math.max(1, r.height); cv.width = w * dpr; cv.height = h * dpr;
    };
    fit(); const ro = new ResizeObserver(fit); ro.observe(cv);
    const N = Math.round(150 * density);
    const ps = Array.from({ length: N }, () => ({ x: Math.random(), y: Math.random(), s: 0.8 + Math.random() * 2.6, v: 0.02 + Math.random() * 0.07, d: (Math.random() - 0.5) * 0.03, a: Math.random() }));
    const draw = now => {
      const t = (now - t0) / 1000;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.fillStyle = '#0b0d0f'; ctx.fillRect(0, 0, w, h);
      const g = ctx.createRadialGradient(w * 0.7, h * 0.7, 0, w * 0.7, h * 0.7, Math.max(w, h) * 0.6);
      g.addColorStop(0, 'rgba(255,90,31,.20)'); g.addColorStop(1, 'rgba(255,90,31,0)'); ctx.fillStyle = g; ctx.fillRect(0, 0, w, h);
      if (cut) {
        const x = ((t * 0.12) % 1.3 - 0.15) * w, y = h * 0.62;
        ctx.fillStyle = 'rgba(255,90,31,.5)'; ctx.fillRect(0, y - 2, Math.max(0, x), 4);
        ctx.shadowColor = '#ff5a1f'; ctx.shadowBlur = 40; ctx.fillStyle = '#ff7a3d'; ctx.fillRect(x - 3, y - 3, 6, 6); ctx.shadowBlur = 0;
        for (let i = 0; i < 6; i++) { const a = Math.random() * Math.PI + Math.PI; ctx.fillStyle = 'rgba(255,170,100,.8)'; ctx.fillRect(x + Math.cos(a) * Math.random() * 60, y + Math.sin(a) * Math.random() * 40, 2, 2); }
      }
      ps.forEach(p => {
        p.y -= p.v * 0.016; p.x += p.d * 0.016 + Math.sin(t + p.a * 9) * 0.0004;
        if (p.y < -0.05) { p.y = 1.05; p.x = Math.random(); }
        const k = 0.5 + 0.5 * Math.sin(t * 2 + p.a * 20);
        ctx.fillStyle = `rgba(255,${110 + p.a * 80 | 0},${40 + p.a * 40 | 0},${0.25 + 0.75 * k * Math.min(1, p.s / 2)})`;
        const r = p.s * 1.7; ctx.shadowColor = 'rgba(255,90,31,.8)'; ctx.shadowBlur = r * 4; ctx.fillRect(p.x * w, p.y * h, r, r); ctx.shadowBlur = 0;
      });
    };
    const tick = now => { draw(now); raf = requestAnimationFrame(tick); };
    if (reduce || !inView) draw(performance.now() - (reduce ? 0 : 0)); else raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); ro.disconnect(); };
  }, [inView, reduce, cut, density]);

  return <canvas ref={ref} className="embers" aria-hidden="true" />;
}
