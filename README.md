# Clauson Geomet website

This repository contains the public website for **Clauson Geomet**, my statistical geometallurgy consultancy.

The site is deliberately simple: static HTML and CSS hosted with GitHub Pages, with no backend or build step.

**Website:** https://clausongeomet.com

## What's here

- `index.html` — consultancy homepage, services, experience and current work.
- `approach/` — a longer explanation of the statistical geometallurgy approach.
- `packages/` — public software and package links.
- `tools/` and `drillhole-optimiser/` — public-facing material for analytical tools.
- `assets/` — branding, social preview images and the public CV.
- `styles.css`, `brand-overrides.css`, `approach.css` and `resource-pages.css` — site styling.

Technical writing is maintained separately and published under the site's `/writing/` section.

## Local preview

From the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

When changing the site, check the homepage and `/approach/` at narrow and wide widths, along with navigation, CV and external links.

## A note on project material

The website only contains material intended to be public. Client data, internal project files and source code for private tools stay outside this repository.

Examples from previous industry roles are intentionally anonymised and are clearly separated from work delivered through Clauson Geomet.
