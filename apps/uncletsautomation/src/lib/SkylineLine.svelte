<script>
  import { onMount } from 'svelte';
  import { gsap, reduced } from '$lib/motion.js';
  import { ridgeY, buildings, stadium, cranes, base, lift } from '$lib/skyline.js';

  let { draw = true, opacity = 0.7 } = $props();
  const W = 1440, H = 400;
  const Y = (y) => lift(y, 0.2) * H;
  const baseY = Y(base);

  const ridgePath = (() => {
    const pts = [];
    for (let x = 0; x <= W; x += 10) pts.push(`${x},${Y(ridgeY(x / W)).toFixed(1)}`);
    return 'M' + pts.join('L');
  })();
  const bld = buildings
    .map(([x, w, h]) => {
      const x0 = x * W, x1 = (x + w) * W, top = Y(base - h);
      return `M${x0.toFixed(1)} ${baseY}V${top.toFixed(1)}H${x1.toFixed(1)}V${baseY}`;
    })
    .join('');
  const stad = `M${(stadium.x * W).toFixed(1)} ${baseY}Q${((stadium.x + stadium.w / 2) * W).toFixed(1)} ${Y(base - stadium.h * 2.4).toFixed(1)} ${((stadium.x + stadium.w) * W).toFixed(1)} ${baseY}`;
  const crane = cranes
    .map(([x, h]) => `M${(x * W).toFixed(1)} ${baseY}V${Y(base - h).toFixed(1)}H${(x * W - 24).toFixed(1)}`)
    .join('');
  const sea = [0, 1, 2, 3].map((i) => `M${40 + i * 90} ${baseY + 14 + i * 12}H${W - 40 - i * 110}`).join('');
  const paths = [ridgePath, bld + stad + crane, sea];

  let svg;
  onMount(() => {
    if (!draw || reduced()) return;
    const els = [...svg.querySelectorAll('path')];
    const ctx = gsap.context(() => {
      gsap.fromTo(els, { strokeDashoffset: 1 }, {
        strokeDashoffset: 0, ease: 'none', stagger: 0.18,
        scrollTrigger: { trigger: svg, start: 'top 92%', end: 'top 30%', scrub: 0.7 }
      });
    }, svg);
    return () => ctx.revert();
  });
</script>

<svg bind:this={svg} viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMax meet" role="img" aria-label="Line drawing of Table Mountain and the Cape Town city centre" style="opacity:{opacity}">
  {#each paths as d}
    <path {d} pathLength="1" fill="none" stroke="currentColor" stroke-width="1.6" vector-effect="non-scaling-stroke" stroke-linejoin="round" stroke-linecap="round" style="stroke-dasharray:1;stroke-dashoffset:0" />
  {/each}
</svg>

<style>
  svg { display: block; width: 100%; height: auto; color: var(--accent); }
</style>
