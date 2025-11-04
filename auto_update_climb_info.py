import os
import json
import gpxpy

GPX_FOLDER = "gpx"
GPX_FILES_JSON = "gpx_files.json"
CLIMBS_INFO_JSON = "climbs_info.json"

# Load current JSON files
with open(GPX_FILES_JSON, "r") as f:
    gpx_files = json.load(f)

with open(CLIMBS_INFO_JSON, "r") as f:
    climbs_info = json.load(f)

for gpx_file in gpx_files:
    path = os.path.join(GPX_FOLDER, gpx_file)
    if not os.path.exists(path):
        continue

    with open(path, "r") as f:
        gpx = gpxpy.parse(f)

    distance_km = sum(segment.length_3d()/1000 for track in gpx.tracks for segment in track.segments)
    elevation_gain_m = sum(max(p2.elevation - p1.elevation,0) for track in gpx.tracks for segment in track.segments for p1,p2 in zip(segment.points[:-1], segment.points[1:]))
    
    # Compute avg gradient if both distance and elevation available
    avg_gradient = f"{round((elevation_gain_m / (distance_km*1000)) * 100, 1)}%" if distance_km > 0 else ""

    info = climbs_info.get(gpx_file, {})

    # Populate only if empty or "--" and not PB/strava
    if info.get("distance","") in ["", "--"]:
        info["distance"] = f"{round(distance_km,1)}km"
    if info.get("elevation_gain","") in ["", "--"]:
        info["elevation_gain"] = f"{round(elevation_gain_m)}m"
    if info.get("avg_gradient","") in ["", "--"]:
        info["avg_gradient"] = avg_gradient

    # Ensure PB and strava are not touched
    if "status" not in info:
        info["status"] = "planned"
    if "start_name" not in info:
        info["start_name"] = os.path.splitext(gpx_file)[0]

    climbs_info[gpx_file] = info

# Save updated climbs info
with open(CLIMBS_INFO_JSON, "w") as f:
    json.dump(climbs_info, f, indent=2)

print("Climbs info updated from GPX files.")
