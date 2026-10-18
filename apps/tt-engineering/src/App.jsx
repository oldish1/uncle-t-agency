import { useCallback, useEffect, useRef, useState } from 'react';
import Lenis from 'lenis';
import {
  AnimatePresence, animate, motion, useMotionValue, useMotionValueEvent, useReducedMotion,
  useScroll, useSpring, useTransform, useInView
} from 'framer-motion';
import MediaFrame from './MediaFrame.jsx';
import { MEDIA, loadManifest } from './media.js';

const EASE = [0.2, 0.7, 0.2, 1];
const PHONE = '021 697 2525';
const EMAIL = 'info@ttengineering.co.za';
const WA = '27824926634';
let lenis = null;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

/* ---------- helpers ---------- */
function Reveal({ children, delay = 0, y = 24, className, as = 'div', ...rest }) {
  const Tag = motion[as];
  return (
    <Tag className={className} initial={{ opacity: 0, y }} whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -8% 0px' }} transition={{ duration: 0.8, ease: EASE, delay }} {...rest}>
      {children}
    </Tag>
  );
}

function Count({ to, reduce }) {
  const [v, setV] = useState(reduce ? to : 0);
  useEffect(() => {
    if (reduce) { setV(to); return; }
    const c = animate(0, to, { duration: 1.2, ease: [0.16, 1, 0.3, 1], onUpdate: x => setV(Math.round(x)) });
    return () => c.stop();
  }, [to, reduce]);
  return <>{v}</>;
}

function MagneticLink({ href, children, className = 'pill', ...rest }) {
  const x = useMotionValue(0), y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 220, damping: 16 }), sy = useSpring(y, { stiffness: 220, damping: 16 });
  const onMove = e => {
    const r = e.currentTarget.getBoundingClientRect();
    x.set((e.clientX - (r.left + r.width / 2)) * 0.2); y.set((e.clientY - (r.top + r.height / 2)) * 0.28);
  };
  const off = () => { x.set(0); y.set(0); };
  return (
    <motion.a className={className} href={href} style={{ x: sx, y: sy }} onPointerMove={onMove} onPointerLeave={off} whileTap={{ scale: 0.96 }} {...rest}>
      {children}
    </motion.a>
  );
}

/* ---------- header ---------- */
function Header() {
  const { scrollY } = useScroll();
  const [hidden, setHidden] = useState(false);
  const [solid, setSolid] = useState(false);
  const last = useRef(0);
  useMotionValueEvent(scrollY, 'change', v => {
    setHidden(v > last.current && v > 300);
    setSolid(v > 60);
    last.current = v;
  });
  return (
    <motion.header className={'top' + (solid ? ' is-solid' : '')} animate={{ y: hidden ? '-100%' : 0 }} transition={{ duration: 0.35, ease: EASE }}>
      <a className="wordmark" href="#top">T &amp; T Engineering</a>
      <nav aria-label="Main">
        <a href="#machines">Machines</a>
        <a href="#work">What we make</a>
        <a href="#about">About</a>
        <a href="#quote">Quote</a>
      </nav>
      <a className="pill pill-light pill-sm" href="tel:+27216972525">{PHONE}</a>
    </motion.header>
  );
}

