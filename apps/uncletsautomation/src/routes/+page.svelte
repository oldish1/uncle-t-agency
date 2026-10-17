<script>
  import { onMount, tick } from 'svelte';
  import { views, WHATSAPP, wa } from '$lib/content.js';
  import { gsap, reduced } from '$lib/motion.js';
  import HomeView from '$lib/views/HomeView.svelte';
  import StudioView from '$lib/views/StudioView.svelte';
  import ProofView from '$lib/views/ProofView.svelte';

  let view = $state('home');
  let delay = $state(0);
  let roll;
  let rollLabel = $state('');
  let busy = false;

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
      window.scrollTo(0, 0);
      return;
    }
    busy = true;
    rollLabel = target.label;
    gsap.timeline({ onComplete: () => { busy = false; } })
      .set(roll, { display: 'grid', yPercent: 100, backgroundColor: target.bg, color: target.theme === 'dark' ? '#f1efe8' : '#0e1511' })
      .to(roll, { yPercent: 0, duration: 0.75, ease: 'power3.inOut' })
      .add(() => { delay = 0.2; view = to; window.scrollTo(0, 0); })
      .to(roll, { yPercent: -100, duration: 0.75, ease: 'power3.inOut' }, '+=0.25')
      .set(roll, { display: 'none' });
  }

  onMount(() => {
    view = fromHash();
    const onPop = () => go(fromHash(), false);
    window.addEventListener('popstate', onPop);
    return () => window.removeEventListener('popstate', onPop);
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
      <ProofView {delay} />
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
  .nav { position: fixed; inset: 0 0 auto 0; z-index: 40; display: flex; align-items: center; justify-content: space-between; gap: 16px; padding: 20px var(--margin); mix-blend-mode: normal; background: color-mix(in srgb, var(--bg) 82%, transparent); backdrop-filter: blur(10px); }
  .mark { font: 500 1.2rem var(--font-display); text-decoration: none; letter-spacing: -0.01em; }
  .mark i { font-style: italic; }
  .tabs { display: flex; gap: clamp(16px, 3vw, 40px); }
  .tabs a { text-decoration: none; font: 500 0.8125rem var(--font-sans); letter-spacing: 0.14em; text-transform: uppercase; padding: 8px 0; background: linear-gradient(currentColor, currentColor) 0 100% / 0 1px no-repeat; transition: background-size 0.3s var(--ease); }
  .tabs a:hover, .tabs a[aria-current='page'] { background-size: 100% 1px; }
  .cta { text-decoration: none; font: 500 0.875rem var(--font-sans); padding: 0 18px; min-height: 40px; display: inline-flex; align-items: center; background: var(--accent); color: var(--on-accent); transition: transform 0.25s var(--ease); }
  .cta:hover { transform: translateY(-2px); }

  .foot { padding: clamp(48px, 8vw, 100px) var(--margin) 32px; overflow: hidden; border-top: 1px solid var(--line); }
  .big { font: 500 clamp(2.2rem, 1rem + 8.4vw, 9.5rem) / 0.95 var(--font-display); letter-spacing: -0.03em; white-space: nowrap; opacity: 0.9; }
  .row { margin-top: 40px; display: flex; flex-wrap: wrap; gap: 20px 48px; justify-content: space-between; color: var(--muted); font-size: 0.9rem; }
  .row nav { display: flex; gap: 24px; flex-wrap: wrap; }
  .row a { text-decoration: none; }
  .row a:hover { color: var(--ink); }

  .roll { position: fixed; inset: 0; z-index: 100; display: none; place-items: center; }
  .roll span { font: italic 500 clamp(2.4rem, 1rem + 6vw, 6rem) var(--font-display); }

  @media (max-width: 720px) {
    .nav { flex-wrap: wrap; padding: 14px var(--margin) 10px; }
    .tabs { order: 3; width: 100%; justify-content: space-between; gap: 8px; }
    .big { white-space: normal; font-size: 14vw; }
  }
</style>
