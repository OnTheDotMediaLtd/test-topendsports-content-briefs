#!/usr/bin/env python3
"""
Generate URL structure for all 28 US state betting pages
Based on official regulator research from December 2025
"""

import csv
from datetime import datetime

# State data with licensed operators (from official regulator research)
STATES_DATA = {
    # ===== 14 STATES CURRENTLY TARGETING =====
    "colorado": {
        "name": "Colorado",
        "slug": "colorado",
        "regulator": "Colorado Division of Gaming",
        "regulator_url": "https://sbg.colorado.gov/sports-betting",
        "priority": "Critical",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "theScore Bet", "Bally Bet", "Circa Sports"],
        "status": "License Obtained"
    },
    "arizona": {
        "name": "Arizona",
        "slug": "arizona",
        "regulator": "Arizona Department of Gaming",
        "regulator_url": "https://gaming.az.gov/",
        "priority": "Critical",
        "operators": ["BetMGM", "Caesars", "bet365", "Hard Rock Bet", "Fanatics", "BetRivers", "FanDuel", "DraftKings"],
        "status": "License Obtained"
    },
    "pennsylvania": {
        "name": "Pennsylvania",
        "slug": "pennsylvania",
        "regulator": "Pennsylvania Gaming Control Board",
        "regulator_url": "https://gamingcontrolboard.pa.gov/",
        "priority": "Critical",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "theScore Bet", "BetParx"],
        "status": "License Obtained"
    },
    "west-virginia": {
        "name": "West Virginia",
        "slug": "west-virginia",
        "regulator": "West Virginia Lottery Commission",
        "regulator_url": "https://business.wvlottery.com/",
        "priority": "Critical",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "BetRivers", "Fanatics", "Betly"],
        "status": "License Obtained"
    },
    "tennessee": {
        "name": "Tennessee",
        "slug": "tennessee",
        "regulator": "Tennessee Sports Wagering Council",
        "regulator_url": "https://www.tn.gov/swac.html",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "Fanatics", "theScore Bet", "Bally Bet", "Hard Rock Bet"],
        "status": "No License Required"
    },
    "kansas": {
        "name": "Kansas",
        "slug": "kansas",
        "regulator": "Kansas Racing and Gaming Commission",
        "regulator_url": "https://www.krgc.ks.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "Fanatics"],
        "status": "No License Required"
    },
    "kentucky": {
        "name": "Kentucky",
        "slug": "kentucky",
        "regulator": "Kentucky Horse Racing Commission",
        "regulator_url": "https://khrc.ky.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "Fanatics", "Circa Sports"],
        "status": "No License Required"
    },
    "north-carolina": {
        "name": "North Carolina",
        "slug": "north-carolina",
        "regulator": "North Carolina State Lottery Commission",
        "regulator_url": "https://ncgaming.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "Fanatics"],
        "status": "No License Required"
    },
    "ohio": {
        "name": "Ohio",
        "slug": "ohio",
        "regulator": "Ohio Casino Control Commission",
        "regulator_url": "https://casinocontrol.ohio.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "Bally Bet"],
        "status": "No License Required"
    },
    "illinois": {
        "name": "Illinois",
        "slug": "illinois",
        "regulator": "Illinois Gaming Board",
        "regulator_url": "https://igb.illinois.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet"],
        "status": "No License Required"
    },
    "missouri": {
        "name": "Missouri",
        "slug": "missouri",
        "regulator": "Missouri Gaming Commission",
        "regulator_url": "https://mgc.dps.mo.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "Fanatics", "theScore Bet", "Circa Sports"],
        "status": "No License Required"
    },
    "michigan": {
        "name": "Michigan",
        "slug": "michigan",
        "regulator": "Michigan Gaming Control Board",
        "regulator_url": "https://www.michigan.gov/mgcb",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "WynnBET"],
        "status": "Allowed to Operate"
    },
    "louisiana": {
        "name": "Louisiana",
        "slug": "louisiana",
        "regulator": "Louisiana Gaming Control Board",
        "regulator_url": "https://lgcb.dps.louisiana.gov/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Bally Bet"],
        "status": "Allowed to Operate (under $500k)"
    },
    "maryland": {
        "name": "Maryland",
        "slug": "maryland",
        "regulator": "Maryland Lottery and Gaming Control Agency",
        "regulator_url": "https://www.mdgaming.com/",
        "priority": "High",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "Bally Bet"],
        "status": "Allowed to Operate (under $500k)"
    },
    # Waiting for License states
    "massachusetts": {
        "name": "Massachusetts",
        "slug": "massachusetts",
        "regulator": "Massachusetts Gaming Commission",
        "regulator_url": "https://massgaming.com/",
        "priority": "Medium",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "Fanatics", "theScore Bet", "Bally Bet"],
        "status": "Waiting for License"
    },
    "virginia": {
        "name": "Virginia",
        "slug": "virginia",
        "regulator": "Virginia Lottery",
        "regulator_url": "https://www.valottery.com/",
        "priority": "Medium",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "Bally Bet"],
        "status": "Waiting for License"
    },
    "indiana": {
        "name": "Indiana",
        "slug": "indiana",
        "regulator": "Indiana Gaming Commission",
        "regulator_url": "https://www.in.gov/igc/",
        "priority": "Medium",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "Bally Bet"],
        "status": "Waiting for License"
    },
    "new-jersey": {
        "name": "New Jersey",
        "slug": "new-jersey",
        "regulator": "NJ Division of Gaming Enforcement",
        "regulator_url": "https://www.njoag.gov/about/divisions-and-offices/division-of-gaming-enforcement-home/",
        "priority": "Medium",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "BetParx"],
        "status": "Waiting for License"
    },
    # ===== 14 STATES NOT TARGETING BUT LEGAL =====
    "arkansas": {
        "name": "Arkansas",
        "slug": "arkansas",
        "regulator": "Arkansas Racing Commission",
        "regulator_url": "https://www.dfa.arkansas.gov/office/racing-commission/",
        "priority": "Low",
        "operators": ["Betly", "BetSaracen", "Oaklawn Sports"],
        "status": "Legal - Not Targeting"
    },
    "connecticut": {
        "name": "Connecticut",
        "slug": "connecticut",
        "regulator": "CT Department of Consumer Protection",
        "regulator_url": "https://portal.ct.gov/dcp",
        "priority": "Low",
        "operators": ["DraftKings", "FanDuel", "Fanatics"],
        "status": "Legal - Not Targeting"
    },
    "delaware": {
        "name": "Delaware",
        "slug": "delaware",
        "regulator": "Delaware Lottery",
        "regulator_url": "https://www.delottery.com/",
        "priority": "Low",
        "operators": ["BetRivers"],
        "status": "Legal - Not Targeting (Monopoly)"
    },
    "florida": {
        "name": "Florida",
        "slug": "florida",
        "regulator": "Florida Gaming Control Commission",
        "regulator_url": "https://flgaming.gov/",
        "priority": "Low",
        "operators": ["Hard Rock Bet"],
        "status": "Legal - Not Targeting (Tribal Monopoly)"
    },
    "iowa": {
        "name": "Iowa",
        "slug": "iowa",
        "regulator": "Iowa Racing and Gaming Commission",
        "regulator_url": "https://irgc.iowa.gov/",
        "priority": "Low",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet", "Circa Sports"],
        "status": "Legal - Not Targeting"
    },
    "maine": {
        "name": "Maine",
        "slug": "maine",
        "regulator": "Maine Gambling Control Unit",
        "regulator_url": "https://www.maine.gov/dps/gcu/",
        "priority": "Low",
        "operators": ["DraftKings", "Caesars"],
        "status": "Legal - Not Targeting"
    },
    "new-hampshire": {
        "name": "New Hampshire",
        "slug": "new-hampshire",
        "regulator": "New Hampshire Lottery Commission",
        "regulator_url": "https://www.nhlottery.com/",
        "priority": "Low",
        "operators": ["DraftKings"],
        "status": "Legal - Not Targeting (Exclusive)"
    },
    "new-york": {
        "name": "New York",
        "slug": "new-york",
        "regulator": "New York State Gaming Commission",
        "regulator_url": "https://gaming.ny.gov/",
        "priority": "Low",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "Fanatics", "theScore Bet", "Bally Bet", "WynnBET"],
        "status": "Legal - Not Targeting"
    },
    "oregon": {
        "name": "Oregon",
        "slug": "oregon",
        "regulator": "Oregon Lottery",
        "regulator_url": "https://www.oregonlottery.org/",
        "priority": "Low",
        "operators": ["DraftKings"],
        "status": "Legal - Not Targeting (Exclusive)"
    },
    "puerto-rico": {
        "name": "Puerto Rico",
        "slug": "puerto-rico",
        "regulator": "Puerto Rico Gaming Commission",
        "regulator_url": "https://www.comjuegos.pr.gov/",
        "priority": "Low",
        "operators": ["BetMGM", "Caesars"],
        "status": "Legal - Not Targeting"
    },
    "rhode-island": {
        "name": "Rhode Island",
        "slug": "rhode-island",
        "regulator": "Rhode Island Lottery",
        "regulator_url": "https://www.rilot.com/",
        "priority": "Low",
        "operators": ["Sportsbook Rhode Island"],
        "status": "Legal - Not Targeting (Monopoly)"
    },
    "vermont": {
        "name": "Vermont",
        "slug": "vermont",
        "regulator": "Vermont Department of Liquor and Lottery",
        "regulator_url": "https://liquorandlottery.vermont.gov/",
        "priority": "Low",
        "operators": ["DraftKings", "FanDuel", "Fanatics"],
        "status": "Legal - Not Targeting"
    },
    "wyoming": {
        "name": "Wyoming",
        "slug": "wyoming",
        "regulator": "Wyoming Gaming Commission",
        "regulator_url": "https://gaming.wyo.gov/",
        "priority": "Low",
        "operators": ["FanDuel", "DraftKings", "BetMGM", "Caesars", "Fanatics"],
        "status": "Legal - Not Targeting"
    },
    "nevada": {
        "name": "Nevada",
        "slug": "nevada",
        "regulator": "Nevada Gaming Control Board",
        "regulator_url": "https://gaming.nv.gov/",
        "priority": "Low",
        "operators": ["BetMGM", "Caesars", "Westgate SuperBook", "Circa Sports", "STN Sports"],
        "status": "Legal - Not Targeting (No DK/FD)"
    },
}

