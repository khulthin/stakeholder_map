# SAGA Stakeholder Map

Interactive stakeholder map for [SAGA](https://saga.school) — Danish EdTech for adaptive K-12 learning.

## What's in here

- **`index.html`** — The interactive stakeholder map (self-contained, no dependencies). Open in any browser.
- **`master_stakeholders.json`** — Master data file with all 148 stakeholder records, organization enrichment, and metadata.
- **`build_v7_restructure.py`** — Python build script that generates `index.html` from the master JSON.

## How to use

**Just browse:** Open `index.html` in your browser. Everything is self-contained.

**Rebuild after data changes:**
```bash
python3 build_v7_restructure.py
```
This reads `master_stakeholders.json` and outputs a new HTML file.

## Structure

The map is organized into three main groups:

- **ORGANISATIONER** — Nationalt Politisk, Kommuner, Foreninger & KL, Fonde, Professionshøjskoler, IT-Myndigheder
- **INFLUENCERS** — Psykologer, Forskere, Erhvervsledere, Skolepersoner, Andre (sortable by tier/relevance)
- **MEDIER** — One entry per media outlet

136 unique stakeholders across 62 organizations with search, sorting, and collapsible org groups.
