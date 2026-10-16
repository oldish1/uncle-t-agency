import { useEffect, useRef, useState } from 'react';
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

/* ---------- helpers ---------- */
function Reveal({ children, delay = 0, y = 28, className, as = 'div', ...rest }) {
  const Tag = motion[as];
  return (
    <Tag className={className} initial={{ opacity: 0, y }} whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '0px 0px -10% 0px' }} transition={{ duration: 0.8, ease: EASE, delay }} {...rest}>
      {children}
    </Tag>
  );
}

function Words({ text, className, as = 'h2', id, delay = 0 }) {
  const Tag = motion[as];
  return (
    <Tag className={className} id={id} aria-label={text} initial="h" whileInView="s" viewport={{ once: true, margin: '0px 0px -12% 0px' }}
      transition={{ staggerChildren: 0.07, delayChildren: delay }}>
      {text.split(' ').map((w, i) => (
        <span className="mask" aria-hidden="true" key={i}>
          <motion.span className="mw" variants={{ h: { y: '112%' }, s: { y: 0 } }} transition={{ duration: 0.85, ease: EASE }}>{w}&nbsp;</motion.span>
        </span>
      ))}
    </Tag>
  );
}

function Count({ to, reduce }) {
  const [v, setV] = useState(reduce ? to : 0);
  useEffect(() => {
    if (reduce) { setV(to); return; }
    const c = animate(0, to, { duration: 1.3, ease: [0.16, 1, 0.3, 1], onUpdate: x => setV(Math.round(x)) });
    return () => c.stop();
  }, [to, reduce]);
  return <>{v}</>;
}

function MagneticButton({ href, children, className = 'btn' }) {
  const x = useMotionValue(0), y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 220, damping: 16 }), sy = useSpring(y, { stiffness: 220, damping: 16 });
  const onMove = e => {
    const r = e.currentTarget.getBoundingClientRect();
    x.set((e.clientX - (r.left + r.width / 2)) * 0.22); y.set((e.clientY - (r.top + r.height / 2)) * 0.3);
  };
  const off = () => { x.set(0); y.set(0); };
  return (
    <motion.a className={className} href={href} style={{ x: sx, y: sy }} onPointerMove={onMove} onPointerLeave={off} whileTap={{ scale: 0.96 }}>
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
    setHidden(v > last.current && v > 260);
    setSolid(v > 80);
    last.current = v;
  });
  return (
    <motion.header className={'top' + (solid ? ' is-solid' : '')} animate={{ y: hidden ? '-100%' : 0 }} transition={{ duration: 0.35, ease: EASE }}>
      <a className="wordmark" href="#top">T &amp; T Engineering</a>
      <nav aria-label="Main">
        <a href="#machines">Machines</a>
        <a href="#work">What we make</a>
        <a href="#quote">Get a quote</a>
      </nav>
      <a className="top-call" href="tel:+27216972525">{PHONE}</a>
    </motion.header>
  );
}

/* ---------- hero ---------- */
function Letters({ text, delay }) {
  return (
    <span className="w mask" aria-hidden="true">
      {[...text].map((ch, i) => (
        <motion.span className="mw" key={i} initial={{ y: '112%' }} animate={{ y: 0 }} transition={{ duration: 1, ease: EASE, delay: delay + i * 0.08 }}>{ch}</motion.span>
      ))}
    </span>
  );
}

