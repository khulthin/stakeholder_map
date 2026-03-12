#!/usr/bin/env python3
"""
Folkeskole Innovationsnetværk – Builder & Management Script
Konsoliderer research-resultater og bygger database + HTML-visning
"""

import json
import re
from datetime import date
from pathlib import Path

DB_FILE = Path("folkeskole_netvaerk.json")
HTML_FILE = Path("netvaerk.html")

SEGMENT_LABELS = {
    "leder_skoleudvikling": "Ledere for skoleudvikling",
    "konsulent_skoleudvikling": "Pædagogiske konsulenter",
    "konsulent_inklusion": "Inklusions- og specialpædagogiske konsulenter",
}

SEGMENT_COLORS = {
    "leder_skoleudvikling": "#1a56db",
    "konsulent_skoleudvikling": "#0e9f6e",
    "konsulent_inklusion": "#e3a008",
}

REQUIRED_FIELDS = ["navn", "titel", "kommune", "segment"]


def load_db():
    if DB_FILE.exists():
        with open(DB_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {
        "meta": {"total_personer": 0, "sidst_opdateret": str(date.today())},
        "personer": [],
    }


def save_db(db):
    db["meta"]["total_personer"] = len(db["personer"])
    db["meta"]["sidst_opdateret"] = str(date.today())
    # Sort by segment, then kommune, then navn
    db["personer"].sort(key=lambda p: (p.get("segment", ""), p.get("kommune", ""), p.get("navn", "")))
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
    print(f"✓ Gemt {len(db['personer'])} personer til {DB_FILE}")


def normalize_person(p):
    """Sikrer alle felter er til stede og normaliserede."""
    defaults = {
        "navn": "",
        "titel": "",
        "kommune": "",
        "afdeling": "",
        "rolle_type": "",
        "fokusområde": "",
        "linkedin_url": "",
        "email": "not publicly available",
        "kilde_url": "",
        "confidence": "medium",
        "segment": "",
        "id": "",
    }
    result = {**defaults, **p}
    # Lav et unikt ID baseret på navn + kommune
    if not result["id"]:
        slug = re.sub(r"[^a-z0-9]", "_", f"{result['navn']}_{result['kommune']}".lower())
        result["id"] = slug
    return result


def merge_persons(existing_list, new_list):
    """Tilføjer nye personer, springer dubletter over (match på navn + kommune)."""
    existing_keys = {(p["navn"].lower().strip(), p["kommune"].lower().strip()) for p in existing_list}
    added = 0
    skipped = 0
    for p in new_list:
        key = (p.get("navn", "").lower().strip(), p.get("kommune", "").lower().strip())
        if not key[0]:  # Spring over hvis ingen navn
            skipped += 1
            continue
        if key in existing_keys:
            skipped += 1
        else:
            existing_list.append(normalize_person(p))
            existing_keys.add(key)
            added += 1
    print(f"  → Tilføjet: {added}, Sprunget over (dublet/tom): {skipped}")
    return existing_list


def add_batch(new_persons):
    """Tilføj en liste af personer til databasen."""
    db = load_db()
    print(f"Nuværende antal: {len(db['personer'])}")
    db["personer"] = merge_persons(db["personer"], new_persons)
    print(f"Nyt antal: {len(db['personer'])}")
    save_db(db)


def stats():
    """Vis statistik over databasen."""
    db = load_db()
    personer = db["personer"]
    print(f"\n{'='*50}")
    print(f"FOLKESKOLE NETVÆRK – STATISTIK")
    print(f"{'='*50}")
    print(f"Total personer: {len(personer)}")
    print()
    for seg, label in SEGMENT_LABELS.items():
        count = sum(1 for p in personer if p.get("segment") == seg)
        print(f"  {label}: {count}")
    print()
    print("Top 20 kommuner:")
    from collections import Counter
    komm_count = Counter(p.get("kommune", "?") for p in personer)
    for k, c in komm_count.most_common(20):
        print(f"  {k}: {c}")
    print()
    conf = Counter(p.get("confidence", "?") for p in personer)
    print("Confidence:")
    for c, n in conf.most_common():
        print(f"  {c}: {n}")
    print(f"{'='*50}\n")


def build_html():
    """Byg HTML-visning af netværksdatabasen."""
    db = load_db()
    personer = db["personer"]
    meta = db["meta"]
    total = len(personer)

    # Byg stats
    seg_counts = {seg: sum(1 for p in personer if p.get("segment") == seg) for seg in SEGMENT_LABELS}
    kommuner = sorted(set(p.get("kommune", "") for p in personer if p.get("kommune")))
    fokus_areas = sorted(set(p.get("fokusområde", "") for p in personer if p.get("fokusområde")))

    # Byg person-kort HTML
    cards_html = ""
    for p in personer:
        seg = p.get("segment", "")
        seg_color = SEGMENT_COLORS.get(seg, "#6b7280")
        seg_label = SEGMENT_LABELS.get(seg, seg)

        linkedin_html = ""
        if p.get("linkedin_url") and p["linkedin_url"].startswith("http"):
            linkedin_html = f'<a href="{p["linkedin_url"]}" target="_blank" class="li-btn">LinkedIn</a>'

        email_html = ""
        if p.get("email") and p["email"] != "not publicly available":
            email_html = f'<a href="mailto:{p["email"]}" class="email-btn">{p["email"]}</a>'

        confidence_class = {"høj": "conf-high", "medium": "conf-med", "lav": "conf-low"}.get(
            p.get("confidence", ""), "conf-med"
        )

        cards_html += f"""
        <div class="card"
             data-segment="{seg}"
             data-kommune="{p.get('kommune','').lower()}"
             data-fokus="{p.get('fokusområde','').lower()}"
             data-navn="{p.get('navn','').lower()}">
            <div class="card-header" style="border-left: 4px solid {seg_color}">
                <div class="card-name">{p.get('navn','')}</div>
                <span class="seg-badge" style="background:{seg_color}20;color:{seg_color}">{seg_label}</span>
            </div>
            <div class="card-body">
                <div class="card-field"><span class="field-label">Titel:</span> {p.get('titel','')}</div>
                <div class="card-field"><span class="field-label">Kommune:</span> {p.get('kommune','')}</div>
                <div class="card-field"><span class="field-label">Afdeling:</span> {p.get('afdeling','') or '–'}</div>
                <div class="card-field"><span class="field-label">Fokus:</span> {p.get('fokusområde','') or '–'}</div>
                <div class="card-actions">
                    {linkedin_html}
                    {email_html}
                    <span class="conf-badge {confidence_class}">{p.get('confidence','?')}</span>
                </div>
            </div>
        </div>"""

    # Kommuner dropdown options
    komm_options = "".join(f'<option value="{k.lower()}">{k}</option>' for k in kommuner)
    fokus_options = "".join(f'<option value="{f.lower()}">{f}</option>' for f in fokus_areas if f)

    html = f"""<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Folkeskole Innovationsnetværk</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f3f4f6; color: #1f2937; }}

  .header {{ background: #1e40af; color: white; padding: 24px 32px; }}
  .header h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; }}
  .header p {{ opacity: 0.85; font-size: 0.9rem; }}

  .stats-bar {{ background: white; border-bottom: 1px solid #e5e7eb; padding: 16px 32px; display: flex; gap: 32px; flex-wrap: wrap; }}
  .stat {{ text-align: center; }}
  .stat-num {{ font-size: 1.8rem; font-weight: 700; color: #1e40af; }}
  .stat-label {{ font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 0.05em; }}
  .stat-num.green {{ color: #0e9f6e; }}
  .stat-num.amber {{ color: #e3a008; }}

  .controls {{ background: white; padding: 16px 32px; border-bottom: 1px solid #e5e7eb; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }}
  .controls input, .controls select {{ padding: 8px 12px; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.875rem; outline: none; }}
  .controls input:focus, .controls select:focus {{ border-color: #1e40af; box-shadow: 0 0 0 3px rgba(30,64,175,0.1); }}
  .controls input {{ width: 260px; }}

  .filter-btns {{ display: flex; gap: 8px; }}
  .filter-btn {{ padding: 7px 14px; border: 1px solid #d1d5db; border-radius: 20px; background: white; cursor: pointer; font-size: 0.8rem; transition: all 0.15s; }}
  .filter-btn:hover {{ background: #eff6ff; border-color: #1e40af; }}
  .filter-btn.active {{ background: #1e40af; color: white; border-color: #1e40af; }}
  .filter-btn.green.active {{ background: #0e9f6e; border-color: #0e9f6e; }}
  .filter-btn.amber.active {{ background: #e3a008; border-color: #e3a008; }}

  .result-info {{ padding: 12px 32px; font-size: 0.85rem; color: #6b7280; background: #f9fafb; border-bottom: 1px solid #e5e7eb; }}

  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; padding: 24px 32px; }}

  .card {{ background: white; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow: hidden; transition: box-shadow 0.2s; }}
  .card:hover {{ box-shadow: 0 4px 12px rgba(0,0,0,0.12); }}
  .card.hidden {{ display: none; }}

  .card-header {{ padding: 14px 16px 10px; }}
  .card-name {{ font-weight: 600; font-size: 0.95rem; margin-bottom: 6px; }}
  .seg-badge {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; font-weight: 500; }}

  .card-body {{ padding: 0 16px 14px; }}
  .card-field {{ font-size: 0.8rem; margin-bottom: 3px; color: #374151; }}
  .field-label {{ font-weight: 500; color: #6b7280; }}

  .card-actions {{ margin-top: 10px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }}
  .li-btn {{ background: #0a66c2; color: white; text-decoration: none; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 500; }}
  .li-btn:hover {{ background: #004182; }}
  .email-btn {{ color: #1e40af; text-decoration: none; font-size: 0.75rem; }}
  .email-btn:hover {{ text-decoration: underline; }}

  .conf-badge {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; margin-left: auto; }}
  .conf-high {{ background: #d1fae5; color: #065f46; }}
  .conf-med {{ background: #fef3c7; color: #92400e; }}
  .conf-low {{ background: #fee2e2; color: #991b1b; }}

  .export-bar {{ position: fixed; bottom: 0; left: 0; right: 0; background: #1e40af; color: white; padding: 10px 32px; display: flex; gap: 16px; align-items: center; font-size: 0.85rem; }}
  .export-btn {{ background: white; color: #1e40af; border: none; padding: 6px 16px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.8rem; }}
  .export-btn:hover {{ background: #eff6ff; }}

  footer {{ height: 60px; }}
</style>
</head>
<body>

<div class="header">
  <h1>Folkeskole Innovationsnetværk</h1>
  <p>National database – konsulenter og ledere inden for skoleudvikling og inklusion · Sidst opdateret: {meta.get('sidst_opdateret', '')}</p>
</div>

<div class="stats-bar">
  <div class="stat"><div class="stat-num">{total}</div><div class="stat-label">Total personer</div></div>
  <div class="stat"><div class="stat-num">{seg_counts.get('leder_skoleudvikling', 0)}</div><div class="stat-label">Ledere</div></div>
  <div class="stat"><div class="stat-num green">{seg_counts.get('konsulent_skoleudvikling', 0)}</div><div class="stat-label">Pæd. konsulenter</div></div>
  <div class="stat"><div class="stat-num amber">{seg_counts.get('konsulent_inklusion', 0)}</div><div class="stat-label">Inklusions-konsulenter</div></div>
  <div class="stat"><div class="stat-num">{len(kommuner)}</div><div class="stat-label">Kommuner</div></div>
  <div class="stat"><div class="stat-num">{sum(1 for p in personer if (p.get('linkedin_url') or '').startswith('http'))}</div><div class="stat-label">Med LinkedIn</div></div>
</div>

<div class="controls">
  <input type="text" id="search" placeholder="Søg navn, titel, fokusområde...">
  <select id="filter-kommune">
    <option value="">Alle kommuner</option>
    {komm_options}
  </select>
  <select id="filter-fokus">
    <option value="">Alle fokusområder</option>
    {fokus_options}
  </select>
  <div class="filter-btns">
    <button class="filter-btn active" data-seg="">Alle</button>
    <button class="filter-btn" data-seg="leder_skoleudvikling">Ledere</button>
    <button class="filter-btn green" data-seg="konsulent_skoleudvikling">Pæd. konsulenter</button>
    <button class="filter-btn amber" data-seg="konsulent_inklusion">Inklusion</button>
  </div>
</div>

<div class="result-info" id="result-info">Viser alle {total} personer</div>

<div class="grid" id="grid">
{cards_html}
</div>

<footer></footer>

<div class="export-bar">
  <span id="export-count">{total} personer i databasen</span>
  <button class="export-btn" onclick="exportCSV()">Eksporter CSV</button>
  <button class="export-btn" onclick="exportLinkedIn()">LinkedIn-liste</button>
  <button class="export-btn" onclick="exportEmails()">Email-liste</button>
</div>

<script>
const data = {json.dumps(personer, ensure_ascii=False)};

let activeSegment = '';
let searchVal = '';
let kommuneVal = '';
let fokusVal = '';

function filterCards() {{
  const cards = document.querySelectorAll('.card');
  let visible = 0;
  cards.forEach(card => {{
    const seg = card.dataset.segment;
    const kom = card.dataset.kommune;
    const fok = card.dataset.fokus;
    const nav = card.dataset.navn;
    const matchSeg = !activeSegment || seg === activeSegment;
    const matchKom = !kommuneVal || kom.includes(kommuneVal);
    const matchFok = !fokusVal || fok.includes(fokusVal);
    const matchSearch = !searchVal || nav.includes(searchVal) ||
      card.querySelector('.card-field')?.textContent.toLowerCase().includes(searchVal);
    const show = matchSeg && matchKom && matchFok && matchSearch;
    card.classList.toggle('hidden', !show);
    if (show) visible++;
  }});
  document.getElementById('result-info').textContent = `Viser ${{visible}} af {total} personer`;
  document.getElementById('export-count').textContent = `${{visible}} synlige / {total} total`;
}}

document.getElementById('search').addEventListener('input', e => {{
  searchVal = e.target.value.toLowerCase();
  filterCards();
}});
document.getElementById('filter-kommune').addEventListener('change', e => {{
  kommuneVal = e.target.value.toLowerCase();
  filterCards();
}});
document.getElementById('filter-fokus').addEventListener('change', e => {{
  fokusVal = e.target.value.toLowerCase();
  filterCards();
}});
document.querySelectorAll('.filter-btn').forEach(btn => {{
  btn.addEventListener('click', () => {{
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    activeSegment = btn.dataset.seg;
    filterCards();
  }});
}});

function getVisiblePersons() {{
  const cards = document.querySelectorAll('.card:not(.hidden)');
  const ids = new Set(Array.from(cards).map(c => c.querySelector('.card-name')?.textContent?.trim()));
  return data.filter(p => ids.has(p.navn));
}}

function exportCSV() {{
  const persons = getVisiblePersons();
  const cols = ['navn','titel','kommune','afdeling','fokusområde','segment','email','linkedin_url','confidence'];
  const header = cols.join(';');
  const rows = persons.map(p => cols.map(c => `"${{(p[c]||'').replace(/"/g,'""')}}"`).join(';'));
  const csv = [header, ...rows].join('\\n');
  const blob = new Blob(['\\ufeff'+csv], {{type:'text/csv;charset=utf-8'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'folkeskole_netvaerk.csv';
  a.click();
}}

function exportLinkedIn() {{
  const persons = getVisiblePersons().filter(p => p.linkedin_url?.startsWith('http'));
  const text = persons.map(p => `${{p.navn}} – ${{p.titel}} – ${{p.kommune}}\\n${{p.linkedin_url}}`).join('\\n\\n');
  const blob = new Blob([text], {{type:'text/plain;charset=utf-8'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'linkedin_liste.txt';
  a.click();
}}

function exportEmails() {{
  const persons = getVisiblePersons().filter(p => p.email && p.email !== 'not publicly available');
  const emails = persons.map(p => p.email).join(';');
  const blob = new Blob([emails], {{type:'text/plain;charset=utf-8'}});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'emails.txt';
  a.click();
}}
</script>
</body>
</html>"""

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ HTML gemt til {HTML_FILE} ({total} personer)")


def import_from_json(filepath):
    """Importer personer fra en JSON-fil og flet ind i databasen."""
    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        persons = data
    elif isinstance(data, dict) and "personer" in data:
        persons = data["personer"]
    else:
        print(f"Ukendt format i {filepath}")
        return
    print(f"Importerer {len(persons)} personer fra {filepath}...")
    add_batch(persons)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Brug: python build_netvaerk.py [stats|html|import <fil>]")
        stats()
    elif sys.argv[1] == "stats":
        stats()
    elif sys.argv[1] == "html":
        build_html()
        print("Åbn netvaerk.html i din browser.")
    elif sys.argv[1] == "import" and len(sys.argv) > 2:
        import_from_json(sys.argv[2])
        build_html()
    else:
        print("Ukendt kommando. Brug: stats | html | import <fil>")