/* ---------- hero: the laser clip, full screen ---------- */
function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] });
  const scale = useTransform(scrollYProgress, [0, 1], [1, 1.12]);
  const textY = useTransform(scrollYProgress, [0, 1], [0, 80]);
  const fade = useTransform(scrollYProgress, [0, 0.75], [1, 0]);
  return (
    <section className="hero" ref={ref}>
      <motion.div className="hero-media" style={{ scale }} initial={{ opacity: 0, scale: 1.08 }} animate={{ opacity: 1 }} transition={{ duration: 1.4, ease: EASE }}>
        <MediaFrame media={MEDIA.laser} cut />
      </motion.div>
      <div className="hero-scrim" />
      <motion.div className="hero-inner" style={{ y: textY, opacity: fade }}>
        <motion.h1 initial={{ opacity: 0, y: 28 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, ease: EASE, delay: 0.3 }}>
          Laser cutting and press brake bending, made in Lansdowne.
        </motion.h1>
        <motion.p className="hero-sub" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, ease: EASE, delay: 0.5 }}>
          A 6 kW laser and a 150 ton press brake, with CNC punching and full fabrication under one roof. Since 2001.
        </motion.p>
        <motion.div className="hero-actions" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 1, ease: EASE, delay: 0.7 }}>
          <MagneticLink href="#quote" className="pill pill-light">Get a quote</MagneticLink>
          <a className="pill pill-ghost" href="#machines">See the machines</a>
        </motion.div>
        <motion.dl className="hero-specs" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1, delay: 1 }}>
          <div><dt>Laser</dt><dd>6 kW</dd></div>
          <div><dt>Press brake</dt><dd>150 ton</dd></div>
          <div><dt>Bending length</dt><dd>3 m</dd></div>
        </motion.dl>
      </motion.div>
    </section>
  );
}

/* ---------- marquee ---------- */
const JOBS = ['Laser cutting', 'Press brake bending', 'CNC punching', 'Welding', 'Rolling', 'Copper pot stills', 'Supra meat machines'];
function Marquee() {
  const set = JOBS.map(j => (<span className="mq-item" key={j}>{j}<i aria-hidden="true" /></span>));
  return (
    <div className="marquee" aria-hidden="true">
      <motion.div className="mq-track" animate={{ x: ['0%', '-50%'] }} transition={{ duration: 45, ease: 'linear', repeat: Infinity }}>
        <div className="mq-set">{set}</div><div className="mq-set">{set}</div>
      </motion.div>
    </div>
  );
}

/* ---------- machines: one pinned story, scroll plays the footage ---------- */
const CHAPTERS = {
  laser: {
    h: 'Cut from the drawing.',
    p: 'The 6 kW laser follows your drawing file. Holes first, then the outline. The edge comes off clean, ready to bend or weld.',
    specs: [{ n: 6, u: ' kW', l: 'Laser power' }, { t: 'JFY', l: 'Machine make' }]
  },
  brake: {
    h: 'Folded to the angle.',
    p: 'The 150 ton press brake folds the flat part to the angle on your drawing, up to 3 metres long in one stroke.',
    specs: [{ n: 150, u: ' ton', l: 'Press force' }, { n: 3, u: ' m', l: 'Bending length' }]
  }
};

