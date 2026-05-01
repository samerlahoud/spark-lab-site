# Contributing to the Spark Lab Site

This repository hosts the public Quarto website for Samer Lahoud and Spark Lab.

Student and lab member contributions are welcome, especially in the `Resources`
section. Team members can use this repository to describe datasets, scripts,
notebooks, reproducibility packages, and other research material.

## Contribution model

Please contribute through a git branch and pull request rather than pushing directly to `main`.

Typical workflow:

```bash
git clone git@github.com:samerlahoud/spark-lab-site.git
cd spark-lab-site
git checkout -b add-my-resource
```

If you do not use SSH with GitHub, clone with HTTPS instead:

```bash
git clone https://github.com/samerlahoud/spark-lab-site.git
cd spark-lab-site
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

Use a short lowercase slug with hyphens, for example `lorawan-measurements-lebanon`.

## Minimum expectations for a resource

Each resource should include:

- a title
- a one-sentence summary
- authors or contributors
- a related paper, report, or project
- a link to the artifact, dataset, code, or script
- one preview figure, screenshot, or example result
- a maintainer name

For datasets, please describe:

- what the data contains
- how it was collected or generated
- file formats and important columns or fields
- where the full dataset is hosted, if it is too large for git
- how the dataset should be cited or acknowledged

For scripts or notebooks, please describe:

- what the script does
- required software, packages, or input files
- how to run it
- expected outputs
- known limitations or assumptions

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

If the material is still being prepared, it is fine to open a draft pull request
with only the `artifacts/` folder and explain what is missing.

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
