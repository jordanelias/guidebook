#!/usr/bin/env node
/*
 * render_audit.js — assert, in a real browser, the properties of the rendered
 * documents that static analysis cannot decide.
 *
 * WHY A BROWSER (session 2026-07-24/25). The Python gate beside this file,
 * check_rendered_docs.py, reads HTML and CSS as text. Text cannot resolve the
 * cascade, cannot see an external stylesheet, and cannot tell what a reader with
 * JavaScript disabled actually gets. Both failure directions were hit for real in
 * one session:
 *
 *   - a print stylesheet hid every source, tier, caveat and disclaimer, and the
 *     page looked perfect on screen;
 *   - the first static check then FAILED three classes that a later !important
 *     rule legitimately re-showed, i.e. it overclaimed in the opposite direction.
 *
 * So the authority on "does the reader see it" is the renderer. This script is
 * that authority. check_rendered_docs.py invokes it when node and playwright are
 * present and reports SKIP, loudly, when they are not.
 *
 * Checks, per document:
 *   R1 print       — sources, tiers, caveats and the colophon survive @media print
 *   R2 no-JS       — every source panel is reachable with JavaScript disabled
 *   R3 reflow      — no horizontal scroll at 320 px, at 1280 px, or under the
 *                    WCAG 1.4.12 text-spacing override
 *   R4 target size — interactive controls meet WCAG 2.2 2.5.8 (24x24 CSS px)
 *   R5 focus       — no focused control is hidden behind a sticky bar (2.4.11)
 *   R6 shell       — doctype, html lang, charset, viewport, title (3.1.1 / 2.4.2)
 *
 * Usage:  node scripts/audit/render_audit.js [doc.html ...]     (default: specs/*.html)
 * Exit 1 on any FAIL. Prints one RESULTS: line, matching house convention.
 */
'use strict';
const fs = require('fs');
const path = require('path');

const REPO = path.resolve(__dirname, '..', '..');

let chromium;
try {
  ({ chromium } = require('playwright'));
} catch (e) {
  try {
    ({ chromium } = require('/opt/node22/lib/node_modules/playwright'));
  } catch (e2) {
    console.error('render_audit: playwright not available — cannot run browser checks.');
    process.exit(2); // 2 = could not run, distinct from 1 = failed
  }
}

// Classes carrying the evidential apparatus. If a document renders citations at
// all, a printed copy must still carry these.
const PRINT_REQUIRED = ['.pop', '.cite, .cite-trigger', '.colophon', '.s-meta', '.honesty'];

const findings = [];
const fail = (check, doc, msg) => findings.push(['FAIL', check, doc, msg]);
const warn = (check, doc, msg) => findings.push(['WARN', check, doc, msg]);

