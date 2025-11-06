import json
import gpxpy
import os
import re

GPX_FOLDER = "gpx"
CLIMBS_JSON = "climbs_info.json"

with open(CLIMBS_JSON, "r") as f:
    climbs_info = json.load(f)

for gpx_file in os.listdir(GPX_FOLDER):
    if not gpx_file.endswith(".gpx"):
        continue
    gpx_path = os.path.join(GPX_FOLDER, gpx_file)
    climb = climbs_info.get(gpx_file, {})
    
    # Parse GPX
    with open(gpx_path, "r") as gpx_f:
        gpx = gpxpy.parse(gpx_f)
        total_distance_m = 0
        total_elevation_gain_m = 0
        points = []

        for track in gpx.tracks:
            for segment in track.segments:
                points.extend(segment.points)
                total_distance_m += segment.length_3d()
                total_elevation_gain_m += sum(
                    max(segment.points[i + 1].elevation - segment.points[i].elevation, 0)
                    for i in range(len(segment.points) - 1)
                )

    # Distance in km
    if not climb.get("distance") or climb.get("distance").strip() in ("", "--"):
        climb["distance"] = f"{total_distance_m / 1000:.1f}km"

    # Elevation gain in m
    if not climb.get("elevation_gain") or climb.get("elevation_gain").strip() in ("", "--"):
        climb["elevation_gain"] = f"{total_elevation_gain_m:.0f}m"

    # Average gradient
    if (not climb.get("avg_gradient") or climb.get("avg_gradient").strip() in ("", "--")) and total_distance_m > 0:
        avg_grad = total_elevation_gain_m / total_distance_m * 100
        climb["avg_gradient"] = f"{avg_grad:.1f}%"

    # Category calculation
    category = "--"
    try:
        dist_m = float(re.sub(r"[^\d.]", "", climb["distance"])) * 1000
        grad_pct = float(re.sub(r"[^\d.]", "", climb["avg_gradient"]))
        score = dist_m * grad_pct
        if score > 80000:
            category = "HC"
        elif score > 64000:
            category = "1"
        elif score > 32000:
            category = "2"
        elif score > 16000:
            category = "3"
        elif score > 8000:
            category = "4"
    except:
        pass
    climb["category"] = category

    # Update the dictionary
    climbs_info[gpx_file] = climb

# Write back to JSON
with open(CLIMBS_JSON, "w") as f:
    json.dump(climbs_info, f, indent=2)

print("Climbs info updated successfully!")
