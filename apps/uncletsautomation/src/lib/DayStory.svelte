<script>
  import { onMount } from 'svelte';
  import { gsap, ScrollTrigger, reduced } from '$lib/motion.js';

  const scenes = [
    { time: '06:10', title: 'Before you are awake.', text: 'A customer messages at dawn. Lexi answers, offers the free slots and books one.',
      chat: [[0.05, 'them', 'Hi, can I get a blow-dry on Saturday?'], [0.2, 'us', 'Saturday has 09:00 and 11:30 free. Which suits you?'], [0.35, 'them', '09:00 please.'], [0.5, 'us', "Booked for Saturday 09:00. I'll remind you on Friday."]] },
    { time: '12:40', title: 'Lunch rush, hands full.', text: 'You are with a client. Another customer asks about braids. Lexi checks the calendar and books it.',
      chat: [[1.05, 'them', 'Do you do braids? Thursday maybe?'], [1.2, 'us', 'Yes. Thursday 14:00 is free.'], [1.35, 'them', 'Book it please.'], [1.5, 'us', 'Done. Thursday 14:00.']] },
    { time: '17:00', title: 'Reminders send themselves.', text: 'The day before, every client gets a WhatsApp reminder, so fewer people forget.',
      chat: [[2.1, 'us', 'Reminder: your blow-dry is tomorrow at 09:00. Reply C to cancel.'], [2.3, 'them', 'See you then!'], [2.45, 'us', 'Lovely. See you tomorrow.']] },
    { time: '21:05', title: 'A cancellation, handled.', text: 'Lexi offers a different day before she cancels, and frees the slot if they still cancel.',
      chat: [[3.05, 'them', 'Sorry, I need to cancel Thursday.'], [3.2, 'us', 'No problem. Want a different day instead?'], [3.35, 'them', 'Just cancel please.'], [3.5, 'us', 'Cancelled. That slot is open again.']] }
  ];
  const days = ['Thu', 'Fri', 'Sat'];
  const times = ['09:00', '11:30', '14:00'];
  /* [day, time, fills at, frees at] */
  const slots = { 'Sat-09:00': [0.55, 99], 'Thu-14:00': [1.55, 3.55], 'Fri-11:30': [2.2, 99] };

  let sec, clock, replies;
  let scenesEl = [], bubbles = [], caps = [], cells = {};
  const total = scenes.length;
  const tmin = (s) => { const [h, m] = s.split(':').map(Number); return h * 60 + m; };

  function render(v) {
    const idx = Math.min(total - 1, Math.floor(v));
    const f = v - idx;
    const a = tmin(scenes[idx].time), b = idx < total - 1 ? tmin(scenes[idx + 1].time) : a + 40;
    const mins = Math.round(a + (b - a) * Math.min(1, f * 1.15));
    clock.textContent = String(Math.floor(mins / 60) % 24).padStart(2, '0') + ':' + String(mins % 60).padStart(2, '0');
    scenesEl.forEach((el, i) => el.classList.toggle('on', i === idx));
    caps.forEach((el, i) => el.classList.toggle('on', i === idx));
    let n = 0;
    bubbles.forEach((el) => { const at = +el.dataset.at; const on = v >= at; el.classList.toggle('on', on); if (on && el.dataset.who === 'us') n++; });
    replies.textContent = n;
    for (const [k, [fill, free]] of Object.entries(slots)) {
      const on = v >= fill && v < free;
      cells[k]?.classList.toggle('on', on);
      cells[k]?.classList.toggle('freed', v >= free);
    }
  }

  onMount(() => {
    scenesEl = [...sec.querySelectorAll('.scene')];
    bubbles = [...sec.querySelectorAll('.m')];
    caps = [...sec.querySelectorAll('.cap')];
    sec.querySelectorAll('.cell').forEach((c) => { cells[c.dataset.k] = c; });
    if (reduced()) { render(total - 0.01); return; }
    render(0);
    const proxy = { v: 0 };
    const ctx = gsap.context(() => {
      gsap.to(proxy, {
        v: total - 0.01, ease: 'none',
        onUpdate: () => render(proxy.v),
        scrollTrigger: { trigger: sec, start: 'top top', end: '+=3200', pin: true, scrub: 0.5, anticipatePin: 1 }
      });
    }, sec);
    return () => ctx.revert();
  });
</script>