function Hero() {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] });
  const scale = useTransform(scrollYProgress, [0, 1], [1, 1.18]);
  const textY = useTransform(scrollYProgress, [0, 1], [0, 140]);
  const fade = useTransform(scrollYProgress, [0, 0.8], [1, 0]);
  return (
    <section className="hero" ref={ref}>
      <motion.div className="hero-media" style={{ scale }} initial={{ clipPath: 'inset(0 0 100% 0)' }} animate={{ clipPath: 'inset(0 0 0% 0)' }} transition={{ duration: 1.3, ease: [0.7, 0, 0.2, 1] }}>
        <MediaFrame media={MEDIA.hero} cut />
      </motion.div>
      <div className="hero-scrim" />
      <motion.div className="hero-inner" style={{ y: textY, opacity: fade }}>
        <h1 className="sentence" aria-label="Cut and bend. Laser cutting and press brake bending.">
          <span className="line"><Letters text="Cut" delay={0.5} /></span>
          <span className="line"><Letters text="bend." delay={0.75} /></span>
        </h1>
        <div className="hero-row">
          <motion.p className="hero-sub" initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.9, ease: EASE, delay: 1.5 }}>
            Laser cutting and press brake bending, with CNC punching and full fabrication. Lansdowne, Cape Town. Since 2001.
          </motion.p>
          <motion.div className="hero-specs" initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.9, ease: EASE, delay: 1.65 }}>
            <p><b>6 kW</b><span>JFY laser</span></p>
            <p><b>150 ton</b><span>JFY press brake</span></p>
            <p><b>3 m</b><span>Bending length</span></p>
          </motion.div>
          <motion.div initial={{ opacity: 0, y: 24 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.9, ease: EASE, delay: 1.8 }}>
            <MagneticButton href="#quote">Get a quote</MagneticButton>
          </motion.div>
        </div>
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
      <motion.div className="mq-track" aria-hidden="true" animate={{ x: ['0%', '-50%'] }} transition={{ duration: 40, ease: 'linear', repeat: Infinity }}>
        <div className="mq-set">{set}</div><div className="mq-set">{set}</div>
      </motion.div>
    </div>
  );
}

/* ---------- statement ---------- */
function Statement() {
  return (
    <section className="statement-section" id="about" aria-labelledby="about-h">
      <h2 className="sr" id="about-h">About T &amp; T Engineering</h2>
      <Reveal as="p" className="statement">
        <b>Errol Jeftha</b> started this workshop in <b>2001</b>, on <b>30&nbsp;years</b> of trade. A <b>6&nbsp;kW</b> laser and a <b>150&nbsp;ton</b> press brake now turn a drawing into a finished part.
      </Reveal>
      <Reveal className="facts" delay={0.1}>
        <p>6 Windsor Road, Lansdowne,<br />Cape Town 7780</p>
        <p>Bring a drawing, a sample or a broken part. We tell you what it will cost and how long it will take.</p>
        <p><a href="tel:+27216972525">{PHONE}</a></p>
      </Reveal>
    </section>
  );
}

/* ---------- machines: full-bleed footage, scroll swaps laser to press brake ---------- */
const CHAPTERS = {
  laser: {
    h: 'Cut from the drawing.',
    p: 'Our 6 kW JFY laser follows your drawing file. Holes first, then the outline. The edge comes off clean and the part is ready to bend or weld.',
    specs: [{ n: 6, u: ' kW', l: 'Laser power' }, { t: 'JFY', l: 'Machine make' }]
  },
  brake: {
    h: 'Folded to the angle.',
    p: 'Our 150 ton JFY press brake folds the flat part to the angle on your drawing, up to 3 metres long in one stroke.',
    specs: [{ n: 150, u: ' ton', l: 'Press force' }, { n: 3, u: ' m', l: 'Bending length' }]
  }
};

