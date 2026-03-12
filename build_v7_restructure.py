#!/usr/bin/env python3
"""
V7 — Major restructure: 3 main groups (Organisationer / Influencers / Medier)
+ Sort by tier/relevance + Search function
ALL existing data preserved — only reorganized
"""
import json, re
from collections import OrderedDict

# ══════════════════════════════════════════════
# MUNICIPALITY PRIORITY DATA (from SAGA Opportunity Score CSV)
# ══════════════════════════════════════════════
MUNICIPALITY_DATA = {
    'Slagelse Kommune': {'rank': 1, 'tier': 'Must wins', 'score': 8.16},
    'Næstved Kommune': {'rank': 2, 'tier': 'Must wins', 'score': 7.83},
    'Holbæk Kommune': {'rank': 3, 'tier': 'Must wins', 'score': 7.78},
    'Høje-Taastrup Kommune': {'rank': 4, 'tier': 'Must wins', 'score': 7.64},
    'Brøndby Kommune': {'rank': 5, 'tier': 'Must wins', 'score': 7.44},
    'Kalundborg Kommune': {'rank': 6, 'tier': 'Must wins', 'score': 7.38},
    'Gribskov Kommune': {'rank': 7, 'tier': 'Must wins', 'score': 7.22},
    'Hvidovre Kommune': {'rank': 8, 'tier': 'Must wins', 'score': 7.2},
    'Struer Kommune': {'rank': 9, 'tier': 'Must wins', 'score': 7.17},
    'Halsnæs Kommune': {'rank': 10, 'tier': 'Must wins', 'score': 7.14},
    'Faaborg-Midtfyn Kommune': {'rank': 11, 'tier': 'Must wins', 'score': 7.14},
    'Haderslev Kommune': {'rank': 12, 'tier': 'Must wins', 'score': 7.12},
    'Odsherred Kommune': {'rank': 13, 'tier': 'Must wins', 'score': 7.09},
    'Aalborg Kommune': {'rank': 14, 'tier': 'Must wins', 'score': 6.93},
    'Norddjurs Kommune': {'rank': 15, 'tier': 'Must wins', 'score': 6.9},
    'Langeland Kommune': {'rank': 16, 'tier': 'Must wins', 'score': 6.9},
    'Silkeborg Kommune': {'rank': 17, 'tier': 'Must wins', 'score': 6.9},
    'Hillerød Kommune': {'rank': 18, 'tier': 'Must wins', 'score': 6.84},
    'Stevns Kommune': {'rank': 19, 'tier': 'Must wins', 'score': 6.78},
    'Vejle Kommune': {'rank': 20, 'tier': 'Must wins', 'score': 6.76},
    'Holstebro Kommune': {'rank': 21, 'tier': 'Important', 'score': 6.75},
    'Odense Kommune': {'rank': 22, 'tier': 'Important', 'score': 6.6},
    'Aarhus Kommune': {'rank': 23, 'tier': 'Important', 'score': 6.44},
    'København Kommune': {'rank': 24, 'tier': 'Important', 'score': 6.42},
    'Herlev Kommune': {'rank': 25, 'tier': 'Important', 'score': 6.36},
    'Kolding Kommune': {'rank': 26, 'tier': 'Important', 'score': 6.27},
    'Frederikssund Kommune': {'rank': 27, 'tier': 'Important', 'score': 6.26},
    'Guldborgsund Kommune': {'rank': 28, 'tier': 'Important', 'score': 6.24},
    'Morsø Kommune': {'rank': 29, 'tier': 'Important', 'score': 6.22},
    'Brønderslev Kommune': {'rank': 30, 'tier': 'Important', 'score': 6.21},
    'Herning Kommune': {'rank': 31, 'tier': 'Important', 'score': 6.2},
    'Furesø Kommune': {'rank': 32, 'tier': 'Important', 'score': 6.15},
    'Middelfart Kommune': {'rank': 33, 'tier': 'Important', 'score': 6.05},
    'Lolland Kommune': {'rank': 34, 'tier': 'Important', 'score': 5.88},
    'Kerteminde Kommune': {'rank': 35, 'tier': 'Important', 'score': 5.85},
    'Køge Kommune': {'rank': 36, 'tier': 'Important', 'score': 5.77},
    'Aabenraa Kommune': {'rank': 37, 'tier': 'Important', 'score': 5.74},
    'Helsingør Kommune': {'rank': 38, 'tier': 'Important', 'score': 5.72},
    'Assens Kommune': {'rank': 39, 'tier': 'Important', 'score': 5.69},
    'Frederiksberg Kommune': {'rank': 40, 'tier': 'Important', 'score': 5.68},
    'Albertslund Kommune': {'rank': 41, 'tier': 'Important', 'score': 5.66},
    'Randers Kommune': {'rank': 42, 'tier': 'Important', 'score': 5.64},
    'Solrød Kommune': {'rank': 43, 'tier': 'Important', 'score': 5.63},
    'Frederikshavn Kommune': {'rank': 44, 'tier': 'Important', 'score': 5.57},
    'Fanø Kommune': {'rank': 45, 'tier': 'Important', 'score': 5.37},
    'Læsø Kommune': {'rank': 46, 'tier': 'Important', 'score': 5.37},
    'Samsø Kommune': {'rank': 47, 'tier': 'Important', 'score': 5.37},
    'Ærø Kommune': {'rank': 48, 'tier': 'Important', 'score': 5.37},
    'Faxe Kommune': {'rank': 49, 'tier': 'Important', 'score': 5.29},
    'Rødovre Kommune': {'rank': 50, 'tier': 'Important', 'score': 5.24},
    'Thisted Kommune': {'rank': 51, 'tier': 'Followers', 'score': 5.22},
    'Lejre Kommune': {'rank': 52, 'tier': 'Followers', 'score': 5.2},
    'Roskilde Kommune': {'rank': 53, 'tier': 'Followers', 'score': 5.19},
    'Ringsted Kommune': {'rank': 54, 'tier': 'Followers', 'score': 5.16},
    'Hedensted Kommune': {'rank': 55, 'tier': 'Followers', 'score': 5.16},
    'Ringkøbing-Skjern Kommune': {'rank': 56, 'tier': 'Followers', 'score': 5.15},
    'Rebild Kommune': {'rank': 57, 'tier': 'Followers', 'score': 5.09},
    'Gladsaxe Kommune': {'rank': 58, 'tier': 'Followers', 'score': 5.06},
    'Skive Kommune': {'rank': 59, 'tier': 'Followers', 'score': 5.04},
    'Lyngby-Taarbæk Kommune': {'rank': 60, 'tier': 'Followers', 'score': 5.02},
    'Sorø Kommune': {'rank': 61, 'tier': 'Followers', 'score': 5.0},
    'Favrskov Kommune': {'rank': 62, 'tier': 'Followers', 'score': 4.9},
    'Allerød Kommune': {'rank': 63, 'tier': 'Followers', 'score': 4.9},
    'Gentofte Kommune': {'rank': 64, 'tier': 'Followers', 'score': 4.88},
    'Horsens Kommune': {'rank': 65, 'tier': 'Followers', 'score': 4.85},
    'Ballerup Kommune': {'rank': 66, 'tier': 'Followers', 'score': 4.8},
    'Jammerbugt Kommune': {'rank': 67, 'tier': 'Followers', 'score': 4.74},
    'Greve Kommune': {'rank': 68, 'tier': 'Followers', 'score': 4.72},
    'Glostrup Kommune': {'rank': 69, 'tier': 'Followers', 'score': 4.71},
    'Varde Kommune': {'rank': 70, 'tier': 'Followers', 'score': 4.7},
    'Skanderborg Kommune': {'rank': 71, 'tier': 'Followers', 'score': 4.53},
    'Sønderborg Kommune': {'rank': 72, 'tier': 'Followers', 'score': 4.5},
    'Viborg Kommune': {'rank': 73, 'tier': 'Followers', 'score': 4.49},
    'Esbjerg Kommune': {'rank': 74, 'tier': 'Followers', 'score': 4.44},
    'Nyborg Kommune': {'rank': 75, 'tier': 'Followers', 'score': 4.33},
    'Vesthimmerlands Kommune': {'rank': 76, 'tier': 'Followers', 'score': 4.3},
    'Mariagerfjord Kommune': {'rank': 77, 'tier': 'Followers', 'score': 4.18},
    'Lemvig Kommune': {'rank': 78, 'tier': 'Followers', 'score': 4.15},
    'Rudersdal Kommune': {'rank': 79, 'tier': 'Followers', 'score': 4.13},
    'Odder Kommune': {'rank': 80, 'tier': 'Followers', 'score': 4.03},
    'Nordfyns Kommune': {'rank': 81, 'tier': 'Followers', 'score': 3.92},
    'Egedal Kommune': {'rank': 82, 'tier': 'Followers', 'score': 3.92},
    'Tønder Kommune': {'rank': 83, 'tier': 'Followers', 'score': 3.8},
    'Fredensborg Kommune': {'rank': 84, 'tier': 'Followers', 'score': 3.66},
    'Svendborg Kommune': {'rank': 85, 'tier': 'Followers', 'score': 3.65},
    'Hjørring Kommune': {'rank': 86, 'tier': 'Followers', 'score': 3.62},
    'Billund Kommune': {'rank': 87, 'tier': 'Followers', 'score': 3.61},
    'Tårnby Kommune': {'rank': 88, 'tier': 'Followers', 'score': 3.53},
    'Hørsholm Kommune': {'rank': 89, 'tier': 'Followers', 'score': 3.44},
    'Fredericia Kommune': {'rank': 90, 'tier': 'Followers', 'score': 3.36},
    'Ishøj Kommune': {'rank': 91, 'tier': 'Followers', 'score': 3.33},
    'Ikast-Brande Kommune': {'rank': 92, 'tier': 'Followers', 'score': 3.1},
    'Vejen Kommune': {'rank': 93, 'tier': 'Followers', 'score': 3.07},
    'Vordingborg Kommune': {'rank': 94, 'tier': 'Followers', 'score': 2.85},
    'Dragør Kommune': {'rank': 95, 'tier': 'Followers', 'score': 2.68},
    'Bornholm Kommune': {'rank': 96, 'tier': 'Followers', 'score': 2.55},
    'Vallensbæk Kommune': {'rank': 97, 'tier': 'Followers', 'score': 2.48},
    'Syddjurs Kommune': {'rank': 98, 'tier': 'Followers', 'score': 2.37},
}

