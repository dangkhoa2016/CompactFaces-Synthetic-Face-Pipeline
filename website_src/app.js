"use strict";
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const SLOTS = ["SOURCE", "P1", "P2", "E1", "E2"];
const translations = {
  en: {
    navExplore:"Explore",navAbout:"About",navContact:"Contact",requestRemoval:"Request removal",navAccess:"Get originals",previewStatus:"IMAGE PREVIEW",
    heroLine1:"One identity.",heroLine2:"Five perspectives.",heroBody:"An intentional collection of synthetic faces, explored through consistent identity, pose, and expression. Meet the dataset through a lighter, more thoughtful lens.",
    heroExplore:"Explore the gallery",heroLearn:"How it works",statFamilies:"identity families",statImages:"curated images",statViews:"views per family",visualCaption:"ONE FACE / MULTIPLE VIEWS",acceptedLabel:"FIVE-VIEW PORTRAITS",
    galleryKicker:"THE COLLECTION",galleryTitle:"Explore every angle.",galleryLead:"Discover identity families or browse individual images. Everything here is a lightweight preview.",
    searchPlaceholder:"Search identity e.g. 0106, AD0036…",viewFamilies:"Families",viewImages:"All images",filterAll:"All collections",filterCore:"Core",filterAdditional:"Additional",sortLabel:"Sort",sortAsc:"ID ascending",sortDesc:"ID descending",slotFilterLabel:"View",slotAll:"All five",loading:"Preparing the collection…",emptyTitle:"No matching identities.",emptyCopy:"Try another ID or remove the active filters.",resetFilters:"Clear filters",
    aboutKicker:"THOUGHTFUL BY DESIGN",aboutTitle:"A clearer way to explore.",feature1Title:"Five views. One identity.",feature1Text:"A SOURCE portrait, two poses (P1, P2), and two expressions (E1, E2), grouped for easier comparison.",feature2Title:"Designed to load lighter.",feature2Text:"400px thumbnails, 768px detail previews, WebP compression, and lazy loading. Original 1024px PNGs stay separate.",feature3Title:"Verifiable data.",feature3Text:"935 synthetic portraits have file checksums for data-integrity studies. Identity labels do not establish biometric uniqueness.",
    accessKicker:"DATA & SOURCE CODE",accessTitle:"Datasets & source code",accessLead:"Explore original PNGs and metadata on Hugging Face or Kaggle, and browse project source code on GitHub.",hfInfo:"ImageFolder and per-image metadata for dataset exploration.",kaggleInfo:"Kaggle Dataset Version 1 with image folders and a CPU verification notebook.",comingSoon:"Dataset link unavailable",openPlatform:"Open dataset ↗",openRepository:"View source code",githubInfo:"Project source code, bilingual documentation and CPU validation tools (MIT).",
    footerText:"Synthetic faces. Carefully curated. Independently explored.",backToTop:"Back to top ↑",detailEyebrow:"IDENTITY STUDY / 1.0.0",viewingLabel:"CURRENT VIEW",detailResolution:"Preview resolution",detailStatus:"Image type",accepted:"Synthetic portrait",copyLink:"Copy direct link",copied:"Link copied",copyFailed:"Copy this URL:",detailOriginals:"Original 1024px PNGs are stored separately on Hugging Face and Kaggle; this gallery shows WebP previews.",prevFamily:"Previous identity",nextFamily:"Next identity",keyboardHint:"Use ← → to change view · Esc to close",familyViews:"5 views",resultFamilies:"families",resultImages:"images",page:"Page",of:"of",
    coreName:"Core collection",additionalName:"Additional Optional collection",
    slot_SOURCE:"Reference portrait for this synthetic identity.",slot_P1:"The first pose variation of the same synthetic identity.",slot_P2:"The second pose variation of the same synthetic identity.",slot_E1:"The first expression variation of this synthetic identity.",slot_E2:"The second expression variation of this synthetic identity.",noData:"Unable to load gallery data. Please serve this site with an HTTP server."
  },
  vi: {
    navExplore:"Khám phá",navAbout:"Giới thiệu",navContact:"Liên hệ",requestRemoval:"Yêu cầu gỡ ảnh",navAccess:"Ảnh gốc",previewStatus:"BẢN XEM ẢNH",
    heroLine1:"Một danh tính.",heroLine2:"Năm góc nhìn.",heroBody:"Bộ ảnh khuôn mặt tổng hợp được tuyển chọn kỹ lưỡng, giúp khám phá sự nhất quán về danh tính, góc mặt và biểu cảm qua một trải nghiệm xem nhẹ và trực quan.",
    heroExplore:"Khám phá bộ ảnh",heroLearn:"Tìm hiểu cách hoạt động",statFamilies:"bộ danh tính",statImages:"ảnh tổng hợp",statViews:"góc nhìn mỗi bộ",visualCaption:"MỘT GƯƠNG MẶT / NHIỀU GÓC NHÌN",acceptedLabel:"ẢNH TỔNG HỢP",
    galleryKicker:"THƯ VIỆN ẢNH",galleryTitle:"Khám phá từng góc nhìn.",galleryLead:"Xem theo từng bộ danh tính hoặc duyệt từng ảnh riêng lẻ. Tất cả đều là bản xem trước tối ưu dung lượng.",
    searchPlaceholder:"Tìm mã danh tính, ví dụ 0106, AD0036…",viewFamilies:"Theo danh tính",viewImages:"Toàn bộ ảnh",filterAll:"Tất cả",filterCore:"Core",filterAdditional:"Additional",sortLabel:"Sắp xếp",sortAsc:"Mã tăng dần",sortDesc:"Mã giảm dần",slotFilterLabel:"Loại ảnh",slotAll:"Cả 5 loại",loading:"Đang tải thư viện…",emptyTitle:"Không tìm thấy danh tính phù hợp.",emptyCopy:"Hãy thử một mã khác hoặc bỏ bộ lọc đang chọn.",resetFilters:"Xóa bộ lọc",
    aboutKicker:"THIẾT KẾ CÓ CHỦ ĐÍCH",aboutTitle:"Xem ảnh dễ dàng hơn.",feature1Title:"Năm góc nhìn, một danh tính.",feature1Text:"Gồm ảnh SOURCE, hai góc mặt P1/P2 và hai biểu cảm E1/E2 để tiện đối chiếu.",feature2Title:"Tải nhanh và tiết kiệm dữ liệu.",feature2Text:"Ảnh nhỏ 400px, xem chi tiết 768px, định dạng WebP và tải theo nhu cầu. Ảnh PNG gốc 1024px được lưu riêng.",feature3Title:"Dữ liệu có thể kiểm chứng.",feature3Text:"935 ảnh tổng hợp có checksum để kiểm tra toàn vẹn dữ liệu. Nhãn danh tính không chứng nhận tính duy nhất sinh trắc học.",
    accessKicker:"DỮ LIỆU VÀ MÃ NGUỒN",accessTitle:"Dataset và mã nguồn",accessLead:"Xem PNG gốc và metadata trên Hugging Face hoặc Kaggle; tham khảo mã nguồn dự án trên GitHub.",hfInfo:"ImageFolder và metadata từng ảnh để duyệt dữ liệu.",kaggleInfo:"Dataset Kaggle Version 1 dạng thư mục ảnh và notebook kiểm chứng CPU.",comingSoon:"Liên kết dataset chưa khả dụng",openPlatform:"Mở bộ dữ liệu ↗",openRepository:"Xem mã nguồn GitHub",githubInfo:"Mã nguồn dự án, tài liệu song ngữ và công cụ kiểm chứng CPU (MIT).",
    footerText:"Ảnh tổng hợp. Tuyển chọn cẩn thận. Khám phá trực quan.",backToTop:"Lên đầu trang ↑",detailEyebrow:"CHI TIẾT DANH TÍNH / 1.0.0",viewingLabel:"ẢNH ĐANG XEM",detailResolution:"Độ phân giải preview",detailStatus:"Loại ảnh",accepted:"Ảnh tổng hợp",copyLink:"Sao chép liên kết",copied:"Đã sao chép liên kết",copyFailed:"Hãy sao chép URL này:",detailOriginals:"PNG gốc 1024px được lưu riêng trên Hugging Face và Kaggle; gallery này chỉ hiển thị ảnh WebP xem trước.",prevFamily:"Danh tính trước",nextFamily:"Danh tính sau",keyboardHint:"Nhấn ← → để đổi ảnh · Esc để đóng",familyViews:"5 ảnh",resultFamilies:"bộ danh tính",resultImages:"ảnh",page:"Trang",of:"trên",
    coreName:"Bộ Core",additionalName:"Bộ Additional Optional",
    slot_SOURCE:"Ảnh tham chiếu của danh tính tổng hợp.",slot_P1:"Góc mặt thứ nhất của cùng danh tính tổng hợp.",slot_P2:"Góc mặt thứ hai của cùng danh tính tổng hợp.",slot_E1:"Biểu cảm thứ nhất của danh tính tổng hợp.",slot_E2:"Biểu cảm thứ hai của danh tính tổng hợp.",noData:"Không tải được dữ liệu ảnh. Hãy mở website bằng một HTTP server."
  }
};

