<script>
  import { onMount } from 'svelte';
  import { setupReveals } from '$lib/motion.js';
  import { theo, steps, places, faq } from '$lib/content.js';

  let { delay = 0 } = $props();
  let root;
  onMount(() => setupReveals(root, { delay }));
</script>

<div bind:this={root}>
  <section class="sec intro">
    <div class="wrap">
      <h1 class="h1" data-words>Built by a local, not a call centre.</h1>
      <div class="cols">
        {#each theo as para}<p data-reveal>{para}</p>{/each}
      </div>
    </div>
  </section>

  <section class="sec how">
    <div class="wrap">
      <h2 class="h2" data-words>Four days from yes to live.</h2>
      <div class="steps">
        {#each steps as [title, text]}
          <div class="row row-rule" data-reveal>
            <h3>{title}</h3>
            <p>{text}</p>
          </div>
        {/each}
      </div>
    </div>
  </section>

  <section class="sec places">
    <div class="wrap">
      <h2 class="h2" data-words>Where we work.</h2>
      <p class="list" data-reveal>
        {#each places as pl, i}<span>{pl}</span>{#if i < places.length - 1}<em> / </em>{/if}{/each}
      </p>
    </div>
  </section>

  <section class="sec faq" id="questions">
    <div class="wrap fgrid">
      <h2 class="h2" data-words>Questions.</h2>
      <div class="items">
        {#each faq as [q, a]}
          <details class="row-rule" data-reveal>
            <summary>{q}</summary>
            <p>{a} {#if q.startsWith("What happens")}<a class="ulink" href="/privacy">Read the privacy policy.</a>{/if}</p>
          </details>
        {/each}
      </div>
    </div>
  </section>
</div>

<style>
  .intro { padding-top: clamp(130px, 15vw, 190px); }
  .intro .h1 { max-width: 16ch; }
  .cols { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: clamp(24px, 5vw, 80px); margin-top: clamp(32px, 5vw, 64px); font-size: clamp(1rem, 0.95rem + 0.3vw, 1.125rem); line-height: 1.6; }
  .cols p { max-width: 36em; }
  .steps { margin-top: clamp(32px, 5vw, 64px); }
  .row { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: 32px; padding: clamp(24px, 3.4vw, 44px) 0; }
  .row h3 { font-size: clamp(1.15rem, 1rem + 0.6vw, 1.5rem); }
  .row p { color: var(--muted); max-width: 52ch; }
  .list { margin-top: 32px; font: italic 500 clamp(1.4rem, 1rem + 2.2vw, 2.8rem) / 1.25 var(--font-display); overflow-wrap: anywhere; }
  .list em { color: var(--accent); font-style: normal; padding: 0 0.3em; }
  .fgrid { display: grid; grid-template-columns: minmax(0, 4fr) minmax(0, 8fr); gap: clamp(24px, 5vw, 80px); align-items: start; }
  .fgrid .h2 { position: sticky; top: 120px; }
  details { padding: 0; }
  summary { list-style: none; cursor: pointer; padding: 22px 0; font: 500 clamp(1rem, 0.95rem + 0.3vw, 1.125rem) / 1.3 var(--font-sans); letter-spacing: -0.01em; display: flex; justify-content: space-between; gap: 20px; align-items: center; min-height: 64px; }
  summary::-webkit-details-marker { display: none; }
  summary::after { content: '+'; font: 300 1.8rem var(--font-sans); color: var(--accent); transition: transform 0.3s var(--ease); flex: none; }
  details[open] summary::after { transform: rotate(45deg); }
  details p { padding: 0 0 24px; color: var(--muted); max-width: 58ch; }
  @media (max-width: 900px) {
    .cols, .fgrid, .row { grid-template-columns: minmax(0, 1fr); }
    .row { gap: 10px; }
    .fgrid .h2 { position: static; }
  }
</style>
