<script>
  import { onMount } from 'svelte';
  import { setupReveals, gsap, reduced } from '$lib/motion.js';
  import { verticals, plans, wa, cbdPhoto } from '$lib/content.js';
  import Chat from '$lib/Chat.svelte';
  import ParticleMountain from '$lib/ParticleMountain.svelte';
  import DayStory from '$lib/DayStory.svelte';

  let { delay = 0, go } = $props();
  let root, hero, tilt;

  onMount(() => {
    const off = setupReveals(root, { delay });
    let move;
    if (!reduced() && matchMedia('(pointer:fine)').matches) {
      const rx = gsap.quickTo(tilt, 'rotationX', { duration: 0.8, ease: 'power3.out' });
      const ry = gsap.quickTo(tilt, 'rotationY', { duration: 0.8, ease: 'power3.out' });
      gsap.set(tilt, { transformPerspective: 1100 });
      move = (e) => {
        const r = hero.getBoundingClientRect();
        ry(((e.clientX - r.left) / r.width - 0.5) * -14 - 6);
        rx(((e.clientY - r.top) / r.height - 0.5) * 8);
      };
      hero.addEventListener('pointermove', move);
      gsap.fromTo(tilt, { rotationY: -26, y: 40, opacity: 0 }, { rotationY: -6, y: 0, opacity: 1, duration: 1.6, ease: 'power3.out', delay: delay + 0.3 });
    }
    return () => { off(); if (move) hero.removeEventListener('pointermove', move); };
  });
</script>

