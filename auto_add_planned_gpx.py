import os
import json

# Paths
gpx_folder = "gpx"
gpx_files_json = "gpx_files.json"
climbs_info_json = "climbs_info.json"

# Load existing JSON files
if os.path.exists(gpx_files_json):
    with open(gpx_files_json, "r") as f:
        gpx_files = json.load(f)
else:
    gpx_files = []

if os.path.exists(climbs_info_json):
    with open(climbs_info_json, "r") as f:
        climbs_info = json.load(f)
else:
    climbs_info = {}

# Scan gpx/ folder
for filename in os.listdir(gpx_folder):
    if filename.endswith(".gpx"):
        # Add to gpx_files.json if new
        if filename not in gpx_files:
            gpx_files.append(filename)
            print(f"Added {filename} to gpx_files.json")

        # Add to climbs_info.json if new
        if filename not in climbs_info:
            climbs_info[filename] = {
                "status": "planned",
                "start_name": "",
                "distance": "",
                "elevation_gain": "",
                "avg_gradient": "",
                "PB": "",
                "strava": ""
            }
            print(f"Created entry for {filename} in climbs_info.json")

# Save updated JSON files
with open(gpx_files_json, "w") as f:
    json.dump(gpx_files, f, indent=4)

with open(climbs_info_json, "w") as f:
    json.dump(climbs_info, f, indent=4)

print("Done updating JSON files.")