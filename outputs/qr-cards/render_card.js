// Renders chales-card.html to front/back PNGs and a print PDF (90 x 55 mm).
const { chromium } = require('playwright');
const dir = __dirname;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 340, height: 208 }, deviceScaleFactor: 8 });
  await p.goto('file://' + dir + '/chales-card.html');
  await p.waitForTimeout(2500);
  await p.evaluate(() => document.fonts.ready);
  const cards = await p.$$('.card');
  await cards[0].screenshot({ path: dir + '/chales-card-front.png' });
  await cards[1].screenshot({ path: dir + '/chales-card-back.png' });
  await p.pdf({ path: dir + '/chales-card-print.pdf', width: '90mm', height: '55mm', printBackground: true });
  console.log(await p.evaluate(() => [...document.fonts].map(f => f.family + ':' + f.status).join(', ')));
  await b.close();
})();
