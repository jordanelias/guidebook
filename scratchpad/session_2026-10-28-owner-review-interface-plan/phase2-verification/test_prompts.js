// Answer flow with an in-memory stand-in for the page's store. Usage: node test_prompts.js <page.html>
const { chromium } = require('playwright'); const fs = require('fs');
const P = process.argv[2];
const SQLJS = '/tmp/claude-0/-home-user-guidebook/e68b09ef-c52a-52a8-96c4-f9727206b4c9/scratchpad/sqljs-dl/sql-wasm.js';
let pass = 0, fail = 0; const ok = (c, m) => { c ? pass++ : fail++; console.log((c ? '  pass ' : '  FAIL ') + m); };
async function open(browser, seed) {
  const ctx = await browser.newContext({ viewport: { width: 400, height: 860 }, isMobile: true, hasTouch: true });
  await ctx.addInitScript((seed) => { const store = Object.assign({}, seed); window.__store = store;
    window.claude = { use: async (n) => n === 'db' ? { collection: () => ({ get: async () => ({ docs: Object.entries(store).map(([id, d]) => ({ id, data: () => d })) }) }),
      doc: (p) => ({ set: async (d) => { store[p.split('/')[1]] = JSON.parse(JSON.stringify(d)); }, delete: async () => { delete store[p.split('/')[1]]; } }) } : null }; }, seed);
  const page = await ctx.newPage(); const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); }); page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await page.route('https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.js', r => r.fulfill({ status: 200, contentType: 'application/javascript', body: fs.readFileSync(SQLJS) }));
  await page.route('https://fonts.googleapis.com/**', r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
  await page.goto('file://' + P + '#waiting'); await page.waitForSelector('html[data-ready]'); await page.waitForSelector('details.prompt');
  return { ctx, page, errs };
}
(async () => {
  const browser = await chromium.launch();
  let { ctx, page, errs } = await open(browser, {});
  const total = await page.$$eval('details.prompt', e => e.length);
  ok((await page.$eval('#answered', e => e.textContent)) === `0 of ${total} answered.`, 'starts with nothing answered and saving available');
  await page.click('#p-OR-1 > summary');
  ok(!(await page.$eval('#p-OR-1 button:has-text("Save my answer")', b => b.disabled)), 'Save is enabled when the view has a store');
  await page.click('#p-OR-1 button.opt >> nth=0');
  ok(await page.$eval('#p-OR-1 button.opt >> nth=0', b => b.getAttribute('aria-pressed')) === 'true', 'choosing an option marks it');
  ok((await page.$eval('#p-OR-1 code', c => c.textContent)).startsWith('OR-1: Yes, only the lens tags'), 'the line to send in chat names the prompt and the choice');
  await page.fill('#note-OR-1', 'Agreed, with the gap text naming the lens.');
  await page.click('#p-OR-1 button:has-text("Save my answer")'); await page.waitForFunction(() => document.querySelector('#p-OR-1 [role=status]').textContent.startsWith('Saved'));
  const doc = await page.evaluate(() => window.__store['OR-1']);
  ok(doc && doc.choice === 'yes' && doc.note === 'Agreed, with the gap text naming the lens.' && doc.prompt === 'OR-1' && /^[0-9a-f]{12}$/.test(doc.database), 'the answer is stored with choice, note, prompt id and the database stamp');
  ok((await page.$eval('#p-OR-1 .chip', c => c.textContent)).startsWith('Answered: Yes'), 'the chip shows the answer');
  ok((await page.$eval('#answered', e => e.textContent)) === `1 of ${total} answered.`, 'the count updates');
  // an option that asks for words is refused without them
  await page.click('#p-OR-9 > summary'); await page.click('#p-OR-9 button.opt >> nth=1');
  await page.click('#p-OR-9 button:has-text("Save my answer")'); await page.waitForTimeout(100);
  ok((await page.$eval('#p-OR-9 [role=status]', e => e.textContent)).includes('asks for your words') && !(await page.evaluate(() => 'OR-9' in window.__store)), 'an option that asks for words is refused without them and nothing is stored');
  // a row prompt saves under list-and-id
  const wf = 'details.prompt[id^="p-withheld_findings-"]';
  const wid = await page.$eval(wf + ' >> nth=0', e => e.id);
  await page.click(wf + ' >> nth=0 >> summary'); await page.click(wf + ' >> nth=0 >> button.opt >> nth=1');
  await page.click(wf + ' >> nth=0 >> button:has-text("Save my answer")'); await page.waitForFunction((id) => id.slice(2) in window.__store, wid);
  ok(true, 'a row prompt is stored as list-and-id (' + wid.slice(2) + ')');
  const store = await page.evaluate(() => window.__store);
  ok(errs.length === 0, 'no console errors' + (errs.length ? ': ' + errs[0] : ''));
  await ctx.close();
  // a later visit reads the saved answers back
  ({ ctx, page, errs } = await open(browser, store));
  ok((await page.$eval('#answered', e => e.textContent)) === `2 of ${total} answered.`, 'a later visit shows the saved answers');
  await page.click('#p-OR-1 > summary');
  ok(await page.$eval('#p-OR-1 button.opt >> nth=0', b => b.getAttribute('aria-pressed')) === 'true' && (await page.$eval('#note-OR-1', t => t.value)).startsWith('Agreed'), 'the saved choice and note come back');
  await page.click('#p-OR-1 button:has-text("Clear")'); await page.waitForFunction(() => !('OR-1' in window.__store));
  ok((await page.$eval('#answered', e => e.textContent)) === `1 of ${total} answered.`, 'Clear removes the answer and updates the count');
  await browser.close(); console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('TEST ERROR', e.message); process.exit(2); });