async function auditDoc(browser, file) {
  const doc = path.relative(REPO, file);
  const url = 'file://' + file;
  let checksRun = 0;

  // ---------------------------------------------------------------- R2 no-JS
  {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, javaScriptEnabled: false });
    const page = await ctx.newPage();
    await page.goto(url, { waitUntil: 'load' });
    const r = await page.evaluate(() => {
      const pops = [...document.querySelectorAll('.pop')];
      const shown = pops.filter(e => getComputedStyle(e).display !== 'none');
      const refs = new Set();
      shown.forEach(e => (e.textContent.match(/REF-\d{5}/g) || []).forEach(x => refs.add(x)));
      return { total: pops.length, shown: shown.length, refs: refs.size,
               overflow: document.documentElement.scrollWidth > window.innerWidth + 1 };
    });
    if (r.total > 0 && r.shown < r.total) {
      fail('R2-nojs', doc,
        `${r.total - r.shown} of ${r.total} source panels are unreachable without JavaScript — ` +
        `provenance is script-contingent`);
    }
    if (r.total > 0 && r.overflow) {
      fail('R2-nojs', doc, 'the no-JS fallback introduces horizontal scrolling');
    }
    checksRun++;
    await ctx.close();
  }

  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const pageErrors = [];
  page.on('pageerror', e => pageErrors.push(e.message));
  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(250);
  if (pageErrors.length) fail('R0-script', doc, `uncaught script error: ${pageErrors[0].slice(0, 160)}`);

  // ---------------------------------------------------------- R6 document shell
  // A document meant to be shared is opened from disk, on someone else's machine,
  // possibly on a phone. Without a doctype it renders in quirks mode; without lang
  // a screen reader picks the wrong voice (WCAG 3.1.1, Level A); without a declared
  // charset the em dashes and the ● ◐ ○ marks depend on sniffing; without a viewport
  // meta a phone lays the page out at 980 px and zooms out, so every bit of reflow
  // work stops short of the device that needs it most. All four are invisible in a
  // desktop browser, which is why this is a check and not a glance.
  {
    const r = await page.evaluate(() => ({
      quirks: document.compatMode === 'BackCompat',
      lang: document.documentElement.lang || null,
      charsetDeclared: !!document.querySelector('meta[charset], meta[http-equiv="Content-Type"]'),
      viewport: !!document.querySelector('meta[name="viewport"]'),
      title: (document.title || '').trim(),
    }));
    if (r.quirks) fail('R6-shell', doc, 'no doctype — the page renders in quirks mode');
    if (!r.lang) fail('R6-shell', doc, 'no lang on <html> — WCAG 3.1.1 (Level A); a screen reader picks the wrong voice');
    if (!r.charsetDeclared) fail('R6-shell', doc, 'no declared charset — non-ASCII text depends on the browser sniffing correctly');
    if (!r.viewport) fail('R6-shell', doc, 'no viewport meta — a phone lays the page out at 980px and zooms out');
    if (!r.title) fail('R6-shell', doc, 'no <title> — WCAG 2.4.2 (Level A)');
    checksRun++;
  }

  // ---------------------------------------------------------------- R1 print
  {
    await page.emulateMedia({ media: 'print' });
    await page.waitForTimeout(120);
    const r = await page.evaluate(sels => {
      const out = {};
      for (const sel of sels) {
        const els = [...document.querySelectorAll(sel)];
        out[sel] = { total: els.length, shown: els.filter(e => getComputedStyle(e).display !== 'none').length };
      }
      return out;
    }, PRINT_REQUIRED);
    for (const [sel, v] of Object.entries(r)) {
      if (v.total && v.shown < v.total) {
        fail('R1-print', doc,
          `${sel}: ${v.total - v.shown} of ${v.total} hidden under @media print — ` +
          `a printed copy loses sources, tiers, caveats or the disclaimer`);
      }
    }
    await page.emulateMedia({ media: 'screen' });
    checksRun++;
  }

  // --------------------------------------------------------------- R3 reflow
  {
    const widths = [320, 768, 1280];
    for (const w of widths) {
      await page.setViewportSize({ width: w, height: 900 });
      await page.waitForTimeout(150);
      const over = await page.evaluate(() => {
        const doc = document.documentElement;
        if (doc.scrollWidth <= window.innerWidth + 1) return null;
        const wide = [...document.querySelectorAll('*')]
          .filter(e => {
            const b = e.getBoundingClientRect();
            if (b.width === 0) return false;
            // an element inside its own scroll container is allowed to be wide
            let p = e.parentElement;
            while (p) {
              const s = getComputedStyle(p);
              if (s.overflowX === 'auto' || s.overflowX === 'scroll') return false;
              p = p.parentElement;
            }
            return b.right > window.innerWidth + 1;
          })
          .slice(0, 4)
          .map(e => e.tagName.toLowerCase() + '.' + String(e.className || '').split(' ')[0]);
        return { scrollWidth: doc.scrollWidth, innerWidth: window.innerWidth, wide };
      });
      if (over) {
        fail('R3-reflow', doc,
          `horizontal scrolling at ${w}px (content ${over.scrollWidth}px) — WCAG 1.4.10; ` +
          `widest: ${over.wide.join(', ') || 'unattributed'}`);
      }
    }
    // 1.4.12 text spacing
    await page.setViewportSize({ width: 1280, height: 900 });
    const styleTag = await page.addStyleTag({
      content: `* { line-height:1.5 !important; letter-spacing:0.12em !important;
                    word-spacing:0.16em !important; } p { margin-bottom:2em !important; }`,
    });
    await page.waitForTimeout(200);
    const spacingOver = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    if (spacingOver) fail('R3-reflow', doc, 'the WCAG 1.4.12 text-spacing override causes horizontal scrolling');
    await page.evaluate(el => el.remove(), styleTag);
    checksRun++;
  }

  // ---------------------------------------------------------- R4 target size
  {
    await page.waitForTimeout(120);
    const small = await page.evaluate(() => {
      const out = [];
      document.querySelectorAll('button, a[href], summary, select, input, [tabindex]:not([tabindex="-1"])').forEach(e => {
        let b = e.getBoundingClientRect();
        if (b.width === 0 && b.height === 0) return;          // not rendered
        if (getComputedStyle(e).display === 'none') return;
        if (e.closest('p, li, dd, td, span.prose')) return;    // 2.5.8 inline exception
        // A control wrapped in (or labelled by) a <label> is activated by the whole
        // label, so the label is the target — this is how a 13x13 UA checkbox inside
        // a padded chip legitimately meets 2.5.8.
        const lab = e.closest('label') ||
                    (e.id ? document.querySelector(`label[for="${CSS.escape(e.id)}"]`) : null);
        if (lab) b = lab.getBoundingClientRect();
        if (b.width < 24 || b.height < 24) {
          out.push({ el: e.tagName.toLowerCase() + '.' + String(e.className || '').split(' ')[0],
                     w: +b.width.toFixed(1), h: +b.height.toFixed(1) });
        }
      });
      return out;
    });
    for (const s of small.slice(0, 6)) {
      fail('R4-target', doc, `${s.el} is ${s.w}x${s.h} CSS px, under the 24x24 minimum (WCAG 2.2 2.5.8)`);
    }
    if (small.length > 6) warn('R4-target', doc, `${small.length - 6} further undersized controls not listed`);
    checksRun++;
  }

  // ------------------------------------------------------ R5 focus not hidden
  {
    await page.evaluate(() => window.scrollTo(0, 0));
    const obscured = [];
    for (let i = 0; i < 30; i++) {
      await page.keyboard.press('Tab');
      const info = await page.evaluate(() => {
        const a = document.activeElement;
        if (!a || a === document.body) return null;
        const b = a.getBoundingClientRect();
        let coverBottom = 0, coverName = null;
        document.querySelectorAll('*').forEach(e => {
          const s = getComputedStyle(e);
          if (s.position !== 'fixed' && s.position !== 'sticky') return;
          if (s.display === 'none' || s.visibility === 'hidden') return;
          // A control inside the sticky bar is not obscured BY the sticky bar.
          if (e.contains(a)) return;
          const r = e.getBoundingClientRect();
          if (r.top <= 0 && r.bottom > coverBottom && r.width > window.innerWidth * 0.5) {
            coverBottom = r.bottom; coverName = e.tagName.toLowerCase() + '.' + String(e.className || '').split(' ')[0];
          }
        });
        const hidden = coverBottom > 0 && b.top < coverBottom && b.bottom > 0;
        const st = getComputedStyle(a);
        return { el: a.tagName.toLowerCase() + '.' + String(a.className || '').split(' ')[0],
                 hidden, coverName,
                 noOutline: st.outlineStyle === 'none' && !st.boxShadow.includes('rgb') };
      });
      if (info && info.hidden) obscured.push(`${info.el} behind ${info.coverName}`);
      if (info && info.noOutline) warn('R5-focus', doc, `${info.el} has no visible focus indicator`);
    }
    for (const o of [...new Set(obscured)].slice(0, 4)) {
      fail('R5-focus', doc, `focused ${o} — the focused control is obscured (WCAG 2.2 2.4.11)`);
    }
    checksRun++;
  }

  await ctx.close();
  return checksRun;
}

