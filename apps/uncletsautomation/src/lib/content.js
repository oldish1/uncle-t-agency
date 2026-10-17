export const WHATSAPP = 'https://wa.me/27764924196';
export const wa = (text) => `${WHATSAPP}?text=${encodeURIComponent(text)}`;

export const views = [
  { id: 'home', label: 'Home', theme: 'dark', bg: '#0a0f0c' },
  { id: 'studio', label: 'Studio', theme: 'light', bg: '#f1eee7' },
  { id: 'start', label: 'Start', theme: 'dark', bg: '#0a0f0c' }
];

export const verticals = [
  'Hair salons', 'Dog groomers', 'Plumbers', 'Nail techs', 'Driving schools', 'Cake bakers', 'Spas', 'Mobile detailers'
];

/* interactive chat */
export const BIZ = {
  salon: { label: 'Salon', name: { en: 'Sample Hair Salon', af: 'Voorbeeld Haarsalon' }, svc: { en: ['Wash & blowdry', 'Braids', 'Nanoplastia'], af: ['Was en blaas', 'Vlegwerk', 'Nanoplastia'] } },
  groomer: { label: 'Dog groomer', name: { en: 'Sample Dog Groomer', af: 'Voorbeeld Hondesalon' }, svc: { en: ['Full groom', 'Bath & brush', 'Nail trim'], af: ['Volle versorging', 'Bad en borsel', 'Naels sny'] } },
  plumber: { label: 'Plumber', name: { en: 'Sample Plumber', af: 'Voorbeeld Loodgieter' }, svc: { en: ['Leaking geyser', 'Blocked drain', 'Quote visit'], af: ['Lekkende geyser', 'Verstopte dreinering', 'Kwotasie-besoek'] } },
  nails: { label: 'Nail studio', name: { en: 'Sample Nail Studio', af: 'Voorbeeld Naelstudio' }, svc: { en: ['Gel nails', 'Pedicure', 'Fill-in'], af: ['Jel-naels', 'Pedikuur', 'Aanvulling'] } }
};

export const T = {
  en: {
    hi: (n) => `Hi! Welcome to ${n}. What can I book for you?`,
    day: 'Lovely. Which day suits you?', time: 'And what time?',
    done: (s, d, t) => `Booked: ${s}, ${d} at ${t}.\nI've put it in the calendar and I'll send you a reminder the day before.`,
    ask: 'Need to change it?', chg: ['Different day', 'Cancel it', 'Start again'],
    cancel: "Done, it's cancelled. Send me a hi any time you want to book again.",
    again: "No problem, let's pick a different day.", tomorrow: 'Tomorrow', hdr: 'Booking assistant (sample)', times: ['09:00', '11:30', '14:00'], loc: 'en-ZA'
  },
  af: {
    hi: (n) => `Hi! Welkom by ${n}. Waarmee kan ek jou help?`,
    day: 'Lekker. Watter dag pas jou?', time: 'En watter tyd?',
    done: (s, d, t) => `Geboek: ${s}, ${d} om ${t}.\nEk het dit in die kalender gesit en stuur jou die dag voor 'n herinnering.`,
    ask: 'Wil jy iets verander?', chg: ['Ander dag', 'Kanselleer', 'Begin oor'],
    cancel: "Reg, dit is gekanselleer. Stuur net 'n hi as jy weer wil book.",
    again: 'Geen probleem nie, kom ons kies \'n ander dag.', tomorrow: 'Môre', hdr: 'Besprekingsassistent (voorbeeld)', times: ['09:00', '11:30', '14:00'], loc: 'af-ZA'
  }
};

export const capabilities = [
  ['She answers when you can\'t.', 'A customer messages your own WhatsApp number at 9pm asking for a Saturday slot. Lexi replies in seconds, lists your services and takes the day and time.'],
  ['Nothing double-books.', 'She checks your Google Calendar live before she confirms, so two people never land on the same slot.'],
  ['Fewer no-shows.', 'Every client gets a WhatsApp reminder the day before. Cancel and reschedule work in the same chat, and Lexi offers a different date before she cancels.'],
  ['A website that matches.', 'One fast page with your services, your suburb, a map and a WhatsApp button. Hosting and your domain are included in the monthly fee.']
];

