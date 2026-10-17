<script>
  import { onMount } from 'svelte';
  import { setupReveals } from '$lib/motion.js';
  import { verticals, capabilities, plans, wa, WHATSAPP } from '$lib/content.js';
  import Rotator from '$lib/Rotator.svelte';
  import Chat from '$lib/Chat.svelte';

  let { delay = 0, go } = $props();
  let root;
  onMount(() => setupReveals(root, { delay }));
</script>

<div bind:this={root}>
  <section class="hero sec">
    <div class="wrap grid">
      <div class="copy">
        <h1 class="h1" data-words>Your WhatsApp books for you.</h1>
        <p class="lead" data-reveal>Lexi answers your customers day and night, puts them in your calendar and reminds them the day before. Built in Cape Town for salons, groomers, tradespeople and small shops.</p>
        <div class="actions" data-reveal>
          <a class="btn fill" href={wa("Hi Theo, I'd like to see Lexi")}>Try Lexi on WhatsApp</a>
          <button class="ulink plain" type="button" onclick={() => go('studio')}>See how it works</button>
        </div>
        <p class="where" data-reveal>Bellville, Parow, Goodwood, Mitchell's Plain and the rest of Cape Town.</p>
      </div>
      <div class="rot" data-reveal><Rotator /></div>
    </div>
  </section>

  <div class="ticker" aria-hidden="true">
    <div class="track">
      {#each [...verticals, ...verticals] as v}<span>{v}</span>{/each}
    </div>
  </div>

  <section class="sec try" id="try">
    <div class="wrap grid">
      <div class="copy">
        <h2 class="h2" data-words>Try it the way a customer would.</h2>
        <p class="lead" data-reveal>Pick a business, tap a service, a day and a time. Cancel it, change it, or switch to Afrikaans. This is the same flow Lexi runs on a real WhatsApp number.</p>
      </div>
      <div data-reveal><Chat /></div>
    </div>
  </section>

  <section class="sec caps">
    <div class="wrap">
      <h2 class="h2" data-words>What Lexi does.</h2>
      <div class="list">
        {#each capabilities as [title, text]}
          <div class="row row-rule" data-reveal>
            <h3>{title}</h3>
            <p>{text}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <section class="sec prices" id="pricing">
    <div class="wrap">
      <h2 class="h2" data-words>Prices in Rand, no contract.</h2>
      <div class="plans">
        {#each plans as p}
          <article class="plan" class:hot={p.hot} data-reveal>
            <h3>{p.name}</h3>
            <p class="who">{p.who}</p>
            <p class="incl">{p.incl}</p>
            <p class="price">{p.price}</p>
            <p class="per">{p.per}</p>
            <a class="btn" class:fill={p.hot} href={wa(p.msg)}>{p.cta}</a>
          </article>
        {/each}
      </div>
    </div>
  </section>
</div>

<style>
  .hero { min-height: 100svh; display: flex; align-items: center; padding-top: clamp(120px, 14vw, 170px); }
  .hero .wrap { width: 100%; }
  .grid { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr); gap: clamp(32px, 6vw, 96px); align-items: center; }
  .copy .lead { margin: 26px 0 32px; }
  .actions { display: flex; gap: 26px; align-items: center; flex-wrap: wrap; }
  .plain { background-color: transparent; border: 0; color: var(--ink); font: 500 0.95rem var(--font-sans); cursor: pointer; padding-inline: 0; }
  .where { margin-top: 44px; font: italic 500 1.05rem var(--font-display); color: var(--muted); }
  .rot { max-width: 460px; justify-self: end; width: 100%; }

  .ticker { overflow: hidden; border-block: 1px solid var(--line); padding: 20px 0; white-space: nowrap; }
  .track { display: inline-flex; animation: slide 45s linear infinite; }
  .track span { font: italic 500 clamp(1.5rem, 1rem + 2vw, 2.6rem) var(--font-display); padding: 0 30px; }
  .track span::after { content: '\2022'; margin-left: 60px; color: var(--accent); font-style: normal; }
  @keyframes slide { to { transform: translateX(-50%); } }

  .try .grid { align-items: start; }
  .try .copy { position: sticky; top: 120px; }
  .list { margin-top: clamp(32px, 5vw, 64px); }
  .row { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 32px; padding: clamp(24px, 3.4vw, 44px) 0; }
  .row h3 { font-size: clamp(1.35rem, 1.05rem + 1vw, 2rem); }
  .row p { color: var(--muted); max-width: 52ch; }

  .plans { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: clamp(16px, 2vw, 28px); margin-top: clamp(32px, 5vw, 64px); }
  .plan { border-top: 1px solid var(--ink); padding: 28px 0 0; display: flex; flex-direction: column; }
  .plan.hot { border-top: 4px solid var(--accent); }
  .plan h3 { font-size: clamp(1.5rem, 1.1rem + 1.2vw, 2.2rem); }
  .who { margin-top: 14px; font-size: 1.05rem; font-weight: 500; }
  .incl { margin-top: 12px; color: var(--muted); }
  .price { margin-top: auto; padding-top: 40px; font: 500 clamp(3rem, 1.5rem + 4vw, 5rem) / 1 var(--font-display); letter-spacing: -0.02em; }
  .per { margin: 8px 0 24px; color: var(--muted); }
  .plan .btn { align-self: flex-start; }

  @media (max-width: 900px) {
    .grid { grid-template-columns: minmax(0, 1fr); }
    .rot { justify-self: stretch; max-width: none; }
    .try .copy { position: static; }
    .row { grid-template-columns: minmax(0, 1fr); gap: 10px; }
    .plans { grid-template-columns: minmax(0, 1fr); gap: 44px; }
  }
</style>
