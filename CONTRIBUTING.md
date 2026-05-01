# Contributing to the Spark Lab Site

This repository hosts the public Quarto website for Samer Lahoud and Spark Lab.

Student contributions are welcome, especially in the `Resources` section.

## Contribution model

Please contribute through a git branch and pull request rather than pushing directly to `main`.

Typical workflow:

```bash
git clone git@github.com:samerlahoud/<repo-name>.git
cd <repo-name>
git checkout -b add-my-resource
```

Make your changes, then:

```bash
git add .
git commit -m "Add resource: short descriptive title"
git push origin add-my-resource
```

Then open a pull request on GitHub.

## What students should add

For a new public resource, the usual contribution is:

- one artifact folder under `artifacts/`
- one public-facing page under `resources/`
- one update to `resources/index.qmd` so the resource appears on the landing page

Recommended files:

```text
artifacts/
  your-resource-slug/
    metadata.yml
    README.md
    preview.png
    scripts/
    data/

resources/
  your-resource-slug.qmd
```

## Minimum expectations for a resource

Each resource should include:

- a title
- a one-sentence summary
- authors or contributors
- a related paper, report, or project
- a link to the artifact, dataset, code, or script
- one preview figure, screenshot, or example result
- a maintainer name

## Public vs internal material

Use this rule:

- `artifacts/` can hold structured research material prepared through git
- `resources/` should contain polished public-facing pages ready to be shown on the website

If something is not ready for public release, it can still be prepared in `artifacts/` first.

## Resource page checklist

Before opening a pull request, please check that your contribution includes:

- a clear overview
- a related paper or citation if available
- access instructions or usage notes
- one preview image or representative result
- links that work
- clean filenames and folder names

## Rendering locally

To preview the site locally:

```bash
quarto preview
```

To build the site:

```bash
quarto render
```

The publications page is generated automatically before render from the BibTeX database.

## Questions

If you are unsure whether a resource is ready for the public site, open a draft pull request first and describe the current state of the material.