# Normalize canonical_org names to match MUNICIPALITY_DATA keys
CANONICAL_NORMALIZE = {
    'Københavns Kommune': 'København Kommune',
    'Københavns Kommune (tidl.)': 'København Kommune',
    'Nordfyn': 'Nordfyns Kommune',
}

TIER_CLASS = {'Must wins': 'mw', 'Important': 'imp', 'Followers': 'fol'}

# Segment → tier mapping for folkeskole_netvaerk persons
SEGMENT_TIER = {
    'leder_skoleudvikling': 2,
    'konsulent_skoleudvikling': 3,
    'konsulent_inklusion': 3,
}
SEGMENT_ROLE = {
    'leder_skoleudvikling': 'Leder, skoleudvikling',
    'konsulent_skoleudvikling': 'Konsulent, skoleudvikling',
    'konsulent_inklusion': 'Konsulent, inklusion',
}

with open('master_stakeholders.json') as f:
    data = json.load(f)

master = data['stakeholders']
org_data = data['organizations']
org_enrichment = data.get('org_enrichment', {})

# Load folkeskole_netvaerk and convert to master-compatible format
with open('folkeskole_netvaerk.json') as f:
    netvaerk_data = json.load(f)

# Names already in master (kommunal sections) — for deduplication
master_kommunal_names = set()
for s in master:
    sec = s.get('section', '')
    if sec in ('Kommunale Skolechefer', 'Kommunalt', 'Kommuner', 'Skoleniveau'):
        master_kommunal_names.add(s.get('name', '').lower().strip())

def normalize_kommune(k):
    """Normalize netvaerk kommune name to match MUNICIPALITY_DATA key"""
    k = k.strip()
    k = CANONICAL_NORMALIZE.get(k, k)
    if not k.endswith(' Kommune'):
        k = k + ' Kommune'
    k = CANONICAL_NORMALIZE.get(k, k)
    return k

netvaerk_persons = []
for p in netvaerk_data['personer']:
    name = p.get('navn', '').strip()
    if not name:
        continue
    # Skip duplicates already in master
    if name.lower() in master_kommunal_names:
        continue
    raw_kommune = p.get('kommune', '').strip()
    if not raw_kommune:
        continue
    canon = normalize_kommune(raw_kommune)
    # Only include persons belonging to a known municipality
    if canon not in MUNICIPALITY_DATA:
        continue
    segment = p.get('segment', '')
    tier = SEGMENT_TIER.get(segment, 3)
    role = p.get('titel', '') or SEGMENT_ROLE.get(segment, 'Kommunal konsulent')
    np_person = {
        'name': name,
        'role': role,
        'title': p.get('titel', ''),
        'organization': canon,
        'canonical_org': canon,
        'section': 'Kommuner',
        'tier': tier,
        'pipeline': '',
        'relevance_score': None,
        'linkedin': p.get('linkedin_url', ''),
        'email': p.get('email', ''),
        'phone': p.get('afdeling', '') if p.get('afdeling', '').startswith('Tlf') else '',
        'baggrund': p.get('fokusområde', ''),
        'fokus': '',
        'saga_relevans': '',
        'abm_strategy': '',
        '_source': 'folkeskole_netvaerk',
        '_sort_key': 2,
        'new_group': 'KOMMUNER',
        'new_section': canon,
    }
    netvaerk_persons.append(np_person)

print(f"Netvaerk: {len(netvaerk_persons)} nye (efter deduplication)")

# ══════════════════════════════════════════════
# NEW STRUCTURE MAPPING
# old section → (new_group, new_section)
# Groups: ORGANISATIONER, INFLUENCERS, MEDIER
# ══════════════════════════════════════════════

