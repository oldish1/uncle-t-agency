<script>
  import { onMount, tick } from 'svelte';
  import { views, WHATSAPP, wa } from '$lib/content.js';
  import Lenis from 'lenis';
  import { gsap, ScrollTrigger, reduced } from '$lib/motion.js';
  import HomeView from '$lib/views/HomeView.svelte';
  import StudioView from '$lib/views/StudioView.svelte';
  import StartView from '$lib/views/StartView.svelte';

  let view = $state('home');
  let delay = $state(0);
  let roll;
  let rollLabel = $state('');
  let busy = false;
  let lenis;
  const toTop = () => (lenis ? lenis.scrollTo(0, { immediate: true, force: true }) : window.scrollTo(0, 0));

  const find = (id) => views.find((v) => v.id === id) ?? views[0];
  const theme = $derived(find(view).theme);
  const fromHash = () => find(location.hash.slice(1)).id;

  function go(to, push = true) {
    if (to === view || busy) return;
    if (push) history.pushState({}, '', '#' + to);
    const target = find(to);
    if (reduced() || !roll) {
      delay = 0;
      view = to;
      toTop();
      return;
    }
    busy = true;
    lenis?.stop();
    rollLabel = target.label;
    gsap.timeline({ onComplete: () => { busy = false; lenis?.start(); ScrollTrigger.refresh(); } })
      .set(roll, { display: 'grid', yPercent: 100, backgroundColor: target.bg, color: target.theme === 'dark' ? '#f1efe8' : '#0e1511' })
      .to(roll, { yPercent: 0, duration: 0.75, ease: 'power3.inOut' })
      .add(() => { delay = 0.2; view = to; toTop(); })
      .to(roll, { yPercent: -100, duration: 0.75, ease: 'power3.inOut' }, '+=0.25')
      .set(roll, { display: 'none' });
  }

  onMount(() => {
    view = fromHash();
    if (!reduced()) {
      lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.95 });
      lenis.on('scroll', ScrollTrigger.update);
      gsap.ticker.add((t) => lenis.raf(t * 1000));
      gsap.ticker.lagSmoothing(0);
    }
    const onPop = () => go(fromHash(), false);
    window.addEventListener('popstate', onPop);
    return () => { window.removeEventListener('popstate', onPop); lenis?.destroy(); };
  });
</script>

<svelte:head>
  <title>Uncle Ts Automation | WhatsApp booking for Cape Town businesses</title>
  <meta name="description" content="Uncle Ts Automation builds a WhatsApp receptionist and a fast website for small Cape Town businesses. Websites from R799 setup and R499 a month, Lexi from R1,499 setup and R799 a month." />
  {@html `<script type="application/ld+json">${JSON.stringify({
    '@context': 'https://schema.org', '@type': 'ProfessionalService', name: 'Uncle Ts Automation',
    url: 'https://uncletsautomation.co.za', telephone: '+27764924196', areaServed: 'Cape Town, South Africa',
    description: 'WhatsApp booking assistant and websites for small local businesses in Cape Town.'
  })}</script>`}
</svelte:head>

<div class="app" data-theme={theme}>
  <header class="nav">
    <a class="mark" href="#home" onclick={(e) => { e.preventDefault(); go('home'); }}>Uncle Ts <i>Automation</i></a>
    <nav class="tabs" aria-label="Views">
      {#each views as v}
        <a href={'#' + v.id} aria-current={view === v.id ? 'page' : undefined} onclick={(e) => { e.preventDefault(); go(v.id); }}>{v.label}</a>
      {/each}
    </nav>
    <a class="cta" href={wa('Hi Theo, I\'d like to see Lexi')}>WhatsApp us</a>
  </header>

  <main id="main">
    {#if view === 'home'}
      <HomeView {delay} {go} />
    {:else if view === 'studio'}
      <StudioView {delay} />
    {:else}
      <StartView {delay} />
    {/if}
  </main>

  <footer class="foot">
    <p class="big" aria-hidden="true">Uncle Ts Automation</p>
    <div class="row">
      <nav aria-label="Footer">
        {#each views as v}
          <a href={'#' + v.id} onclick={(e) => { e.preventDefault(); go(v.id); }}>{v.label}</a>
        {/each}
        <a href="/privacy">Privacy</a>
      </nav>
      <p>Uncle Ts Automation, Cape Town, South Africa. Prices in Rand.</p>
    </div>
  </footer>

  <div class="roll" bind:this={roll} aria-hidden="true"><span>{rollLabel}</span></div>
</div>

<style>
  .app { min-height: 100svh; background: var(--bg); color: var(--ink); transition: background-color 0.4s, color 0.4s; }
  .nav { position: fixed; inset: 0 0 auto 0; z-index: 40; display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 14px var(--margin); background: color-mix(in srgb, var(--bg) 70%, transparent); backdrop-filter: blur(14px); border-bottom: 1px solid var(--line); }
  .mark { font: 500 1.05rem var(--font-sans); text-decoration: none; letter-spacing: -0.03em; }
  .mark i { font: italic 500 1.1rem var(--font-display); letter-spacing: -0.01em; }
  .tabs { display: flex; gap: clamp(16px, 3vw, 40px); }
  .tabs a { text-decoration: none; font: 500 0.8125rem var(--font-sans); letter-spacing: 0; padding: 8px 0; opacity: 0.8; background: linear-gradient(currentColor, currentColor) 0 100% / 0 1px no-repeat; transition: background-size 0.3s var(--ease); }
  .tabs a:hover, .tabs a[aria-current='page'] { background-size: 100% 1px; opacity: 1; }
  .cta { text-decoration: none; font: 500 0.8125rem var(--font-sans); padding: 0 16px; min-height: 36px; border-radius: 999px; display: inline-flex; align-items: center; background: var(--ink); color: var(--bg); transition: transform 0.25s var(--ease); }
  .cta:hover { transform: translateY(-2px); }

  .foot { padding: clamp(48px, 8vw, 100px) var(--margin) 32px; overflow: hidden; border-top: 1px solid var(--line); }
  .big { font: 500 clamp(2rem, 1rem + 7vw, 8rem) / 0.95 var(--font-sans); letter-spacing: -0.06em; white-space: nowrap; color: var(--ink); opacity: 0.92; }
  .row { margin-top: 40px; display: flex; flex-wrap: wrap; gap: 20px 48px; justify-content: space-between; color: var(--muted); font-size: 0.9rem; }
  .row nav { display: flex; gap: 24px; flex-wrap: wrap; }
  .row a { text-decoration: none; }
  .row a:hover { color: var(--ink); }

  .roll { position: fixed; inset: 0; z-index: 100; display: none; place-items: center; }
  .roll span { font: italic 500 clamp(2.2rem, 1rem + 4vw, 4.5rem) var(--font-display); }

  @media (max-width: 720px) {
    .nav { flex-wrap: wrap; padding: 14px var(--margin) 10px; }
    .tabs { order: 3; width: 100%; justify-content: space-between; gap: 8px; }
    .big { white-space: normal; font-size: 14vw; }
  }
</style>
