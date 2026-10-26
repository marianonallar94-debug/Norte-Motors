/* =========================================================
   CONFIGURACIÓN GENERAL — Palm Tree Motors
   Cambiá acá los valores y se actualiza toda la web.
   ========================================================= */
const SITE = {
  phone: "15714246410",            // WhatsApp / teléfono (solo números)
  phonePretty: "+1 (571) 424-6410",
  // Meta Pixel: pegá acá el ID (solo números) cuando lo crees en el Administrador de eventos.
  // Mientras esté vacío, la web no carga el Pixel.
  metaPixelId: "1105858505482319",
  // Calculadora de cuota (estimado, sujeto a aprobación del banco)
  termDefault: 72,                 // meses
  terms: [48, 60, 72],
  credit: [                        // tasa anual (APR) estimada según el crédito
    { key: "exc", es: "Excelente (720+)",       en: "Excellent (720+)",     apr: 4 },
    { key: "good", es: "Bueno (660–719)",       en: "Good (660–719)",       apr: 9 },
    { key: "fair", es: "Regular (600–659)",     en: "Fair (600–659)",       apr: 12 },
    { key: "build", es: "En construcción / sin crédito", en: "Rebuilding / no credit", apr: 14 }
  ],
  creditDefault: "exc",            // el que usan las tarjetas, el filtro "hasta $X al mes" y la calculadora al abrir
  googleReviewsUrl: "https://www.google.com/maps/place/?q=place_id:ChIJF_YCa7Wp2YgROUH7qLLcmc0",
  googleRating: "4.8",
  googleReviewCount: 39
};

/* ---------- Cálculo de cuota ---------- */
function monthlyPayment(amount, aprPct, months){
  const r = aprPct / 100 / 12;
  if (!amount || amount <= 0) return 0;
  if (r === 0) return amount / months;
  return amount * r / (1 - Math.pow(1 + r, -months));
}
function defaultApr(){ return SITE.credit.find(c => c.key === SITE.creditDefault).apr; }
function estMonthly(price){ return monthlyPayment(price, defaultApr(), SITE.termDefault); }
const fmt$ = n => "$" + Math.round(n).toLocaleString("en-US");