# We need per-stakeholder mapping since some sections split
def assign_new_group(s):
    """Returns (group, section, subsort_key) for a stakeholder"""
    sec = s['section']
    name = s['name']
    org = s.get('organization', '')

    # MEDIER — all from Medier & Journalister
    if sec == 'Medier & Journalister':
        return ('MEDIER', 'Medier', 0)

    # ORGANISATIONER
    if sec == 'Nationalt Politisk':
        return ('ORGANISATIONER', 'Nationalt Politisk', 0)
    if sec in ('Kommunalt', 'Kommunale Skolechefer', 'Kommuner'):
        canon = s.get('canonical_org', '')
        canon = CANONICAL_NORMALIZE.get(canon, canon)
        # Only real municipalities (canonical_org ends with "Kommune") go to KOMMUNER
        if canon.endswith('Kommune'):
            return ('KOMMUNER', canon, 1)
        # KL, BKF and other associations go to Foreninger & KL
        return ('ORGANISATIONER', 'Foreninger & KL', 2)
    if sec == 'Foreninger':
        return ('ORGANISATIONER', 'Foreninger & KL', 2)
    if sec == 'Fonde':
        return ('ORGANISATIONER', 'Fonde', 3)
    if sec == 'Professionshøjskoler':
        return ('ORGANISATIONER', 'Professionshøjskoler', 4)
    if sec == 'IT-Myndigheder':
        return ('ORGANISATIONER', 'IT-Myndigheder', 5)

    # INFLUENCERS
    if sec == 'Nøglepersoner (Influencers)':
        # Categorize by background
        if any(k in org for k in ['Psykolog', 'psykolog']):
            return ('INFLUENCERS', 'Psykologer', 0)
        if any(k in org for k in ['DPU', 'AAU', 'VIA UC', 'LIFE', 'RISING', 'STABIL', 'DECLINING']):
            # Determine if researcher or other
            if any(k in org for k in ['DPU', 'AAU', 'VIA UC']):
                return ('INFLUENCERS', 'Forskere', 1)
            if 'LIFE' in org:
                return ('INFLUENCERS', 'Forskere', 1)
            # Rising/Stabil/Declining people
            if any(k in org for k in ['DLF', 'Skoleleder']):
                return ('INFLUENCERS', 'Skolepersoner', 2)
            return ('INFLUENCERS', 'Andre', 3)
        if 'DLF' in org or 'Skoleleder' in org:
            return ('INFLUENCERS', 'Skolepersoner', 2)
        return ('INFLUENCERS', 'Andre', 3)

    if sec == 'Psykologer & Forskere':
        if 'psykolog' in org.lower() or 'privatpraksis' in org.lower():
            return ('INFLUENCERS', 'Psykologer', 0)
        return ('INFLUENCERS', 'Forskere', 1)

    if sec == 'Vidensinstitutioner':
        return ('INFLUENCERS', 'Forskere', 1)

    if sec == 'Erhvervsledere':
        return ('INFLUENCERS', 'Erhvervsledere', 2)

    if sec == 'Skoleniveau':
        return ('INFLUENCERS', 'Skolepersoner', 2)

    # Fallback
    return ('ORGANISATIONER', sec, 99)


# ══════════════════════════════════════════════
# Build new structure
# ══════════════════════════════════════════════

# Assign new_group and new_section to each stakeholder
for s in master:
    g, sec, sort_key = assign_new_group(s)
    s['new_group'] = g
    s['new_section'] = sec
    s['_sort_key'] = sort_key

# Deduplicate: keep each person only once, choosing the richest entry
# Priority: Nøglepersoner version often has less data than Vidensinstitutioner/Foreninger/etc.
# So we prefer the non-Nøglepersoner entry, or the one with more data
from collections import defaultdict
name_entries = defaultdict(list)
for s in master:
    name_entries[s['name']].append(s)

deduped_master = []
seen_names_in_layout = set()
for s in master:
    name = s['name']
    if name in seen_names_in_layout:
        continue
    entries = name_entries[name]
    if len(entries) == 1:
        deduped_master.append(s)
    else:
        # Pick the best entry: prefer non-Nøglepersoner, then most data
        def score_entry(e):
            score = 0
            if e['section'] != 'Nøglepersoner (Influencers)':
                score += 100  # prefer non-influencer entry (has org context)
            if e.get('v1_profile'):
                score += 10
            if e.get('baggrund') and len(e.get('baggrund','')) > 50:
                score += 5
            if e.get('linkedin'):
                score += 3
            if e.get('email'):
                score += 2
            return score
        best = max(entries, key=score_entry)
        # But keep the new_group/section from the Nøglepersoner entry if it was INFLUENCERS
        # since that's where we want influencers to show up
        inf_entry = next((e for e in entries if e['section'] == 'Nøglepersoner (Influencers)'), None)
        if inf_entry and best['section'] != 'Nøglepersoner (Influencers)':
            # Person has dual role: keep in INFLUENCERS group but use richer data
            best = dict(best)  # copy
            best['new_group'] = inf_entry['new_group']
            best['new_section'] = inf_entry['new_section']
            best['_sort_key'] = inf_entry['_sort_key']
        deduped_master.append(best)
    seen_names_in_layout.add(name)

print(f"Deduplication: {len(master)} → {len(deduped_master)} (removed {len(master)-len(deduped_master)} duplicates)")
layout_master = deduped_master

# Group hierarchy: group → section → org → people
GROUPS = OrderedDict()
GROUPS['ORGANISATIONER'] = OrderedDict()
GROUPS['INFLUENCERS'] = OrderedDict()
GROUPS['MEDIER'] = OrderedDict()
GROUPS['KOMMUNER'] = OrderedDict()

# Section order within each group
ORG_SECTIONS = ['Nationalt Politisk', 'Foreninger & KL', 'Fonde', 'Professionshøjskoler', 'IT-Myndigheder']
INF_SECTIONS = ['Psykologer', 'Forskere', 'Erhvervsledere', 'Skolepersoner', 'Andre']
MED_SECTIONS = ['Medier']

for sec in ORG_SECTIONS:
    GROUPS['ORGANISATIONER'][sec] = []
for sec in INF_SECTIONS:
    GROUPS['INFLUENCERS'][sec] = []
for sec in MED_SECTIONS:
    GROUPS['MEDIER'][sec] = []

for s in layout_master:
    g = s['new_group']
    sec = s['new_section']
    if sec not in GROUPS[g]:
        GROUPS[g][sec] = []
    GROUPS[g][sec].append(s)

# Add folkeskole_netvaerk persons to KOMMUNER
for np in netvaerk_persons:
    canon = np['canonical_org']
    if canon not in GROUPS['KOMMUNER']:
        GROUPS['KOMMUNER'][canon] = []
    GROUPS['KOMMUNER'][canon].append(np)

# Add all 98 municipalities from CSV (even those with no stakeholders yet)
for mname in MUNICIPALITY_DATA:
    if mname not in GROUPS['KOMMUNER']:
        GROUPS['KOMMUNER'][mname] = []

# Sort municipalities by priority_rank
GROUPS['KOMMUNER'] = OrderedDict(
    sorted(GROUPS['KOMMUNER'].items(),
           key=lambda x: MUNICIPALITY_DATA.get(x[0], {}).get('rank', 999))
)

# For Foreninger & KL: also move the KL org-level stakeholder
# (the one named "KL (Kommunernes Landsforening)" currently in Kommunalt)
# Actually we keep them where they are mapped — the "Foreninger & KL" name covers it

# ══════════════════════════════════════════════
# Organization grouping within each section
# ══════════════════════════════════════════════

def get_org_key(s):
    """Get the organization group key for a stakeholder"""
    co = s.get('canonical_org', '')
    if co:
        return co
    return s.get('organization', 'Øvrige')

def build_org_groups(people):
    """Group a list of people by their canonical org"""
    groups = OrderedDict()
    for p in people:
        key = get_org_key(p)
        if key not in groups:
            groups[key] = []
        groups[key].append(p)
    return groups

# For MEDIER, group by media outlet
def get_media_key(s):
    org = s.get('organization', '')
    co = s.get('canonical_org', '')
    if co:
        return co
    if 'Folkeskolen' in org or 'folkeskolen' in org.lower():
        return 'Folkeskolen.dk'
    if 'Skolemonitor' in org:
        return 'Skolemonitor'
    if 'Uddannelsesmonitor' in org:
        return 'Uddannelsesmonitor'
    if 'Altinget' in org or 'Mandag Morgen' in org:
        return 'Altinget: Uddannelse'
    if 'Politiken' in org:
        return 'Politiken'
    if 'DR' in org:
        return 'DR'
    return org

# ══════════════════════════════════════════════
# Section descriptions (from old org_data, adapted)
# ══════════════════════════════════════════════

