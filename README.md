# Clauson Geomet website

This repository contains the public website for **Clauson Geomet**, my statistical geometallurgy consultancy.

The site is deliberately simple: static HTML and CSS hosted with GitHub Pages, with no backend or build step.

**Website:** https://clausongeomet.com

## What's here

- `index.html` — consultancy homepage, services, experience and current work.
- `approach/` — a longer explanation of the statistical geometallurgy approach.
- `packages/` — public software and package links.
- `tools/` — index of the two interactive educational tools.
- `beat-the-sampler/` — public-facing landing page for the fictional sampling challenge and its separate hosted help guide.
- `drillhole-optimiser/` — landing page for coverage-first specimen planning and the simulated laboratory/IG workflow.
- `demo-landing.css` — shared styles for public demo pages and homepage demo cards.
- `assets/` — branding, social preview images and the public CV.
- `styles.css`, `brand-overrides.css`, `approach.css` and `resource-pages.css` — site styling.

Technical writing is maintained separately and published under the site's `/writing/` section.

## Local preview

From the repository root:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

When changing the site, check the homepage, `/tools/`, `/beat-the-sampler/` and `/drillhole-optimiser/` at narrow and wide widths, along with navigation, CV and external links. The game and DH apps are separately hosted on Posit Connect Cloud. The website pages link to them; they do not bundle private scientific source code or sensitive inputs.

## A note on project material

The website only contains material intended to be public. Client data, internal project files and source code for private tools stay outside this repository.

Examples from previous industry roles are intentionally anonymised and are clearly separated from work delivered through Clauson Geomet.
