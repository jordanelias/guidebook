// Scratch acceptance run for the owner's browser page (Phase 2). Usage: node test_browser.js <page.html> <expected.json> [--probe]
const { chromium } = require('playwright');
const fs = require('fs');
const [page_path, exp_path] = process.argv.slice(2);
const probe = process.argv.includes('--probe');
const exp = JSON.parse(fs.readFileSync(exp_path));
const SQLJS = '/tmp/claude-0/-home-user-guidebook/e68b09ef-c52a-52a8-96c4-f9727206b4c9/scratchpad/sqljs-dl/sql-wasm.js';
let pass = 0, fail = 0;
const ok = (c, m) => { c ? pass++ : fail++; console.log((c ? '  pass ' : '  FAIL ') + m); };
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 400, height: 800 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  const errs = [];
  page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  page.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await page.route('https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.js', r => r.fulfill({ status: 200, contentType: 'application/javascript', body: fs.readFileSync(SQLJS) }));
  await page.route('https://fonts.googleapis.com/**', r => r.fulfill({ status: 200, contentType: 'text/css', body: '' }));
  await page.goto('file://' + page_path);
  await page.waitForSelector('html[data-ready]', { timeout: 60000 });
  ok(await page.evaluate(() => document.documentElement.dataset.ready) === '1', 'database opened and first screen rendered');
  const noOverflow = async (label) => ok(!(await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth)), `no horizontal overflow at 400px: ${label}`);

  // 1. table list equals the database; counts equal select count(*)
  const items = await page.$$eval('#main a.item[data-find]', els => els.map(e => [e.querySelector('.nm').textContent, e.querySelector('.n').textContent]));
  const got = Object.fromEntries(items.map(([n, c]) => [n, Number(c.replace(/[^0-9]/g, ''))]));
  const want = exp.tables;
  ok(JSON.stringify(Object.keys(got).sort()) === JSON.stringify(Object.keys(want).sort()), `table list equals sqlite_master (${Object.keys(got).length} tables)`);
  ok(Object.keys(want).every(t => got[t] === want[t]), 'every table count equals select count(*)');
  const views = await page.$$eval('a.item[href^="#v-"] .nm', els => els.map(e => e.textContent));
  ok(JSON.stringify(views.sort()) === JSON.stringify(exp.views), `view list equals sqlite_master (${views.length} views)`);
  const foot = await page.$eval('.foot', e => e.textContent);
  ok(foot.includes('Database version ' + exp.user_version) && foot.includes('sha256 ' + exp.sha12), 'stamp shows user_version and sha256 of the file');
  await noOverflow('home');
  if (probe) {
    const un = await page.$$eval('section[data-stage="unmapped"] a.item .nm', els => els.map(e => e.textContent));
    ok(un.includes('zz_probe'), 'a table added to a copy appears with no code change (listed as unmapped)');
    await browser.close(); console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
  }

  // 2. waiting page
  await page.goto('file://' + page_path + '#waiting'); await page.waitForSelector('h1');
  const qn = await page.$$eval('section.sec h2', els => els.map(e => Number(e.textContent.split('·').pop().replace(/[^0-9]/g, ''))));
  ok(JSON.stringify(qn) === JSON.stringify(exp.queue), `queue counts equal the queries (${qn.join(',')})`);
  const navLabel = await page.$eval('#nav-waiting', e => e.textContent);
  ok(navLabel.includes(String(exp.queue.reduce((a, b) => a + b, 0))), 'nav label carries the total waiting count');
  await noOverflow('waiting');
  const firstCard = await page.$('a.card'); const href = await firstCard.getAttribute('href');
  ok(/^#r-adversarial-findings-\d+$/.test(href), 'a queue row links to its row page');

  // 3. table page: cards, paging, search, sort, retired dimming
  await page.goto('file://' + page_path + '#t-source-value-extractions'); await page.waitForSelector('#rows .card');
  ok(await page.$$eval('#rows .card', e => e.length) === 40, 'table page shows 40 cards first');
  await page.click('text=/Show \\d+ more/'); await page.waitForFunction(() => document.querySelectorAll('#rows .card').length === 80);
  ok(true, 'show more extends to 80');
  await page.fill('input[type=search]', 'REF-01008'); await page.waitForTimeout(500);
  const nSearch = await page.$$eval('#rows .card', e => e.length);
  ok(nSearch > 0 && nSearch < 80, `search narrows the list (${nSearch})`);
  await noOverflow('table');

  // 4. row page and foreign-key navigation
  await page.fill('input[type=search]', ''); await page.waitForTimeout(500);
  await page.click('#rows a.card >> nth=0'); await page.waitForSelector('h1');
  ok(/^#r-source-value-extractions-\d+$/.test(await page.evaluate(() => location.hash)), 'tapping a card opens its row page');
  await noOverflow('row');
  const fk = await page.waitForSelector('.kv .v a[href^="#r-evidence-sources-"]', { timeout: 5000 }).catch(() => null);
  ok(!!fk, 'a foreign-key value is a link to the referenced row');
  if (fk) { await fk.click(); await page.waitForFunction(() => /^#r-evidence-sources-\d+$/.test(location.hash) && /^REF-/.test((document.querySelector('h1') || {}).textContent || '')); ok(/^REF-/.test(await page.$eval('h1', e => e.textContent)), 'the link opens the referenced source'); }

  // 5. pointed-to-by opens a filtered table
  const back = await page.$('a.item[href^="#t-"]');
  if (back) { await back.click(); await page.waitForSelector('#rows .card'); ok(!!(await page.$('text=/where .* = /')), 'pointed-to-by opens the table filtered to this row'); }

  // 6. vocabulary on the field note
  await page.goto('file://' + page_path + '#t-term-adjudications'); await page.waitForFunction(() => document.querySelector('h1') && document.querySelector('h1').textContent === 'term_adjudications'); await page.waitForSelector('#rows .card');
  await page.click('#rows a.card >> nth=0'); await page.waitForFunction(() => location.hash.startsWith('#r-term-adjudications-') && document.querySelector('.kv details'));
  const vocab = await page.evaluate(() => {
    for (const k of document.querySelectorAll('.kv')) if (k.querySelector('.k').textContent.startsWith('outcome')) { k.querySelector('details.fld').open = true; return [...k.querySelectorAll('.chips .chip')].map(c => c.textContent).sort(); }
    return null; });
  ok(JSON.stringify(vocab) === JSON.stringify(exp.vocab_outcome), `field note lists the column's own CHECK values (${vocab && vocab.length})`);

  // 7. a view page, the column list, and the wide table
  await page.goto('file://' + page_path + '#v-v-open-determination-gates'); await page.waitForFunction(() => document.querySelector('h1') && document.querySelector('h1').textContent === 'v_open_determination_gates');
  ok((await page.$eval('h1', e => e.textContent)) === 'v_open_determination_gates', 'a view page opens');
  await page.goto('file://' + page_path + '#t-evidence-sources'); await page.waitForFunction(() => document.querySelector('h1') && document.querySelector('h1').textContent === 'evidence_sources'); await page.waitForSelector('#rows .card');
  await page.click('summary:has-text("Columns")'); await noOverflow('wide table (97 columns), columns open');
  ok(errs.length === 0, 'no console errors' + (errs.length ? ': ' + errs.slice(0, 3).join(' | ') : ''));
  await browser.close();
  console.log(`${pass} passed, ${fail} failed`); process.exit(fail ? 1 : 0);
})().catch(e => { console.error('TEST ERROR', e.message); process.exit(2); });