SECTION_DESCRIPTIONS = {
    'Nationalt Politisk': {
        'desc': 'Politikere og styrelser der sætter den nationale retning for uddannelse og teknologi i folkeskolen.',
        'saga': 'Top-down legitimering. Ministeriel endorsement åbner kommunale døre. Policy briefs og succespiloter er nøglen.'
    },
    'Kommuner': {
        'desc': 'Kommuner er de reelle indkøbere af skole-IT. Budget-beslutninger, pilotprojekter og skalering sker her. 28 skolechefer fra de største kommuner + kommunalpolitikere og KL-repræsentanter.',
        'saga': 'Pilot-samarbejder med progressive kommuner → succeshistorier → KL-spredning til 98 kommuner.'
    },
    'Foreninger & KL': {
        'desc': 'Fagforeninger, interesseorganisationer og KL (Kommunernes Landsforening) der former holdninger til teknologi i skolen.',
        'saga': 'SAGA må ALDRIG opfattes som erstatning for lærere. Positionér som lærer-empowerment og inklusionsstøtte. KL er nøglen til 98 kommuner.'
    },
    'Fonde': {
        'desc': 'Danske fonde investerer massivt i uddannelse. LEGO Fonden alene giver 2.8 mia DKK/år. Solid evidens er nøglen til funding.',
        'saga': 'Evidens-drevet pitch. Pilotresultater → fondsansøgning → skalering. Hver fond har forskellige fokusområder.'
    },
    'Professionshøjskoler': {
        'desc': 'Professionshøjskolerne uddanner fremtidens lærere. Integration i læreruddannelsen sikrer SAGA-kompetencer fra dag 1.',
        'saga': 'SAGA som del af læreruddannelsen → kommende lærere kender produktet → organisk adoption i skolerne.'
    },
    'IT-Myndigheder': {
        'desc': 'Gatekeepers for digital infrastruktur i skoler. STIL og KOMBIT styrer UNI-Login og AULA.',
        'saga': 'STIL-alignment er KRITISK for adgang til skoler. UNI-Login integration og GDPR-compliance er must-haves.'
    },
    'Psykologer': {
        'desc': 'Psykologer der former narrativet om børns trivsel, mental sundhed og digital skærmtid.',
        'saga': 'SAGA som trivsel-værktøj, ikke skærm-tid. Tidlig involvering af tech-skeptikere er afgørende.'
    },
    'Forskere': {
        'desc': 'Forskere fra DPU, AAU, VIA UC og andre institutioner der leverer akademisk validering og former uddannelsesdebatten.',
        'saga': 'Forsknings-partnership → peer-reviewed evidens → fondenes og politikernes tillid.'
    },
    'Erhvervsledere': {
        'desc': 'Erhvervslivet og EdTech-økosystemet. EdTech Denmark er det direkte peer-netværk med 70+ medlemmer.',
        'saga': 'EdTech Denmark membership ASAP. DI-endorsement = arbejdsmarkedsrelevans. Investor-dialog med tech-ledere.'
    },
    'Skolepersoner': {
        'desc': 'Lærere, skoleledere, elever og forældre — SAGA\'s primære slutbrugere og de vigtigste ambassadører.',
        'saga': 'Bottom-up adoption: lærere → læringsvejledere → skoleledere → kommune. Viral spredning via word-of-mouth.'
    },
    'Andre': {
        'desc': 'Tværgående influencers fra politik, innovation og uddannelse der former den offentlige debat.',
        'saga': 'Identificér rising voices for tidlig alliance-building. Advisory board-potentiale.'
    },
    'Medier': {
        'desc': 'Uddannelsesmedierne former den offentlige debat. Folkeskolen.dk når 50.000+ lærere direkte.',
        'saga': 'Eksklusivt interview + pilotdata → presseomtale → politisk opmærksomhed → kommunal legitimitet.'
    },
}

# ══════════════════════════════════════════════
# Save updated master
# ══════════════════════════════════════════════

data['stakeholders'] = master
data['meta']['version'] = '7.0'
data['meta']['description'] = 'V7: Reorganized into Organisationer/Influencers/Medier with sort+search'
with open('master_stakeholders.json', 'w') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved master JSON v7.0")

# ══════════════════════════════════════════════
# Build HTML
# ══════════════════════════════════════════════

TIER_LABELS = {1: 'Tier 1', 2: 'Tier 2', 3: 'Tier 3'}
TIER_FULL = {
    1: 'Tier 1 — Strategisk prioritet',
    2: 'Tier 2 — Vigtig stakeholder',
    3: 'Tier 3 — Awareness & netværk',
}

def esc(t):
    if not t: return ""
    return str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;').replace("'","&#39;")

def mkid(name):
    s = name.lower().replace('ø','oe').replace('æ','ae').replace('å','aa')
    s = s.replace('&','--').replace('(','').replace(')','')
    s = re.sub(r'[^a-z0-9-]','-',s)
    return re.sub(r'-+','-',s).strip('-')

tg = {1:('#1b7a3d','#2da85a'),2:('#6d28d9','#8b5cf6'),3:('#b45309','#d97706')}

# Build date (Danish month name)
import datetime as _dt
_da_months = ['januar','februar','marts','april','maj','juni','juli','august','september','oktober','november','december']
build_date = f"{_da_months[_dt.date.today().month - 1]} {_dt.date.today().year}"

# Count stats — all persons (master + netvaerk)
lm = layout_master
all_persons = lm + netvaerk_persons
total_count = len(all_persons)
t1=sum(1 for r in all_persons if r['tier']==1)
t2=sum(1 for r in all_persons if r['tier']==2)
t3=sum(1 for r in all_persons if r['tier']==3)
li=sum(1 for r in all_persons if r.get('linkedin'))
ct=sum(1 for r in all_persons if r.get('email') or r.get('phone'))

# Count per group
org_count = sum(1 for s in lm if s['new_group'] == 'ORGANISATIONER')
inf_count = sum(1 for s in lm if s['new_group'] == 'INFLUENCERS')
med_count = sum(1 for s in lm if s['new_group'] == 'MEDIER')
kom_count = sum(1 for s in lm if s['new_group'] == 'KOMMUNER') + len(netvaerk_persons)

building_svg = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M3 21h18v-2H3v2zm0-4h4v-2H3v2zm6 0h4v-2H9v2zm6 0h4v-2h-4v2zM3 13h4v-2H3v2zm6 0h4v-2H9v2zm6 0h4v-2h-4v2zM3 9h4V7H3v2zm6 0h4V7H9v2zm6 0h4V7h-4v2zM3 5h18V3H3v2z"/></svg>'

