import gpxpy
import requests
import json
import time

# Load settings from config.json
with open('configGPX.json', 'r') as config_file:
    config = json.load(config_file)
input_gpx = config["INPUT_GPX"]
output_gpx = config["OUTPUT_GPX"]

def get_elevation_batch(coordinates):
    """
    Fetch elevation for a batch of coordinates using OpenTopoData API.
    """
    url = "https://api.opentopodata.org/v1/test-dataset"
    locations = "|".join([f"{lon},{lat}" for lat, lon in coordinates])
    params = {"locations": locations}

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()["results"]
        else:
            print(f"Batch request failed: HTTP {response.status_code}")
            return None
    except Exception as e:
        print(f"Batch request error: {e}")
        return None

def update_gpx_elevation(input_file, output_file):
    with open(input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    coordinates = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinates.append((point.latitude, point.longitude))

    # Process in batches of 50 (OpenTopoData's limit)
    batch_size = 50
    for i in range(0, len(coordinates), batch_size):
        batch = coordinates[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}...")
        elevations = get_elevation_batch(batch)

        if elevations:
            for j, result in enumerate(elevations):
                idx = i + j
                if "elevation" in result:
                    # Find the corresponding point in the GPX
                    for track in gpx.tracks:
                        for segment in track.segments:
                            for point in segment.points:
                                if point.latitude == coordinates[idx][0] and point.longitude == coordinates[idx][1]:
                                    point.elevation = result["elevation"]
                                    break
        time.sleep(2)  # Respectful delay between batches

    with open(output_file, 'w') as gpx_file:
        gpx_file.write(gpx.to_xml())

update_gpx_elevation(input_gpx, output_gpx)
print(f"Updated GPX file saved as {output_gpx}")
