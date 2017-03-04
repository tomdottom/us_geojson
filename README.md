# us_geojson

A simple script to generate state by state geojson files.

geojson files are outputted as US/{State}/{type}.geojson.gz

# Usage

```
pip install -r requirements.txt
python generate_us_geojson.py
```

# Pre-generated geojson files

Each state folder contains the following gzipped files:

```
File                | Description
---------------------------------------------
cd.geojson.gz       | Congressional Districts
county.geojson.gz   | Counties
state.geojson.gz    | State
tract.geojson.gz    | Census Tracts
zcta.geojson.gz     | Zip Code Tabulation Areas
```