<section class="story" bind:this={sec} aria-label="A day with Lexi">
  <div class="pin">
    <div class="left">
      <p class="clock" bind:this={clock} aria-hidden="true">06:10</p>
      <div class="caps">
        {#each scenes as s, i}
          <div class="cap">
            <h2 class="h2">{s.title}</h2>
            <p class="lead">{s.text}</p>
          </div>
        {/each}
      </div>
      <p class="tally"><b bind:this={replies}>0</b> replies sent. <b>0</b> double-bookings.</p>
    </div>
    <div class="right">
      <div class="phone" data-ui>
        <div class="head"><span class="av" aria-hidden="true">L</span><div><b>Sample Hair Salon</b><span>Booking assistant (sample)</span></div></div>
        <div class="body">
          {#each scenes as s, i}
            <div class="scene">
              {#each s.chat as [at, who, text]}
                <p class="m {who}" data-at={at} data-who={who}>{text}</p>
              {/each}
            </div>
          {/each}
        </div>
      </div>
      <div class="cal" aria-label="Calendar">
        <p class="cal-h">Calendar</p>
        <div class="grid">
          {#each days as d}<span class="dh">{d}</span>{/each}
          {#each times as t}
            {#each days as d}
              <span class="cell" data-k={d + '-' + t}>{t}</span>
            {/each}
          {/each}
        </div>
      </div>
    </div>
  </div>
</section>

<style>
  .story { position: relative; }
  .pin { min-height: 100svh; display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: clamp(24px, 5vw, 80px); align-items: center; padding: 90px var(--margin) 40px; max-width: 1360px; margin-inline: auto; }
  .clock { font: 500 clamp(3.2rem, 1.5rem + 6vw, 7rem) / 1 var(--font-sans); letter-spacing: -0.05em; font-variant-numeric: tabular-nums; color: var(--accent); }
  .caps { position: relative; margin-top: 18px; min-height: 190px; }
  .cap { position: absolute; inset: 0 auto auto 0; opacity: 0; transform: translateY(14px); transition: opacity 0.5s, transform 0.5s var(--ease); pointer-events: none; }
  .cap.on { opacity: 1; transform: none; }
  .cap .lead { margin-top: 12px; max-width: 34ch; }
  .tally { margin-top: 28px; color: var(--muted); font-size: 0.9rem; }
  .tally b { color: var(--ink); font-weight: 500; }
  .right { display: grid; grid-template-columns: minmax(0, 340px) minmax(0, 200px); gap: 22px; align-items: center; justify-content: center; }
  .phone { height: min(520px, 66svh); min-height: 400px; background: #e6ebe7; color: #111; border-radius: 28px; overflow: hidden; display: flex; flex-direction: column; border: 6px solid #1c2721; font-size: 0.9rem; line-height: 1.4; }
  .head { background: #075e54; color: #fff; padding: 11px 13px; display: flex; align-items: center; gap: 10px; }
  .av { width: 36px; height: 36px; border-radius: 50%; background: var(--green); color: #04120a; display: grid; place-items: center; font: 600 1.05rem var(--font-display); flex: none; }
  .head b { display: block; font-weight: 600; font-size: 0.9rem; }
  .head span:not(.av) { font-size: 0.75rem; opacity: 0.85; }
  .body { position: relative; flex: 1; overflow: hidden; }
  .scene { position: absolute; inset: 0; padding: 14px 12px; display: flex; flex-direction: column; gap: 8px; justify-content: flex-end; opacity: 0; transition: opacity 0.4s; }
  .scene.on { opacity: 1; }
  .m { max-width: 84%; padding: 8px 11px; border-radius: 10px; opacity: 0; transform: translateY(8px); transition: opacity 0.35s, transform 0.35s var(--ease); }
  .m.on { opacity: 1; transform: none; }
  .m.them { align-self: flex-start; background: #fff; border-top-left-radius: 2px; }
  .m.us { align-self: flex-end; background: #cdeed2; border-top-right-radius: 2px; }
  .cal { background: var(--panel); border: 1px solid var(--line); border-radius: 18px; padding: 16px; }
  .cal-h { font-weight: 500; margin-bottom: 12px; font-size: 0.9rem; }
  .grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
  .dh { font-size: 0.75rem; color: var(--muted); text-align: center; }
  .cell { font-size: 0.72rem; text-align: center; padding: 9px 0; border-radius: 8px; background: var(--panel2); color: var(--muted); transition: background 0.4s, color 0.4s, transform 0.4s var(--ease); }
  .cell.on { background: var(--green); color: #04120a; font-weight: 600; transform: scale(1.06); }
  .cell.freed { background: transparent; border: 1px dashed var(--green); color: var(--green); }
  @media (max-width: 900px) {
    .pin { grid-template-columns: minmax(0, 1fr); gap: 12px; padding-top: 108px; align-content: start; }
    .clock { font-size: 3rem; }
    .caps { min-height: 150px; margin-top: 8px; }
    .cap .h2 { font-size: 1.4rem; }
    .tally { display: none; }
    .right { grid-template-columns: minmax(0, 1fr) 110px; gap: 10px; }
    .phone { height: 360px; min-height: 0; font-size: 0.8rem; }
    .scene { gap: 6px; padding: 10px; }
    .m { padding: 6px 9px; }
    .cal { padding: 10px; }
    .cell { font-size: 0.62rem; padding: 6px 0; }
    .dh { font-size: 0.65rem; }
  }
  @media (prefers-reduced-motion: reduce) {
    .cap { position: static; opacity: 1; transform: none; margin-bottom: 18px; }
    .caps { min-height: 0; }
  }
</style>