# Brand slug mapping
BRAND_SLUGS = {
    "FanDuel": "fanduel",
    "DraftKings": "draftkings",
    "BetMGM": "betmgm",
    "Caesars": "caesars",
    "bet365": "bet365",
    "BetRivers": "betrivers",
    "Fanatics": "fanatics",
    "theScore Bet": "thescore-bet",
    "Hard Rock Bet": "hard-rock-bet",
    "Bally Bet": "bally-bet",
    "WynnBET": "wynnbet",
    "BetParx": "betparx",
    "Circa Sports": "circa-sports",
    "Betly": "betly",
    "BetSaracen": "betsaracen",
    "Oaklawn Sports": "oaklawn-sports",
    "Sportsbook Rhode Island": "sportsbook-ri",
    "Westgate SuperBook": "superbook",
    "STN Sports": "stn-sports",
}

# Major brands that should get promo code pages (high search volume)
PROMO_CODE_BRANDS = ["FanDuel", "DraftKings", "BetMGM", "Caesars", "bet365", "BetRivers", "Fanatics", "Hard Rock Bet"]

def generate_urls():
    """Generate all state betting URLs"""
    rows = []

    # Writers assignment (alternating)
    writers = ["Lewis Humphries", "Tom Goldsmith"]
    writer_idx = 0

    for state_slug, state_data in STATES_DATA.items():
        state_name = state_data["name"]
        priority = state_data["priority"]
        operators = state_data["operators"]
        status = state_data["status"]
        regulator = state_data["regulator"]

        # Assign writer for this state
        state_writer = writers[writer_idx % 2]
        writer_idx += 1

        # 1. Hub page
        rows.append({
            "Level 1": f"{state_name} Betting",
            "Level 2": "",
            "Level 3": "",
            "Level 4": "",
            "Full URL": f"https://www.topendsports.com/sport/betting/{state_slug}/index.htm",
            "Page Name": f"Best Betting Sites in {state_name}",
            "Writer": state_writer,
            "Status": "Not Started",
            "Priority": priority,
            "Research Summary": "",
            "Writer Brief Link": "",
            "AI Brief Link": "",
            "Target Keywords": f"best betting sites {state_name.lower()}",
            "Volume": "",
            "Phase": "PHASE 1",
            "Notes": f"{state_name} Hub - {status} - Regulator: {regulator}"
        })

        # 2. Betting Apps page
        rows.append({
            "Level 1": f"{state_name} Betting",
            "Level 2": "Comparison Pages",
            "Level 3": "",
            "Level 4": "",
            "Full URL": f"https://www.topendsports.com/sport/betting/{state_slug}/betting-apps.htm",
            "Page Name": f"Best Betting Apps in {state_name}",
            "Writer": state_writer,
            "Status": "Not Started",
            "Priority": "High" if priority == "Critical" else "Medium",
            "Research Summary": "",
            "Writer Brief Link": "",
            "AI Brief Link": "",
            "Target Keywords": f"best betting apps {state_name.lower()}",
            "Volume": "",
            "Phase": "PHASE 1",
            "Notes": f"{state_name} Apps"
        })

        # 3. Bonuses page
        rows.append({
            "Level 1": f"{state_name} Betting",
            "Level 2": "Comparison Pages",
            "Level 3": "Bonuses",
            "Level 4": "",
            "Full URL": f"https://www.topendsports.com/sport/betting/{state_slug}/bonuses.htm",
            "Page Name": f"Best Sportsbook Bonuses in {state_name}",
            "Writer": state_writer,
            "Status": "Not Started",
            "Priority": "High" if priority == "Critical" else "Medium",
            "Research Summary": "",
            "Writer Brief Link": "",
            "AI Brief Link": "",
            "Target Keywords": f"sportsbook bonuses {state_name.lower()}",
            "Volume": "",
            "Phase": "PHASE 1",
            "Notes": f"{state_name} Bonuses"
        })

        # 4. Brand review pages
        for i, brand in enumerate(operators):
            brand_slug = BRAND_SLUGS.get(brand, brand.lower().replace(" ", "-"))
            brand_priority = "Critical" if i < 2 else ("High" if i < 5 else "Medium")

            rows.append({
                "Level 1": f"{state_name} Betting",
                "Level 2": "Sportsbook Reviews",
                "Level 3": brand,
                "Level 4": "",
                "Full URL": f"https://www.topendsports.com/sport/betting/{state_slug}/{brand_slug}-review.htm",
                "Page Name": f"{brand} {state_name} Review",
                "Writer": state_writer,
                "Status": "Not Started",
                "Priority": brand_priority,
                "Research Summary": "",
                "Writer Brief Link": "",
                "AI Brief Link": "",
                "Target Keywords": f"{brand.lower()} {state_name.lower()}",
                "Volume": "",
                "Phase": "PHASE 1",
                "Notes": f"{state_name} Brand #{i+1}"
            })

            # 5. Promo code pages for major brands only
            if brand in PROMO_CODE_BRANDS:
                rows.append({
                    "Level 1": f"{state_name} Betting",
                    "Level 2": "Sportsbook Reviews",
                    "Level 3": brand,
                    "Level 4": "Promo Code",
                    "Full URL": f"https://www.topendsports.com/sport/betting/{state_slug}/{brand_slug}-promo-code.htm",
                    "Page Name": f"{brand} {state_name} Promo Code",
                    "Writer": state_writer,
                    "Status": "Not Started",
                    "Priority": "High" if brand in ["FanDuel", "DraftKings", "BetMGM"] else "Medium",
                    "Research Summary": "",
                    "Writer Brief Link": "",
                    "AI Brief Link": "",
                    "Target Keywords": f"{brand.lower()} promo code {state_name.lower()}",
                    "Volume": "",
                    "Phase": "PHASE 1",
                    "Notes": f"{state_name} {brand} Promo"
                })

    return rows

def main():
    rows = generate_urls()

    # Write to CSV
    output_path = "/home/user/topendsports-content-briefs/content-briefs-skill/output/us-state-pages-export.csv"
    fieldnames = ["Level 1", "Level 2", "Level 3", "Level 4", "Full URL", "Page Name",
                  "Writer", "Status", "Priority", "Research Summary", "Writer Brief Link",
                  "AI Brief Link", "Target Keywords", "Volume", "Phase", "Notes"]

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} URLs")
    print(f"Output: {output_path}")

    # Count by state
    state_counts = {}
    for row in rows:
        state = row["Level 1"].replace(" Betting", "")
        state_counts[state] = state_counts.get(state, 0) + 1

    print("\nURLs per state:")
    for state, count in sorted(state_counts.items()):
        print(f"  {state}: {count}")

    return rows

if __name__ == "__main__":
    main()
