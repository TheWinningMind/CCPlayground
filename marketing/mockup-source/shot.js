const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const [dir, mode, w, h, out] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +w, height: +h }, deviceScaleFactor: 2 });
  await p.goto(`file://${dir}/scene.html?mode=${mode}&sw=${w}&sh=${h}`, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: out }); await b.close();
})();
