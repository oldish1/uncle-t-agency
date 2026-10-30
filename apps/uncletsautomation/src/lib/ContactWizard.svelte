<script>
  import { wa } from '$lib/content.js';

  const types = ['Hair salon', 'Dog groomer', 'Plumber', 'Nail studio', 'Driving school', 'Bakery', 'Spa', 'Something else'];
  const needs = [['Lexi on WhatsApp', 'Lexi'], ['A website', 'a website'], ['Both', 'Lexi and a website']];

  let step = $state(0);
  let biz = $state('');
  let other = $state('');
  let need = $state('');
  let name = $state('');
  let suburb = $state('');
  const total = 4;

  const bizName = $derived(biz === 'Something else' ? other.trim() || 'small business' : biz.toLowerCase());
  const who = $derived(name.trim() || '');
  const art = (t) => (/^[aeiou]/.test(t) ? 'an ' : 'a ') + t;
  const trade = ['plumber', 'dog groomer'];
  const what = $derived(!bizName ? 'run a small business' : trade.includes(bizName) ? 'am ' + art(bizName) : 'run ' + art(bizName));
  const msg = $derived(
    `Hi Theo${who ? ", it's " + who : ''}. I ${what}${suburb.trim() ? ' in ' + suburb.trim() : ''}${need ? ` and I'd like ${need} for my business.` : ' and I would like to see how Lexi could help.'}`
  );

  const next = () => { if (step < total) step++; };
  const back = () => { if (step > 0) step--; };
  const pickBiz = (t) => { biz = t; if (t !== 'Something else') next(); };
  const pickNeed = (n) => { need = n; next(); };
  function send(e) { e.preventDefault(); window.open(wa(msg), '_blank', 'noopener'); }
</script>

