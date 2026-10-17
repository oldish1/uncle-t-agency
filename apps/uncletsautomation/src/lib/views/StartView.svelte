<script>
  import { onMount } from 'svelte';
  import { setupReveals } from '$lib/motion.js';
  import { stats, wa } from '$lib/content.js';
  import SkyRotator from '$lib/SkyRotator.svelte';

  let { delay = 0 } = $props();
  let root;
  let biz = $state('');
  onMount(() => setupReveals(root, { delay }));
  function ask(e) {
    e.preventDefault();
    const what = biz.trim() || 'a small business';
    window.open(wa(`Hi Theo, I run ${what} and I'd like to see how Lexi could take my bookings on WhatsApp.`), '_blank', 'noopener');
  }
</script>

<div bind:this={root}>
  <section class="sec top">
    <div class="wrap grid">
      <div class="copy">
        <h1 class="h1" data-words>She works the hours you can't.</h1>
        <p class="lead" data-reveal>Early mornings, lunch rush, late nights. Customers message when it suits them, and Lexi answers every time, books the slot and sends the reminder.</p>
        <dl class="stats">
          {#each stats as [n, t]}
            <div class="row-rule" data-reveal><dt>{n}</dt><dd>{t}</dd></div>
          {/each}
        </dl>
      </div>
      <div class="sky" data-reveal><SkyRotator /></div>
    </div>
  </section>

  <section class="sec first">
    <div class="wrap narrowish">
      <h2 class="h2" data-words>First client: a Bellville salon.</h2>
      <p class="lead" data-reveal>Lexi runs the bookings at Chales Hair Boutique today, with cancellations, reschedules, reminders and a prepaid wash-and-blowdry membership. It's a real salon with a real diary, so you can see it working before you pay anything.</p>
      <a class="btn" data-reveal href="https://chaleshairboutique.co.za" rel="noopener">See the Chales website</a>
    </div>
  </section>

  <section class="sec contact" id="contact">
    <div class="wrap narrow">
      <h2 class="h2" data-words>Tell us what you do.</h2>
      <p class="lead" data-reveal>We'll show you Lexi on your kind of business.</p>
      <form class="ask" onsubmit={ask} data-reveal>
        <label class="sr" for="biz">Your business</label>
        <input id="biz" type="text" placeholder="e.g. hair salon in Parow" autocomplete="organization" bind:value={biz} />
        <button type="submit" aria-label="Send on WhatsApp">&rarr;</button>
      </form>
      <p class="next">This opens WhatsApp with your message ready. Theo replies himself.</p>
      <dl class="details">
        <div class="row-rule"><dt>WhatsApp</dt><dd><a class="ulink" href="https://wa.me/27764924196">076 492 4196</a></dd></div>
        <div class="row-rule"><dt>Email</dt><dd><span class="todo">[add email on the domain]</span></dd></div>
        <div class="row-rule"><dt>Address</dt><dd><span class="todo">[add street address, suburb, Cape Town]</span></dd></div>
      </dl>
    </div>
  </section>
</div>

<style>
  .top { padding-top: clamp(130px, 15vw, 190px); }
  .grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 0.8fr); gap: clamp(32px, 6vw, 96px); align-items: start; }
  .copy .lead { margin: 24px 0 36px; max-width: 44ch; }
  .stats { margin: 0; }
  .stats div { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 20px; padding: 18px 0; align-items: baseline; }
  .stats dt { font: 500 clamp(1.5rem, 1.1rem + 1.2vw, 2.1rem) / 1 var(--font-sans); letter-spacing: -0.04em; color: var(--accent); }
  .stats dd { margin: 0; color: var(--muted); }
  .sky { max-width: 520px; width: 100%; justify-self: end; }
  .narrowish { max-width: 820px; }
  .narrowish .lead { margin: 22px 0 30px; max-width: 48ch; }
  .narrow { max-width: 680px; text-align: center; }
  .narrow .lead { margin: 18px auto 0; }
  .ask { position: relative; margin-top: 40px; }
  .ask input { width: 100%; height: 66px; padding: 0 84px 0 24px; border: 1px solid var(--line); border-radius: 0; background: var(--panel); color: var(--ink); font: 400 1rem var(--font-sans); }
  .ask input::placeholder { color: var(--muted); }
  .ask input:focus { outline: none; border-color: var(--accent); }
  .ask button { position: absolute; right: 8px; top: 8px; width: 50px; height: 50px; border: 0; background: var(--accent); color: var(--on-accent); font-size: 1.5rem; cursor: pointer; transition: transform 0.25s var(--ease); }
  .ask button:hover { transform: translateX(4px); }
  .next { margin-top: 14px; font-size: 0.9rem; color: var(--muted); }
  .details { margin: 56px 0 0; text-align: left; }
  .details div { display: grid; grid-template-columns: 110px 1fr; gap: 16px; padding: 16px 0; }
  .details dt { color: var(--muted); }
  .details dd { margin: 0; }
  @media (max-width: 900px) {
    .grid { grid-template-columns: minmax(0, 1fr); }
    .sky { justify-self: stretch; max-width: none; }
    .stats div { grid-template-columns: minmax(0, 1fr); gap: 4px; }
    .details div { grid-template-columns: 1fr; gap: 2px; }
  }
</style>