H = []
H.append(f'''<!DOCTYPE html>
<html lang="da">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SAGA Stakeholder Map</title>
<style>
:root{{--o:#e8913a;--r:#d4543a;--bg:#faf9f7;--c:#fff;--tx:#1a1a1a;--m:#888;--b:#e8e4de;--t1:#1b7a3d;--t1b:#ecf8f0;--t2:#7c3aed;--t2b:#f5f0ff;--t3:#b45309;--t3b:#fef9ee}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--tx);display:flex;min-height:100vh;line-height:1.5}}

/* Sidebar */
.sb{{width:260px;min-width:260px;background:#18181b;position:fixed;top:0;left:0;height:100vh;overflow-y:auto;z-index:100;padding:20px 14px}}
.sb::-webkit-scrollbar{{width:4px}}.sb::-webkit-scrollbar-thumb{{background:#333;border-radius:2px}}
.logo{{font-size:22px;font-weight:800;letter-spacing:2px;background:linear-gradient(135deg,var(--o),var(--r));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.sb-bdg{{font-size:9px;padding:2px 6px;border-radius:4px;background:rgba(232,145,58,.15);color:var(--o);font-weight:600;letter-spacing:.5px;margin-left:8px}}
.sb-s{{color:#555;font-size:11px;margin:4px 0 16px 0}}
/* Search */
.sb-search{{position:relative;margin-bottom:16px}}
.sb-search input{{width:100%;padding:7px 10px 7px 30px;background:#2a2a2e;border:1px solid #3a3a3e;border-radius:8px;color:#ddd;font-size:12px;outline:none;transition:border .2s}}
.sb-search input:focus{{border-color:var(--o)}}
.sb-search input::placeholder{{color:#666}}
.sb-search svg{{position:absolute;left:8px;top:50%;transform:translateY(-50%);width:14px;height:14px;fill:#666}}
/* Nav groups */
.ng{{margin-bottom:14px}}
.ng-h{{color:var(--o);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:1px;padding:4px 10px;display:flex;justify-content:space-between;align-items:center}}
.ng-h .ng-c{{font-size:9px;color:#555;font-weight:400;background:rgba(232,145,58,.1);padding:1px 6px;border-radius:6px}}
.sb a{{display:flex;align-items:center;justify-content:space-between;color:#777;text-decoration:none;padding:5px 10px;border-radius:6px;font-size:12px;transition:all .15s;margin-bottom:1px}}
.sb a:hover{{background:rgba(255,255,255,.06);color:#ccc}}.sb a.active{{background:rgba(232,145,58,.12);color:#fff;font-weight:500}}
.nc{{font-size:10px;color:#555;background:rgba(255,255,255,.05);padding:1px 5px;border-radius:6px}}
/* Municipality rank badges (nav) */
.rnk{{font-size:9px;font-weight:700;padding:1px 5px;border-radius:4px;margin-right:4px;flex-shrink:0;letter-spacing:.2px}}
.rnk.mw{{background:#dc2626;color:#fff}}.rnk.imp{{background:#d97706;color:#fff}}.rnk.fol{{background:#444;color:#888}}
/* Tier badge (section header) */
.tier-bdg{{font-size:10px;font-weight:600;padding:2px 8px;border-radius:8px;margin-left:8px;vertical-align:middle}}
.tier-bdg.mw{{background:#fef2f2;color:#dc2626;border:1px solid #fca5a5}}
.tier-bdg.imp{{background:#fffbeb;color:#d97706;border:1px solid #fde68a}}
.tier-bdg.fol{{background:#f4f4f5;color:#71717a;border:1px solid #d4d4d8}}
/* Empty municipality placeholder */
.kom-empty{{padding:16px;color:#aaa;font-size:12px;font-style:italic;border:1px dashed #e0ddd8;border-radius:8px;text-align:center}}
/* Stats */
.ss{{margin-top:14px;padding-top:14px;border-top:1px solid #2a2a2a}}
.sr{{display:flex;justify-content:space-between;padding:2px 10px;font-size:10px}}.sr .l{{color:#555}}.sr .v{{color:#777;font-weight:600}}

/* Main */
.mn{{margin-left:260px;flex:1;padding:32px 40px;max-width:1000px}}
.pt{{font-size:28px;font-weight:800;letter-spacing:-.5px;background:linear-gradient(135deg,var(--o),var(--r));-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.ps{{color:#666;font-size:13px;margin:4px 0 12px 0}}

/* Search bar main */
.main-search{{position:relative;margin-bottom:28px;max-width:480px}}
.main-search input{{width:100%;padding:10px 14px 10px 38px;background:var(--c);border:1px solid var(--b);border-radius:10px;font-size:14px;color:var(--tx);outline:none;transition:border .2s,box-shadow .2s}}
.main-search input:focus{{border-color:var(--o);box-shadow:0 0 0 3px rgba(232,145,58,.12)}}
.main-search input::placeholder{{color:#aaa}}
.main-search svg{{position:absolute;left:12px;top:50%;transform:translateY(-50%);width:16px;height:16px;fill:#aaa}}
.search-count{{position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:11px;color:var(--m);display:none}}

/* Sort bar (for Influencers) */
.sort-bar{{display:flex;gap:8px;margin-bottom:16px;align-items:center;flex-wrap:wrap}}
.sort-bar label{{font-size:11px;color:var(--m);font-weight:600}}
.sort-btn{{font-size:11px;padding:4px 12px;border-radius:6px;border:1px solid var(--b);background:var(--c);color:#666;cursor:pointer;transition:all .15s}}
.sort-btn:hover{{border-color:var(--o);color:var(--o)}}
.sort-btn.active{{background:var(--o);color:#fff;border-color:var(--o)}}

/* Group header */
.gh{{font-size:18px;font-weight:800;letter-spacing:-.3px;color:var(--tx);padding:20px 0 8px;border-bottom:2px solid var(--b);margin-bottom:16px;display:flex;align-items:center;gap:10px}}
.gh-icon{{width:28px;height:28px;border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.gh-icon svg{{width:16px;height:16px;fill:#fff}}
.gh-org{{background:linear-gradient(135deg,var(--o),var(--r))}}.gh-inf{{background:linear-gradient(135deg,#6d28d9,#8b5cf6)}}
.gh-med{{background:linear-gradient(135deg,#2563eb,#3b82f6)}}.gh-kom{{background:linear-gradient(135deg,#059669,#10b981)}}

/* Section */
.sec{{margin-bottom:36px}}
.sh{{display:flex;align-items:flex-start;justify-content:space-between;padding-bottom:10px;border-bottom:1px solid #f0ede5;margin-bottom:12px}}
.st{{font-size:16px;font-weight:700}}.sc_{{font-size:11px;color:var(--m);background:#f0ede5;padding:2px 8px;border-radius:10px;margin-top:3px;white-space:nowrap}}
.sec-desc{{background:linear-gradient(135deg,#fdfcfa,#f8f6f2);border:1px solid var(--b);border-radius:10px;padding:12px 16px;margin-bottom:14px;font-size:12px}}
.sec-desc .od{{color:#666;line-height:1.5}}.sec-desc .os{{color:var(--o);font-weight:500;margin-top:4px}}

/* Organization group */
.og{{margin-bottom:16px;border:1px solid #e8e4de;border-radius:12px;overflow:hidden;background:#fff}}
.og-h{{padding:12px 16px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;background:linear-gradient(135deg,#fdfcfa,#f7f5f0);border-bottom:1px solid transparent;user-select:none;transition:background .15s}}
.og.open .og-h{{border-bottom-color:#f0ede5}}
.og-h:hover{{background:linear-gradient(135deg,#faf8f5,#f2efe8)}}
.og-left{{display:flex;align-items:center;gap:10px;flex:1;min-width:0}}
.og-icon{{width:32px;height:32px;border-radius:7px;background:linear-gradient(135deg,var(--o),var(--r));display:flex;align-items:center;justify-content:center;flex-shrink:0}}
.og-icon svg{{width:16px;height:16px;fill:#fff}}
.og-info{{min-width:0}}
.og-name{{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.og-meta{{font-size:10px;color:var(--m);display:flex;gap:8px;flex-wrap:wrap}}
.og-right{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.og-link{{font-size:10px;color:#2563eb;text-decoration:none;padding:3px 8px;background:#eff6ff;border-radius:5px;white-space:nowrap}}
.og-link:hover{{background:#dbeafe}}
.og-cnt{{font-size:10px;color:var(--m);background:#f0ede5;padding:2px 7px;border-radius:6px}}
.og-cv{{font-size:12px;color:#ccc;transition:transform .2s;margin-left:2px}}.og.open .og-cv{{transform:rotate(180deg)}}
.og-detail{{display:none;padding:10px 16px 6px;background:#fefefe;border-bottom:1px solid #f0ede5;font-size:12px;color:#555;line-height:1.6}}.og.open .og-detail{{display:block}}
.og-detail p{{margin:0 0 4px}}.og-detail .og-lbl{{font-weight:600;color:var(--tx);font-size:11px}}
.og-detail .og-lbl-e{{color:#1e40af}}.og-detail .og-lbl-a{{color:#854d0e}}.og-detail .og-lbl-s{{color:#065f46}}
.og-cards{{padding:4px 8px 8px 20px}}.og.open .og-cards{{display:block}}.og-cards{{display:none}}

/* Person card */
.cd{{background:var(--c);border-radius:8px;margin-bottom:5px;border:1px solid var(--b);border-left:3px solid #ccc;transition:box-shadow .2s;overflow:hidden}}
.cd:hover{{box-shadow:0 2px 8px rgba(0,0,0,.05)}}
.cd.t1{{border-left-color:var(--t1)}}.cd.t2{{border-left-color:var(--t2)}}.cd.t3{{border-left-color:var(--t3)}}
.cd.search-hide{{display:none}}
.ch{{padding:8px 12px;cursor:pointer;display:flex;align-items:center;justify-content:space-between;user-select:none}}
.ch:hover{{background:rgba(0,0,0,.01)}}
.cl{{display:flex;align-items:center;gap:10px;flex:1;min-width:0}}
.av{{width:34px;height:34px;border-radius:50%;flex-shrink:0;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.12)}}
.av svg{{width:34px;height:34px}}
.ci{{min-width:0}}
.cn{{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.cr{{font-size:11px;color:var(--o);font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.co{{font-size:10px;color:var(--m);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.crt{{display:flex;align-items:center;gap:5px;flex-shrink:0}}
.li-b{{width:20px;height:20px;border-radius:4px;background:#0077b5;color:#fff;display:flex;align-items:center;justify-content:center;text-decoration:none;opacity:.75;transition:opacity .15s;flex-shrink:0}}
.li-b:hover{{opacity:1;transform:scale(1.1)}}
.li-b svg{{width:12px;height:12px;fill:#fff}}
.tp{{font-size:10px;font-weight:600;padding:2px 6px;border-radius:6px;white-space:nowrap}}
.tp.t1{{background:var(--t1b);color:var(--t1)}}.tp.t2{{background:var(--t2b);color:var(--t2)}}.tp.t3{{background:var(--t3b);color:var(--t3)}}
.cv{{font-size:11px;color:#ccc;transition:transform .2s;margin-left:2px}}.cd.open .cv{{transform:rotate(180deg)}}
.dt{{display:none;padding:0 12px 12px;border-top:1px solid #f0ede5}}.cd.open .dt{{display:block;padding-top:10px}}
.ds{{margin-bottom:10px}}.dl{{font-size:9px;font-weight:600;color:var(--o);text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px}}
.dx{{font-size:12px;color:#444;line-height:1.55}}
.dq{{font-style:italic;color:#666;border-left:2px solid var(--o);padding:2px 0 2px 10px;margin:4px 0;font-size:12px;line-height:1.5}}
.ib{{margin-top:10px;padding:8px 10px;border-radius:6px;font-size:11px;line-height:1.4}}
.ib.rel{{background:#fffbeb;border:1px solid #fde68a}}.ib.abm{{background:#ecfdf5;border:1px solid #a7f3d0}}
.ib-l{{font-weight:700;margin-bottom:2px}}.ib-t{{color:#555}}
.cb{{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:10px;padding:6px 8px;background:#f8f7f5;border-radius:6px;font-size:11px;color:#666}}
.cb a{{color:#2563eb;text-decoration:none}}.cb a:hover{{text-decoration:underline}}

/* No results */
.no-results{{display:none;text-align:center;padding:40px 20px;color:var(--m);font-size:14px}}

@media(max-width:768px){{.sb{{display:none}}.mn{{margin-left:0;padding:16px 14px}}.og-h{{flex-wrap:wrap}}.og-right{{margin-top:6px}}}}
</style>
</head>
<body>
<nav class="sb">
<div style="display:flex;align-items:center"><span class="logo">SAGA</span><span class="sb-bdg">STAKEHOLDERS</span></div>
<div class="sb-s">{total_count} stakeholders &middot; Opdateret {build_date}</div>
<div class="sb-search">
<svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
<input type="text" placeholder="Søg stakeholder..." oninput="doSearch(this.value)">
</div>
''')

