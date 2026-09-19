# Clauson Geomet website

Static consultancy site hosted by GitHub Pages. There is no package manager, backend or build step.

## Content

- `index.html`: client-facing homepage, experience and release-status cards.
- `approach/index.html`: expanded methodology page.
- `styles.css`, `brand-overrides.css`, `approach.css`: base design and responsive layouts.
- `assets/`: existing approved branding and public CV. These assets have not been replaced in this update.

## Release checklist

The homepage deliberately does not link unreleased resources to a generic GitHub profile.

- [ ] **chRonostatistics:** once released, add its exact public repository/documentation URL to `#chronostatistics` and replace the preparation status. Confirm the package name, install command, README and licence before linking.
- [ ] **Element-to-mineral conversion:** publish the reviewed article and link it from `#element-to-mineral`.
- [ ] **Geometallurgical Drillhole Optimiser:** link the hosted public Shiny app from `#drillhole-optimiser`. Keep source code private; do not upload app code or client data to this public website repository. Confirm app examples and data handling before launch.
- [ ] Add a final custom domain and update canonical/Open Graph URLs on both pages after it is configured.
- [ ] Add a dedicated social-preview image and `og:image` metadata.
- [ ] Review the public CV, permissions and anonymised project summaries before promoting the site widely.

No release date, live app URL or source-code availability is implied by the status cards. Update them when each resource is actually released.

## Local preview

From this folder, run `python3 -m http.server 8000`, then open `http://localhost:8000/`.
Check the homepage and `/approach/` on narrow and wide screens, all section links, the CV and the email links. Do not use a local file preview to test directory URLs.

## Editing safely

Retain the existing `#approach`, `#services`, `#experience`, `#work`, `#research`, `#about` and `#contact` anchors. Change only the relevant status card when releasing a resource. Keep the methodology page concise and client-facing; add references only when they materially support published technical content.
