<script>
  import { onMount } from 'svelte';
  import { photos } from '$lib/content.js';
  import { reduced } from '$lib/motion.js';

  let i = $state(0);
  let timer;
  function run() {
    clearInterval(timer);
    if (reduced()) return;
    timer = setInterval(() => { if (!document.hidden) i = (i + 1) % photos.length; }, 4600);
  }
  function pick(n) { i = n; run(); }
  onMount(() => { run(); return () => clearInterval(timer); });
</script>

<div class="stage">
  <div class="main">
    {#each photos as p, n}
      <img src={p.src} alt={p.alt} width="900" height="1200" loading={n === 0 ? 'eager' : 'lazy'} class:on={n === i} />
    {/each}
  </div>
  <div class="thumbs">
    {#each photos as p, n}
      <button type="button" aria-label="Show photo {n + 1}" aria-current={n === i} onclick={() => pick(n)}>
        <img src={p.src} alt="" width="90" height="120" loading="lazy" />
      </button>
    {/each}
  </div>
</div>

<style>
  .stage { display: grid; grid-template-columns: minmax(0, 1fr) 72px; gap: 14px; }
  .main { position: relative; aspect-ratio: 3 / 4; overflow: hidden; background: var(--panel); }
  .main img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: opacity 1.4s ease, transform 6s ease; transform: scale(1.06); }
  .main img.on { opacity: 1; transform: scale(1); }
  .thumbs { display: flex; flex-direction: column; gap: 10px; }
  .thumbs button { padding: 0; border: 0; background: none; cursor: pointer; aspect-ratio: 3 / 4; overflow: hidden; opacity: 0.45; transition: opacity 0.3s; }
  .thumbs button[aria-current='true'], .thumbs button:hover { opacity: 1; }
  .thumbs img { width: 100%; height: 100%; object-fit: cover; }
  @media (max-width: 560px) { .stage { grid-template-columns: minmax(0, 1fr); } .thumbs { flex-direction: row; } .thumbs button { flex: 1; } }
</style>
