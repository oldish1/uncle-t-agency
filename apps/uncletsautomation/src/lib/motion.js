import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export const reduced = () => typeof matchMedia !== 'undefined' && matchMedia('(prefers-reduced-motion: reduce)').matches;

/* editorial reveals for one view. Returns a cleanup function. */
export function setupReveals(root, { delay = 0 } = {}) {
  if (typeof window !== 'undefined') window.__motion = true;
  if (reduced() || !root) return () => {};

  const ctx = gsap.context(() => {
    gsap.utils.toArray('[data-words]', root).forEach((el) => {
      const text = el.textContent.trim();
      const tokens = [];
      el.childNodes.forEach((n) => {
        const cls = n.nodeType === 3 ? '' : n.className || '';
        const startsPunct = n.nodeType === 3 && /^[.,!?;:]/.test(n.textContent);
        n.textContent.split(/\s+/).filter(Boolean).forEach((w, i) => {
          if (i === 0 && startsPunct && tokens.length) tokens[tokens.length - 1][0] += w;
          else tokens.push([w, cls]);
        });
      });
      el.setAttribute('aria-label', text);
      el.textContent = '';
      const inner = tokens.map(([w, cls]) => {
        const outer = document.createElement('span');
        outer.className = 'word';
        outer.setAttribute('aria-hidden', 'true');
        const s = document.createElement('span');
        s.textContent = w;
        if (cls) s.className = cls;
        outer.appendChild(s);
        el.appendChild(outer);
        el.appendChild(document.createTextNode(' '));
        return s;
      });
      gsap.set(el, { visibility: 'visible' });
      gsap.from(inner, {
        yPercent: 110, duration: 1.1, ease: 'power4.out', stagger: 0.06, delay,
        scrollTrigger: { trigger: el, start: 'top 90%', once: true }
      });
    });

    const rv = gsap.utils.toArray('[data-reveal]', root);
    gsap.set(rv, { autoAlpha: 0, y: 34 });
    ScrollTrigger.batch(rv, {
      start: 'top 90%', once: true,
      onEnter: (els) => gsap.to(els, { autoAlpha: 1, y: 0, duration: 1, ease: 'power3.out', stagger: 0.09, delay: delay * 0.6, overwrite: true })
    });

    gsap.utils.toArray('[data-parallax]', root).forEach((el) => {
      const amt = parseFloat(el.dataset.parallax) || 8;
      gsap.fromTo(el, { yPercent: -amt }, {
        yPercent: amt, ease: 'none',
        scrollTrigger: { trigger: el.parentElement, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });
  }, root);

  requestAnimationFrame(() => ScrollTrigger.refresh());
  return () => ctx.revert();
}

export { gsap, ScrollTrigger };
