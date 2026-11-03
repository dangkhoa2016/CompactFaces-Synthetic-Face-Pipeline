"use strict";
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
const page = document.body.dataset.page || "about";
const params = new URLSearchParams(location.search);
const strings = {
  en: {
    navExplore:"Explore",navAbout:"About",navContact:"Contact",navAccess:"Get originals",footerText:"Synthetic faces. Carefully curated. Independently explored.",
    backToTop:"Back to top ↑",backGallery:"Back to gallery",families:"identity families",images:"accepted images",originals:"original PNG resolution",
    aboutKicker:"ABOUT THE PROJECT",aboutHeading:"Synthetic faces, curated for exploration.",
    aboutIntro:"CompactFaces 1.0.0 is a curated synthetic-face collection organized by identity. The gallery lets people inspect each five-image family without downloading the original files.",
    structureKicker:"DATASET STRUCTURE",structureHeading:"One identity, five views",
    structureIntro:"There are 120 Core families (600 images) and 67 Additional Optional families (335 images). Each family has five named views:",
    sourceDescription:"Reference portrait for the synthetic identity.",p1Description:"First pose variation.",p2Description:"Second pose variation.",e1Description:"First expression variation.",e2Description:"Second expression variation.",
    datasetCaution:"Synthetic identity labels help organize images, but do not establish biometric uniqueness or guarantee that a face cannot resemble a real person.",
    sourceKicker:"TECHNICAL IMPLEMENTATION",sourceHeading:"How the source code works",
    dataTitle:"Image generation and edits",dataText:"The dataset documents image generation using Mage-Flow-Turbo and Mage-Flow-Edit-Turbo. Published checksums verify files; prompt metadata alone does not guarantee byte-identical regeneration of all 935 images.",
    verifyTitle:"Integrity verification",verifyText:"Python validators check each identity’s five slots, the release inventory and SHA256 hashes of the 1024px original PNGs before generating previews.",
    buildTitle:"Static gallery build",buildText:"Python and Pillow produce WebP thumbnails at 400px and previews at 768px. Responsive HTML, CSS and vanilla JavaScript power the gallery with no backend or external UI framework.",
    accessTitle:"Separate original downloads",accessText:"Original 1024px PNGs and metadata are hosted on Hugging Face and Kaggle. The engineering toolkit is on GitHub.",
    openRepository:"View source on GitHub",openHuggingFace:"View dataset on Hugging Face",openKaggle:"View dataset on Kaggle",contactSourceTitle:"Dataset and source code",contactSourceText:"Explore original image datasets on Hugging Face and Kaggle, or browse project tools on GitHub.",sourceRepoTitle:"Dataset and source code",sourceRepoText:"Access original images and metadata via Hugging Face or Kaggle, and explore the project tools on GitHub.",
    ethicsKicker:"TRANSPARENCY AND REMOVAL",ethicsHeading:"Synthetic faces can still resemble someone.",
    ethicsText:"If a face resembles you, or you have a privacy or rights concern, you can request review of a specific identity or view. Include the identity code and view when possible; no selfie upload is necessary.",
    licenseText:"MIT applies to the repository-owned software, not to externally supplied image collections or model weights. This viewer does not claim biometric uniqueness or grant image redistribution rights.",
    contactCta:"Contact about an image",
    contactKicker:"PRIVACY & IMAGE REMOVAL",contactHeading:"Concerned about a face in the dataset?",
    contactIntro:"Synthetic faces can sometimes resemble real people. If an image looks like you or you have another rights concern, contact the maintainer with the image identifier for review.",
    requestKicker:"SUBMIT A REQUEST",requestHeading:"Request a review or removal",
    formIntro:"This form prepares an email in your own email application. The website itself does not collect or submit your details.",
    identityLabel:"Identity code",identityHelp:"Use the code shown on the image card. Optional for general inquiries.",
    viewLabel:"Specific view (optional)",wholeFamily:"Entire identity / not specified",
    replyLabel:"Your reply email (optional)",replyHelp:"You can provide an address or simply send from your email client.",
    reasonLabel:"Reason for your request",reasonResemblance:"The face resembles me",reasonPrivacy:"Privacy or image rights concern",reasonOther:"Other concern",
    detailLabel:"Details (optional)",detailPlaceholder:"Tell us which identity you would like reviewed and why.",
    disclosure:"Please do not send identity documents, biometric data or sensitive photos through this form. Further information, if needed, can be discussed by email.",
    prepareEmail:"Open email application",copyRequest:"Copy request text",
    directKicker:"DIRECT CONTACT",directText:"For removal requests, include the identity code (e.g. CORE:0106), view if known, and why you are concerned.",
    processTitle:"How requests are handled",process1:"You identify the image and explain your concern by email.",
    process2:"The maintainer reviews the request and the referenced identity.",
    process3:"When appropriate, controlled copies can be updated to remove the identity or image. Independent mirrors or cached copies may need separate follow-up.",
    noAutoRemoval:"Submitting a request does not delete an image automatically and cannot guarantee deletion from third-party mirrors.",
    invalidIdentity:"Please enter a valid identity code such as CORE:0106 or AD:AD0036.",
    invalidReply:"Please enter a valid reply email or leave this field blank.",
    copied:"Request text copied. Paste it into an email to i.am@dangkhoa.dev and send it.",
    copyFallback:"Select and copy this request:",
    mailHint:"If your email client opens, review the message and press Send. Nothing has been submitted by this website. If no app opens, use ‘Copy request text’.",
    mailSubject:"CompactFaces — image review/removal request",
    mailBodyHeading:"CompactFaces 1.0.0 — image review/removal request",
    mailBodyIdentity:"Identity",mailBodyView:"View",mailBodyReason:"Reason",mailBodyReplyTo:"Reply-to",
    mailBodyGallery:"Gallery reference",mailBodyDetails:"Details",mailBodyUnspecified:"Not specified",
    mailBodyWholeFamily:"Entire identity / not specified",mailBodySender:"Reply to the sender's email",
    mailBodyNoDetails:"No additional details",mailBodyClosing:"Please review this request and advise on next steps."
  },
  vi: {
    navExplore:"Khám phá",navAbout:"Giới thiệu",navContact:"Liên hệ",navAccess:"Ảnh gốc",footerText:"Ảnh tổng hợp. Tuyển chọn cẩn thận. Khám phá trực quan.",
    backToTop:"Lên đầu trang ↑",backGallery:"Trở về gallery",families:"bộ danh tính",images:"ảnh đã nghiệm thu",originals:"độ phân giải PNG gốc",
    aboutKicker:"VỀ DỰ ÁN",aboutHeading:"Khuôn mặt tổng hợp, tuyển chọn để khám phá.",
    aboutIntro:"CompactFaces 1.0.0 là bộ dữ liệu khuôn mặt tổng hợp được tổ chức theo từng danh tính. Gallery giúp xem đủ năm ảnh của một bộ mà không cần tải dữ liệu PNG nguyên gốc.",
    structureKicker:"CẤU TRÚC BỘ DỮ LIỆU",structureHeading:"Một danh tính, năm góc nhìn",
    structureIntro:"Bộ Core gồm 120 danh tính (600 ảnh), bộ Additional Optional gồm 67 danh tính (335 ảnh). Mỗi danh tính có năm loại ảnh:",
    sourceDescription:"Ảnh chân dung tham chiếu cho danh tính tổng hợp.",p1Description:"Biến thể góc mặt thứ nhất.",p2Description:"Biến thể góc mặt thứ hai.",e1Description:"Biến thể biểu cảm thứ nhất.",e2Description:"Biến thể biểu cảm thứ hai.",
    datasetCaution:"Nhãn danh tính giúp tổ chức ảnh tổng hợp; chúng không chứng nhận tính duy nhất sinh trắc học hoặc bảo đảm không giống người thật.",
    sourceKicker:"KỸ THUẬT TRIỂN KHAI",sourceHeading:"Mã nguồn hoạt động thế nào?",
    dataTitle:"Sinh ảnh và chỉnh sửa khuôn mặt",dataText:"Bộ dữ liệu sử dụng Mage-Flow-Turbo và Mage-Flow-Edit-Turbo. Checksum xác minh ảnh đã phát hành; metadata prompt không bảo đảm tái tạo chính xác từng byte của toàn bộ 935 ảnh.",
    verifyTitle:"Kiểm tra tính toàn vẹn",verifyText:"Các script Python xác minh năm slot trong từng danh tính, số lượng ảnh và SHA256 của ảnh PNG gốc 1024px trước khi tạo các bản xem trước.",
    buildTitle:"Tạo website tĩnh",buildText:"Python và Pillow tạo thumbnail WebP 400px và preview 768px. Website dùng HTML, CSS và JavaScript thuần; không phụ thuộc backend hoặc framework giao diện ngoài.",
    accessTitle:"Tải ảnh gốc tại nền tảng riêng",accessText:"PNG gốc 1024px cùng metadata được lưu trên Hugging Face và Kaggle. Mã nguồn và công cụ kỹ thuật có trên GitHub.",
    openRepository:"Xem mã nguồn trên GitHub",openHuggingFace:"Xem dataset trên Hugging Face",openKaggle:"Xem dataset trên Kaggle",contactSourceTitle:"Dữ liệu và mã nguồn",contactSourceText:"Xem dữ liệu ảnh gốc trên Hugging Face hoặc Kaggle và công cụ dự án trên GitHub.",sourceRepoTitle:"Dữ liệu và mã nguồn",sourceRepoText:"Ảnh gốc và metadata có trên Hugging Face hoặc Kaggle; mã nguồn và công cụ dự án có trên GitHub.",
    ethicsKicker:"MINH BẠCH VÀ YÊU CẦU GỠ ẢNH",ethicsHeading:"Ảnh tổng hợp vẫn có thể giống người thật.",
    ethicsText:"Nếu ảnh khuôn mặt trông giống bạn hoặc có quan ngại về quyền riêng tư/bản quyền, bạn có thể yêu cầu xem xét một danh tính hoặc ảnh cụ thể. Hãy cung cấp mã danh tính và loại ảnh nếu biết; không cần tải ảnh tự chụp lên website.",
    licenseText:"MIT chỉ áp dụng cho phần mềm do repository sở hữu, không tự áp dụng cho ảnh hoặc model ngoài. Website không cam kết danh tính duy nhất sinh trắc học và không cấp quyền phân phối lại ảnh.",
    contactCta:"Liên hệ về hình ảnh",
    contactKicker:"QUYỀN RIÊNG TƯ & YÊU CẦU GỠ ẢNH",contactHeading:"Bạn lo ngại khuôn mặt trong bộ ảnh giống mình?",
    contactIntro:"Khuôn mặt tổng hợp đôi khi có thể giống người thật. Nếu bạn thấy ảnh giống mình hoặc có quan ngại về quyền lợi, hãy liên hệ người duy trì để yêu cầu xem xét.",
    requestKicker:"GỬI YÊU CẦU",requestHeading:"Yêu cầu xem xét hoặc gỡ bỏ ảnh",
    formIntro:"Form này chỉ chuẩn bị email trong ứng dụng email của bạn. Website không tự thu thập hoặc gửi nội dung yêu cầu.",
    identityLabel:"Mã danh tính",identityHelp:"Nhập mã hiển thị ở thẻ ảnh; có thể bỏ trống nếu chỉ muốn liên hệ chung.",
    viewLabel:"Ảnh cụ thể (không bắt buộc)",wholeFamily:"Toàn bộ identity / không chỉ định",
    replyLabel:"Email nhận phản hồi (không bắt buộc)",replyHelp:"Có thể điền địa chỉ email hoặc gửi từ ứng dụng email của bạn.",
    reasonLabel:"Lý do khiếu nại",reasonResemblance:"Khuôn mặt giống mình",reasonPrivacy:"Quan ngại quyền riêng tư/quyền hình ảnh",reasonOther:"Vấn đề khác",
    detailLabel:"Mô tả thêm (không bắt buộc)",detailPlaceholder:"Hãy nêu mã ảnh cần xem xét và lý do của bạn.",
    disclosure:"Không gửi giấy tờ tùy thân, dữ liệu sinh trắc hoặc ảnh nhạy cảm qua form này. Nếu cần thông tin bổ sung, chúng ta có thể trao đổi riêng qua email.",
    prepareEmail:"Mở ứng dụng email",copyRequest:"Sao chép nội dung yêu cầu",
    directKicker:"LIÊN HỆ TRỰC TIẾP",directText:"Khi yêu cầu gỡ ảnh, vui lòng cung cấp mã identity (ví dụ CORE:0106), loại ảnh nếu biết và lý do quan ngại.",
    processTitle:"Quy trình xem xét yêu cầu",process1:"Bạn xác định hình ảnh và gửi email mô tả quan ngại.",
    process2:"Người duy trì xem xét yêu cầu và bộ danh tính liên quan.",
    process3:"Khi phù hợp, bản dữ liệu do dự án kiểm soát sẽ được điều chỉnh hoặc gỡ. Bản sao/ảnh cache do bên thứ ba quản lý có thể cần liên hệ riêng.",
    noAutoRemoval:"Gửi yêu cầu không đồng nghĩa ảnh được tự động xóa; không thể bảo đảm xóa ngay các bản sao do bên thứ ba lưu giữ.",
    invalidIdentity:"Hãy nhập mã hợp lệ như CORE:0106 hoặc AD:AD0036.",
    invalidReply:"Hãy nhập email đúng định dạng hoặc để trống.",
    copied:"Đã sao chép nội dung. Hãy dán vào email gửi i.am@dangkhoa.dev và nhấn Gửi.",
    copyFallback:"Hãy chọn và sao chép nội dung này:",
    mailHint:"Nếu ứng dụng email mở ra, hãy kiểm tra nội dung và nhấn Gửi. Website chưa tự gửi yêu cầu. Nếu không thấy ứng dụng email, hãy dùng nút 'Sao chép nội dung yêu cầu'.",
    mailSubject:"CompactFaces — yêu cầu xem xét/gỡ ảnh",
    mailBodyHeading:"CompactFaces 1.0.0 — yêu cầu xem xét/gỡ ảnh",
    mailBodyIdentity:"Mã danh tính",mailBodyView:"Ảnh",mailBodyReason:"Lý do",mailBodyReplyTo:"Email phản hồi",
    mailBodyGallery:"Liên kết gallery",mailBodyDetails:"Chi tiết",mailBodyUnspecified:"Không chỉ định",
    mailBodyWholeFamily:"Toàn bộ danh tính / không chỉ định",mailBodySender:"Trả lời email người gửi",
    mailBodyNoDetails:"Không có thông tin bổ sung",mailBodyClosing:"Vui lòng xem xét yêu cầu và phản hồi hướng xử lý tiếp theo."
  }
};
function getPref(key, fallback) { try {return localStorage.getItem("compactfaces_"+key)||fallback;}catch(_){return fallback;} }
function setPref(key, value) { try {localStorage.setItem("compactfaces_"+key,value);}catch(_){} }
let lang = ["en","vi"].includes(params.get("lang")) ? params.get("lang") : getPref("lang","en");
let theme = getPref("theme","light");
function t(key) { return strings[lang]?.[key] || strings.en[key] || key; }
function renderLanguage() {
  document.documentElement.lang = lang;
  $$("[data-i18n]").forEach(el=>{el.textContent=t(el.dataset.i18n);});
  $$("[data-i18n-placeholder]").forEach(el=>{el.placeholder=t(el.dataset.i18nPlaceholder);});
  $("#languageToggle").textContent=lang==="en"?"VI":"EN";
  $("#languageToggle").setAttribute("aria-label",lang==="en"?"Chuyển sang tiếng Việt":"Switch to English");
  document.title=(page==="contact" ? (lang==="vi"?"Liên hệ và yêu cầu gỡ ảnh":"Contact & image removal") : (lang==="vi"?"Giới thiệu CompactFaces":"About CompactFaces"))+" — CompactFaces 1.0.0";
}
function renderTheme() { document.documentElement.dataset.theme = theme === "dark" ? "dark":"light"; }
function showMessage(value, error=false) {
  const status=$("#formMessage");
  if (!status) return;
  status.hidden=false;status.textContent=value;status.classList.toggle("error",error);
}
function validIdentity(value) {
  return !value || /^(CORE:\d{4}|AD:AD\d{4})$/.test(value);
}
function buildEmailText() {
  const identity=$("#identityInput").value.trim().toUpperCase();
  const slot=$("#slotInput").value;
  const reply=$("#replyInput").value.trim();
  const reason=$("#reasonInput");
  const reasonText=reason.options[reason.selectedIndex].textContent.trim();
  const details=$("#detailInput").value.trim();
  const imageUrl = new URL("./index.html",location.href);
  if (identity) imageUrl.searchParams.set("id",identity);
  if (slot) imageUrl.searchParams.set("slot",slot);
  imageUrl.searchParams.set("lang",lang);
  const lines=[
    t("mailBodyHeading"),
    "",
    t("mailBodyIdentity")+": "+(identity||t("mailBodyUnspecified")),
    t("mailBodyView")+": "+(slot||t("mailBodyWholeFamily")),
    t("mailBodyReason")+": "+reasonText,
    t("mailBodyReplyTo")+": "+(reply||t("mailBodySender")),
    t("mailBodyGallery")+": "+(identity ? imageUrl.href : t("mailBodyUnspecified")),
    "",
    t("mailBodyDetails")+": "+(details||t("mailBodyNoDetails")),
    "",
    t("mailBodyClosing")
  ];
  return lines.join("\n");
}
function validateForm() {
  const id=$("#identityInput").value.trim().toUpperCase();
  $("#identityInput").value=id;
  if (!validIdentity(id)) {
    $("#identityInput").focus();showMessage(t("invalidIdentity"),true);return false;
  }
  const reply=$("#replyInput");
  if (reply.value.trim() && !reply.checkValidity()) {
    reply.focus();showMessage(t("invalidReply"),true);return false;
  }
  return true;
}
function initContact() {
  if (page!=="contact") return;
  const incoming = params.get("identity") || "";
  const slot = params.get("slot") || "";
  if (validIdentity(incoming.toUpperCase()) && incoming) $("#identityInput").value=incoming.toUpperCase();
  if (["SOURCE","P1","P2","E1","E2"].includes(slot)) $("#slotInput").value=slot;
  $("#removalForm").addEventListener("submit", ev=>{
    ev.preventDefault();
    if(!validateForm())return;
    const url="mailto:i.am@dangkhoa.dev?subject="+encodeURIComponent(t("mailSubject"))+"&body="+encodeURIComponent(buildEmailText());
    showMessage(t("mailHint"));
    // Opens the user's email application; does not submit data to the site or claim email delivery.
    window.location.href=url;
  });
  $("#copyRequest").addEventListener("click",async()=>{
    if(!validateForm())return;
    const content=buildEmailText();
    try { await navigator.clipboard.writeText(content); showMessage(t("copied")); }
    catch (_) { window.prompt(t("copyFallback"),content); }
  });
}
document.documentElement.dataset.theme=theme;
renderTheme();renderLanguage();
$("#themeToggle").addEventListener("click",()=>{theme=theme==="dark"?"light":"dark";setPref("theme",theme);renderTheme();});
$("#languageToggle").addEventListener("click",()=>{
  lang=lang==="vi"?"en":"vi";setPref("lang",lang);
  const url=new URL(location.href);url.searchParams.set("lang",lang);
  history.replaceState(null,"",url);
  renderLanguage();
});
$$(".back-to-top").forEach(link=>link.addEventListener("click",ev=>{
  ev.preventDefault(); window.scrollTo({top:0,left:0,behavior:"smooth"});
}));
initContact();