(async () => {
  let docs = process.argv.slice(2).map(d => path.resolve(REPO, d));
  if (!docs.length) {
    const dir = path.join(REPO, 'specs');
    docs = fs.existsSync(dir)
      ? fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort().map(f => path.join(dir, f))
      : [];
  }
  docs = docs.filter(d => fs.existsSync(d));
  if (!docs.length) { console.log('No rendered documents found under specs/.'); process.exit(0); }

  const browser = await chromium.launch();
  let total = 0;
  for (const d of docs) total += await auditDoc(browser, d);
  await browser.close();

  const fails = findings.filter(f => f[0] === 'FAIL');
  const warns = findings.filter(f => f[0] === 'WARN');
  const seen = new Set();
  for (const [sev, check, doc, msg] of findings) {
    const k = sev + check + doc + msg;
    if (seen.has(k)) continue;
    seen.add(k);
    console.log(`  [${sev}] ${check.padEnd(12)} ${doc}: ${msg}`);
  }
  // A check is one (family x document) pair; several findings can share one.
  const failedChecks = new Set(fails.map(f => f[1] + '|' + f[2])).size;
  console.log(`\nRESULTS: ${total - failedChecks}/${total} checks passed ` +
              `(${docs.length} document(s), ${fails.length} failure(s), ${warns.length} warning(s))`);
  process.exit(fails.length ? 1 : 0);
})().catch(e => {
  // Exit 3, NOT 2. Exit 2 is claimed above for "playwright is not installed here",
  // and the runner maps 2 to SKIP for this check. Reusing it for an uncaught error
  // meant a genuinely broken audit — a bug, a changed DOM, a missing module —
  // reported as "no browser available" and was indistinguishable from a legitimate
  // skip. A crash must not be able to disguise itself as an absent environment.
  console.error('render_audit: CRASHED (not a clean skip) — ' + (e && e.stack || e));
  process.exit(3);
});
