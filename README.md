# macdnie.com — marketing & support site

Static, hand-written HTML + shared CSS/JS. **No build step, no dependencies**
(no CDNs, no web fonts, no build tooling). The one deliberate third-party
exception is Google Analytics, loaded only after explicit cookie-banner
consent — see `privacidad.html` §6 and `assets/consent.js`.

## Deploy

Upload the contents of this directory (`www/`) to any static host — GitHub
Pages, Cloudflare Pages, Netlify, an S3 bucket + CloudFront, or a plain nginx
`root`. There is nothing to compile.

- **DNS**: `macdnie.com` is **not configured yet**. Canonical URLs, hreflang,
  `sitemap.xml` and `robots.txt` already point at `https://macdnie.com/`, so
  once DNS + TLS are live nothing needs editing.
- **404**: configure the host to serve `404.html` for missing paths (GitHub
  Pages and Netlify pick it up automatically). It uses root-absolute URLs, so
  it works from any depth.
- Everything else uses relative URLs, so the site also works from a subpath or
  straight from `file://` for local preview.

## File map

```
www/
├── index.html            Spanish home (hero, journeys, privacy pledge, pricing, FAQ, download)
├── privacidad.html       Spanish privacy policy (real, complete)
├── condiciones.html      Spanish terms of use
├── 404.html              not-found page (bilingual, root-absolute links, noindex)
├── en/
│   ├── index.html        English home
│   ├── privacy.html      English privacy policy
│   └── terms.html        English terms of use
├── assets/
│   ├── site.css          the single shared stylesheet (light + dark via tokens)
│   ├── site.js           the only script: hero transcript reveal (reduced-motion aware)
│   ├── favicon.svg       the brand mark (copy of app/src/logo.svg)
│   └── og-source.svg     source for og.png — regenerate with:
│                           rsvg-convert -w 1200 -h 630 assets/og-source.svg -o og.png
├── og.png                1200×630 Open Graph card (generated from og-source.svg)
├── robots.txt
├── sitemap.xml           6 URLs with es/en hreflang alternates
└── scripts/
    └── check-links.py    internal link + anchor + tag-structure checker (stdlib only)
```

## The es/en content-parity rule

Spanish (site root) is the language of record; `/en/` is its mirror. **Every
content change must land in both languages in the same commit**, and every
page must keep its counterpart wired in three places:

1. the `EN`/`ES` toggle in the header,
2. the `English`/`Español` link in the footer,
3. the `hreflang` pair in `<head>` (plus the matching entry in `sitemap.xml`).

`x-default` always points at the Spanish version. Anchors are localized
(`#descargar` ↔ `#download`, `#funciones` ↔ `#features`, `#como-funciona` ↔
`#how-it-works`, `#precio` ↔ `#pricing`); `#faq` is shared.

After any edit, run the checker from `www/`:

```sh
python3 scripts/check-links.py
```

It verifies every internal href/src resolves, every `#anchor` exists in its
target document, and that tags balance; it also prints the external URLs so
they can be spot-checked (all were returning HTTP 200 on 2026-07-10).

## Fact discipline

Every claim on the site traces to the repo: `app/src/i18n.js` (app copy,
guidance flows, the four languages), `docs/app-store.md` (pricing, IAP,
App Store vs direct-download editions), `README.md` (protocol/engine facts).
Do not add capability claims that are not shipped.

## TODOs

- **Mac App Store badge + URL**: the download buttons currently point at
  `#descargar` / `#download` (marked with `TODO` comments in both index
  pages). Replace with the official badge artwork and the real store URL when
  the app is published. Also add the direct-download `.zip` link when
  `scripts/package-devid.sh` artifacts are hosted.
- **DNS**: point `macdnie.com` (+ `www`) at the chosen host; enable TLS.
- **Privacy-policy URL in App Store Connect**: `docs/app-store.md` references
  `https://nexoapex.com/macDNIe/privacidad`; once macdnie.com is live, prefer
  `https://macdnie.com/privacidad.html` and update `LINK_PRIVACY` in
  `app/src/main.js` accordingly (app-side change, outside `www/`).
- **og.png** exists (generated); if the tagline changes, edit
  `assets/og-source.svg` and re-render.
