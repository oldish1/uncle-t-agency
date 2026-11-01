<script>
  import { onMount, tick } from 'svelte';
  import { BIZ, T } from '$lib/content.js';

  let lang = $state('en');
  let biz = $state('salon');
  let msgs = $state([]);
  let chips = $state([]);
  let typing = $state(false);
  let box;
  let gen = 0;
  let svc = '', day = '';

  const t = () => T[lang];
  const clock = () => new Date().toLocaleTimeString('en-ZA', { hour: '2-digit', minute: '2-digit', timeZone: 'Africa/Johannesburg' });

  async function push(text, who) {
    msgs.push({ text, who, time: clock() });
    await tick();
    box?.scrollTo({ top: box.scrollHeight, behavior: 'smooth' });
  }
  function days() {
    const out = [];
    const d = new Date();
    for (let i = 1; out.length < 3; i++) {
      const x = new Date(d.getTime() + i * 86400000);
      if (x.getDay() === 0) continue;
      out.push(i === 1 ? t().tomorrow : x.toLocaleDateString(t().loc, { weekday: 'long', day: 'numeric', month: 'short', timeZone: 'Africa/Johannesburg' }));
    }
    return out;
  }
  function say(text, next) {
    const my = gen;
    chips = [];
    typing = true;
    tick().then(() => box?.scrollTo({ top: box.scrollHeight }));
    setTimeout(async () => {
      if (my !== gen) return;
      typing = false;
      await push(text, 'in');
      next?.();
    }, 650);
  }
  function offer(list, fn) {
    chips = list.map((label) => ({ label, fn: () => { fn(label); } }));
  }
  function start() {
    gen++;
    msgs = [];
    chips = [];
    svc = day = '';
    say(t().hi(BIZ[biz].name[lang]), () =>
      offer(BIZ[biz].svc[lang], (s) => { svc = s; push(s, 'out'); askDay(); }));
  }
  function askDay() {
    say(t().day, () => offer(days(), (d) => { day = d; push(d, 'out'); askTime(); }));
  }
  function askTime() {
    say(t().time, () => offer(t().times, (time) => {
      push(time, 'out');
      say(t().done(svc, day, time), () => say(t().ask, () => offer(t().chg, (c) => {
        push(c, 'out');
        const i = t().chg.indexOf(c);
        if (i === 0) say(t().again, askDay);
        else if (i === 1) say(t().cancel, () => offer([t().chg[2]], () => start()));
        else start();
      })));
    }));
  }
  function setLang(l) { lang = l; start(); }
  function setBiz(b) { biz = b; start(); }
  onMount(start);
</script>

<div class="wrap">
  <div class="tabs" role="group" aria-label="Pick a business type">
    {#each Object.entries(BIZ) as [id, b]}
      <button type="button" aria-pressed={biz === id} onclick={() => setBiz(id)}>{b.label}</button>
    {/each}
  </div>
  <div class="phone">
    <div class="head">
      <span class="av" aria-hidden="true">L</span>
      <div class="who"><b>{BIZ[biz].name[lang]}</b><span>{t().hdr}</span></div>
      <div class="lang" role="group" aria-label="Language">
        <button type="button" aria-pressed={lang === 'en'} onclick={() => setLang('en')}>EN</button>
        <button type="button" aria-pressed={lang === 'af'} onclick={() => setLang('af')}>AF</button>
      </div>
    </div>
    <div class="msgs" bind:this={box} aria-live="polite">
      {#each msgs as m}
        <div class="m {m.who}">{m.text}<time>{m.time}</time></div>
      {/each}
      {#if typing}<div class="typing"><i></i><i></i><i></i></div>{/if}
    </div>
    <div class="chips">
      {#each chips as c}
        <button type="button" onclick={c.fn}>{c.label}</button>
      {/each}
    </div>
  </div>
  <p class="note">A sample for each kind of business. Nothing here is booked for real.</p>
</div>

<style>
  .wrap { width: min(380px, 100%); margin-inline: auto; }
  .tabs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 18px; }
  .tabs button { background: none; border: 1px solid var(--line); color: var(--ink); padding: 0 14px; min-height: 38px; font: 500 0.8125rem var(--font-sans); border-radius: 999px; cursor: pointer; transition: background 0.2s, color 0.2s, border-color 0.2s; }
  .tabs button:hover { border-color: var(--ink); }
  .tabs button[aria-pressed='true'] { background: var(--ink); color: var(--bg); border-color: var(--ink); }
  .phone { height: min(540px, 72svh); min-height: 430px; background: #e6ebe7; color: #111; border-radius: 30px; overflow: hidden; display: flex; flex-direction: column; border: 6px solid #1b2620; font-size: 0.95rem; line-height: 1.4; }
  .head { background: #075e54; color: #fff; padding: 12px 14px; display: flex; align-items: center; gap: 10px; }
  .av { width: 40px; height: 40px; border-radius: 50%; background: var(--green); color: #04120a; display: grid; place-items: center; font: 600 1.2rem var(--font-display); flex: none; }
  .who { flex: 1; min-width: 0; }
  .who b { display: block; font-weight: 600; font-size: 0.95rem; }
  .who span { font-size: 0.8rem; opacity: 0.85; }
  .lang { display: flex; gap: 4px; }
  .lang button { border: 0; background: rgba(255, 255, 255, 0.18); color: #fff; padding: 0 11px; min-height: 36px; font: 600 0.8rem var(--font-sans); cursor: pointer; border-radius: 8px; }
  .lang button[aria-pressed='true'] { background: #fff; color: #075e54; }
  .msgs { flex: 1; overflow-y: auto; padding: 14px 12px; display: flex; flex-direction: column; gap: 8px; overscroll-behavior: contain; }
  .m { max-width: 82%; padding: 8px 11px; border-radius: 10px; white-space: pre-line; animation: pop 0.28s ease both; }
  .m.in { align-self: flex-start; background: #fff; border-top-left-radius: 2px; }
  .m.out { align-self: flex-end; background: #cdeed2; border-top-right-radius: 2px; }
  .m time { display: block; text-align: right; font-size: 0.68rem; color: #667; margin-top: 2px; }
  .typing { align-self: flex-start; background: #fff; padding: 10px 14px; border-radius: 10px; border-top-left-radius: 2px; display: flex; gap: 4px; }
  .typing i { width: 7px; height: 7px; border-radius: 50%; background: #99a; animation: blink 1s infinite; }
  .typing i:nth-child(2) { animation-delay: 0.15s; }
  .typing i:nth-child(3) { animation-delay: 0.3s; }
  .chips { display: flex; flex-wrap: wrap; gap: 8px; padding: 10px 12px 14px; background: #f3f2ee; min-height: 68px; }
  .chips button { min-height: 44px; padding: 0 16px; border: 0; background: #fff; color: #075e54; font: 600 0.9rem var(--font-sans); border-radius: 22px; cursor: pointer; transition: transform 0.15s, background 0.15s; }
  .chips button:hover { background: #dff5e3; transform: translateY(-2px); }
  .note { margin-top: 12px; font-size: 0.8rem; color: var(--muted); }
  @keyframes pop { from { opacity: 0; transform: translateY(8px) scale(0.98); } to { opacity: 1; transform: none; } }
  @keyframes blink { 50% { opacity: 0.25; } }
</style>