function Machines() {
  const ref = useRef(null);
  const reduce = useReducedMotion();
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end end'] });
  const sp = useSpring(scrollYProgress, { stiffness: 140, damping: 32, mass: 0.3 });
  const [chap, setChap] = useState('laser');
  useMotionValueEvent(sp, 'change', v => { if (!reduce) setChap(v < 0.5 ? 'laser' : 'brake'); });
  const brakeOpacity = useTransform(sp, [0.42, 0.58], [0, 1]);
  const laserScale = useTransform(sp, [0, 0.5], [1.02, 1.14]);
  const brakeScale = useTransform(sp, [0.5, 1], [1.14, 1.02]);
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
        <motion.div className="layer" style={{ scale: reduce ? 1 : laserScale }}><MediaFrame media={MEDIA.laser} cut /></motion.div>
        <motion.div className="layer" style={{ opacity: reduce ? (chap === 'brake' ? 1 : 0) : brakeOpacity, scale: reduce ? 1 : brakeScale }}><MediaFrame media={MEDIA.brake} /></motion.div>
        <div className="stage-scrim" />
        <div className="stage-text">
          <AnimatePresence mode="wait">
            <motion.h2 id="mach-h" key={chap} initial={{ y: 40, opacity: 0 }} animate={{ y: 0, opacity: 1 }} exit={{ y: -40, opacity: 0 }} transition={{ duration: 0.4, ease: EASE }}>
              {c.h}
            </motion.h2>
          </AnimatePresence>
          <AnimatePresence mode="wait">
            <motion.div key={chap + 'b'} className="stage-body" initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }} transition={{ duration: 0.4, ease: EASE, delay: 0.08 }}>
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
              <motion.button type="button" key={k} className={'chap' + (chap === k ? ' is-on' : '')} onClick={() => go(k)} whileTap={{ scale: 0.95 }} whileHover={{ y: -2 }}>
                {k === 'laser' ? 'Laser cutting' : 'Press brake'}
              </motion.button>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}

/* ---------- process: a horizontal strip driven by vertical scroll ---------- */
const STEPS = [
  { t: 'Send it.', d: 'Email or WhatsApp a drawing, a sample or photos of the broken part.', tone: 'p-accent' },
  { t: 'Quote it.', d: 'We tell you the price and how long it will take before any metal is cut.', tone: 'p-light' },
  { t: 'Cut it.', d: 'The 6 kW laser cuts your flat parts from the drawing file.', tone: 'p-dark' },
  { t: 'Bend it.', d: 'The 150 ton press brake folds them to the angle, up to 3 metres long.', tone: 'p-light' },
  { t: 'Collect it.', d: 'Finished parts, checked against your drawing, ready at 6 Windsor Road.', tone: 'p-accent' }
];
function Process() {
  const ref = useRef(null);
  const track = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end end'] });
  const sp = useSpring(scrollYProgress, { stiffness: 120, damping: 30, mass: 0.3 });
  const [shift, setShift] = useState(1);
  useEffect(() => {
    const m = () => setShift(Math.max(1, track.current.scrollWidth - window.innerWidth));
    m(); window.addEventListener('resize', m); return () => window.removeEventListener('resize', m);
  }, []);
  const x = useTransform(sp, [0, 1], [0, -shift]);
  return (
    <section className="process" ref={ref} aria-labelledby="proc-h">
      <div className="proc-stage">
        <h2 className="sr" id="proc-h">How a job moves through the shop</h2>
        <motion.ol className="proc-track" ref={track} style={{ x }}>
          {STEPS.map(s => (
            <li className={'proc-panel ' + s.tone} key={s.t}><h3>{s.t}</h3><p>{s.d}</p></li>
          ))}
        </motion.ol>
      </div>
    </section>
  );
}

/* ---------- work: typographic rows with a sweep on hover ---------- */
const ROWS = [
  { t: 'Laser cutting', d: 'Flat parts cut from your drawing file or a sample on our 6 kW JFY laser. Brackets, plates, covers, panels and one-off shapes.', tag: '6 kW JFY laser' },
  { t: 'Press brake bending', d: 'Sheet folded to the angle on your drawing. Trays, channels, brackets and enclosures, up to 3 metres long.', tag: '150 ton JFY press brake' },
  { t: 'CNC punching', d: 'Hole patterns and shapes punched quickly and repeated exactly. A good fit when you need many of the same part.', tag: 'CNC punch' },
  { t: 'Copper pot stills', d: 'New stills built for distilleries, and repairs when a condenser, column or pot needs work.', tag: 'Distilleries' },
  { t: 'Supra meat machines', d: 'Bandsaws, mincers, mixers and sausage fillers. Spares for the full Supra range, plus repairs on other makes.', tag: 'Meat industry' },
  { t: 'Fabrication', d: 'Rolling, welding, turning, milling and general fabrication to finish the job under one roof.', tag: 'One workshop' }
];