<div class="wiz">
  <div class="left">
    <div class="prog" role="progressbar" aria-valuemin="0" aria-valuemax={total} aria-valuenow={step}>
      <i style="width:{(step / total) * 100}%"></i>
    </div>
    <p class="count">{step < total ? `Question ${step + 1} of ${total}` : 'Ready to send'}</p>

    {#key step}
      <div class="q">
        {#if step === 0}
          <h3>What kind of business do you run?</h3>
          <div class="chips">
            {#each types as t}<button type="button" class:on={biz === t} onclick={() => pickBiz(t)}>{t}</button>{/each}
          </div>
          {#if biz === 'Something else'}
            <div class="row"><input type="text" placeholder="e.g. tattoo studio" bind:value={other} aria-label="Your business type" /><button class="go" type="button" onclick={next} disabled={!other.trim()}>Next</button></div>
          {/if}
        {:else if step === 1}
          <h3>Nice, {bizName === 'small business' ? 'a small business' : /^[aeiou]/.test(bizName) ? 'an ' + bizName : 'a ' + bizName}. What do you need?</h3>
          <div class="chips">
            {#each needs as [label, v]}<button type="button" class:on={need === v} onclick={() => pickNeed(v)}>{label}</button>{/each}
          </div>
        {:else if step === 2}
          <h3>Which suburb are you in?</h3>
          <p class="why">So Theo knows if he can come to you in person.</p>
          <div class="row"><input type="text" placeholder="e.g. Parow" bind:value={suburb} aria-label="Your suburb" /><button class="go" type="button" onclick={next}>Next</button></div>
        {:else if step === 3}
          <h3>And your first name?</h3>
          <p class="why">So Theo can say hello properly.</p>
          <div class="row"><input type="text" placeholder="e.g. Chanté" bind:value={name} aria-label="Your first name" autocomplete="given-name" /><button class="go" type="button" onclick={next}>Next</button></div>
        {:else}
          <h3>All set{who ? ', ' + who : ''}.</h3>
          <p class="why">This opens WhatsApp with your message ready. Theo replies himself.</p>
          <form onsubmit={send}><button class="send" type="submit">Send to Theo on WhatsApp</button></form>
        {/if}
      </div>
    {/key}

    {#if step > 0}<button class="back" type="button" onclick={back}>Back</button>{/if}
  </div>

  <div class="right" aria-live="polite">
    <div class="phone">
      <div class="head"><span class="av">T</span><div><b>Theo (Uncle T)</b><span>WhatsApp</span></div></div>
      <div class="chat">
        <p class="m out">{msg}<time>now</time></p>
      </div>
    </div>
    <p class="note">Your message, as Theo will see it.</p>
  </div>
</div>

<style>
  .wiz { display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr); gap: clamp(28px, 5vw, 80px); align-items: center; text-align: left; }
  .prog { height: 3px; background: var(--line); border-radius: 3px; overflow: hidden; }
  .prog i { display: block; height: 100%; background: var(--green); transition: width 0.5s var(--ease); }
  .count { margin-top: 12px; font-size: 0.8rem; color: var(--muted); }
  .q { margin-top: 26px; min-height: 220px; animation: in 0.5s var(--ease) both; }
  @keyframes in { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
  h3 { font-size: clamp(1.4rem, 1.1rem + 1vw, 1.9rem); max-width: 22ch; }
  .why { margin-top: 10px; color: var(--muted); font-size: 0.9rem; }
  .chips { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
  .chips button { min-height: 46px; padding: 0 20px; border-radius: 999px; border: 1px solid var(--line); background: var(--panel); color: var(--ink); font: 500 0.9rem var(--font-sans); cursor: pointer; transition: transform 0.2s var(--ease), border-color 0.2s, background 0.2s; }
  .chips button:hover { border-color: var(--green); transform: translateY(-2px); }
  .chips button.on { background: var(--green); border-color: var(--green); color: #04120a; }
  .row { display: flex; gap: 10px; margin-top: 22px; }
  input { flex: 1; min-width: 0; height: 54px; padding: 0 20px; border-radius: 999px; border: 1px solid var(--line); background: var(--panel); color: var(--ink); font: 400 1rem var(--font-sans); }
  input:focus { outline: none; border-color: var(--green); }
  .go, .send { min-height: 54px; padding: 0 26px; border-radius: 999px; border: 0; background: var(--ink); color: var(--bg); font: 500 0.95rem var(--font-sans); cursor: pointer; transition: background 0.25s, transform 0.25s var(--ease); }
  .go:hover:not(:disabled), .send:hover { background: var(--green); color: #04120a; transform: translateY(-2px); }
  .go:disabled { opacity: 0.4; cursor: default; }
  .send { margin-top: 22px; background: var(--green); color: #04120a; }
  .back { margin-top: 18px; background: none; border: 0; color: var(--muted); font: 500 0.85rem var(--font-sans); cursor: pointer; padding: 6px 0; }
  .back:hover { color: var(--ink); }
  .phone { width: min(340px, 100%); margin-inline: auto; height: 340px; background: #e6ebe7; color: #111; border-radius: 26px; overflow: hidden; display: flex; flex-direction: column; border: 6px solid #1c2721; }
  .head { background: #075e54; color: #fff; padding: 11px 13px; display: flex; align-items: center; gap: 10px; }
  .av { width: 36px; height: 36px; border-radius: 50%; background: var(--green); color: #04120a; display: grid; place-items: center; font: 600 1rem var(--font-display); }
  .head b { display: block; font-size: 0.9rem; font-weight: 600; }
  .head span:not(.av) { font-size: 0.75rem; opacity: 0.85; }
  .chat { flex: 1; padding: 16px 12px; display: flex; flex-direction: column; justify-content: flex-end; }
  .m { align-self: flex-end; max-width: 88%; background: #cdeed2; padding: 9px 12px; border-radius: 10px; border-top-right-radius: 2px; font-size: 0.9rem; line-height: 1.4; margin: 0; }
  .m time { display: block; text-align: right; font-size: 0.68rem; color: #667; margin-top: 2px; }
  .note { margin-top: 12px; text-align: center; font-size: 0.8rem; color: var(--muted); }
  @media (max-width: 900px) { .wiz { grid-template-columns: minmax(0, 1fr); } .row { flex-direction: column; } .go { width: 100%; } .q { min-height: 0; } }
  @media (prefers-reduced-motion: reduce) { .q { animation: none; } }
</style>
