<script>
  import { onMount } from 'svelte';
  import { setupReveals, gsap, reduced } from '$lib/motion.js';
  import { theo, places, faq, wa } from '$lib/content.js';
  import FourDays from '$lib/FourDays.svelte';
  import SkylineLine from '$lib/SkylineLine.svelte';

  let { delay = 0 } = $props();
  let root, story, clock = $state('');
  let open = $state(-1);

  onMount(() => {
    const off = setupReveals(root, { delay });
    const tick = () => { clock = new Date().toLocaleTimeString('en-ZA', { hour: '2-digit', minute: '2-digit', timeZone: 'Africa/Johannesburg' }); };
    tick();
    const iv = setInterval(tick, 20000);
    /* scroll-fill paragraph: words go from muted to full ink */
    let ctx;
    if (!reduced() && story) {
      ctx = gsap.context(() => {
        const text = story.textContent.trim();
        story.setAttribute('aria-label', text);
        story.textContent = '';
        const spans = text.split(/\s+/).map((w) => {
          const s = document.createElement('span');
          s.textContent = w;
          s.setAttribute('aria-hidden', 'true');
          s.className = 'fw';
          story.appendChild(s);
          story.appendChild(document.createTextNode(' '));
          return s;
        });
        gsap.fromTo(spans, { opacity: 0.18 }, { opacity: 1, ease: 'none', stagger: 0.12,
          scrollTrigger: { trigger: story, start: 'top 82%', end: 'bottom 42%', scrub: 0.5 } });
      }, root);
    }
    return () => { off(); clearInterval(iv); ctx?.revert(); };
  });
</script>

