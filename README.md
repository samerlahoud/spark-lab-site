# Spark Lab Website

This repository contains the public Quarto website for Samer Lahoud and Spark Lab.
It is a simplified, maintainable recreation of the existing site at:

- https://web.cs.dal.ca/~lahoud/site/

The site includes profile, lab, research, resources, publications, habilitation,
and contact pages. Publications are generated from a BibTeX database before each
render.

## Requirements

- Quarto
- Python 3
- Python packages used by `scripts/generate_publications.py`:
  - `jinja2`
  - `latexcodec`
  - `pybtex`

## Preview Locally

```bash
quarto preview
```

Quarto will run the pre-render publication generator automatically.

## Build the Site

```bash
quarto render
```

The rendered site is written to `_site/`.

## Publications

The publications page is generated from:

- `data/samer-lahoud-ref-db.bib`

The generator script is:

- `scripts/generate_publications.py`

The generator also supports the legacy BibTeX location:

- `/Applications/MAMP/htdocs/mywebpage/docs/img/samer-lahoud-ref-db.bib`

To regenerate publications manually with a specific BibTeX file:

```bash
python3 scripts/generate_publications.py /path/to/publications.bib
```

## Resources and Artifacts

Student and lab contributions should normally add:

- one artifact folder under `artifacts/`
- one public-facing page under `resources/`
- one entry in `resources/index.qmd`

Use `artifacts/_template/` as the starting point for new research artifacts.
See `CONTRIBUTING.md` for the recommended pull request workflow and resource
checklist.

## Deploy the Site

To render and upload the site to your Dalhousie account:

```bash
./scripts/deploy.sh
```

By default this deploys to:

- `lahoud@timberlea.cs.dal.ca:public_html/`

You can override the destination if needed:

```bash
REMOTE_USER=lahoud REMOTE_HOST=timberlea.cs.dal.ca REMOTE_PATH=public_html/ ./scripts/deploy.sh
```

## Repository Layout

```text
.
├── _quarto.yml
├── data/
├── resources/
├── artifacts/
├── scripts/
├── _templates/
└── _site/
```

- `_quarto.yml` configures the Quarto website and navigation.
- `data/` stores the BibTeX publication source.
- `resources/` contains polished public resource pages.
- `artifacts/` contains structured research material prepared through git.
- `scripts/` contains publication generation and deployment scripts.
- `_templates/` contains the publication page template.
- `_site/` contains the rendered website output.
