import { useEffect, useRef } from 'react';
import { useInView } from 'framer-motion';
import { drawLaser, drawBrake } from './scenes.js';

/* Canvas that paints a machine scene. `drive()` returns { mode: 'laser' | 'brake', p, live }
   and is called every frame, but only while the canvas is on screen. */
export default function Scene({ drive, id, label, className }) {
  const ref = useRef(null);
  const inView = useInView(ref, { margin: '120px' });
  const driveRef = useRef(drive);
  driveRef.current = drive;

  useEffect(() => {
    const canvas = ref.current; if (!canvas) return;
    const o = { ctx: canvas.getContext('2d'), w: 1, h: 1, dpr: 1 };
    const fit = () => {
      const r = canvas.getBoundingClientRect();
      o.dpr = Math.min(window.devicePixelRatio || 1, 2);
      o.w = Math.max(1, r.width); o.h = Math.max(1, r.height);
      canvas.width = Math.round(o.w * o.dpr); canvas.height = Math.round(o.h * o.dpr);
      paint();
    };
    const paint = () => {
      const s = driveRef.current();
      if (s.mode === 'brake') drawBrake(o, s.p); else drawLaser(o, s.p, id, s.live);
    };
    fit();
    const ro = new ResizeObserver(fit); ro.observe(canvas);
    let raf = 0;
    const tick = () => { paint(); raf = requestAnimationFrame(tick); };
    if (inView) raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); ro.disconnect(); };
  }, [inView, id]);

  return <canvas ref={ref} className={className} role="img" aria-label={label} />;
}