<div bind:this={root}>
  <section class="hero" bind:this={hero}>
    <img class="bg" src={cbdPhoto.src} alt={cbdPhoto.alt} width="1920" height="1280" decoding="async" />
    <div class="glow" aria-hidden="true"></div>
    <ParticleMountain />
    <div class="in wrap">
      <div class="copy">
        <p class="pill" data-reveal><i></i> Live at a Bellville salon</p>
        <h1 class="h1" data-words>Your WhatsApp <em>books</em> for you.</h1>
        <p class="lead" data-reveal>Lexi answers your customers day and night, puts them in your calendar and reminds them the day before. Built in Cape Town for salons, groomers, tradespeople and small shops.</p>
        <div class="actions" data-reveal>
          <a class="btn solid" href={wa("Hi Theo, I'd like to see Lexi")}>Try Lexi on WhatsApp</a>
          <button class="btn" type="button" onclick={() => go('studio')}>How it works</button>
        </div>
      </div>
      <div class="stage">
        <div class="tilt" bind:this={tilt}>
          <Chat />
          <p class="chip c1" aria-hidden="true">Booked: Sat 09:00</p>
          <p class="chip c2" aria-hidden="true">Reminder sent</p>
          <p class="chip c3" aria-hidden="true">0 double-bookings</p>
        </div>
      </div>
    </div>
    <div class="fade" aria-hidden="true"></div>
  </section>

  <div class="ticker" aria-hidden="true">
    <div class="track">
      {#each [...verticals, ...verticals] as v}<span>{v}</span>{/each}
    </div>
  </div>

  <DayStory />

  <section class="sec bento">
    <div class="wrap">
      <h2 class="h2" data-words>Everything a receptionist does, <em>none</em> of the wages.</h2>
      <div class="grid">
        <article class="tile a" data-reveal>
          <h3>Replies in seconds</h3>
          <p>2 to 5 seconds per reply in the live build, at any hour.</p>
          <div class="v speed"><span class="big">2 to 5 sec</span><span class="typing"><i></i><i></i><i></i></span></div>
        </article>
        <article class="tile b" data-reveal>
          <h3>Checks your calendar live</h3>
          <p>She reads your Google Calendar before she confirms, so a taken slot is never offered.</p>
          <div class="v mini">
            {#each ['09:00', '11:30', '14:00', '15:30'] as t, i}<span class:taken={i === 1 || i === 3}>{t}</span>{/each}
          </div>
        </article>
        <article class="tile c" data-reveal>
          <h3>Reminders, the day before</h3>
          <p>A WhatsApp nudge goes out on its own.</p>
          <div class="v notes"><span>Tomorrow 09:00, blow-dry</span><span>Tomorrow 14:00, groom</span></div>
        </article>
        <article class="tile d" data-reveal>
          <h3>Cancel and reschedule</h3>
          <p>She offers a new day before she cancels.</p>
          <div class="v flow"><span>Cancel</span><b>&rarr;</b><span>Another day?</span><b>&rarr;</b><span class="ok">Rebooked</span></div>
        </article>
        <article class="tile e" data-reveal>
          <h3>English and Afrikaans</h3>
          <p>Greeting tested in your language before you go live.</p>
          <div class="v lang"><span class="en">Welcome! What can I book?</span><span class="af">Welkom! Wat kan ek book?</span></div>
        </article>
        <article class="tile f" data-reveal>
          <div class="txt">
            <h3>A website that matches</h3>
            <p>One fast page with your services, suburb, a map and a WhatsApp button. Hosting and your domain are included.</p>
          </div>
          <div class="v browser" aria-hidden="true">
            <div class="bar"><i></i><i></i><i></i><span>yourbusiness.co.za</span></div>
            <div class="page"><b></b><u></u><u class="s"></u><span class="wa">WhatsApp us</span></div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <section class="sec prices" id="pricing">
    <div class="wrap">
      <h2 class="h2" data-words>Prices in Rand, <em>no</em> contract.</h2>
      <div class="plans">
        {#each plans as p}
          <article class="plan" class:hot={p.hot} data-reveal>
            {#if p.hot}<span class="badge">Most popular</span>{/if}
            <h3>{p.name}</h3>
            <p class="who">{p.who}</p>
            <ul class="ticks">{#each p.ticks as t}<li>{t}</li>{/each}</ul>
            <p class="price">{p.price}</p>
            <p class="per">{p.per}</p>
            <a class="btn" class:solid={p.hot} href={wa(p.msg)}>{p.cta}</a>
          </article>
        {/each}
      </div>
    </div>
  </section>
</div>

<style>
  .hero { position: relative; min-height: 100svh; display: flex; align-items: center; padding: 110px var(--margin) 60px; overflow: hidden; isolation: isolate; }
  .bg { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; object-position: 50% 42%; z-index: -2; filter: saturate(0.6) brightness(0.7) contrast(1.05); }
  .glow { position: absolute; inset: 0; z-index: -1; background: linear-gradient(90deg, rgba(6, 9, 8, 0.88) 0%, rgba(6, 9, 8, 0.5) 55%, rgba(6, 9, 8, 0.28) 100%), radial-gradient(700px 520px at 78% 42%, rgba(37, 211, 102, 0.16), transparent 70%), radial-gradient(600px 420px at 8% 8%, rgba(11, 93, 74, 0.3), transparent 70%); animation: drift 14s ease-in-out infinite alternate; }
  @keyframes drift { to { transform: translate3d(-2%, 2%, 0) scale(1.05); } }
  .fade { position: absolute; inset: auto 0 0 0; height: 160px; background: linear-gradient(0deg, var(--bg), transparent); pointer-events: none; }
  .in { width: 100%; display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr); gap: clamp(24px, 5vw, 80px); align-items: center; position: relative; }
  .pill { display: inline-flex; align-items: center; gap: 8px; border: 1px solid var(--line); padding: 6px 14px; border-radius: 999px; font-size: 0.8rem; color: var(--muted); margin-bottom: 22px; background: rgba(255, 255, 255, 0.03); }
  .pill i { width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 4px rgba(37, 211, 102, 0.2); animation: ping 2s infinite; }
  @keyframes ping { 50% { box-shadow: 0 0 0 8px rgba(37, 211, 102, 0); } }
  .copy .lead { margin: 20px 0 28px; max-width: 40ch; }
  .actions { display: flex; gap: 12px; flex-wrap: wrap; }
  .btn.solid { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .btn.solid:hover { background: var(--green); border-color: var(--green); color: #04120a; }
  .stage { justify-self: center; width: 100%; max-width: 420px; }
  .tilt { position: relative; will-change: transform; transform-style: preserve-3d; }
  .chip { position: absolute; margin: 0; white-space: nowrap; background: rgba(13, 19, 16, 0.92); border: 1px solid var(--line); padding: 8px 14px; border-radius: 999px; font-size: 0.8rem; color: var(--ink); backdrop-filter: blur(8px); animation: bob 5s ease-in-out infinite; transform: translateZ(60px); }
  .chip::before { content: ''; display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: var(--green); margin-right: 8px; }
  .c1 { right: calc(100% - 26px); top: 16%; }
  .c2 { left: calc(100% - 26px); top: 50%; animation-delay: -1.7s; }
  .c3 { right: calc(100% - 26px); bottom: 16%; animation-delay: -3.2s; }
  @keyframes bob { 50% { translate: 0 -10px; } }

  .ticker { overflow: hidden; border-block: 1px solid var(--line); padding: 16px 0; white-space: nowrap; mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); }
  .track { display: inline-flex; animation: slide 50s linear infinite; }
  .track span { font-size: 0.95rem; color: var(--muted); padding: 0 26px; }
  .track span::after { content: ''; display: inline-block; width: 4px; height: 4px; border-radius: 50%; background: var(--green); margin-left: 52px; vertical-align: middle; }
  @keyframes slide { to { transform: translateX(-50%); } }

  .bento .h2 { max-width: 20ch; }
  .grid { margin-top: clamp(28px, 4vw, 48px); display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: 14px; }
  .tile { background: var(--panel); border: 1px solid var(--line); border-radius: 22px; padding: 26px; display: flex; flex-direction: column; gap: 8px; min-height: 250px; overflow: hidden; position: relative; transition: border-color 0.3s, transform 0.4s var(--ease); }
  .tile:hover { border-color: rgba(37, 211, 102, 0.45); transform: translateY(-4px); }
  .tile h3 { font-size: 1.1rem; letter-spacing: -0.02em; }
  .tile p { color: var(--muted); font-size: 0.9rem; max-width: 38ch; }
  .a { grid-column: span 7; } .b { grid-column: span 5; }
  .c, .d, .e { grid-column: span 4; } .f { grid-column: span 12; flex-direction: row; align-items: center; justify-content: space-between; gap: 32px; }
  .v { margin-top: auto; padding-top: 18px; }
  .speed { display: flex; align-items: flex-end; justify-content: space-between; }
  .big { font: 500 clamp(2.6rem, 1.4rem + 4vw, 5rem) / 1 var(--font-sans); letter-spacing: -0.05em; color: var(--green); }
  .typing { display: flex; gap: 5px; margin-bottom: 10px; }
  .typing i { width: 9px; height: 9px; border-radius: 50%; background: var(--muted); animation: blink 1.2s infinite; }
  .typing i:nth-child(2) { animation-delay: 0.2s; } .typing i:nth-child(3) { animation-delay: 0.4s; }
  @keyframes blink { 50% { opacity: 0.2; } }
  .mini { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; }
  .mini span { text-align: center; padding: 10px 0; border-radius: 10px; background: var(--panel2); font-size: 0.8rem; color: var(--muted); }
  .mini span.taken { background: transparent; border: 1px dashed var(--line); text-decoration: line-through; opacity: 0.55; }
  .mini span:not(.taken) { animation: glowpick 4s infinite; }
  .mini span:nth-child(3) { animation-delay: 1.6s; }
  @keyframes glowpick { 0%, 100% { background: var(--panel2); color: var(--muted); } 40%, 60% { background: var(--green); color: #04120a; } }
  .notes { display: grid; gap: 8px; }
  .notes span { background: var(--panel2); border-radius: 12px; padding: 10px 14px; font-size: 0.82rem; animation: slidein 5s infinite; }
  .notes span:nth-child(2) { animation-delay: 1s; opacity: 0.8; margin-left: 14px; }
  @keyframes slidein { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(8px); } }
  .flow { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; font-size: 0.8rem; }
  .flow span { background: var(--panel2); padding: 8px 12px; border-radius: 999px; }
  .flow b { color: var(--muted); font-weight: 400; }
  .flow .ok { background: var(--green); color: #04120a; font-weight: 600; }
  .lang { display: grid; gap: 8px; font-size: 0.85rem; }
  .lang span { padding: 10px 14px; border-radius: 14px; width: fit-content; }
  .lang .en { background: #fff; color: #111; border-top-left-radius: 3px; }
  .lang .af { background: #cdeed2; color: #0a2a1a; border-top-right-radius: 3px; justify-self: end; }
  .f .txt { max-width: 42ch; }
  .browser { width: min(420px, 100%); margin: 0; padding: 0; background: var(--panel2); border-radius: 14px; overflow: hidden; border: 1px solid var(--line); flex: none; }
  .browser .bar { display: flex; gap: 6px; align-items: center; padding: 10px 12px; border-bottom: 1px solid var(--line); }
  .browser .bar i { width: 8px; height: 8px; border-radius: 50%; background: var(--line); }
  .browser .bar span { margin-left: 8px; font-size: 0.72rem; color: var(--muted); }
  .browser .page { padding: 18px; display: grid; gap: 8px; }
  .browser b { display: block; height: 14px; width: 60%; background: var(--ink); border-radius: 4px; opacity: 0.85; }
  .browser u { display: block; height: 8px; width: 90%; background: var(--line); border-radius: 4px; }
  .browser u.s { width: 55%; }
  .browser .wa { justify-self: start; background: var(--green); color: #04120a; font-size: 0.78rem; font-weight: 600; padding: 7px 14px; border-radius: 999px; margin-top: 6px; animation: nudge 3s infinite; }
  @keyframes nudge { 50% { transform: translateY(-3px); } }

  .plans { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin-top: clamp(28px, 4vw, 48px); }
  .plan { background: var(--panel); border: 1px solid var(--line); border-radius: 22px; padding: 28px; display: flex; flex-direction: column; transition: transform 0.4s var(--ease), border-color 0.3s; }
  .plan:hover { transform: translateY(-4px); }
  .plan.hot { border-color: transparent; background: linear-gradient(var(--panel), var(--panel)) padding-box, linear-gradient(140deg, #25d366, rgba(37, 211, 102, 0.1) 40%, #0b5d4a) border-box; border: 1px solid transparent; }
  .plan h3 { font-size: 1.25rem; }
  .who { margin-top: 12px; font-weight: 500; }
  .badge { align-self: flex-start; background: var(--green); color: #04120a; font: 600 0.75rem var(--font-sans); padding: 5px 12px; border-radius: 999px; margin-bottom: 14px; }
  .ticks { list-style: none; margin: 18px 0 0; padding: 0; display: grid; gap: 10px; font-size: 0.9rem; color: var(--muted); }
  .ticks li { position: relative; padding-left: 26px; }
  .ticks li::before { content: ''; position: absolute; left: 0; top: 0.3em; width: 14px; height: 14px; border-radius: 50%; background: rgba(37, 211, 102, 0.18); }
  .ticks li::after { content: ''; position: absolute; left: 4.5px; top: calc(0.3em + 3px); width: 4px; height: 7px; border: solid var(--green); border-width: 0 2px 2px 0; transform: rotate(40deg) scale(0.9); }
  .price { margin-top: auto; padding-top: 32px; font: 500 clamp(2.4rem, 1.4rem + 2.6vw, 3.6rem) / 1 var(--font-sans); letter-spacing: -0.05em; }
  .per { margin: 6px 0 22px; color: var(--muted); font-size: 0.85rem; }
  .plan .btn { align-self: flex-start; }

  @media (max-width: 1180px) { .chip { display: none; } }
  @media (max-width: 900px) {
    .in { grid-template-columns: minmax(0, 1fr); }
    .stage { max-width: 400px; }
    .chip { display: none; }
    .a, .b, .c, .d, .e, .f { grid-column: span 12; }
    .f { flex-direction: column; align-items: flex-start; }
    .plans { grid-template-columns: minmax(0, 1fr); }
    .hero { padding-top: 132px; align-items: flex-start; }
  }
  @media (prefers-reduced-motion: reduce) { .glow, .chip, .pill i, .track, .typing i { animation: none; } }
</style>
