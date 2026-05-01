#!/usr/bin/env python3
from __future__ import annotations

import codecs
import re
import sys
import urllib.parse
from pathlib import Path

import latexcodec  # noqa: F401  # required by codecs.decode(..., "ulatex")
from jinja2 import Environment, FileSystemLoader
from pybtex.database.input import bibtex


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BIB_PATHS = [
    PROJECT_ROOT / "data" / "samer-lahoud-ref-db.bib",
    Path("/Applications/MAMP/htdocs/mywebpage/docs/img/samer-lahoud-ref-db.bib"),
]
TEMPLATE_PATH = PROJECT_ROOT / "_templates" / "publications.qmd.j2"
OUTPUT_PATH = PROJECT_ROOT / "publications.qmd"


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = codecs.decode(text, "ulatex")
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"\s+,", ",", text)
    return text.strip()


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    doi = clean_text(doi)
    while re.match(r"^https?://(dx\.)?doi\.org/", doi, flags=re.IGNORECASE):
        doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    return doi or None


def find_bib_path() -> Path:
    if len(sys.argv) > 1:
        candidate = Path(sys.argv[1]).expanduser()
        if candidate.exists():
            return candidate
        raise FileNotFoundError(f"BibTeX file not found: {candidate}")

    for candidate in DEFAULT_BIB_PATHS:
        if candidate.exists():
            return candidate

    searched = "\n".join(str(path) for path in DEFAULT_BIB_PATHS)
    raise FileNotFoundError(
        "Could not find a BibTeX file. Checked:\n" + searched + "\n"
        "Pass a path explicitly, e.g. `python3 scripts/generate_publications.py /path/to/file.bib`."
    )


def format_people(persons) -> str:
    authors = []
    for person in persons:
        initials = "".join(
            name[0] + "." for name in (person.first_names + person.middle_names) if name
        )
        last_names = " ".join(person.last_names)
        authors.append(clean_text(f"{initials} {last_names}".strip()))
    return ", ".join(authors) if authors else "No Author"


def build_entry_fields(key: str, entry) -> dict:
    fields: dict[str, str | int | None] = {}
    fields["id"] = urllib.parse.quote(key)

    year_str = clean_text(entry.fields.get("year", "0"))
    fields["year"] = year_str
    try:
        fields["year_int"] = int(year_str)
    except ValueError:
        fields["year_int"] = 0

    fields["title"] = clean_text(entry.fields.get("title", "No Title"))
    fields["author"] = format_people(entry.persons.get("author", []))

    entry_type = entry.type.lower()
    if entry_type == "article":
        fields["venue"] = clean_text(entry.fields.get("journal", ""))
        fields["venue_type"] = "journal"
    elif entry_type == "inproceedings":
        fields["venue"] = clean_text(entry.fields.get("booktitle", ""))
        fields["venue_type"] = "conference"
    elif entry_type in {"incollection", "inbook"}:
        fields["venue"] = clean_text(entry.fields.get("booktitle", ""))
        fields["venue_type"] = "incollection"
    elif entry_type == "book":
        fields["venue"] = clean_text(entry.fields.get("publisher", ""))
        fields["venue_type"] = "book"
    elif "howpublished" in entry.fields:
        fields["venue"] = clean_text(entry.fields.get("howpublished", ""))
        fields["venue_type"] = "misc"
    else:
        fields["venue"] = ""
        fields["venue_type"] = "misc"

    for name in [
        "volume",
        "number",
        "pages",
        "publisher",
        "address",
        "month",
        "editor",
    ]:
        fields[name] = clean_text(entry.fields.get(name, ""))

    fields["doi"] = normalize_doi(entry.fields.get("doi"))
    fields["url"] = entry.fields.get("url")
    fields["pdf"] = entry.fields.get("pdf")
    fields["citation"] = build_citation(fields, entry)
    return fields


