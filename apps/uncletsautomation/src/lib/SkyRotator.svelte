<script>
  import { onMount } from 'svelte';
  import { skies } from '$lib/content.js';
  import { reduced } from '$lib/motion.js';

  let i = $state(0);
  let timer;
  function run() {
    clearInterval(timer);
    if (reduced()) return;
    timer = setInterval(() => { if (!document.hidden) i = (i + 1) % skies.length; }, 5600);
  }
  function pick(n) { i = n; run(); }
  onMount(() => { run(); return () => clearInterval(timer); });

  const mtn = 'M0 500V338C40 330 70 338 100 324C120 298 140 284 165 300C180 310 195 314 215 300L245 258L262 252H345L362 258L380 283C395 296 400 300 400 304V500Z';
  const near = 'M0 500V420C70 408 140 428 220 414C290 402 350 418 400 408V500Z';
</script>

<figure class="frame" aria-label="Lexi at three times of day over Cape Town">
  {#each skies as s, n}
    <div class="scene" class:on={n === i} aria-hidden={n !== i}>
      <svg viewBox="0 0 400 500" preserveAspectRatio="xMidYMid slice" role="img" aria-label={s.alt}>
        <rect width="400" height="500" fill={s.sky} />
        <rect y="250" width="400" height="120" fill={s.glow} />
        {#if s.stars}
          {#each [[40, 60], [90, 120], [150, 50], [210, 100], [270, 40], [330, 90], [370, 150], [60, 190], [300, 170], [120, 210]] as [x, y]}
            <circle cx={x} cy={y} r="1.6" fill="#f1efe8" opacity="0.8" />
          {/each}
        {/if}
        <circle cx={s.sun[0]} cy={s.sun[1]} r={s.sun[2]} fill={s.sunColor} />
        <path d={mtn} fill={s.far} />
        <path d={near} fill={s.near} />
      </svg>
      <p class="msg"><b>{s.time}</b>{s.text}</p>
    </div>
  {/each}
  <figcaption>
    <span>Cape Town, {skies[i].label}</span>
    <span class="dots">
      {#each skies as s, n}
        <button type="button" aria-label="Show {s.label}" aria-current={n === i} onclick={() => pick(n)}></button>
      {/each}
    </span>
  </figcaption>
</figure>

<style>
  .frame { margin: 0; position: relative; aspect-ratio: 4 / 5; overflow: hidden; background: var(--panel); border-radius: 4px; }
  .scene { position: absolute; inset: 0 0 52px 0; opacity: 0; transition: opacity 1.6s ease; }
  .scene.on { opacity: 1; }
  svg { width: 100%; height: 100%; display: block; }
  .msg { position: absolute; left: 20px; right: 20px; bottom: 28px; background: #fff; color: #111; padding: 12px 16px; border-radius: 14px; border-bottom-left-radius: 3px; font-size: 0.95rem; line-height: 1.4; max-width: 86%; }
  .msg b { display: block; font: 600 0.8rem var(--font-sans); color: #075e54; margin-bottom: 2px; }
  figcaption { position: absolute; inset: auto 0 0 0; height: 52px; background: var(--bg); display: flex; align-items: center; justify-content: space-between; padding: 0 20px; font: italic 500 1rem var(--font-display); }
  .dots { display: flex; gap: 4px; }
  .dots button { width: 28px; height: 28px; padding: 0; border: 0; background: none; cursor: pointer; position: relative; }
  .dots button::after { content: ''; position: absolute; left: 8px; top: 12px; width: 12px; height: 3px; background: var(--ink); opacity: 0.3; transition: opacity 0.3s, width 0.3s; }
  .dots button[aria-current='true']::after { opacity: 1; width: 16px; left: 6px; }
</style>
