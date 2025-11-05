import json

# Path to your climbs info
CLIMBS_JSON = "climbs_info.json"
OUTPUT_JSON = "stats.json"

with open(CLIMBS_JSON, "r", encoding="utf-8") as f:
    climbs = json.load(f)

total_climbs = len(climbs)
ridden_climbs = sum(1 for c in climbs.values() if c.get("status") == "ridden")

# Save a simple JSON with counts
stats = {
    "total": total_climbs,
    "ridden": ridden_climbs
}

with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(stats, f, indent=2)

print(f"Total climbs: {total_climbs}, Ridden climbs: {ridden_climbs}")
