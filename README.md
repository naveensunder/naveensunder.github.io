# Naveen Sunder Academic Website

Source for `https://www.naveensunder.com` (GitHub Pages, repository `naveensunder/naveensunder.github.io`).

## Make Changes Live

After editing files in this folder, run from Terminal:

```bash
cd "/Users/nsunder/Library/CloudStorage/Dropbox/My Academic Website"
./publish.sh "Update website"
```

The script copies the newest PDF in `CV/` to `assets/files/cv.pdf`, commits every change in the folder, and pushes to GitHub. The public site updates within a few minutes.

Everything in the folder is published, including the PDFs in `Published Papers/` and `Working Papers/`. Only put files there that can be public.

## Common Edits

- **Homepage text:** `index.html`.
- **Publications:** `_data/publications.yml`. One record per paper, newest first. Example:

  ```yaml
  - title: Health Insurance and Infant Mortality: Evidence from India
    authors: [Anaka Aiyar, Naveen Sunder]        # full author order; used for the Cite button
    journal: Health Economics
    year: 2024
    doi: ""                                      # optional; adds a Published version link
    pdf: /Published Papers/2024, Health insurance and child mortality (Health Economics).pdf
    section: economics                           # economics | health-policy
    abstract: >
      Text of the abstract.
  ```

- **Working papers and work in progress:** `_data/working_papers.yml`. A paper with a draft PDF goes under `papers:` (fields `title`, `authors`, `version`, `year`, `pdf` and/or `ssrn` link, `abstract`). A paper without a draft goes under `progress:` (fields `title`, `authors`, optional `status`). Put the draft PDF in `Working Papers/`.
- **Courses:** `teaching.html`.
- **Contact and CV pages:** `contact.html`, `cv.html`.
- **Navigation, name, email, profile links (Google Scholar, faculty page):** `_config.yml`.
- **Visual styling:** `assets/css/style.scss`. Fonts are loaded from Google Fonts in `_layouts/default.html`.
- **Department logo:** `assets/images/bentley-econ.png`. Replace the file to change it.
- Add a newer CV PDF to `CV/`; the publish script uses the newest PDF automatically.

## Preview Locally

The preview renders the same templates GitHub Pages uses. First time only:

```bash
python3 -m pip install --user python-liquid pyyaml
```

Then build and serve:

```bash
./scripts/build_preview.py
python3 -m http.server 8001 --directory _preview
```

Open `http://localhost:8001`.

## CV Only

To refresh the public CV file without publishing:

```bash
./scripts/sync_latest_cv.sh
```

## Hosting

GitHub Pages builds the `main` branch from the repository root. `CNAME` sets the custom domain `www.naveensunder.com`. The old `/research/` address redirects to `/publications/`.
