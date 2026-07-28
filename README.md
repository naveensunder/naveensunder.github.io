# Naveen Sunder Academic Website

This folder contains the source for the academic website:

- `https://naveensunder.github.io`
- `https://www.naveensunder.com` once DNS and GitHub Pages are connected

## Make Changes Live

After editing files in this folder, run this from Terminal:

```bash
cd "/Users/nsunder/Library/CloudStorage/Dropbox/My Academic Website"
./publish.sh "Update website"
```

That script will:

1. Find the newest PDF in `CV/`.
2. Copy it to `assets/files/cv.pdf`.
3. Commit all website changes.
4. Push them to GitHub.

After the push, GitHub Pages usually updates the public website within a few minutes.

## Common Edits

- Edit homepage text in `index.md`.
- Edit publications in `research.md`.
- Edit working papers and works in progress in `working-papers.md`.
- Edit courses in `teaching.md`.
- Add a newer CV PDF to `CV/`; the publish script will automatically use the newest PDF.
- Edit site-wide navigation, name, email, and affiliation in `_config.yml`.
- Edit visual styling in `assets/css/style.scss`.

## Preview Locally

To preview before publishing, rebuild the local preview:

```bash
./scripts/build_preview.py
```

Then serve the preview folder:

```bash
python3 -m http.server 8001 --directory _preview
```

Open:

```text
http://localhost:8001
```

## CV Only

If you only want to update the public CV file locally without publishing:

```bash
./scripts/sync_latest_cv.sh
```

Then run `./publish.sh "Update CV"` when you are ready to put it online.

## GitHub Pages Setup

The GitHub repository should be named exactly:

```text
naveensunder.github.io
```

In GitHub, go to `Settings > Pages` and use:

- Source: `Deploy from a branch`
- Branch: `main`
- Folder: `/ root`

The `CNAME` file sets the custom domain to `www.naveensunder.com`.