# Sidebar nav groups
group_labels = {
    'ORGANISATIONER': ('Organisationer', org_count),
    'INFLUENCERS': ('Influencers', inf_count),
    'MEDIER': ('Medier', med_count),
    'KOMMUNER': ('Kommuner', kom_count),
}
group_sections = {
    'ORGANISATIONER': ORG_SECTIONS,
    'INFLUENCERS': INF_SECTIONS,
    'MEDIER': MED_SECTIONS,
    'KOMMUNER': list(GROUPS['KOMMUNER'].keys()),
}

for gname, (glabel, gcount) in group_labels.items():
    H.append(f'<div class="ng">\n<div class="ng-h">{glabel} <span class="ng-c">{gcount}</span></div>\n')
    for sec in group_sections[gname]:
        people = GROUPS[gname].get(sec, [])
        if gname == 'KOMMUNER':
            mdata = MUNICIPALITY_DATA.get(sec, {})
            rank = mdata.get('rank', '')
            display = sec.replace(' Kommune', '')  # strip suffix for brevity
            cnt = f'<span class="nc">{len(people)}</span>' if people else ''
            H.append(f'<a href="#{mkid(gname+"-"+sec)}" onclick="go(\'{mkid(gname+"-"+sec)}\');return false">{esc(display)} {cnt}</a>\n')
        elif people:
            H.append(f'<a href="#{mkid(gname+"-"+sec)}" onclick="go(\'{mkid(gname+"-"+sec)}\');return false">{esc(sec)} <span class="nc">{len(people)}</span></a>\n')
    H.append('</div>\n')

H.append(f'''<div class="ss">
<div class="sr"><span class="l">Total</span><span class="v">{total_count}</span></div>
<div class="sr"><span class="l">Tier 1</span><span class="v">{t1}</span></div>
<div class="sr"><span class="l">Tier 2</span><span class="v">{t2}</span></div>
<div class="sr"><span class="l">Tier 3</span><span class="v">{t3}</span></div>
<div class="sr"><span class="l">Kommuner</span><span class="v">{len(GROUPS["KOMMUNER"])}</span></div>
<div class="sr"><span class="l">LinkedIn</span><span class="v">{li}</span></div>
<div class="sr"><span class="l">Kontakt</span><span class="v">{ct}</span></div>
</div></nav>
<main class="mn">
<div class="pt">Stakeholder Map</div>
<div class="ps">{total_count} stakeholders &middot; {org_count} i organisationer &middot; {inf_count} influencers &middot; {med_count} i medier &middot; {kom_count} i kommuner</div>
<div class="main-search">
<svg viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0016 9.5 6.5 6.5 0 109.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
<input type="text" id="mainSearch" placeholder="Søg efter navn, organisation, rolle..." oninput="doSearch(this.value)">
<span class="search-count" id="searchCount"></span>
</div>
<div class="no-results" id="noResults">Ingen stakeholders matcher din søgning</div>
''')

svgid = 0

