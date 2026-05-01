# Simple Quarto Website

This directory contains a simplified Quarto recreation of the existing website at:

- https://web.cs.dal.ca/~lahoud/site/

## Run locally

```bash
quarto preview
```

The publications page is generated automatically before each render from the BibTeX file used by `scripts/generate_publications.py`.

## Build

```bash
quarto render
```

The rendered site is written to `_site/`.

## Deploy

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

## GitHub collaboration

Students should contribute through pull requests.

- See [CONTRIBUTING.md](CONTRIBUTING.md) for the recommended workflow
- Use the `artifacts/` structure for new research materials
- Add polished public entries under `resources/`

## Publications Source

By default, the generator looks for the BibTeX database in one of these locations:

- `data/samer-lahoud-ref-db.bib`
- `/Applications/MAMP/htdocs/mywebpage/docs/img/samer-lahoud-ref-db.bib`

You can also run it manually with an explicit path:

```bash
python3 scripts/generate_publications.py /path/to/publications.bib
```
