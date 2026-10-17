(function(){
  var root=document.documentElement;root.classList.add('js');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* split headlines into letters that rise */
  document.querySelectorAll('[data-split]').forEach(function(el){
    var text=el.textContent.trim(),n=0;el.setAttribute('aria-label',text);el.textContent='';
    text.split(' ').forEach(function(word,wi){
      var w=document.createElement('span');w.className='w';w.setAttribute('aria-hidden','true');
      word.split('').forEach(function(ch){var c=document.createElement('span');c.className='c';c.style.setProperty('--n',n++);c.textContent=ch;w.appendChild(c)});
      el.appendChild(w);el.appendChild(document.createTextNode(' '));
    });
  });
  var rv=[].slice.call(document.querySelectorAll('.rv,[data-split]'));
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15});
    rv.forEach(function(el){io.observe(el)});
  }else rv.forEach(function(el){el.classList.add('in')});

  /* counters */
  document.querySelectorAll('[data-count]').forEach(function(el){
    var to=+el.dataset.count,done=false;
    new IntersectionObserver(function(es,o){if(es[0].isIntersecting&&!done){done=true;o.disconnect();if(reduce)return;var t0=performance.now();
      (function tick(t){var p=Math.min(1,(t-t0)/1200);el.textContent=Math.round(to*(1-Math.pow(1-p,3)));if(p<1)requestAnimationFrame(tick)})(t0)}},{threshold:.6}).observe(el);
  });

  /* scroll effects: header, parallax, pinned gallery, magnetic buttons */
  var top=document.querySelector('.top'),pars=[].slice.call(document.querySelectorAll('[data-par]')),
      hs=document.querySelector('.hs'),track=document.querySelector('.hs-track'),ticking=false;
  function frame(){
    ticking=false;var y=window.scrollY,vh=window.innerHeight;
    top.classList.toggle('solid',y>40);
    if(!reduce){
      pars.forEach(function(el){var r=el.parentElement.getBoundingClientRect();var off=(r.top+r.height/2-vh/2)*parseFloat(el.dataset.par);el.style.transform='translate3d(0,'+off.toFixed(1)+'px,0)'});
      if(hs&&track){var r=hs.getBoundingClientRect(),span=hs.offsetHeight-vh,p=Math.max(0,Math.min(1,-r.top/span)),max=track.scrollWidth-window.innerWidth;track.style.transform='translate3d('+(-p*max).toFixed(1)+'px,0,0)'}
    }
  }
  function req(){if(!ticking){ticking=true;requestAnimationFrame(frame)}}
  window.addEventListener('scroll',req,{passive:true});window.addEventListener('resize',req);frame();
  if(!reduce&&window.matchMedia('(pointer:fine)').matches){
    document.querySelectorAll('.btn').forEach(function(b){
      b.addEventListener('mousemove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18).toFixed(1)+'px,'+((e.clientY-r.top-r.height/2)*.28).toFixed(1)+'px)'});
      b.addEventListener('mouseleave',function(){b.style.transform=''});
    });
  }

  /* sample booking chat, switchable by business type */
  var BIZ={
    salon:{name:{en:"Sample Hair Salon",af:"Voorbeeld Haarsalon"},svc:{en:["Wash & blowdry","Braids","Nanoplastia"],af:["Was en blaas","Vlegwerk","Nanoplastia"]}},
    groomer:{name:{en:"Sample Dog Groomer",af:"Voorbeeld Hondesalon"},svc:{en:["Full groom","Bath & brush","Nail trim"],af:["Volle versorging","Bad en borsel","Naels sny"]}},
    plumber:{name:{en:"Sample Plumber",af:"Voorbeeld Loodgieter"},svc:{en:["Leaking geyser","Blocked drain","Quote visit"],af:["Lekkende geyser","Verstopte dreinering","Kwotasie-besoek"]}},
    nails:{name:{en:"Sample Nail Studio",af:"Voorbeeld Naelstudio"},svc:{en:["Gel nails","Pedicure","Fill-in"],af:["Jel-naels","Pedikuur","Aanvulling"]}}
  };
  var T={
    en:{
      hi:function(n){return "Hi! Welcome to "+n+". What can I book for you?"},
      day:"Lovely. Which day suits you?",time:"And what time?",
      done:function(s,d,t){return "Booked: "+s+", "+d+" at "+t+".\nI've put it in the calendar and I'll send you a reminder the day before."},
      ask:"Need to change it?",chg:["Different day","Cancel it","Start again"],
      cancel:"Done, it's cancelled. Send me a hi any time you want to book again.",
      again:"No problem, let's pick a different day.",today:"Tomorrow",hdr:"Booking assistant (sample)",times:["09:00","11:30","14:00"]
    },
    af:{
      hi:function(n){return "Hi! Welkom by "+n+". Waarmee kan ek jou help?"},
      day:"Lekker. Watter dag pas jou?",time:"En watter tyd?",
      done:function(s,d,t){return "Geboek: "+s+", "+d+" om "+t+".\nEk het dit in die kalender gesit en stuur jou die dag voor 'n herinnering."},
      ask:"Wil jy iets verander?",chg:["Ander dag","Kanselleer","Begin oor"],
      cancel:"Reg, dit is gekanselleer. Stuur net 'n hi as jy weer wil book.",
      again:"Geen probleem nie, kom ons kies 'n ander dag.",today:"Môre",hdr:"Besprekingsassistent (voorbeeld)",times:["09:00","11:30","14:00"]
    }
  };
  var lang='en',biz='salon',svc='',day='',msgs=document.getElementById('msgs'),chips=document.getElementById('chips'),gen=0;
  if(!msgs)return;
  function now(){return new Date().toLocaleTimeString('en-ZA',{hour:'2-digit',minute:'2-digit',timeZone:'Africa/Johannesburg'})}
  function bubble(t,who){var m=document.createElement('div');m.className='m '+who;m.textContent=t;var ti=document.createElement('time');ti.textContent=now();m.appendChild(ti);msgs.appendChild(m);msgs.scrollTop=msgs.scrollHeight}
  function typing(ms,cb){var my=gen,t=document.createElement('div');t.className='typing';t.innerHTML='<i></i><i></i><i></i>';msgs.appendChild(t);msgs.scrollTop=msgs.scrollHeight;chips.innerHTML='';
    setTimeout(function(){if(my!==gen)return;t.remove();cb()},ms)}
  function setChips(list,fn){chips.innerHTML='';list.forEach(function(l){var b=document.createElement('button');b.type='button';b.textContent=l;b.onclick=function(){fn(l)};chips.appendChild(b)})}
  function days(){var out=[],loc=lang==='en'?'en-ZA':'af-ZA',d=new Date();
    for(var i=1;out.length<3;i++){var x=new Date(d.getTime()+i*86400000);if(x.getDay()===0)continue;
      out.push(i===1?T[lang].today:x.toLocaleDateString(loc,{weekday:'long',day:'numeric',month:'short',timeZone:'Africa/Johannesburg'}))}
    return out}
  function say(text,next){typing(650,function(){bubble(text,'in');next&&next()})}
  function head(){document.getElementById('phname').textContent=BIZ[biz].name[lang];document.getElementById('phsub').textContent=T[lang].hdr}
  function start(){gen++;msgs.innerHTML='';chips.innerHTML='';svc=day='';head();
    say(T[lang].hi(BIZ[biz].name[lang]),function(){setChips(BIZ[biz].svc[lang],function(s){svc=s;bubble(s,'out');askDay()})})}
  function askDay(){say(T[lang].day,function(){setChips(days(),function(d){day=d;bubble(d,'out');askTime()})})}
  function askTime(){say(T[lang].time,function(){setChips(T[lang].times,function(t){bubble(t,'out');
    say(T[lang].done(svc,day,t),function(){say(T[lang].ask,function(){setChips(T[lang].chg,function(c){bubble(c,'out');
      var i=T[lang].chg.indexOf(c);
      if(i===0)say(T[lang].again,askDay);
      else if(i===1)say(T[lang].cancel,function(){setChips([T[lang].chg[2]],function(){start()})});
      else start();
    })})})})})}
  document.querySelectorAll('.lang button').forEach(function(b){b.addEventListener('click',function(){
    lang=b.dataset.l;document.querySelectorAll('.lang button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});start()})});
  document.querySelectorAll('.biz button').forEach(function(b){b.addEventListener('click',function(){
    biz=b.dataset.b;document.querySelectorAll('.biz button').forEach(function(x){x.setAttribute('aria-pressed',x===b)});start()})});
  start();

  /* contact: opens WhatsApp with a written message */
  var f=document.getElementById('ask');
  if(f)f.addEventListener('submit',function(e){e.preventDefault();var v=document.getElementById('biz').value.trim();
    var t="Hi Theo, I run "+(v||"a small business")+" and I'd like to see how Lexi could take my bookings on WhatsApp.";
    window.open('https://wa.me/27764924196?text='+encodeURIComponent(t),'_blank','noopener')});
})();