function Work() {
  return (
    <section className="work" id="work" aria-labelledby="work-h">
      <Words as="h2" id="work-h" className="work-head" text="One workshop, many jobs." />
      <ul className="rows">
        {ROWS.map(r => (
          <motion.li className="row" key={r.t} initial="rest" whileHover="hover" whileFocus="hover" animate="rest" tabIndex={0}>
            <motion.span className="sweep" variants={{ rest: { scaleY: 0 }, hover: { scaleY: 1 } }} transition={{ duration: 0.45, ease: EASE }} />
            <Reveal as="h3" className="row-title">{r.t}</Reveal>
            <Reveal as="p" className="row-desc" delay={0.08}>{r.d}</Reveal>
          </motion.li>
        ))}
      </ul>
    </section>
  );
}

/* ---------- shop floor gallery: shows only when real photos exist ---------- */
function Gallery() {
  const [ok, setOk] = useState({});
  const [have, setHave] = useState(new Set());
  useEffect(() => { loadManifest().then(setHave); }, []);
  const any = Object.values(ok).some(Boolean);
  return (
    <section className="gallery" aria-label="Inside the workshop" hidden={!any}>
      <div className="gal-grid">
        {MEDIA.shop.filter(s => have.has(s)).map((src, i) => (
          <Reveal className={'gal-item g' + (i + 1)} key={src} delay={i * 0.08} y={40} hidden={!ok[src]}>
            <img src={src} alt="Inside the T & T Engineering workshop" loading="eager" onLoad={() => setOk(o => ({ ...o, [src]: true }))} onError={() => setOk(o => ({ ...o, [src]: false }))} />
          </Reveal>
        ))}
      </div>
    </section>
  );
}

/* ---------- quote (opens an email or WhatsApp with the details filled in) ---------- */
const NEEDS = ['Laser cutting', 'Press brake bending', 'Laser cutting and bending', 'CNC punching', 'Fabrication or welding', 'Copper still build or repair', 'Supra machine spares or repair', 'Something else'];
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
        <Words as="h2" className="quote-head" text="Send us the job." />
        <Reveal as="p" className="lead" delay={0.1}>A drawing, a sample or a broken part. Tell us what it is and we will quote the cutting, bending or repair.</Reveal>
        <Reveal className="quote-links" delay={0.2}>
          <p><a href={'mailto:' + EMAIL}>{EMAIL}</a></p>
          <p><a href="tel:+27216972497">021 697 2497</a></p>
          <p className="soft">6 Windsor Road, Lansdowne, Cape Town 7780. <a href="https://www.google.com/maps/search/?api=1&query=T+%26+T+Engineering+6+Windsor+Rd+Lansdowne+Cape+Town">Directions</a></p>
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
          <motion.a className="btn" href={mail} whileHover={{ y: -2 }} whileTap={{ scale: 0.96 }}>Send by email</motion.a>
          <motion.a className="btn btn-alt" href={wa} target="_blank" rel="noreferrer" whileHover={{ y: -2 }} whileTap={{ scale: 0.96 }}>Send on WhatsApp</motion.a>
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
        <p className="to-top"><a href="#top">Back to top</a></p>
      </div>
      <div className="foot-phone-wrap">
        <motion.a className="foot-phone" href="tel:+27216972525" aria-label={'Call ' + PHONE}
          initial={{ y: '40%', opacity: 0 }} animate={inView ? { y: 0, opacity: 1 } : {}} transition={{ duration: 1.1, ease: EASE }} whileHover={{ x: 12 }}>
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
        <Statement />
        <Machines />
        <Process />
        <Work />
        <Gallery />
        <Quote />
      </main>
      <Footer />
    </>
  );
}