def build_citation(fields: dict, entry) -> str:
    parts = [fields["author"], f"**{fields['title']}**"]
    venue_type = fields["venue_type"]

    if venue_type == "journal":
        if fields["venue"]:
            parts.append(f"*{fields['venue']}*")
        details = []
        if fields["volume"]:
            details.append(f"vol. {fields['volume']}")
        if fields["number"]:
            details.append(f"no. {fields['number']}")
        if fields["pages"]:
            details.append(f"pp. {fields['pages']}")
        if details:
            parts.append(", ".join(details))
        date_info = (
            f"{fields['month']} {fields['year']}".strip()
            if fields["month"] and fields["year"]
            else fields["year"]
        )
        if date_info:
            parts.append(f"{date_info}.")
    elif venue_type == "conference":
        if fields["venue"]:
            parts.append(f"*{fields['venue']}*")
        details = []
        if fields["address"]:
            details.append(fields["address"])
        if fields["pages"]:
            details.append(f"pp. {fields['pages']}")
        if details:
            parts.append(", ".join(details))
        date_info = (
            f"{fields['month']} {fields['year']}".strip()
            if fields["month"] and fields["year"]
            else fields["year"]
        )
        if date_info:
            parts.append(f"{date_info}.")
    elif venue_type == "incollection":
        editors = format_people(entry.persons.get("editor", []))
        venue_info = f"In *{fields['venue']}*" if fields["venue"] else ""
        if editors:
            venue_info = f"{venue_info}, edited by {editors}" if venue_info else f"edited by {editors}"
        if venue_info:
            parts.append(venue_info)
        details = []
        if fields["publisher"]:
            details.append(fields["publisher"])
        if fields["address"]:
            details.append(fields["address"])
        if fields["pages"]:
            details.append(f"pp. {fields['pages']}")
        if details:
            parts.append(", ".join(details))
        if fields["year"]:
            parts.append(f"{fields['year']}.")
    elif venue_type == "book":
        if fields["publisher"]:
            parts.append(fields["publisher"])
        details = []
        if fields["address"]:
            details.append(fields["address"])
        if fields["year"]:
            details.append(fields["year"])
        if details:
            parts.append(", ".join(details) + ".")
    else:
        if fields["venue"]:
            parts.append(fields["venue"])
        if fields["year"]:
            parts.append(f"{fields['year']}.")

    citation = ", ".join(part for part in parts if part)
    citation = re.sub(r",\s*\.", ".", citation)
    return citation


def main() -> None:
    bib_path = find_bib_path()

    parser = bibtex.Parser()
    bib_data = parser.parse_file(str(bib_path))

    entries_by_type: dict[str, list[dict]] = {}
    for key, entry in bib_data.entries.items():
        if entry.type.lower() == "techreport":
            continue
        entry_type = entry.type.lower()
        fields = build_entry_fields(key, entry)
        entries_by_type.setdefault(entry_type, []).append(fields)

    type_order = [
        ("article", "Journal Articles"),
        ("inproceedings", "Conference Papers"),
        ("incollection", "Book Chapters"),
        ("book", "Books"),
        ("inbook", "Book Chapters"),
        ("phdthesis", "PhD Theses"),
        ("mastersthesis", "Master's Theses"),
        ("misc", "Miscellaneous"),
    ]

    all_types = set(entries_by_type.keys())
    ordered_types = {name for name, _ in type_order}
    other_types = all_types - ordered_types
    if other_types:
        entries_by_type["other"] = []
        for other_type in sorted(other_types):
            entries_by_type["other"].extend(entries_by_type[other_type])
        type_order.append(("other", "Other Publications"))

    for entry_list in entries_by_type.values():
        entry_list.sort(key=lambda x: (x["year_int"], x["title"]), reverse=True)

    entries_all = []
    for entry_list in entries_by_type.values():
        entries_all.extend(entry_list)
    entries_all.sort(key=lambda x: (x["year_int"], x["title"]), reverse=True)

    entries_by_year: list[dict] = []
    grouped_by_year: dict[int, list[dict]] = {}
    for entry in entries_all:
        grouped_by_year.setdefault(entry["year_int"], []).append(entry)

    for year in sorted(grouped_by_year.keys(), reverse=True):
        entries_by_year.append({"year": year, "entries": grouped_by_year[year]})

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_PATH.parent)))
    template = env.get_template(TEMPLATE_PATH.name)
    rendered = template.render(
        entries_by_type=entries_by_type,
        entries_by_year=entries_by_year,
        type_order=type_order,
        bib_path=str(bib_path),
    )
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    print(f"Generated {OUTPUT_PATH} from {bib_path}")


if __name__ == "__main__":
    main()
