# Naveen Sunder Academic Website

This repository contains the source for `https://naveensunder.github.io`.

## Edit The Site

- Edit homepage text in `index.md`.
- Edit publications and working papers in `research.md`.
- Edit courses in `teaching.md`.
- Add a newer CV PDF to `CV/`.

## Publish Updates

Run:

```bash
./publish.sh "Update website"
```

The publish script copies the newest PDF from `CV/` to `assets/files/cv.pdf`, commits the site, and pushes to GitHub.

If you only want to sync the CV without publishing:

```bash
./scripts/sync_latest_cv.sh
```

## First-Time GitHub Setup

The repository should be named `naveensunder.github.io` under the `naveensunder` GitHub account. GitHub Pages will serve it at `https://naveensunder.github.io`.
