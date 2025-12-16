#!/usr/bin/env python3
"""
Optimize state betting page keywords based on Ahrefs research
December 2025
"""

import csv
import re

# Optimized keyword data from Ahrefs research
KEYWORD_DATA = {
    # State: (hub_keyword, hub_volume, apps_keyword, apps_volume, use_abbr_in_url, abbr)
    "colorado": ("colorado sports betting", 2100, "colorado betting apps", 300, False, "co"),
    "arizona": ("arizona sports betting", 1600, "arizona betting apps", 450, False, "az"),
    "pennsylvania": ("pennsylvania sports betting", 1500, "pa betting apps", 350, False, "pa"),
    "west-virginia": ("west virginia sports betting", 1100, "west virginia betting apps", 200, False, "wv"),
    "tennessee": ("tennessee sports betting", 1600, "tennessee betting apps", 300, False, "tn"),
    "kansas": ("kansas sports betting", 900, "kansas betting apps", 300, False, "ks"),
    "kentucky": ("kentucky sports betting", 900, "kentucky betting apps", 350, False, "ky"),
    "north-carolina": ("north carolina sports betting", 9800, "north carolina betting apps", 3500, False, "nc"),
    "ohio": ("ohio sports betting", 1700, "ohio betting apps", 400, False, "oh"),
    "illinois": ("illinois sports betting", 2600, "illinois betting apps", 450, False, "il"),
    "missouri": ("missouri sports betting", 4200, "missouri betting apps", 600, False, "mo"),
    "michigan": ("michigan sports betting", 1300, "michigan betting apps", 500, False, "mi"),
    "louisiana": ("louisiana sports betting", 1600, "louisiana betting apps", 400, False, "la"),
    "maryland": ("maryland sports betting", 1700, "maryland betting apps", 500, False, "md"),
    "massachusetts": ("massachusetts sports betting", 1900, "massachusetts betting apps", 250, False, "ma"),
    "virginia": ("virginia sports betting", 1100, "va betting apps", 400, False, "va"),
    "indiana": ("indiana sports betting", 1400, "indiana betting apps", 250, False, "in"),
    "new-jersey": ("nj sports betting", 1400, "nj betting apps", 450, True, "nj"),  # Abbr wins!
    "new-york": ("new york sports betting", 1500, "ny betting apps", 600, False, "ny"),
    "connecticut": ("connecticut sports betting", 1200, "connecticut betting apps", 200, False, "ct"),
    "arkansas": ("arkansas sports betting", 1000, "arkansas betting apps", 300, False, "ar"),
    "delaware": ("delaware sports betting", 1400, "delaware betting apps", 200, False, "de"),
    "florida": ("florida sports betting", 6000, "florida betting apps", 900, False, "fl"),
    "iowa": ("iowa sports betting", 1500, "iowa betting apps", 250, False, "ia"),
    "maine": ("maine sports betting", 900, "maine betting apps", 150, False, "me"),
    "new-hampshire": ("new hampshire sports betting", 600, "new hampshire betting apps", 40, False, "nh"),
    "oregon": ("oregon sports betting", 1200, "oregon betting apps", 100, False, "or"),
    "puerto-rico": ("puerto rico sports betting", 150, "puerto rico betting apps", 20, False, "pr"),
    "rhode-island": ("rhode island sports betting", 1200, "rhode island betting apps", 100, False, "ri"),
    "vermont": ("vermont sports betting", 800, "vermont betting apps", 200, False, "vt"),
    "wyoming": ("wyoming sports betting", 700, "wyoming betting apps", 200, False, "wy"),
    "nevada": ("nevada sports betting", 900, "nevada betting apps", 300, False, "nv"),
}

def get_state_from_url(url):
    """Extract state slug from URL"""
    match = re.search(r'/sport/betting/([a-z-]+)/', url)
    if match:
        return match.group(1)
    return None

def optimize_keywords(input_file, output_file):
    """Read CSV and optimize keywords based on research"""

    rows = []
    updated_count = 0

    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            url = row.get('Full URL', '')
            state_slug = get_state_from_url(url)

            if state_slug and state_slug in KEYWORD_DATA:
                hub_kw, hub_vol, apps_kw, apps_vol, use_abbr, abbr = KEYWORD_DATA[state_slug]

                # Determine page type from URL
                if url.endswith('/index.htm'):
                    # Hub page
                    row['Target Keywords'] = hub_kw
                    row['Volume'] = str(hub_vol)
                    updated_count += 1
                elif 'betting-apps.htm' in url:
                    # Apps page
                    row['Target Keywords'] = apps_kw
                    row['Volume'] = str(apps_vol)
                    updated_count += 1
                elif 'bonuses.htm' in url:
                    # Bonuses page - use sportsbook bonuses pattern
                    state_name = state_slug.replace('-', ' ')
                    row['Target Keywords'] = f"{state_name} sportsbook bonuses"
                    updated_count += 1

            rows.append(row)

    # Write updated CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return updated_count, len(rows)

def generate_summary_report():
    """Generate a summary of keyword optimizations"""

    print("\n" + "="*80)
    print("KEYWORD OPTIMIZATION SUMMARY - ALL 28 STATES")
    print("="*80)

    # Sort by hub volume
    sorted_states = sorted(KEYWORD_DATA.items(), key=lambda x: x[1][1], reverse=True)

    print("\n### HUB PAGE KEYWORDS (Sorted by Volume)")
    print("-" * 70)
    print(f"{'State':<20} {'Optimal Keyword':<35} {'Volume':>10}")
    print("-" * 70)

    total_hub_volume = 0
    for state, data in sorted_states:
        hub_kw, hub_vol, _, _, _, _ = data
        print(f"{state:<20} {hub_kw:<35} {hub_vol:>10,}")
        total_hub_volume += hub_vol

    print("-" * 70)
    print(f"{'TOTAL':<20} {'':<35} {total_hub_volume:>10,}")

    print("\n### APPS PAGE KEYWORDS (Sorted by Volume)")
    print("-" * 70)
    sorted_by_apps = sorted(KEYWORD_DATA.items(), key=lambda x: x[1][3], reverse=True)

    total_apps_volume = 0
    for state, data in sorted_by_apps[:10]:  # Top 10
        _, _, apps_kw, apps_vol, _, _ = data
        print(f"{state:<20} {apps_kw:<35} {apps_vol:>10,}")
        total_apps_volume += apps_vol

    print("\n### ABBREVIATION RECOMMENDATIONS")
    print("-" * 70)
    print("States where abbreviation should be used in URL:")
    for state, data in KEYWORD_DATA.items():
        _, _, _, _, use_abbr, abbr = data
        if use_abbr:
            print(f"  - {state} → /{abbr}/ (abbreviation has HIGHER volume)")

    print("\nStates where abbreviation is AMBIGUOUS (avoid):")
    print("  - indiana (IN) - 'in sports betting' confused with generic term")
    print("  - oregon (OR) - 'or sports betting' confused with betting terminology")

if __name__ == "__main__":
    input_file = "/home/user/topendsports-content-briefs/content-briefs-skill/assets/data/site-structure-english.csv"
    output_file = "/home/user/topendsports-content-briefs/content-briefs-skill/assets/data/site-structure-english.csv"

    updated, total = optimize_keywords(input_file, output_file)
    print(f"Updated {updated} keywords out of {total} rows")

    generate_summary_report()
