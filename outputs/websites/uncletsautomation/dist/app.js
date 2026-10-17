(function(){
  document.documentElement.classList.add('js');
  var rv=[].slice.call(document.querySelectorAll('.rv'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
    rv.forEach(function(el){io.observe(el)});
  }else rv.forEach(function(el){el.classList.add('in')});

  /* sample booking chat */
  var T={
    en:{
      hi:"Hi! Welcome to Chales Hair Boutique. What can I book for you?",
      svc:["Wash & blowdry","Braids","Nanoplastia"],
      day:"Lovely. Which day suits you?",
      time:"And what time?",
      done:function(s,d,t){return "Booked: "+s+", "+d+" at "+t+".\nI've put it in Chanté's calendar and I'll send you a reminder the day before."},
      ask:"Need to change it?",
      chg:["Different day","Cancel it","Start again"],
      cancel:"Done, it's cancelled. Send me a hi any time you want to book again.",
      again:"No problem, let's pick a different day.",
      today:"Tomorrow",hdr:"Booking assistant (sample)",
      times:["09:00","11:30","14:00"]
    },
    af:{
      hi:"Hi! Welkom by Chales Hair Boutique. Waarmee kan ek jou help?",
      svc:["Was en blaas","Vlegwerk","Nanoplastia"],
      day:"Lekker. Watter dag pas jou?",
      time:"En watter tyd?",
      done:function(s,d,t){return "Geboek: "+s+", "+d+" om "+t+".\nEk het dit in Chanté se kalender gesit en stuur jou die dag voor 'n herinnering."},
      ask:"Wil jy iets verander?",
      chg:["Ander dag","Kanselleer","Begin oor"],
      cancel:"Reg, dit is gekanselleer. Stuur net 'n hi as jy weer wil book.",
      again:"Geen probleem nie, kom ons kies 'n ander dag.",
      today:"Môre",hdr:"Besprekingsassistent (voorbeeld)",
      times:["09:00","11:30","14:00"]
    }
  };
  var lang='en',svc='',day='',msgs=document.getElementById('msgs'),chips=document.getElementById('chips'),busy=false,gen=0;
  if(!msgs)return;
  function now(){var d=new Date();return d.toLocaleTimeString('en-ZA',{hour:'2-digit',minute:'2-digit',timeZone:'Africa/Johannesburg'})}
  function bubble(t,who){var m=document.createElement('div');m.className='m '+who;m.textContent=t;var ti=document.createElement('time');ti.textContent=now();m.appendChild(ti);msgs.appendChild(m);msgs.scrollTop=msgs.scrollHeight}
  function typing(ms,cb){var my=gen,t=document.createElement('div');t.className='typing';t.innerHTML='<i></i><i></i><i></i>';msgs.appendChild(t);msgs.scrollTop=msgs.scrollHeight;chips.innerHTML='';
    setTimeout(function(){if(my!==gen)return;t.remove();cb()},ms)}
  function setChips(list,fn){chips.innerHTML='';list.forEach(function(l){var b=document.createElement('button');b.type='button';b.textContent=l;b.onclick=function(){fn(l)};chips.appendChild(b)})}
  function days(){var out=[],names=lang==='en'?'en-ZA':'af-ZA',d=new Date();
    for(var i=1;out.length<3;i++){var x=new Date(d.getTime()+i*86400000);if(x.getDay()===0)continue;
      out.push(i===1?T[lang].today:x.toLocaleDateString(names,{weekday:'long',day:'numeric',month:'short',timeZone:'Africa/Johannesburg'}))}
    return out}
  function say(text,next){typing(650,function(){bubble(text,'in');next&&next()})}
  function start(){gen++;msgs.innerHTML='';chips.innerHTML='';svc=day='';
    say(T[lang].hi,function(){setChips(T[lang].svc,function(s){svc=s;bubble(s,'out');askDay()})})}
  function askDay(){say(T[lang].day,function(){setChips(days(),function(d){day=d;bubble(d,'out');askTime()})})}
  function askTime(){say(T[lang].time,function(){setChips(T[lang].times,function(t){bubble(t,'out');
    say(T[lang].done(svc,day,t),function(){say(T[lang].ask,function(){setChips(T[lang].chg,function(c){bubble(c,'out');
      var i=T[lang].chg.indexOf(c);
      if(i===0)say(T[lang].again,askDay);
      else if(i===1)say(T[lang].cancel,function(){setChips([T[lang].chg[2]],function(){start()})});
      else start();
    })})})})})}
  document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){
    lang=b.dataset.l;document.querySelectorAll('.lang button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});
    document.getElementById('phsub').textContent=T[lang].hdr;start()})});
  start();

  /* contact: opens WhatsApp with a written message */
  var f=document.getElementById('ask');
  if(f)f.addEventListener('submit',function(e){e.preventDefault();var v=document.getElementById('biz').value.trim();
    var t="Hi Theo, I run "+(v||"a small business")+" and I'd like to see how Lexi could take my bookings on WhatsApp.";
    window.open('https://wa.me/27764924196?text='+encodeURIComponent(t),'_blank','noopener')});
})();