<div bind:this={root}>
  <section class="sec intro">
    <div class="wrap">
      <p class="live" data-reveal><i></i> Cape Town, {clock}</p>
      <h1 class="h1" data-words>Built by a <em>local</em>, not a call centre.</h1>
      <div class="storywrap">
        <div class="mono" data-reveal aria-hidden="true"><span>T</span></div>
        <p class="story" bind:this={story}>{theo[0]} {theo[1]}</p>
      </div>
    </div>
  </section>

  <FourDays />

  <section class="sec places">
    <div class="bgline" aria-hidden="true"><SkylineLine draw={false} opacity={0.16} /></div>
    <div class="wrap">
      <h2 class="h2" data-words>Where we <em>work</em>.</h2>
      <ul class="list">
        {#each places as pl}<li data-reveal><span>{pl}</span></li>{/each}
      </ul>
      <p class="note" data-reveal>I come to you for the setup, wherever in the city you are.</p>
    </div>
  </section>

  <section class="sec faq" id="questions">
    <div class="wrap fgrid">
      <h2 class="h2" data-words>Questions.</h2>
      <div class="items">
        {#each faq as [q, a], i}
          <div class="item" class:open={open === i} data-reveal>
            <button type="button" aria-expanded={open === i} aria-controls={'a' + i} onclick={() => (open = open === i ? -1 : i)}>
              <span>{q}</span><i aria-hidden="true"></i>
            </button>
            <div class="panel" id={'a' + i} role="region"><div class="inner"><p>{a} {#if q.startsWith('What happens')}<a class="ulink" href="/privacy">Read the privacy policy.</a>{/if}</p></div></div>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <section class="sec close">
    <div class="wrap">
      <h2 class="h2" data-words>Got a question I haven't <em>answered</em>?</h2>
      <a class="btn big" data-reveal href={wa("Hi Theo, I have a question about Lexi")}>Ask Theo on WhatsApp</a>
    </div>
    <div class="skyline"><SkylineLine /></div>
  </section>
</div>

<style>
  .intro { padding-top: clamp(130px, 14vw, 180px); }
  .live { display: inline-flex; align-items: center; gap: 8px; font-size: 0.8rem; color: var(--muted); border: 1px solid var(--line); padding: 6px 14px; border-radius: 999px; margin-bottom: 22px; font-variant-numeric: tabular-nums; }
  .live i { width: 7px; height: 7px; border-radius: 50%; background: #0b5d4a; animation: ping 2s infinite; }
  @keyframes ping { 0% { box-shadow: 0 0 0 0 rgba(11, 93, 74, 0.5); } 100% { box-shadow: 0 0 0 9px rgba(11, 93, 74, 0); } }
  .intro .h1 { max-width: 15ch; }
  .storywrap { margin-top: clamp(48px, 8vw, 110px); display: grid; grid-template-columns: 140px minmax(0, 1fr); gap: clamp(20px, 4vw, 56px); align-items: start; }
  .mono { width: 120px; height: 120px; border-radius: 50%; background: #0b5d4a; color: #f1efe8; display: grid; place-items: center; font: italic 500 4rem var(--font-display); }
  .story { font: 500 clamp(1.3rem, 1rem + 1.6vw, 2.2rem) / 1.3 var(--font-sans); letter-spacing: -0.03em; max-width: 34em; }
  .story :global(.fw) { display: inline-block; }
  .list { list-style: none; margin: clamp(28px, 4vw, 48px) 0 0; padding: 0; }
  .list li { border-top: 1px solid var(--line); }
  .list li:last-child { border-bottom: 1px solid var(--line); }
  .list span { display: block; padding: 18px 0; font: 500 clamp(1.8rem, 1rem + 3.4vw, 3.6rem) / 1.1 var(--font-sans); letter-spacing: -0.045em; transition: transform 0.4s var(--ease), color 0.3s; cursor: default; }
  .list:hover span { color: var(--muted); opacity: 0.55; }
  .list li:hover span { color: var(--accent); opacity: 1; transform: translateX(18px); }
  .note { margin-top: 22px; color: var(--muted); }
  .fgrid { display: grid; grid-template-columns: minmax(0, 4fr) minmax(0, 8fr); gap: clamp(24px, 5vw, 80px); align-items: start; }
  .fgrid .h2 { position: sticky; top: 110px; }
  .item { border-top: 1px solid var(--line); }
  .item:last-child { border-bottom: 1px solid var(--line); }
  .item button { width: 100%; background: none; border: 0; color: inherit; text-align: left; cursor: pointer; padding: 22px 0; display: flex; justify-content: space-between; align-items: center; gap: 20px; font: 500 clamp(1rem, 0.95rem + 0.4vw, 1.2rem) / 1.3 var(--font-sans); letter-spacing: -0.015em; min-height: 64px; }
  .item i { width: 14px; height: 14px; position: relative; flex: none; }
  .item i::before, .item i::after { content: ''; position: absolute; background: var(--accent); inset: 6px 0 auto 0; height: 2px; transition: transform 0.35s var(--ease); }
  .item i::after { transform: rotate(90deg); }
  .item.open i::after { transform: rotate(0); }
  .panel { display: grid; grid-template-rows: 0fr; transition: grid-template-rows 0.45s var(--ease); }
  .item.open .panel { grid-template-rows: 1fr; }
  .inner { overflow: hidden; }
  .inner p { padding: 0 0 24px; color: var(--muted); max-width: 56ch; }
  .places { position: relative; overflow: hidden; }
  .places .wrap { position: relative; z-index: 1; }
  .bgline { position: absolute; inset: auto 0 0 0; pointer-events: none; }
  .close { padding-bottom: 0; overflow: hidden; }
  .close .wrap { padding-bottom: clamp(40px, 6vw, 80px); }
  .skyline { margin: 0 calc(var(--margin) * -1); }
  .close .h2 { max-width: 16ch; margin-bottom: 28px; }
  .btn.big { min-height: 56px; padding: 0 30px; background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .btn.big:hover { background: var(--accent); border-color: var(--accent); color: var(--on-accent); }
  @media (max-width: 900px) {
    .storywrap, .fgrid { grid-template-columns: minmax(0, 1fr); }
    .mono { width: 72px; height: 72px; font-size: 2.4rem; }
    .fgrid .h2 { position: static; }
  }
  @media (prefers-reduced-motion: reduce) { .live i { animation: none; } }
</style>
