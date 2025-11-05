import json
import os

# Paths
CLIMBS_JSON = 'climbs_info.json'

# Load climbs info
with open(CLIMBS_JSON, 'r', encoding='utf-8') as f:
    climbs_info = json.load(f)

updated = 0

for gpx_file, info in climbs_info.items():
    if info.get('start_name', '--') == '--':
        info['start_name'] = gpx_file.replace('.gpx','')
        updated += 1

# Save back
with open(CLIMBS_JSON, 'w', encoding='utf-8') as f:
    json.dump(climbs_info, f, ensure_ascii=False, indent=2)

print(f"Updated start_name for {updated} climbs.")
