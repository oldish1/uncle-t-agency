<script>
  import { onMount } from 'svelte';
  import { gsap, reduced } from '$lib/motion.js';

  const days = [
    ['Day one', 'We set up Lexi on her own number.', 'She gets a dedicated WhatsApp number, separate from yours. You tell us your services, prices and hours, and we write her greeting in your voice.'],
    ['Day two', 'We connect your calendar.', "Your Google Calendar becomes the single source of truth for what's free."],
    ['Day three', 'We test it with you.', 'You book, cancel and reschedule as a customer until it feels right.'],
    ['Day four', 'You go live.', 'Customers book while you cut, braid or fit pipes. We keep it running.']
  ];
  let sec, track, bar;

  onMount(() => {
    if (reduced() || matchMedia('(max-width: 900px)').matches) return;
    const ctx = gsap.context(() => {
      const dist = () => track.scrollWidth - window.innerWidth + 2 * parseFloat(getComputedStyle(track).paddingLeft);
      gsap.to(track, {
        x: () => -dist(), ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top top', end: () => '+=' + (dist() + 400), pin: true, scrub: 0.6, invalidateOnRefresh: true, anticipatePin: 1,
          onUpdate: (self) => { bar.style.transform = `scaleX(${self.progress})`; } }
      });
    }, sec);
    return () => ctx.revert();
  });
</script>

<section class="fd" bind:this={sec} aria-labelledby="fdh">
  <div class="stick">
    <div class="head">
      <h2 class="h2" id="fdh">Four days from yes to <em>live</em>.</h2>
      <div class="rail" aria-hidden="true"><i bind:this={bar}></i></div>
    </div>
    <div class="track" bind:this={track}>
      {#each days as [d, t, p], i}
        <article class="card">
          <div class="art" aria-hidden="true">
            {#if i === 0}
              <div class="ph"><span class="av">L</span><u></u><u class="s"></u><em>076 ••• ••••</em></div>
            {:else if i === 1}
              <div class="cg">{#each Array(12) as _, k}<span class:on={k === 5 || k === 8}></span>{/each}</div>
            {:else if i === 2}
              <div class="bb"><p class="a">Book Saturday 09:00</p><p class="b">Booked. Reminder on Friday.</p><p class="a">Cancel it</p><p class="b">Want a different day?</p></div>
            {:else}
              <div class="live"><i></i><b>Live</b><span>First booking just came in</span></div>
            {/if}
          </div>
          <p class="day">{d}</p>
          <h3>{t}</h3>
          <p>{p}</p>
        </article>
      {/each}
    </div>
  </div>
</section>

<style>
  .fd { position: relative; }
  .stick { min-height: 100svh; display: flex; flex-direction: column; justify-content: center; gap: 36px; padding: 90px 0 40px; overflow: hidden; }
  .head { padding: 0 var(--margin); display: flex; align-items: flex-end; justify-content: space-between; gap: 32px; }
  .head .h2 { max-width: 14ch; }
  .rail { flex: 1; max-width: 360px; height: 3px; background: var(--line); border-radius: 3px; overflow: hidden; margin-bottom: 12px; }
  .rail i { display: block; height: 100%; background: var(--accent); transform: scaleX(0); transform-origin: left; }
  .track { display: flex; gap: 20px; padding: 0 var(--margin); width: max-content; will-change: transform; }
  .card { flex: none; width: clamp(300px, 34vw, 480px); background: var(--panel); border-radius: 22px; padding: 22px; display: flex; flex-direction: column; min-height: 420px; }
  .art { height: 200px; border-radius: 14px; background: var(--bg); display: grid; place-items: center; margin-bottom: 22px; overflow: hidden; }
  .day { color: var(--accent); font-weight: 500; font-size: 0.85rem; }
  .card h3 { font-size: 1.4rem; margin: 6px 0 10px; max-width: 18ch; }
  .card p:last-child { color: var(--muted); max-width: 34ch; }
  .ph { width: 150px; background: #fff; border-radius: 16px; padding: 14px; display: grid; gap: 8px; justify-items: start; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12); }
  .av { width: 30px; height: 30px; border-radius: 50%; background: #0b5d4a; color: #fff; display: grid; place-items: center; font: 600 0.95rem var(--font-display); }
  .ph u { height: 7px; width: 100%; background: #dfe4e0; border-radius: 4px; }
  .ph u.s { width: 60%; }
  .ph em { font: 500 0.78rem var(--font-sans); color: #0b5d4a; font-style: normal; }
  .cg { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; width: 220px; }
  .cg span { height: 34px; border-radius: 8px; background: var(--panel); }
  .cg span.on { background: #0b5d4a; animation: pulse 2.4s infinite; }
  .bb { width: 230px; display: grid; gap: 7px; font-size: 0.78rem; }
  .bb p { padding: 7px 11px; border-radius: 12px; width: fit-content; max-width: 90%; }
  .bb .a { background: #fff; color: #111; }
  .bb .b { background: #cdeed2; color: #0a2a1a; justify-self: end; }
  .live { display: grid; justify-items: center; gap: 6px; }
  .live i { width: 18px; height: 18px; border-radius: 50%; background: #25d366; animation: ping 2s infinite; }
  .live b { font: 500 1.6rem var(--font-sans); letter-spacing: -0.04em; }
  .live span { font-size: 0.8rem; color: var(--muted); }
  @keyframes pulse { 50% { transform: scale(1.08); } }
  @keyframes ping { 0% { box-shadow: 0 0 0 0 rgba(37, 211, 102, 0.5); } 100% { box-shadow: 0 0 0 22px rgba(37, 211, 102, 0); } }
  @media (max-width: 900px) {
    .stick { min-height: 0; padding: 56px 0; }
    .head { flex-direction: column; align-items: flex-start; }
    .rail { display: none; }
    .track { width: auto; flex-direction: column; }
    .card { width: auto; min-height: 0; }
  }
  @media (prefers-reduced-motion: reduce) {
    .stick { min-height: 0; padding: 56px 0; }
    .track { width: auto; flex-wrap: wrap; }
    .rail { display: none; }
    .cg span.on, .live i { animation: none; }
  }
</style>
