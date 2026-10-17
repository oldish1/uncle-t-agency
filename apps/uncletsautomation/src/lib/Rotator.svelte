<script>
  import { onMount } from 'svelte';
  import { screens } from '$lib/content.js';
  import { reduced } from '$lib/motion.js';

  let i = $state(0);
  let timer;
  function run() {
    stop();
    if (reduced()) return;
    timer = setInterval(() => { if (!document.hidden) i = (i + 1) % screens.length; }, 5200);
  }
  function stop() { clearInterval(timer); }
  function pick(n) { i = n; run(); }
  onMount(() => { run(); return stop; });
</script>

<figure class="frame" aria-label="Sample conversations for different businesses">
  {#each screens as s, n}
    <div class="screen" class:on={n === i} aria-hidden={n !== i}>
      <div class="bar"><span class="av" aria-hidden="true">L</span><div><b>{s.name}</b><span>Booking assistant (sample)</span></div></div>
      <div class="lines">
        {#each s.lines as [who, text]}
          <p class="b {who}">{text}</p>
        {/each}
      </div>
    </div>
  {/each}
  <figcaption>
    <span>{screens[i].note}</span>
    <span class="dots">
      {#each screens as s, n}
        <button type="button" aria-label="Show {s.note}" aria-current={n === i} onclick={() => pick(n)}></button>
      {/each}
    </span>
  </figcaption>
</figure>

<style>
  .frame { margin: 0; position: relative; aspect-ratio: 4 / 5; background: var(--panel); border: 1px solid var(--line); border-radius: 4px; overflow: hidden; }
  .screen { position: absolute; inset: 0 0 52px 0; padding: 24px; display: flex; flex-direction: column; gap: 22px; opacity: 0; transition: opacity 1.4s ease; pointer-events: none; }
  .screen.on { opacity: 1; pointer-events: auto; }
  .bar { display: flex; align-items: center; gap: 12px; }
  .av { width: 40px; height: 40px; border-radius: 50%; background: var(--green); color: #04120a; display: grid; place-items: center; font: 600 1.2rem var(--font-display); flex: none; }
  .bar b { display: block; font: 500 1.15rem var(--font-display); }
  .bar span:not(.av) { font-size: 0.8rem; color: var(--muted); }
  .lines { display: flex; flex-direction: column; gap: 12px; margin-top: auto; }
  .b { max-width: 84%; padding: 11px 15px; border-radius: 14px; font-size: 0.95rem; line-height: 1.4; }
  .b.them { align-self: flex-start; background: #fff; color: #111; border-bottom-left-radius: 3px; }
  .b.us { align-self: flex-end; background: #cdeed2; color: #0a2a1a; border-bottom-right-radius: 3px; }
  figcaption { position: absolute; inset: auto 0 0 0; height: 52px; border-top: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; padding: 0 24px; font: italic 500 1rem var(--font-display); }
  .dots { display: flex; gap: 4px; }
  .dots button { width: 28px; height: 28px; padding: 0; border: 0; background: none; cursor: pointer; position: relative; }
  .dots button::after { content: ''; position: absolute; left: 8px; top: 12px; width: 12px; height: 3px; background: var(--ink); opacity: 0.3; transition: opacity 0.3s, width 0.3s; }
  .dots button[aria-current='true']::after { opacity: 1; width: 16px; left: 6px; }
</style>
