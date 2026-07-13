/* macdnie.com — the only script on the site.
 * Reveals the hero's secure-channel transcript line by line, like the real
 * handshake. Without JS (or with reduced motion) every line is simply visible:
 * the class that hides lines is only ever added here. No tracking, no fetches. */
(function () {
  "use strict";
  var t = document.querySelector(".transcript");
  if (!t) return;
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var lines = t.querySelectorAll(".ln");
  if (!lines.length) return;
  t.classList.add("armed");

  var i = 0;
  function next() {
    if (i >= lines.length) return;
    lines[i].classList.add("on");
    i += 1;
    window.setTimeout(next, 620);
  }
  window.setTimeout(next, 420);
})();
