#!/usr/bin/env node
"use strict";
/* Browser-free regression tests for Gallery history and Contact email localization. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const WEBSITE = path.resolve(__dirname, "../website_src");
const SLOTS = ["SOURCE", "P1", "P2", "E1", "E2"];

function fakeElement() {
  return {
    dataset: {}, style: {}, open: false, textContent: "",
    classList: { add() {}, remove() {}, toggle() {} },
    children: [],
    appendChild(child) { this.children.push(child); return child; },
    replaceChildren(...children) { this.children = children; },
    addEventListener() {}, setAttribute() {}, removeAttribute() {},
    focus() {}, showModal() { this.open = true; }, close() { this.open = false; }
  };
}

function browser(url) {
  let href = url;
  let entries = [{ href, state: null }];
  let index = 0;
  const counters = { pushes: 0, replaces: 0, backs: 0 };
  const elements = new Map();
  const get = selector => {
    if (!elements.has(selector)) elements.set(selector, fakeElement());
    return elements.get(selector);
  };
  const location = {
    get href() { return href; },
    get search() { return new URL(href).search; }
  };
  const history = {
    get state() { return entries[index].state; },
    pushState(state, _title, urlValue) {
      href = new URL(urlValue, href).href;
      entries = entries.slice(0, index + 1);
      entries.push({ href, state });
      index++;
      counters.pushes++;
    },
    replaceState(state, _title, urlValue) {
      href = new URL(urlValue, href).href;
      entries[index] = { href, state };
      counters.replaces++;
    },
    back() {
      assert.ok(index > 0, "Cannot navigate back without a prior entry");
      index--;
      href = entries[index].href;
      counters.backs++;
    }
  };
  const document = {
    body: { style: {}, dataset: { page: "contact" } },
    documentElement: { dataset: {} },
    querySelector: get, querySelectorAll: () => [],
    createElement: () => fakeElement()
  };
  const context = vm.createContext({
    URL, URLSearchParams, location, history, document,
    localStorage: { getItem: () => null, setItem() {} },
    console, setTimeout, clearTimeout
  });
  return { context, counters, elements, history, get href() { return href; } };
}

function loadViewer(env) {
  const source = fs.readFileSync(path.join(WEBSITE, "app.js"), "utf8");
  assert.match(source, /\binit\(\);\s*$/, "Gallery bootstrap must remain at the file end");
  vm.runInContext(source.replace(/\binit\(\);\s*$/, ""), env.context, { filename: "app.js" });
  vm.runInContext(
    "state.catalog = ['CORE:0001','CORE:0002'].map(id => ({id, collection:'core', images:Object.fromEntries(SLOTS.map(slot => [slot, {thumb:'/thumb.webp',preview:'/preview.webp'}]))})); state.filteredFamilies = state.catalog;",
    env.context
  );
}
function evalIn(env, code) { return vm.runInContext(code, env.context); }

function testViewerHistory() {
  const env = browser("https://example.test/index.html?lang=vi");
  loadViewer(env);
  evalIn(env, "openDetail('CORE:0001', 'SOURCE')");
  assert.equal(env.counters.pushes, 1, "Opening viewer adds one history entry");
  assert.equal(env.counters.replaces, 0, "Opening viewer must not replace the gallery URL first");
  assert.equal(env.history.state.compactfacesViewer, true);
  assert.match(env.href, /id=CORE%3A0001/);

  evalIn(env, "setDetailSlot('P1')");
  assert.equal(env.counters.pushes, 1, "Changing view must not create an extra entry");
  assert.equal(env.counters.replaces, 1);
  assert.match(env.href, /slot=P1/);

  evalIn(env, "openDetail('CORE:0002', 'E1')");
  assert.equal(env.counters.pushes, 1, "Changing identity in viewer must not create an extra entry");
  assert.equal(env.counters.replaces, 2);
  assert.match(env.href, /id=CORE%3A0002/);

  evalIn(env, "closeDetail()");
  assert.equal(env.counters.backs, 1, "Closing a viewer opened in-gallery returns to gallery history");
  assert.equal(env.href, "https://example.test/index.html?lang=vi");
  assert.equal(env.history.state, null);
}
function testDirectLink() {
  const env = browser("https://example.test/index.html?id=CORE%3A0001&slot=P1&lang=vi");
  loadViewer(env);
  evalIn(env, "openDetail('CORE:0001', 'P1', true)");
  assert.equal(env.counters.pushes, 0);
  assert.equal(env.counters.replaces, 0, "Opening a deep link must not write duplicate history");
  evalIn(env, "closeDetail()");
  assert.equal(env.counters.backs, 0, "Deep links must not navigate away from their initial history entry");
  assert.equal(env.counters.replaces, 1);
  assert.equal(env.href, "https://example.test/index.html?lang=vi");
}

function loadContact(env) {
  const source = fs.readFileSync(path.join(WEBSITE, "pages.js"), "utf8");
  const boot = "\ndocument.documentElement.dataset.theme=theme;";
  const index = source.indexOf(boot);
  assert.ok(index > 0, "Contact script bootstrap must be present");
  vm.runInContext(source.slice(0, index), env.context, { filename: "pages.js" });
  env.elements.set("#identityInput", { value: "CORE:0106" });
  env.elements.set("#slotInput", { value: "P1" });
  env.elements.set("#replyInput", { value: "" });
  env.elements.set("#reasonInput", { selectedIndex: 0, options: [{ textContent: "Example reason" }] });
  env.elements.set("#detailInput", { value: "" });
}
function testLocalizedContact() {
  const vi = browser("https://example.test/contact.html?lang=vi");
  loadContact(vi);
  const viText = evalIn(vi, "buildEmailText()");
  assert.match(viText, /Mã danh tính: CORE:0106/);
  assert.match(viText, /Liên kết gallery: https:\/\/example\.test\/index\.html\?id=CORE%3A0106&slot=P1&lang=vi/);
  assert.match(viText, /Không có thông tin bổ sung/);
  assert.doesNotMatch(viText, /Please review this request/);
  const en = browser("https://example.test/contact.html?lang=en");
  loadContact(en);
  const enText = evalIn(en, "buildEmailText()");
  assert.match(enText, /Identity: CORE:0106/);
  assert.match(enText, /Gallery reference: https:\/\/example\.test\/index\.html\?id=CORE%3A0106&slot=P1&lang=en/);
  assert.match(enText, /Please review this request and advise on next steps/);
  assert.doesNotMatch(enText, /Vui lòng xem xét yêu cầu/);
}

testViewerHistory();
testDirectLink();
testLocalizedContact();
console.log("PASS: Gallery navigation (open, slot, family, close, deep link) and bilingual Contact request text");