export const plans = [
  { id: 'both', hot: true, name: 'Lexi and a website', who: 'The full set: she books on WhatsApp, the site brings customers to her.',
    incl: 'Everything in Lexi, plus a fast website for phones with your services, suburb and a map. Hosting and your domain are included.',
    price: 'R999', per: 'a month, after R1,499 once-off setup', cta: 'Get both', msg: "Hi Theo, I'd like Lexi and a website for my business" },
  { id: 'lexi', name: 'Lexi', who: 'For salons, spas, groomers and trades who take bookings on WhatsApp.',
    incl: 'Setup, calendar connection, day-before reminders, cancel and reschedule, and ongoing support.',
    price: 'R799', per: 'a month, after R1,499 once-off setup', cta: 'Get Lexi', msg: "Hi Theo, I'd like Lexi for my business" },
  { id: 'site', name: 'A website', who: 'One fast page that shows up on Google and sends customers to your WhatsApp.',
    incl: 'Built for phones, with your services, suburb and a map. Hosting and your domain are included in the monthly fee.',
    price: 'R499', per: 'a month, after R799 once-off setup', cta: 'Get a website', msg: "Hi Theo, I'd like a website for my business" }
];

export const theo = [
  "I'm Theo, Uncle T to most people. I'm from Cape Town, I speak English and Afrikaans, and I'm learning Xhosa. By day I'm a boilermaker and sheet metal worker. At night I build WhatsApp receptionists for small businesses that lose bookings because the owner is busy working.",
  'I come to you, I set Lexi up on your own number, and when something needs fixing you message me, not a ticket system. The prices are ones a small business can carry.'
];

export const steps = [
  ['We set up Lexi on your number.', 'You tell us your services, prices and hours. We write her greeting in your voice.'],
  ['We connect your calendar.', "Your Google Calendar becomes the single source of truth for what's free."],
  ['We test it with you.', 'You book, cancel and reschedule as a customer until it feels right.'],
  ['You go live.', 'Customers book while you cut, braid or fit pipes. We keep it running.']
];

export const places = ['Bellville', 'Parow', 'Goodwood', "Mitchell's Plain", 'Cape Town'];

export const faq = [
  ['Is it a chatbot?', "She's a receptionist who talks like a person, not like a phone menu. Customers tap a service, a day and a time, or just type."],
  ['Does it use my own WhatsApp number?', 'Yes, your WhatsApp Business number, so customers keep messaging the number they already know.'],
  ['What if two people want the same slot?', 'Lexi checks your calendar before she confirms. The second person gets offered another time.'],
  ['Can she speak Afrikaans?', 'Lexi runs on Claude, which reads and writes Afrikaans. We test your own greeting in the language you want before you go live.'],
  ['How long until it works?', 'About four days from the day you say yes.'],
  ['Is there a contract?', 'No. You pay the setup once, then the monthly fee, and you can cancel any time.'],
  ['Who am I dealing with?', 'Theo, a Cape Town local who builds and supports every setup himself. You message him on WhatsApp, not a call centre.'],
  ["What happens to my customers' details?", "They're used to make bookings and nothing else. The privacy policy has the detail."]
];

export const skies = [
  { label: 'dawn', time: '6:10 am', text: 'Booked: blow-dry, Saturday 09:00. I will remind you on Friday.', alt: 'Table Mountain at dawn',
    sky: '#c97b5f', glow: '#e9b48a', sun: [200, 262, 34], sunColor: '#f6dba8', far: '#0b3f33', near: '#06251d' },
  { label: 'midday', time: '12:40 pm', text: 'Blocked drain quote: Thursday 14:00 is free. Shall I book it?', alt: 'Table Mountain at midday',
    sky: '#5aa6cf', glow: '#a9d4e8', sun: [88, 90, 30], sunColor: '#fff6d6', far: '#0b4a3b', near: '#06301f' },
  { label: 'dusk', time: '9:05 pm', text: 'Thursday 11:30 is yours. Confirmed, with a reminder on Wednesday.', alt: 'Table Mountain at dusk', stars: true,
    sky: '#16213f', glow: '#7a4a5e', sun: [310, 120, 22], sunColor: '#e9e4d4', far: '#071a15', near: '#030d0a' }
];

export const stats = [
  ['24/7', 'She answers, even when you are closed.'],
  ['4 days', 'From saying yes to being live.'],
  ['2 to 5 sec', 'Per reply in the live build.']
];