function ScrubVideo({ media, progress, active, className }) {
  const ref = useRef(null);
  const [src, setSrc] = useState(null);
  const near = useInView(ref, { margin: '600px' });
  useEffect(() => { loadManifest().then(s => { if (s.has(media.src)) setSrc(media.src); }); }, [media.src]);
  useEffect(() => {
    const v = ref.current; if (!v || !src) return;
    let raf = 0, cur = 0;
    const tick = () => {
      const d = v.duration; const target = progress.get();
      if (d && isFinite(d)) { cur += (clamp(target) * (d - 0.05) - cur) * 0.22; if (Math.abs(v.currentTime - cur) > 0.03) v.currentTime = cur; }
      raf = requestAnimationFrame(tick);
    };
    if (active && near) raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [src, active, near, progress]);
  return <video ref={ref} className={className} src={src || undefined} poster={media.poster} muted playsInline preload={near ? 'auto' : 'none'} />;
}

function Machines() {
  const ref = useRef(null);
  const reduce = useReducedMotion();
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end end'] });
  const sp = useSpring(scrollYProgress, { stiffness: 140, damping: 32, mass: 0.3 });
  const [chap, setChap] = useState('laser');
  useMotionValueEvent(sp, 'change', v => { if (!reduce) setChap(v < 0.5 ? 'laser' : 'brake'); });
  const laserP = useTransform(sp, [0, 0.46], [0, 1]);
  const brakeP = useTransform(sp, [0.54, 1], [0, 1]);
  const brakeOpacity = useTransform(sp, [0.44, 0.56], [0, 1]);
  const go = key => {
    if (reduce) { setChap(key); return; }
    const el = ref.current, span = el.offsetHeight - window.innerHeight, top = el.getBoundingClientRect().top + window.scrollY;
    const y = top + span * (key === 'brake' ? 0.98 : 0.02);
    if (lenis) lenis.scrollTo(y, { duration: 1.4 }); else window.scrollTo({ top: y, behavior: 'smooth' });
  };
  const c = CHAPTERS[chap];
  return (
    <section className="machines" id="machines" ref={ref} aria-labelledby="mach-h">
      <div className="stage">
        <div className="layer"><ScrubVideo media={MEDIA.laser} progress={laserP} active className="scrub" /></div>
        <motion.div className="layer" style={{ opacity: reduce ? (chap === 'brake' ? 1 : 0) : brakeOpacity }}><ScrubVideo media={MEDIA.brake} progress={brakeP} active className="scrub" /></motion.div>
        <div className="stage-scrim" />
        <div className="stage-text">
          <AnimatePresence mode="wait">
            <motion.h2 id="mach-h" key={chap} initial={{ y: 28, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: -28, opacity: 0 }} transition={{ duration: 0.4, ease: EASE }}>
              {c.h}
            </motion.h2>
          </AnimatePresence>
          <AnimatePresence mode="wait">
            <motion.div key={chap + 'b'} className="stage-body" initial={{ opacity: 0, y: 14 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4, ease: EASE, delay: 0.06 }}>
              <p className="cap">{c.p}</p>
              <dl className="specs">
                {c.specs.map(s => (
                  <div key={s.l}><dt>{s.l}</dt><dd>{s.n ? <><Count to={s.n} reduce={reduce} />{s.u}</> : s.t}</dd></div>
                ))}
              </dl>
            </motion.div>
          </AnimatePresence>
          <div className="chapters" role="group" aria-label="Choose a machine">
            {Object.keys(CHAPTERS).map(k => (
              <motion.button type="button" key={k} className={'chip' + (chap === k ? ' is-on' : '')} onClick={() => go(k)} whileTap={{ scale: 0.95 }}>
                {k === 'laser' ? 'Laser cutting' : 'Press brake'}
              </motion.button>
            ))}
          </div>
          <p className="note">Scroll to run the machines. Footage shows the JFY machines.</p>
        </div>
      </div>
    </section>
  );
}

/* ---------- about: words fill in as you scroll ---------- */
const STORY = 'Errol Jeftha started T & T Engineering in 2001, on thirty years in the trade. We build copper pot stills for distilleries and make the Supra meat machines. A laser and a press brake now sit beside the CNC punch, so a drawing can leave here as a finished part.';
function FillWord({ w, p, a, b }) {
  const o = useTransform(p, [a, b], [0.22, 1]);
  return <motion.span style={{ opacity: o }}>{w} </motion.span>;
}
function About() {
  const ref = useRef(null);
  const reduce = useReducedMotion();
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start 0.85', 'end 0.55'] });
  const words = STORY.split(' ');
  return (
    <section className="about" id="about" ref={ref} aria-labelledby="about-h">
      <h2 className="sr" id="about-h">About T &amp; T Engineering</h2>
      <p className="story" aria-label={STORY}>
        <span aria-hidden="true">
          {words.map((w, i) => reduce ? <span key={i}>{w} </span> : <FillWord key={i} w={w} p={scrollYProgress} a={i / words.length * 0.8} b={i / words.length * 0.8 + 0.12} />)}
        </span>
      </p>
      <Reveal className="facts">
        <p><b>Since 2001</b>Lansdowne, Cape Town</p>
        <p><b>30 years</b>of trade behind every job</p>
        <p><b>Bring us</b>a drawing, a sample or a broken part</p>
      </Reveal>
    </section>
  );
}

/* ---------- capabilities: bento grid ---------- */
function Tile({ className = '', children, video, delay = 0 }) {
  return (
    <motion.article className={'tile ' + className} initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -6% 0px' }} transition={{ duration: 0.8, ease: EASE, delay }} whileHover={{ y: -4 }}>
      {video && <div className="tile-media"><MediaFrame media={video} /><div className="tile-scrim" /></div>}
      <div className="tile-body">{children}</div>
    </motion.article>
  );
}
function Work() {
  return (
    <section className="work" id="work" aria-labelledby="work-h">
      <Reveal as="h2" id="work-h" className="section-head">What we make.</Reveal>
      <div className="bento">
        <Tile className="t-laser" video={MEDIA.laser}>
          <h3>Laser cutting</h3>
          <p>Flat parts cut from your drawing file or a sample on a 6 kW JFY laser. Brackets, plates, covers, panels and one-off shapes.</p>
          <span className="tag">6 kW</span>
        </Tile>
        <Tile className="t-brake" video={MEDIA.bend} delay={0.08}>
          <h3>Press brake bending</h3>
          <p>Sheet folded to the angle on your drawing, up to 3 metres long on a 150 ton JFY press brake.</p>
          <span className="tag">150 ton, 3 m</span>
        </Tile>
        <Tile className="t-punch" delay={0.12}>
          <h3>CNC punching</h3>
          <p>Hole patterns and shapes punched quickly and repeated exactly. A good fit when you need many of the same part.</p>
        </Tile>
        <Tile className="t-still" delay={0.16}>
          <h3>Copper pot stills</h3>
          <p>New stills built for distilleries, and repairs on condensers, columns and pots.</p>
        </Tile>
        <Tile className="t-supra" delay={0.2}>
          <h3>Supra meat machines</h3>
          <p>Bandsaws, mincers, mixers and sausage fillers. Spares for the full Supra range, plus repairs on other makes.</p>
        </Tile>
        <Tile className="t-fab" delay={0.24}>
          <h3>Fabrication</h3>
          <p>Rolling, welding, turning and milling to finish the job under one roof.</p>
        </Tile>
      </div>
    </section>
  );
}

/* ---------- quote: opens an email or WhatsApp with the details filled in ---------- */
const NEEDS = ['Laser cutting', 'Press brake bending', 'Laser cutting and bending', 'CNC punching', 'Fabrication or welding', 'Copper still build or repair', 'Supra machine spares or repair', 'Something else'];
const STEPS = ['Send it', 'Quote it', 'Cut it', 'Bend it', 'Collect it'];
function Quote() {
  const [f, setF] = useState({ name: '', phone: '', need: NEEDS[2], material: '', qty: '', notes: '' });
  const set = k => e => setF({ ...f, [k]: e.target.value });
  const body = [
    'Hi T & T Engineering, I would like a quote.', '',
    `Name: ${f.name}`, `Phone: ${f.phone}`, `Job: ${f.need}`,
    `Material and thickness: ${f.material}`, `Quantity: ${f.qty}`, `Notes: ${f.notes}`, '',
    'I will send my drawing or sample photos.'
  ].join('\n');
  const mail = `mailto:${EMAIL}?subject=${encodeURIComponent('Quote request: ' + f.need)}&body=${encodeURIComponent(body)}`;
  const wa = `https://wa.me/${WA}?text=${encodeURIComponent(body)}`;
  return (
    <section className="quote" id="quote">
      <div className="quote-intro">
        <Reveal as="h2" className="section-head">Send us the job.</Reveal>
        <Reveal as="p" className="lead" delay={0.08}>A drawing, a sample or a broken part. Tell us what it is and we will quote the cutting, bending or repair.</Reveal>
        <Reveal as="ol" className="steps" delay={0.14}>{STEPS.map(s => <li key={s}>{s}</li>)}</Reveal>
        <Reveal className="quote-links" delay={0.2}>
          <p><a href={'mailto:' + EMAIL}>{EMAIL}</a></p>
          <p><a href="tel:+27216972497">021 697 2497</a></p>
          <p className="soft">6 Windsor Road, Lansdowne, Cape Town 7780. <a href="https://www.google.com/maps/search/?api=1&query=T+%26+T+Engineering+6+Windsor+Rd+Lansdowne+Cape+Town">Directions</a></p>
          <dl className="hours">
            <div><dt>Monday to Thursday</dt><dd>07:30 to 16:30</dd></div>
            <div><dt>Friday</dt><dd>07:30 to 13:30</dd></div>
          </dl>
          <p className="soft">Send your request any time. We pick it up when we open.</p>
        </Reveal>
      </div>
      <Reveal as="form" className="form" delay={0.1} onSubmit={e => e.preventDefault()} aria-label="Quote request">
        <label>Your name<input value={f.name} onChange={set('name')} autoComplete="name" /></label>
        <label>Phone<input value={f.phone} onChange={set('phone')} autoComplete="tel" inputMode="tel" /></label>
        <label className="wide">What do you need?
          <select value={f.need} onChange={set('need')}>{NEEDS.map(n => <option key={n}>{n}</option>)}</select>
        </label>
        <label>Material and thickness<input value={f.material} onChange={set('material')} placeholder="Mild steel 3 mm" /></label>
        <label>Quantity<input value={f.qty} onChange={set('qty')} placeholder="10" inputMode="numeric" /></label>
        <label className="wide">Notes<textarea rows="3" value={f.notes} onChange={set('notes')} /></label>
        <div className="wide actions">
          <motion.a className="pill pill-accent" href={mail} whileTap={{ scale: 0.96 }}>Send by email</motion.a>
          <motion.a className="pill pill-light" href={wa} target="_blank" rel="noreferrer" whileTap={{ scale: 0.96 }}>Send on WhatsApp</motion.a>
        </div>
      </Reveal>
    </section>
  );
}

/* ---------- footer ---------- */
function Footer() {
  const ref = useRef(null);
  const inView = useInView(ref, { once: true, margin: '0px 0px -20% 0px' });
  return (
    <footer className="foot" ref={ref}>
      <div className="foot-top">
        <p>6 Windsor Road, Lansdowne, Cape Town 7780</p>
        <p>Laser cutting, press brake bending, CNC punching and fabrication.</p>
        <p>Mon to Thu 07:30 to 16:30<br />Fri 07:30 to 13:30</p>
        <p className="to-top"><a href="#top">Back to top</a></p>
      </div>
      <div className="foot-phone-wrap">
        <motion.a className="foot-phone" href="tel:+27216972525" aria-label={'Call ' + PHONE}
          initial={{ y: '40%', opacity: 0 }} animate={inView ? { y: 0, opacity: 1 } : {}} transition={{ duration: 1.1, ease: EASE }} whileHover={{ x: 10 }}>
          {PHONE}
        </motion.a>
      </div>
      <div className="foot-meta">
        <p><a href={'mailto:' + EMAIL}>{EMAIL}</a> · <a href="tel:+27824926634">082 492 6634</a> · <a href="tel:+27628132945">062 813 2945</a></p>
        <p>Site by Uncle T Agency</p>
        <p>Cape Town, 2026</p>
      </div>
    </footer>
  );
}

export default function App() {
  const reduce = useReducedMotion();
  useEffect(() => {
    if (reduce) return;
    lenis = new Lenis({ lerp: 0.09, smoothWheel: true });
    let raf = 0;
    const tick = t => { lenis.raf(t); raf = requestAnimationFrame(tick); };
    raf = requestAnimationFrame(tick);
    return () => { cancelAnimationFrame(raf); lenis.destroy(); lenis = null; };
  }, [reduce]);
  return (
    <>
      <Header />
      <main id="top">
        <Hero />
        <Marquee />
        <Machines />
        <About />
        <Work />
        <Quote />
      </main>
      <Footer />
      <div className="grain" aria-hidden="true" />
    </>
  );
}
