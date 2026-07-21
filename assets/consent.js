/* macdnie.com — Google Analytics 4, loaded only after explicit consent.
 * Until "Aceptar/Accept" is clicked, gtag.js is never requested: this file
 * injects it, it is never present as a static <script> in page source. */
(function () {
  "use strict";
  var GA_ID = "G-N6JCPVBQ5Q";
  var STORAGE_KEY = "macdnie_consent";
  var banner = document.getElementById("consent-banner");

  function loadGA() {
    if (window.__gaLoaded) return;
    window.__gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID);
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
  }

  function purgeGACookies() {
    var host = location.hostname;
    document.cookie.split(";").forEach(function (entry) {
      var name = entry.split("=")[0].trim();
      if (name.indexOf("_ga") === 0) {
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;";
        document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=" + host + ";";
      }
    });
  }

  function setConsent(value) {
    try { window.localStorage.setItem(STORAGE_KEY, value); } catch (e) {}
    if (value === "granted") {
      loadGA();
    } else {
      purgeGACookies();
    }
  }

  var stored = null;
  try { stored = window.localStorage.getItem(STORAGE_KEY); } catch (e) {}

  if (stored === "granted") {
    loadGA();
  } else if (stored !== "denied" && banner) {
    banner.hidden = false;
  }

  if (banner) {
    var acceptBtn = document.getElementById("consent-accept");
    var rejectBtn = document.getElementById("consent-reject");
    if (acceptBtn) acceptBtn.addEventListener("click", function () {
      setConsent("granted");
      banner.hidden = true;
    });
    if (rejectBtn) rejectBtn.addEventListener("click", function () {
      setConsent("denied");
      banner.hidden = true;
    });
  }

  document.querySelectorAll(".consent-reopen").forEach(function (link) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      if (banner) banner.hidden = false;
    });
  });
})();