def render_person_card(r):
    global svgid
    t = r['tier']
    ini = ''.join(w[0] for w in r['name'].split()[:2] if w and w[0].isalpha()).upper() or r['name'][0].upper()
    g1,g2 = tg.get(t,('#666','#888'))
    svgid += 1
    score = r.get('relevance_score')
    search_text = f"{r['name']} {r.get('role','')} {r.get('organization','')} {r.get('canonical_org','')}".lower()

    svg = f'<svg viewBox="0 0 34 34" xmlns="http://www.w3.org/2000/svg"><defs><linearGradient id="g{svgid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="{g1}"/><stop offset="100%" stop-color="{g2}"/></linearGradient></defs><circle cx="17" cy="17" r="17" fill="url(#g{svgid})"/><text x="17" y="17" text-anchor="middle" dominant-baseline="central" fill="white" font-family="-apple-system,sans-serif" font-size="11" font-weight="600">{ini}</text></svg>'

    out = []
    out.append(f'<div class="cd t{t}" data-search="{esc(search_text)}" data-tier="{t}" data-score="{score or 0}">\n')
    out.append(f'<div class="ch" onclick="toggle(this.parentElement)">\n<div class="cl">\n<div class="av">{svg}</div>\n<div class="ci">\n<div class="cn">{esc(r["name"])}</div>\n<div class="cr">{esc(r["role"])}</div>\n')
    # Show org for influencers/medier (useful context)
    org_display = r.get('canonical_org', '') or r.get('organization', '')
    if org_display:
        out.append(f'<div class="co">{esc(org_display)}</div>\n')
    out.append('</div></div>\n<div class="crt">\n')
    if r.get('linkedin'):
        li_svg = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>'
        out.append(f'<a class="li-b" href="{r["linkedin"]}" target="_blank" onclick="event.stopPropagation()" title="LinkedIn profil">{li_svg}</a>\n')
    if score is not None:
        out.append(f'<span class="tp t{t}">{score}/10</span>\n')
    out.append(f'<span class="tp t{t}">{TIER_LABELS[t]}</span>\n')
    out.append(f'<span class="cv">&#9660;</span>\n</div></div>\n')

    # Detail
    out.append('<div class="dt">\n')
    bg = r.get('baggrund','')
    if bg:
        out.append(f'<div class="ds"><div class="dl">Rolle og baggrund</div>\n')
        qm = re.search(r'["\u201c\u201d]([^"\u201c\u201d]{10,})["\u201c\u201d]', bg)
        if qm:
            rest = bg.replace(qm.group(0),'').strip().strip('.')
            if rest: out.append(f'<div class="dx">{esc(rest)}</div>\n')
            out.append(f'<div class="dq">&ldquo;{esc(qm.group(1))}&rdquo;</div>\n')
        else:
            out.append(f'<div class="dx">{esc(bg)}</div>\n')
        out.append('</div>\n')
    fk = r.get('fokus','') or r.get('focus','')
    if fk:
        out.append(f'<div class="ds"><div class="dl">Fokus</div>\n<div class="dx">{esc(fk)}</div></div>\n')
    sr = r.get('saga_relevans','')
    if sr:
        out.append(f'<div class="ds"><div class="dl">SAGA Relevans</div>\n<div class="dx">{esc(sr)}</div></div>\n')
    if score is not None:
        out.append(f'<div class="ib rel"><div class="ib-l">SAGA-Relevans: {score}/10</div><div class="ib-t">{esc(TIER_FULL.get(t,""))}</div></div>\n')
    abm = r.get('abm_strategy','') or r.get('v2_abm_strategy','')
    if abm and abm != sr:
        out.append(f'<div class="ib abm"><div class="ib-l">ABM Strategi</div><div class="ib-t">{esc(abm)}</div></div>\n')
    parts = []
    if r.get('email'): parts.append(f'&#9993; <a href="mailto:{esc(r["email"])}" onclick="event.stopPropagation()">{esc(r["email"])}</a>')
    if r.get('phone'): parts.append(f'&#9742; {esc(r["phone"])}')
    if r.get('linkedin'): parts.append(f'<a href="{r["linkedin"]}" target="_blank" onclick="event.stopPropagation()">LinkedIn &#8599;</a>')
    if parts: out.append(f'<div class="cb">{" &nbsp;&middot;&nbsp; ".join(parts)}</div>\n')
    out.append('</div></div>\n')
    return ''.join(out)


def render_org_group(canon_org, people, section_name):
    """Render an org group with its people cards inside"""
    oid = mkid(section_name + '-' + canon_org)
    enrich = org_enrichment.get(canon_org, {})
    website = ''
    stats = ''
    # Find website from org_data
    for sec_key, od in org_data.items():
        for o in od.get('orgs', []):
            if o['name'] == canon_org or canon_org.startswith(o['name']) or o['name'] in canon_org:
                website = o.get('website', '')
                stats = o.get('stats', '')
                break
        if website:
            break

    out = []
    out.append(f'<div class="og" id="{oid}">\n')
    out.append(f'<div class="og-h" onclick="toggleOrg(this.parentElement)">\n')
    out.append(f'<div class="og-left">\n<div class="og-icon">{building_svg}</div>\n<div class="og-info">\n')
    # For municipalities: show display name without " Kommune" suffix
    display_name = canon_org.replace(' Kommune', '') if section_name == 'KOMMUNER' else canon_org
    out.append(f'<div class="og-name">{esc(display_name)}</div>\n')
    meta = []
    kom_badge = ''
    if section_name == 'KOMMUNER':
        mdata = MUNICIPALITY_DATA.get(canon_org, {})
        rank = mdata.get('rank', '')
        tier = mdata.get('tier', '')
        if rank:
            tc = TIER_CLASS.get(tier, 'fol')
            kom_badge = f'<span class="tier-bdg {tc}">{tier}</span>'
    if stats: meta.append(esc(stats))
    meta.append(f'{len(people)} {"person" if len(people)==1 else "personer"}')
    out.append(f'<div class="og-meta">{"&middot;".join(meta)}</div>\n')
    out.append('</div></div>\n<div class="og-right">\n')
    if kom_badge:
        out.append(f'{kom_badge}\n')
    if website:
        out.append(f'<a class="og-link" href="{website}" target="_blank" onclick="event.stopPropagation()">Hjemmeside &#8599;</a>\n')
    out.append(f'<span class="og-cnt">{len(people)}</span>\n<span class="og-cv">&#9660;</span>\n</div></div>\n')

    if enrich:
        out.append('<div class="og-detail">\n')
        events = enrich.get('events', [])
        agenda = enrich.get('agenda', '')
        influence = enrich.get('influence', '')
        if events:
            out.append(f'<p><span class="og-lbl og-lbl-e">Events:</span> {esc("; ".join(events))}</p>\n')
        if agenda:
            out.append(f'<p><span class="og-lbl og-lbl-a">Agenda:</span> {esc(agenda)}</p>\n')
        if influence:
            out.append(f'<p><span class="og-lbl og-lbl-s">SAGA-indgang:</span> {esc(influence)}</p>\n')
        out.append('</div>\n')

    out.append('<div class="og-cards">\n')
    for p in people:
        out.append(render_person_card(p))
    out.append('</div>\n</div>\n')
    return ''.join(out)


# ═══════════════ RENDER GROUPS ═══════════════

group_icons = {
    'ORGANISATIONER': ('<div class="gh-icon gh-org"><svg viewBox="0 0 24 24"><path d="M12 7V3H2v18h20V7H12zM6 19H4v-2h2v2zm0-4H4v-2h2v2zm0-4H4V9h2v2zm0-4H4V5h2v2zm4 12H8v-2h2v2zm0-4H8v-2h2v2zm0-4H8V9h2v2zm0-4H8V5h2v2zm10 12h-8v-2h2v-2h-2v-2h2v-2h-2V9h8v10zm-2-8h-2v2h2v-2zm0 4h-2v2h2v-2z"/></svg></div>', 'Organisationer'),
    'INFLUENCERS': ('<div class="gh-icon gh-inf"><svg viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div>', 'Influencers'),
    'MEDIER': ('<div class="gh-icon gh-med"><svg viewBox="0 0 24 24"><path d="M22 3l-1.67 1.67L18.67 3 17 4.67 15.33 3l-1.66 1.67L12 3l-1.67 1.67L8.67 3 7 4.67 5.33 3 3.67 4.67 2 3v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V3zM11 19H4v-6h7v6zm9 0h-7v-2h7v2zm0-4h-7v-2h7v2zm0-4H4V8h16v3z"/></svg></div>', 'Medier'),
    'KOMMUNER': ('<div class="gh-icon gh-kom"><svg viewBox="0 0 24 24"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg></div>', 'Kommuner'),
}