/* ---------- Idioma (ES / EN) ---------- */
const I18N = {
  en: {
    "nav.home":"Home","nav.inventory":"Inventory","nav.financing":"Financing","nav.about":"About","nav.contact":"Contact","nav.outofstate":"Out of state","nav.reviews":"Reviews",
    "hero.eyebrow":"Hollywood, Florida · Clean title guaranteed",
    "hero.title":"Your next car is on this lot.",
    "hero.lead":"Verified clean title and a 3-year bumper to bumper warranty on every car. Financing for all credit types, and we ship anywhere in the U.S.",
    "hero.apply":"Apply for financing","hero.inventory":"See inventory",
    "trust.title.t":"Clean title","trust.title.d":"Verified before the sale",
    "trust.warranty.t":"3-year warranty","trust.warranty.d":"Bumper to bumper, included",
    "trust.fin.t":"All credit types","trust.fin.d":"With or without credit history",
    "trust.loc.t":"All of the U.S.","trust.loc.d":"We ship it by car carrier",
    "inv.title":"The lot, today","inv.lead":"Pickups, SUVs, sedans and minivans. Search by the monthly payment you can afford.","inv.more":"See more cars","why.quote":"No fine print. No runaround.","card.applyShort":"Apply",
    "f.all":"All","f.pickup":"Pickups","f.suv":"SUVs","f.sedan":"Sedans","f.minivan":"Minivans","f.hatchback":"Hatchbacks","f.coupe":"Coupes","f.convertible":"Convertibles",
    "f.brand":"All makes","f.model":"Search model...","f.min":"Min price","f.max":"Max price","f.monthly":"Monthly up to $","f.sort":"Sort by","f.priceAsc":"Price: low to high","f.priceDesc":"Price: high to low","f.reset":"Clear filters",
    "inv.none":"No cars match those filters.","inv.count":"cars available",
    "card.soon":"Photo coming soon","card.sub":"clean title and 3-year warranty","card.apply":"Apply for Financing","card.ask":"Ask on WhatsApp",
    "card.permonth":"/mo est. · subject to approval","card.footnote":"*Estimated payment, {term} months, {credit} credit. Subject to bank approval.",
    "price.note":"Amount to finance from",
    "why.title":"Why buy at Palm Tree Motors","why.lead":"A family lot in Hollywood, backed by a real warranty and direct service for the Hispanic community.",
    "why.1t":"Clean title guaranteed","why.1d":"Every vehicle goes through title verification before it reaches our lot — no surprises, no fine print.",
    "why.2t":"3-year bumper to bumper warranty","why.2d":"Every car you buy at Palm Tree Motors leaves with 3 years of full coverage, bumper to bumper.",
    "why.3t":"The best financing options","why.3d":"We work with multiple lenders to get you the approval and monthly payment that fits you best.",
    "why.4t":"Direct service","why.4d":"Talk to us directly on WhatsApp — no runaround, no middlemen, from start to finish.",
    "oos.title":"Buy from any state","oos.lead":"We sell to customers all over the U.S. Choose your car here and we take care of the rest.",
    "oos.1t":"Pick your car","oos.1d":"Browse the inventory and message us on WhatsApp. We send you more photos, videos and the details of the car you want.",
    "oos.2t":"Get approved remotely","oos.2d":"We handle financing with you by phone and WhatsApp. No need to come in to get approved.",
    "oos.3t":"Choose how to get it","oos.3d":"Fly to Miami and pick it up, or sign everything online and we ship it to your door by car carrier.",
    "oos.cta":"I'm out of state — message us",
    "rev.title":"What our customers say","rev.lead":"Real reviews from customers who bought with us.","rev.on":"on Google","rev.reviews":"reviews","rev.all":"Read all reviews on Google","rev.from":"Google review","rev.deliveries":"Happy customers",
    "finb.title":"Approval today, with or without credit","finb.lead":"Every car includes clean title and a 3-year bumper to bumper warranty. Apply online in 2 minutes.",
    "form.title":"Apply for Financing","form.lead":"Fill in your info and we'll contact you on WhatsApp to continue your approval — no commitment.",
    "form.name":"Full name *","form.phone":"Phone *","form.email":"Email","form.car":"Car of interest","form.carOpt":"Choose a car (optional)",
    "form.down":"Approximate down payment","form.income":"Approximate monthly income","form.employed":"Currently employed?","form.notes":"Additional comments",
    "form.range":"Choose a range","form.option":"Choose an option","form.more":"or more","form.less":"Less than",
    "form.emp1":"Yes, employed","form.emp2":"Yes, self-employed","form.emp3":"Not currently",
    "form.notesPh":"Tell us anything else","form.namePh":"E.g. John Smith","form.emailPh":"you@example.com",
    "form.disclaimer":"We do not ask for your Social Security number, bank information or ID documents in this form. We complete that step securely by phone or in person.",
    "form.submit":"Send request on WhatsApp",
    "contact.title":"Visit or message us","contact.lead":"We're in Hollywood, Florida — come to the lot or chat with us on WhatsApp.",
    "contact.address":"Address","contact.phone":"Phone / WhatsApp","contact.hours":"Hours","contact.hoursVal":"Monday to Sunday — 10:00 AM to 7:00 PM","contact.chat":"Chat on WhatsApp",
    "calc.title":"Estimate your monthly payment","calc.amount":"Amount to finance","calc.term":"Term","calc.months":"months","calc.credit":"Your credit","calc.result":"Estimated payment","calc.apr":"Estimated APR",
    "calc.disc":"Estimate subject to approval. The final rate, down payment and monthly payment depend on the bank.","calc.subj":"Subject to approval","price.subj":"Subject to approval",
    "car.back":"← Back to inventory","car.miles":"Mileage","car.trans":"Engine / Transmission","car.title":"Title","car.titleVal":"Clean, verified","car.warranty":"Warranty","car.warrantyVal":"3 years bumper to bumper",
    "car.ask":"Ask on WhatsApp","car.available":"Is it still available?","car.call":"Call","car.share":"Share","car.copied":"Link copied",
    "car.formTitle":"Apply for financing on this vehicle","car.nf":"We couldn't find that vehicle","car.nfd":"It may have been sold or the link is incomplete.","car.nfBtn":"View full inventory",
    "car.oos":"Out of state? We ship it to your door by car carrier.",
    "foot.rights":"Hollywood, FL"
  }
};
let LANG = "es";
// Por defecto español; inglés solo si la persona lo elige (o entra con ?lang=en)
try { LANG = new URLSearchParams(location.search).get("lang") || localStorage.getItem("ptm_lang") || "es"; } catch(e) {}
if (LANG !== "en") LANG = "es";

// Guarda el texto original en español la primera vez para poder volver
function applyLang(){
  document.documentElement.lang = LANG;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const k = el.dataset.i18n;
    if (el.dataset.es === undefined) el.dataset.es = el.textContent;
    el.textContent = LANG === "en" && I18N.en[k] ? I18N.en[k] : el.dataset.es;
  });
  document.querySelectorAll("[data-i18n-ph]").forEach(el => {
    const k = el.dataset.i18nPh;
    if (el.dataset.esPh === undefined) el.dataset.esPh = el.placeholder;
    el.placeholder = LANG === "en" && I18N.en[k] ? I18N.en[k] : el.dataset.esPh;
  });
  document.querySelectorAll(".lang-toggle").forEach(b => b.textContent = LANG === "en" ? "ES" : "EN");
}
function t(key, es){ return LANG === "en" && I18N.en[key] ? I18N.en[key] : es; }
function setLang(l){
  LANG = l;
  try { localStorage.setItem("ptm_lang", l); } catch(e) {}
  applyLang();
  document.dispatchEvent(new Event("langchange"));
}
document.addEventListener("click", e => {
  const b = e.target.closest(".lang-toggle");
  if (b) setLang(LANG === "en" ? "es" : "en");
});

/* ---------- Meta Pixel ---------- */
function track(ev, params){ try { if (window.fbq) fbq("track", ev, params || {}); } catch(e) {} }
(function initPixel(){
  if (!SITE.metaPixelId) return;
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq("init", SITE.metaPixelId);
  fbq("track", "PageView");
})();
// Cualquier clic a WhatsApp o a llamar cuenta como "Contact"
document.addEventListener("click", e => {
  const a = e.target.closest("a[href*='wa.me'], a[href^='tel:']");
  if (a) track("Contact", { method: a.href.startsWith("tel:") ? "phone" : "whatsapp" });
});

document.addEventListener("DOMContentLoaded", applyLang);
