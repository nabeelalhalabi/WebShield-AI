import{M as d}from"./assets/messages.js";import{l as _}from"./assets/localSettings.js";import{l as o,a as E}from"./assets/logger.js";const v=`.webshield-warning-banner {
  position: fixed;
  top: 12px;
  right: 12px;
  z-index: 2147483646;
  display: flex;
  gap: 0.75rem;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 999px;
  background: rgba(17, 24, 39, 0.92);
  color: white;
  font: 13px/1.4 Inter, system-ui, sans-serif;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.webshield-warning-banner button {
  background: white;
  color: #111827;
  border: none;
  border-radius: 999px;
  padding: 0.3rem 0.7rem;
  cursor: pointer;
}

.webshield-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  z-index: 2147483645;
  background: #f59e0b;
  color: #111827;
  border-radius: 999px;
  padding: 0.2rem 0.5rem;
  font: 11px/1.2 Inter, system-ui, sans-serif;
  font-weight: 700;
}

.webshield-explanation-panel {
  position: fixed;
  top: 64px;
  right: 12px;
  z-index: 2147483646;
  width: 360px;
  max-height: 70vh;
  overflow: auto;
  background: white;
  color: #111827;
  border-radius: 1rem;
  border: 1px solid #d1d5db;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.18);
  transform: translateX(calc(100% + 16px));
  transition: transform 150ms ease;
}

.webshield-explanation-panel.is-open {
  transform: translateX(0);
}

.webshield-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1rem;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: white;
}

.webshield-panel-header button {
  border: none;
  background: transparent;
  font-size: 1.3rem;
  cursor: pointer;
}

.webshield-panel-body {
  padding: 1rem;
  font: 13px/1.5 Inter, system-ui, sans-serif;
}

.webshield-panel-body ul {
  padding-left: 1.2rem;
}

.webshield-replaced {
  display: inline-block;
  padding: 0.35rem 0.55rem;
  border-radius: 0.45rem;
  background: #f3f4f6;
  color: #4b5563;
  font: 13px/1.2 Inter, system-ui, sans-serif;
}
`;function O(e){e.dataset.webshieldOriginalFilter||(e.dataset.webshieldOriginalFilter=e.style.filter||""),e.dataset.webshieldOriginalUserSelect||(e.dataset.webshieldOriginalUserSelect=e.style.userSelect||""),e.dataset.webshieldManaged="true",e.style.filter="blur(10px)",e.style.userSelect="none"}function g(e){e.dataset.webshieldOriginalDisplay||(e.dataset.webshieldOriginalDisplay=e.style.display||""),e.dataset.webshieldManaged="true",e.style.display="none"}function A(e){e.dataset.webshieldOriginalHtml||(e.dataset.webshieldOriginalHtml=e.innerHTML),e.dataset.webshieldManaged="true",e.innerHTML='<span class="webshield-replaced">[Filtered by WebShield]</span>'}function c(){const e=Array.from(document.querySelectorAll("[data-webshield-managed='true']"));for(const t of e)t.dataset.webshieldOriginalDisplay!==void 0&&(t.style.display=t.dataset.webshieldOriginalDisplay),t.dataset.webshieldOriginalFilter!==void 0&&(t.style.filter=t.dataset.webshieldOriginalFilter),t.dataset.webshieldOriginalUserSelect!==void 0&&(t.style.userSelect=t.dataset.webshieldOriginalUserSelect),t.dataset.webshieldOriginalOutline!==void 0&&(t.style.outline=t.dataset.webshieldOriginalOutline),t.dataset.webshieldOriginalPosition!==void 0&&(t.style.position=t.dataset.webshieldOriginalPosition),t.dataset.webshieldOriginalHtml!==void 0&&(t.innerHTML=t.dataset.webshieldOriginalHtml),delete t.dataset.webshieldManaged;document.querySelectorAll(".webshield-badge").forEach(t=>t.remove()),document.querySelectorAll(".webshield-warning-banner").forEach(t=>t.remove()),document.querySelectorAll(".webshield-explanation-panel").forEach(t=>t.remove())}function I(e){e.dataset.webshieldOriginalOutline||(e.dataset.webshieldOriginalOutline=e.style.outline||""),e.dataset.webshieldOriginalPosition||(e.dataset.webshieldOriginalPosition=e.style.position||""),e.dataset.webshieldManaged="true",window.getComputedStyle(e).position==="static"&&(e.style.position="relative"),e.style.outline="2px solid #f59e0b"}function C(e){return e.map(t=>({itemId:t.item_id,action:t.action,explanation:t.explanation,category:t.primary_category}))}function N(e,t){return{url:e.url,title:e.title,text_items:e.text_items,image_items:e.image_items,promo_items:e.promo_items,headings:e.headings,preferences:t}}const m="webshield-explanation-panel";function L(e){var i;const t=document.getElementById(m);t==null||t.remove();const n=document.createElement("aside");n.id=m,n.className="webshield-explanation-panel",n.innerHTML=`
    <div class="webshield-panel-header">
      <strong>WebShield analysis</strong>
      <button type="button" data-action="close">×</button>
    </div>
    <div class="webshield-panel-body">
      <p>${e.summary.explanation}</p>
      <p><strong>Safety score:</strong> ${e.summary.safety_score}/100</p>
      <p><strong>Preference match:</strong> ${e.summary.preference_match.score.toFixed(1)}%</p>
      <p><strong>Top interests:</strong> ${e.summary.preference_match.top_interests.join(", ")||"None"}</p>
      <ul>
        ${e.decisions.filter(a=>a.action!=="allow").slice(0,10).map(a=>`<li><strong>${a.primary_category||"flagged"}</strong> — ${a.action} — ${a.explanation}</li>`).join("")}
      </ul>
    </div>
  `,(i=n.querySelector("[data-action='close']"))==null||i.addEventListener("click",()=>{n.classList.remove("is-open")}),document.body.appendChild(n)}function l(e,t){if(e.querySelector(":scope > .webshield-badge"))return;window.getComputedStyle(e).position==="static"&&(e.style.position="relative");const n=document.createElement("span");n.className="webshield-badge",n.textContent=t,e.appendChild(n)}const h="webshield-warning-banner";function k(e){var i;const t=document.getElementById(h);t==null||t.remove();const n=document.createElement("div");n.id=h,n.className="webshield-warning-banner",n.innerHTML=`
    <strong>WebShield:</strong>
    <span>Score ${e.summary.safety_score}/100 · ${e.summary.status}</span>
    <button type="button" data-action="toggle-panel">Details</button>
  `,(i=n.querySelector("[data-action='toggle-panel']"))==null||i.addEventListener("click",()=>{var a;(a=document.getElementById("webshield-explanation-panel"))==null||a.classList.toggle("is-open")}),document.body.appendChild(n)}let f=0;function s(e,t="ws"){const n=e,i=n.dataset.webshieldId;if(i)return i;f+=1;const a=`${t}-${Date.now().toString(36)}-${f}`;return n.dataset.webshieldId=a,a}function T(e){const t=typeof CSS<"u"&&CSS.escape?CSS.escape(e):e;return document.querySelector(`[data-webshield-id="${t}"]`)}const P=["article p","main p","section p","div","p","li","blockquote","span","h1","h2","h3","h4"],q=["button","a[role='button']","[class*='promo']","[class*='banner']","[class*='offer']","[class*='modal']","[class*='popup']","[class*='dialog']","[id*='popup']","[id*='modal']"],M=["script","style","noscript","code","pre","svg","canvas","nav","footer"],H=["h1","h2","h3"];function w(e){const t=e,n=window.getComputedStyle(t),i=t.getBoundingClientRect();return n.display!=="none"&&n.visibility!=="hidden"&&Number(n.opacity)!==0&&i.width>8&&i.height>8}function u(e){return M.some(t=>e.matches(t)||e.closest(t))}function r(e){return(e.textContent||"").replace(/\s+/g," ").trim()}function $(e){return e.className||""}function R(e){const t=r(e);return!u(e)&&w(e)&&t.length>=20}function B(e){return w(e)&&e.naturalWidth>=80&&e.naturalHeight>=80&&!!(e.currentSrc||e.src)}function x(e){const t=new Set,n=[];for(const i of e){const a=r(i).slice(0,160);!a||t.has(a)||(t.add(a),n.push(i))}return n}function D(){const t=Array.from(document.querySelectorAll(P.join(","))).filter(n=>R(n));return x(t).slice(0,200)}function U(){return Array.from(document.querySelectorAll("img")).filter(t=>B(t)).slice(0,60)}function j(){const t=Array.from(document.querySelectorAll(q.join(","))).filter(n=>!u(n)&&r(n).length>=6);return x(t).slice(0,80)}function W(){return Array.from(document.querySelectorAll(H.join(","))).filter(t=>!u(t)&&r(t).length>=3).slice(0,20)}function z(e=10){return W().slice(0,e).map(t=>({item_id:s(t,"heading"),text:r(t),level:Number(t.tagName.toLowerCase().replace("h",""))||1,page_url:location.href,meta:{}}))}function F(e){return U().slice(0,e).map(t=>({item_id:s(t,"image"),src:t.currentSrc||t.src,alt_text:t.alt||"",width:t.naturalWidth||t.width,height:t.naturalHeight||t.height,tag_name:t.tagName.toLowerCase(),page_url:location.href,meta:{class_name:t.className||""}}))}function G(e){return j().slice(0,e).map(t=>({item_id:s(t,"promo"),text:r(t),tag_name:t.tagName.toLowerCase(),role:t.getAttribute("role")||void 0,class_name:$(t),page_url:location.href,meta:{aria_label:t.getAttribute("aria-label")||""}}))}function X(e){return D().slice(0,e).map(t=>({item_id:s(t,"text"),text:r(t),tag_name:t.tagName.toLowerCase(),page_url:location.href,meta:{class_name:t.className||"",text_length:r(t).length}}))}function V(e){return{url:location.href,title:document.title||location.href,text_items:X(e.max_text_items),image_items:F(e.max_image_items),promo_items:G(e.max_promo_items),headings:z()}}let b=location.href,y=!1;function Y(){if(document.getElementById("webshield-overlay-styles"))return;const e=document.createElement("style");e.id="webshield-overlay-styles",e.textContent=v,document.documentElement.appendChild(e)}function Z(e){c();const t=C(e.decisions);for(const n of t){if(n.action==="allow")continue;const i=T(n.itemId);if(i)switch(n.action){case"warn":I(i),l(i,n.category||"warning");break;case"blur":O(i),l(i,n.category||"blurred");break;case"hide":g(i);break;case"replace":A(i),l(i,n.category||"replaced");break;case"block":g(i);break}}k(e),L(e)}async function p(e="initial"){Y();const t=await _();if(!t.enabled){c();return}if(e==="initial"&&!t.scan_on_load)return;const n=V(t),i=N(n,t);try{const a=await chrome.runtime.sendMessage({type:d.ANALYZE_PAGE,payload:{request:i}});if(!(a!=null&&a.ok))throw new Error((a==null?void 0:a.error)||"Page analysis failed.");Z(a.data)}catch(a){o("Analysis failed",a)}}function J(){setInterval(()=>{location.href!==b&&(b=location.href,p("initial").catch(o))},1500)}function S(){y||(y=!0,p("initial").catch(o),J())}chrome.runtime.onMessage.addListener(e=>{e.type===d.RESCAN_PAGE&&p("manual").catch(o),e.type===d.RESTORE_PAGE&&c()});window.addEventListener("load",S);(document.readyState==="complete"||document.readyState==="interactive")&&S();E("WebShield content script loaded.");