for gname in ['ORGANISATIONER', 'INFLUENCERS', 'MEDIER', 'KOMMUNER']:
    icon_html, label = group_icons[gname]
    H.append(f'<div class="gh" id="{mkid(gname)}">{icon_html} {label}</div>\n')

    # Sort bar for Influencers
    if gname == 'INFLUENCERS':
        H.append('''<div class="sort-bar">
<label>Sortér:</label>
<button class="sort-btn active" onclick="sortInfluencers('default',this)">Standard</button>
<button class="sort-btn" onclick="sortInfluencers('tier',this)">Tier (1→3)</button>
<button class="sort-btn" onclick="sortInfluencers('relevance',this)">Relevans (høj→lav)</button>
<button class="sort-btn" onclick="sortInfluencers('name',this)">Navn (A→Z)</button>
</div>
<div id="influencer-container">
''')

    sections = group_sections[gname]
    for sec in sections:
        people = GROUPS[gname].get(sec, [])
        # For non-KOMMUNER: skip empty sections
        if not people and gname != 'KOMMUNER':
            continue

        sec_id = mkid(gname + "-" + sec)
        sd = SECTION_DESCRIPTIONS.get(sec, {})

        H.append(f'<div class="sec" id="{sec_id}" data-group="{gname}">\n')

        if gname != 'KOMMUNER':
            H.append(f'<div class="sh"><div class="st">{esc(sec)}</div><div class="sc_">{len(people)} stakeholders</div></div>\n')

        if sd:
            H.append(f'<div class="sec-desc"><div class="od">{esc(sd.get("desc",""))}</div>')
            if sd.get('saga'):
                H.append(f'<div class="os">SAGA-strategi: {esc(sd["saga"])}</div>')
            H.append('</div>\n')

        # For ORGANISATIONER: group by org
        if gname == 'ORGANISATIONER':
            org_groups = build_org_groups(people)
            for canon_org, org_people in org_groups.items():
                H.append(render_org_group(canon_org, org_people, sec))
        elif gname == 'KOMMUNER':
            H.append(render_org_group(sec, people, gname))
        else:
            # For INFLUENCERS and MEDIER: render cards directly (or grouped by media outlet)
            if gname == 'MEDIER':
                media_groups = OrderedDict()
                for p in people:
                    mk = get_media_key(p)
                    if mk not in media_groups:
                        media_groups[mk] = []
                    media_groups[mk].append(p)
                for mk, mp in media_groups.items():
                    H.append(render_org_group(mk, mp, sec))
            else:
                # Influencers — flat cards, sortable
                for p in people:
                    H.append(render_person_card(p))

        H.append('</div>\n')

    if gname == 'INFLUENCERS':
        H.append('</div>\n')  # close influencer-container

H.append('''</main>
<script>
function toggle(e){e.classList.toggle('open')}
function toggleOrg(e){e.classList.toggle('open')}
function go(id){const e=document.getElementById(id);if(e)e.scrollIntoView({behavior:'smooth',block:'start'});document.querySelectorAll('.sb a').forEach(a=>a.classList.remove('active'));const l=document.querySelector(`.sb a[onclick*="${id}"]`);if(l)l.classList.add('active')}

// Scroll spy
window.addEventListener('scroll',()=>{const s=document.querySelectorAll('.sec');let c='';s.forEach(x=>{if(scrollY>=x.offsetTop-120)c=x.id});if(c)document.querySelectorAll('.sb a').forEach(a=>{a.classList.toggle('active',a.getAttribute('onclick')?.includes(c))})});

// Search
function doSearch(q){
  q=q.toLowerCase().trim();
  const cards=document.querySelectorAll('.cd');
  const orgs=document.querySelectorAll('.og');
  const secs=document.querySelectorAll('.sec');
  const nr=document.getElementById('noResults');
  const sc=document.getElementById('searchCount');
  // Also sync sidebar search
  document.querySelectorAll('.sb-search input, #mainSearch').forEach(i=>{if(document.activeElement!==i)i.value=q.charAt(0).toUpperCase()+q.slice(1)});
  let shown=0;
  if(!q){
    cards.forEach(c=>{c.classList.remove('search-hide');c.style.display=''});
    orgs.forEach(o=>{o.style.display=''});
    secs.forEach(s=>{s.style.display=''});
    nr.style.display='none';
    sc.style.display='none';
    return;
  }
  cards.forEach(c=>{
    const d=c.getAttribute('data-search')||'';
    if(d.includes(q)){c.classList.remove('search-hide');c.style.display='';shown++}
    else{c.classList.add('search-hide');c.style.display='none'}
  });
  // Hide empty org groups
  orgs.forEach(o=>{
    const vis=o.querySelectorAll('.cd:not(.search-hide)');
    o.style.display=vis.length?'':'none';
    if(vis.length)o.classList.add('open');
  });
  // Hide empty sections
  secs.forEach(s=>{
    const vis=s.querySelectorAll('.cd:not(.search-hide)');
    s.style.display=vis.length?'':'none';
  });
  nr.style.display=shown?'none':'block';
  sc.textContent=shown+' fundet';
  sc.style.display=shown?'block':'none';
}

// Sort influencers
function sortInfluencers(mode,btn){
  document.querySelectorAll('.sort-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const container=document.getElementById('influencer-container');
  if(!container)return;
  // Get all influencer sections
  const secs=Array.from(container.querySelectorAll('.sec'));
  // Collect ALL cards across sections
  let allCards=[];
  secs.forEach(s=>{
    const cards=Array.from(s.querySelectorAll('.cd'));
    cards.forEach(c=>allCards.push(c));
  });
  if(mode==='default'){
    // Restore original order — put cards back in their sections
    secs.forEach(s=>s.style.display='');
    // Cards stay in sections as-is
    return;
  }
  // For tier/relevance/name sort: hide section headers, show flat sorted list
  // Create or reuse a flat container
  let flat=document.getElementById('inf-flat');
  if(!flat){
    flat=document.createElement('div');
    flat.id='inf-flat';
    container.appendChild(flat);
  }
  flat.innerHTML='';
  // Hide sections
  secs.forEach(s=>s.style.display='none');
  // Sort
  if(mode==='tier'){
    allCards.sort((a,b)=>{
      const ta=parseInt(a.dataset.tier),tb=parseInt(b.dataset.tier);
      if(ta!==tb)return ta-tb;
      return parseFloat(b.dataset.score)-parseFloat(a.dataset.score);
    });
  }else if(mode==='relevance'){
    allCards.sort((a,b)=>parseFloat(b.dataset.score)-parseFloat(a.dataset.score));
  }else if(mode==='name'){
    allCards.sort((a,b)=>{
      const na=a.querySelector('.cn')?.textContent||'';
      const nb=b.querySelector('.cn')?.textContent||'';
      return na.localeCompare(nb,'da');
    });
  }
  allCards.forEach(c=>{
    const clone=c.cloneNode(true);
    clone.querySelector('.ch')?.setAttribute('onclick','toggle(this.parentElement)');
    clone.querySelectorAll('a').forEach(a=>{if(a.onclick)a.setAttribute('onclick','event.stopPropagation()')});
    flat.appendChild(clone);
  });
  flat.style.display='block';
}
</script></body></html>''')

html = ''.join(H)
out = 'index.html'
with open(out,'w') as f: f.write(html)

cards = html.count('data-search=')
org_cards = html.count('class="og"')
print(f"\n=== V7.0 ===")
print(f"Person cards: {cards}")
print(f"Org groups: {org_cards}")
print(f"File: {len(html)/1024:.0f} KB")
print(f"ORGANISATIONER: {org_count}")
print(f"INFLUENCERS: {inf_count}")
print(f"MEDIER: {med_count}")
print(f"KOMMUNER: {kom_count} ({len(GROUPS['KOMMUNER'])} kommuner)")
print(f"Total: {org_count+inf_count+med_count+kom_count}")

# Verify
all_scored = sum(1 for r in master if r.get('relevance_score') is not None)
all_bg = sum(1 for r in master if r.get('baggrund'))
all_sr = sum(1 for r in master if r.get('saga_relevans'))
print(f"Scores: {all_scored}/148")
print(f"Baggrund: {all_bg}/148")
print(f"SAGA Relevans: {all_sr}/148")