function savedPref(name, fallback) { try { return localStorage.getItem("compactfaces_" + name) || fallback; } catch (_) { return fallback; } }
function storePref(name, value) { try { localStorage.setItem("compactfaces_" + name, value); } catch (_) {} }
const queryLang = new URLSearchParams(location.search).get("lang");
const state = {
  catalog: [], families: [], config: {}, lang: ["en", "vi"].includes(queryLang) ? queryLang : savedPref("lang", "en"),
  theme: savedPref("theme", "light"), view: "families", filter: "all", slotFilter: "ALL", sort: "asc",
  search: "", page: 1, activeId: null, activeSlot: "SOURCE", filteredFamilies: [],
  toastTimer: null, touchStartX: null,
};
const t = (name) => translations[state.lang]?.[name] ?? translations.en[name] ?? name;
const mk = (tag, className, text) => {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (text !== undefined) el.textContent = text;
  return el;
};
function applyTranslations() {
  document.documentElement.lang = state.lang;
  $$("[data-i18n]").forEach(el => { el.textContent = t(el.dataset.i18n); });
  $$("[data-i18n-placeholder]").forEach(el => { el.placeholder = t(el.dataset.i18nPlaceholder); });
  $("#languageToggle").textContent = state.lang === "en" ? "VI" : "EN";
  $("#languageToggle").setAttribute("aria-label", state.lang === "en" ? "Chuyển sang tiếng Việt" : "Switch to English");
  document.title = state.lang === "vi" ? "CompactFaces — Thư viện khuôn mặt tổng hợp" : "CompactFaces — Synthetic Face Identity Gallery";
  setupDownloads();
}
function setupDownloads() {
  const published = ["PUBLIC", "PUBLIC_GALLERY_PREVIEW"].includes(state.config.publication_status);
  for (const platform of ["huggingface", "kaggle"]) {
    const anchor = $("#" + (platform === "huggingface" ? "hfLink" : "kaggleLink"));
    const raw = state.config.downloads?.[platform] || "";
    let usable = false;
    try {
      const u = new URL(raw);
      usable = published && u.protocol === "https:" &&
        (platform === "huggingface" ? u.hostname === "huggingface.co" : ["www.kaggle.com", "kaggle.com"].includes(u.hostname));
    } catch (_) {}
    if (usable) {
      anchor.href = raw;
      anchor.rel = "noopener noreferrer";
      anchor.target = "_blank";
      anchor.classList.remove("unavailable");
      anchor.removeAttribute("aria-disabled");
      anchor.firstElementChild.textContent = t("openPlatform").replace(" ↗", "");
    } else {
      anchor.removeAttribute("href");
      anchor.removeAttribute("target");
      anchor.classList.add("unavailable");
      anchor.setAttribute("aria-disabled", "true");
      anchor.firstElementChild.textContent = t("comingSoon");
    }
  }
}
function updateControls() {
  $$("[data-view]").forEach(el => {
    const current = el.dataset.view === state.view;
    el.classList.toggle("active", current);
    el.setAttribute("aria-pressed", String(current));
  });
  $$("[data-filter]").forEach(el => {
    const current = el.dataset.filter === state.filter;
    el.classList.toggle("active", current);
    el.setAttribute("aria-pressed", String(current));
  });
  $$("[data-slot]").forEach(el => {
    const current = el.dataset.slot === state.slotFilter;
    el.classList.toggle("active", current);
    el.setAttribute("aria-pressed", String(current));
  });
  $("#slotRow").hidden = state.view !== "images";
  $("#sortSelect").value = state.sort;
  $("#galleryGrid").classList.toggle("images-mode", state.view === "images");
}
function filteredGroups() {
  const text = state.search.trim().toUpperCase();
  const match = state.catalog.filter(g => (state.filter === "all" || g.collection === state.filter) &&
    (!text || g.id.toUpperCase().includes(text) || g.id.replace(/^CORE:|^AD:/, "").includes(text)));
  match.sort((a, b) => {
    if (a.collection !== b.collection) return a.collection === "core" ? -1 : 1;
    return a.id.localeCompare(b.id, "en", { numeric: true }) * (state.sort === "asc" ? 1 : -1);
  });
  return match;
}
function reportHref(id, slot, wholeFamily = false) {
  const url = new URL("./contact.html", location.href);
  url.searchParams.set("identity", id);
  if (!wholeFamily) url.searchParams.set("slot", slot);
  url.searchParams.set("lang", state.lang);
  return url.pathname + url.search;
}
function cardButton(data, family, slot, familyMode) {
  const card = mk("article", familyMode ? "family-card" : "image-card");
  const btn = mk("button", "card-open");
  btn.type = "button";
  btn.setAttribute("aria-label", family.id + " – " + (familyMode ? t("familyViews") : slot));
  const visual = mk("div", "card-visual");
  const img = mk("img");
  img.src = data.thumb; img.alt = family.id + " " + slot + " synthetic face thumbnail";
  img.width = 400; img.height = 400; img.loading = "lazy"; img.decoding = "async";
  visual.appendChild(img);
  visual.appendChild(mk("span", "card-badge", family.collection === "core" ? "CORE" : "ADDITIONAL"));
  if (familyMode) visual.appendChild(mk("span", "card-corner", "↗"));
  else visual.appendChild(mk("span", "image-slot-badge", slot));
  btn.appendChild(visual);
  btn.addEventListener("click", () => openDetail(family.id, slot));
  card.appendChild(btn);
  const caption = mk("div", "card-caption");
  const info = mk("div", "card-identity");
  info.appendChild(mk("strong", "", family.id));
  if (!familyMode) info.appendChild(mk("span", "", slot));
  const report = mk("a", "report-link", t("requestRemoval"));
  report.href = reportHref(family.id, slot, familyMode);
  report.setAttribute("aria-label", t("requestRemoval") + ": " + family.id + (familyMode ? "" : "/" + slot));
  caption.appendChild(info);
  caption.appendChild(report);
  card.appendChild(caption);
  if (familyMode) {
    const track = mk("div", "slots-row");
    for (const _ of SLOTS) track.appendChild(mk("span"));
    card.appendChild(track);
  }
  return card;
}
function render() {
  if (!state.catalog.length) return;
  updateControls();
  const families = filteredGroups();
  state.filteredFamilies = families;
  const entries = state.view === "families" ? families.map(f => ({family:f, slot:"SOURCE"})) :
    families.flatMap(f => SLOTS.filter(slot => state.slotFilter === "ALL" || state.slotFilter === slot).map(slot => ({family:f, slot})));
  const pageSize = state.view === "families" ? 24 : 48;
  const totalPages = Math.max(1, Math.ceil(entries.length / pageSize));
  state.page = Math.max(1, Math.min(state.page, totalPages));
  const start = (state.page - 1) * pageSize;
  const grid = $("#galleryGrid");
  const fragment = document.createDocumentFragment();
  for (const entry of entries.slice(start, start + pageSize)) {
    fragment.appendChild(cardButton(entry.family.images[entry.slot], entry.family, entry.slot, state.view === "families"));
  }
  grid.replaceChildren(fragment);
  grid.setAttribute("aria-busy", "false");
  $("#emptyState").hidden = entries.length > 0;
  $("#resultCount").textContent = entries.length + " " + t(state.view === "families" ? "resultFamilies" : "resultImages");
  $("#pagination").hidden = entries.length <= pageSize;
  $("#pageInfo").textContent = t("page") + " " + state.page + " " + t("of") + " " + totalPages;
  $("#prevPage").disabled = state.page === 1;
  $("#nextPage").disabled = state.page === totalPages;
}
function changePage(delta) {
  state.page += delta;
  render();
  $("#explore").scrollIntoView({ behavior: "smooth", block: "start" });
}
function collectionName(family) { return t(family.collection === "core" ? "coreName" : "additionalName"); }
function setDetailSlot(slot, updateURL = true) {
  const family = state.catalog.find(g => g.id === state.activeId);
  if (!family) return;
  state.activeSlot = slot;
  $("#detailImage").src = family.images[slot].preview;
  $("#detailImage").alt = family.id + " " + slot + " — 768px synthetic face preview";
  $("#detailSlotPill").textContent = slot;
  $("#viewTitle").textContent = slot;
  $("#viewDescription").textContent = t("slot_" + slot);
  $("#dialogCounter").textContent = (SLOTS.indexOf(slot) + 1) + " / 5";
  $("#detailReport").href = reportHref(family.id, slot);
  $$(".detail-thumb").forEach(btn => {
    const active = btn.dataset.slot === slot;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-pressed", String(active));
  });
  if (updateURL) syncURL("replace");
}
function makeStrip(family) {
  const strip = $("#detailStrip");
  strip.replaceChildren();
  for (const slot of SLOTS) {
    const btn = mk("button", "detail-thumb");
    btn.type = "button"; btn.dataset.slot = slot; btn.setAttribute("aria-label", slot);
    const img = mk("img");
    img.src = family.images[slot].thumb;
    img.alt = slot + " preview"; img.width=400; img.height=400; img.decoding="async";
    btn.appendChild(img); btn.appendChild(mk("span", "", slot));
    btn.addEventListener("click", () => setDetailSlot(slot));
    strip.appendChild(btn);
  }
}
function openDetail(id, slot = "SOURCE", fromHistory = false) {
  const family = state.catalog.find(g => g.id === id);
  if (!family || !SLOTS.includes(slot)) return;
  const wasOpen = Boolean(state.activeId);
  state.activeId = id;
  $("#detailTitle").textContent = family.id;
  $("#detailCollection").textContent = collectionName(family);
  makeStrip(family);
  const dlg = $("#detailDialog");
  if (!dlg.open) dlg.showModal();
  document.body.style.overflow = "hidden";
  setDetailSlot(slot, false);
  if (!fromHistory) syncURL(wasOpen ? "replace" : "push");
  $("#closeDialog").focus();
}
function closeDetail(fromHistory = false) {
  const returnToGallery = !fromHistory && history.state?.compactfacesViewer === true;
  const dlg = $("#detailDialog");
  if (dlg.open) dlg.close();
  document.body.style.overflow = "";
  state.activeId = null;
  if (!fromHistory) {
    if (returnToGallery) history.back();
    else syncURL("replace");
  }
}
function syncURL(mode) {
  const url = new URL(location.href);
  if (state.activeId) {
    url.searchParams.set("id", state.activeId);
    url.searchParams.set("slot", state.activeSlot);
  } else {
    url.searchParams.delete("id");
    url.searchParams.delete("slot");
  }
  url.searchParams.set("lang", state.lang);
  if (mode === "push") history.pushState({compactfacesViewer: true}, "", url);
  else history.replaceState(history.state, "", url);
}
function shiftSlot(delta) {
  if (!state.activeId) return;
  const current = SLOTS.indexOf(state.activeSlot);
  setDetailSlot(SLOTS[(current + delta + SLOTS.length) % SLOTS.length]);
}
function shiftFamily(delta) {
  if (!state.activeId) return;
  const families = state.filteredFamilies.length ? state.filteredFamilies : state.catalog;
  let index = families.findIndex(g => g.id === state.activeId);
  if (index < 0) index = 0;
  const next = families[(index + delta + families.length) % families.length];
  openDetail(next.id, state.activeSlot);
}
function setLanguage(next) {
  state.lang = next;
  storePref("lang", next);
  applyTranslations();
  render();
  if (state.activeId) {
    const family = state.catalog.find(g => g.id === state.activeId);
    $("#detailCollection").textContent = collectionName(family);
    setDetailSlot(state.activeSlot);
  } else syncURL("replace");
}
function toast(message) {
  const node = $("#toast");
  node.textContent = message; node.classList.add("show");
  clearTimeout(state.toastTimer);
  state.toastTimer = setTimeout(() => node.classList.remove("show"), 2300);
}
function attachEvents() {
  $("#themeToggle").addEventListener("click", () => {
    state.theme = state.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = state.theme;
    storePref("theme", state.theme);
  });
  $("#languageToggle").addEventListener("click", () => setLanguage(state.lang === "vi" ? "en" : "vi"));
  $$("[data-view]").forEach(btn => btn.addEventListener("click", () => { state.view = btn.dataset.view; state.page = 1; render(); }));
  $$("[data-filter]").forEach(btn => btn.addEventListener("click", () => { state.filter = btn.dataset.filter; state.page = 1; render(); }));
  $$("[data-slot]").forEach(btn => btn.addEventListener("click", () => { state.slotFilter = btn.dataset.slot; state.page = 1; render(); }));
  $("#searchBox").addEventListener("input", ev => { state.search = ev.target.value; state.page = 1; render(); });
  $("#sortSelect").addEventListener("change", ev => { state.sort = ev.target.value; state.page = 1; render(); });
  $("#prevPage").addEventListener("click", () => changePage(-1));
  $("#nextPage").addEventListener("click", () => changePage(1));
  $$(".back-to-top").forEach(link => link.addEventListener("click", ev => { ev.preventDefault(); window.scrollTo({top: 0, left: 0, behavior: "smooth"}); }));
  $("#resetFilters").addEventListener("click", () => {
    state.search = ""; state.filter = "all"; state.slotFilter = "ALL"; state.page = 1;
    $("#searchBox").value = ""; render();
  });
  $("#closeDialog").addEventListener("click", () => closeDetail());
  $("#detailDialog").addEventListener("close", () => { if (state.activeId) closeDetail(); });
  $("#prevSlot").addEventListener("click", () => shiftSlot(-1));
  $("#nextSlot").addEventListener("click", () => shiftSlot(1));
  $("#prevFamily").addEventListener("click", () => shiftFamily(-1));
  $("#nextFamily").addEventListener("click", () => shiftFamily(1));
  $("#copyLink").addEventListener("click", async () => {
    const url = location.href;
    try { await navigator.clipboard.writeText(url); toast(t("copied")); }
    catch (_) { window.prompt(t("copyFailed"), url); }
  });
  const viewer = $("#detailImage");
  viewer.addEventListener("touchstart", ev => { state.touchStartX = ev.changedTouches[0].screenX; }, {passive:true});
  viewer.addEventListener("touchend", ev => {
    if (state.touchStartX == null) return;
    const distance = ev.changedTouches[0].screenX - state.touchStartX;
    state.touchStartX = null;
    if (Math.abs(distance) > 45) shiftSlot(distance < 0 ? 1 : -1);
  }, {passive:true});
  document.addEventListener("keydown", ev => {
    if (ev.key === "/" && !["INPUT","TEXTAREA"].includes(document.activeElement.tagName) && !state.activeId) {
      ev.preventDefault(); $("#searchBox").focus();
    }
    if (!state.activeId) return;
    if (ev.key === "ArrowLeft") { ev.preventDefault(); shiftSlot(-1); }
    else if (ev.key === "ArrowRight") { ev.preventDefault(); shiftSlot(1); }
    else if (ev.key === "ArrowUp") { ev.preventDefault(); shiftFamily(-1); }
    else if (ev.key === "ArrowDown") { ev.preventDefault(); shiftFamily(1); }
  });
  window.addEventListener("popstate", () => {
    const p = new URLSearchParams(location.search);
    const id = p.get("id");
    const slot = p.get("slot") || "SOURCE";
    if (id && state.catalog.some(g=>g.id === id)) openDetail(id, SLOTS.includes(slot) ? slot : "SOURCE", true);
    else closeDetail(true);
  });
}
async function init() {
  document.documentElement.dataset.theme = state.theme === "dark" ? "dark" : "light";
  attachEvents();
  try {
    const [catalogResponse, configResponse] = await Promise.all([fetch("./data/catalog.json"),fetch("./site-config.json")]);
    if (!catalogResponse.ok || !configResponse.ok) throw new Error("Failed to fetch site data");
    const catalog = await catalogResponse.json();
    state.config = await configResponse.json();
    if (catalog.release !== "1.0.0" || catalog.families !== 187 || catalog.images !== 935 || catalog.items.length !== 187)
      throw new Error("Unexpected dataset catalog");
    state.catalog = catalog.items;
    state.families = catalog.items;
    for (const [id, index] of [["heroImage1", 8], ["heroImage2", 78], ["heroImage3", 158]]) {
      const family = catalog.items[index];
      if (family) $("#" + id).src = family.images.SOURCE.thumb;
    }
    applyTranslations();
    render();
    const params = new URLSearchParams(location.search);
    const id = params.get("id"), slot = params.get("slot") || "SOURCE";
    if (id) openDetail(id, SLOTS.includes(slot) ? slot : "SOURCE", true);
  } catch (err) {
    applyTranslations();
    $("#galleryGrid").replaceChildren(mk("div", "loading-state", t("noData")));
    console.error("CompactFaces gallery initialization error:", err);
  }
}
init();
