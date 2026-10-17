<script>
  import { onMount } from 'svelte';
  import { setupReveals } from '$lib/motion.js';
  import { stats } from '$lib/content.js';
  import MountainDay from '$lib/MountainDay.svelte';
  import ContactWizard from '$lib/ContactWizard.svelte';

  let { delay = 0 } = $props();
  let root;
  onMount(() => setupReveals(root, { delay }));
</script>

<div bind:this={root}>
  <MountainDay />

  <section class="sec stats">
    <div class="wrap row">
      {#each stats as [n, t]}
        <div data-reveal><b>{n}</b><span>{t}</span></div>
      {/each}
    </div>
  </section>

  <section class="sec first">
    <div class="wrap">
      <h2 class="h2" data-words>First client: a Bellville <em>salon</em>.</h2>
      <p class="lead" data-reveal>Lexi runs the bookings at Chales Hair Boutique today, with cancellations, reschedules, reminders and a prepaid wash-and-blowdry membership. It's a real salon with a real diary, so you can see it working before you pay anything.</p>
      <a class="btn" data-reveal href="https://chaleshairboutique.co.za" rel="noopener">See the Chales website</a>
    </div>
  </section>

  <section class="sec contact" id="contact">
    <div class="wrap">
      <h2 class="h2" data-words>Start in thirty seconds.</h2>
      <p class="lead" data-reveal>Answer four quick questions and your message to Theo writes itself.</p>
      <div class="w" data-reveal><ContactWizard /></div>
      <dl class="details" data-reveal>
        <div><dt>WhatsApp</dt><dd><a class="ulink" href="https://wa.me/27764924196">076 492 4196</a></dd></div>
        <div><dt>Email</dt><dd><span class="todo">[add email on the domain]</span></dd></div>
        <div><dt>Address</dt><dd><span class="todo">[add street address, suburb, Cape Town]</span></dd></div>
      </dl>
    </div>
  </section>
</div>

<style>
  .row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
  .row div { border-top: 1px solid var(--line); padding-top: 22px; }
  .row b { display: block; font: 500 clamp(1.8rem, 1.2rem + 2vw, 3rem) / 1 var(--font-sans); letter-spacing: -0.05em; color: var(--accent); }
  .row span { display: block; margin-top: 10px; color: var(--muted); max-width: 26ch; }
  .first .lead { margin: 20px 0 28px; max-width: 52ch; }
  .first .h2 { max-width: 18ch; }
  .contact { background: var(--panel); }
  .contact .h2 { max-width: 16ch; }
  .contact .lead { margin: 14px 0 clamp(28px, 4vw, 52px); }
  .details { margin: clamp(40px, 6vw, 72px) 0 0; display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 24px; }
  .details div { border-top: 1px solid var(--line); padding-top: 16px; }
  .details dt { color: var(--muted); font-size: 0.85rem; }
  .details dd { margin: 6px 0 0; }
  @media (max-width: 900px) { .row, .details { grid-template-columns: minmax(0, 1fr); } }
</style>
