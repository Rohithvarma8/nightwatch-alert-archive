# nightwatch-alert-archive

Every 10 minutes, a GitHub Actions workflow records the active National Weather Service alerts for California.

## What it records

`record.py` fetches `https://api.weather.gov/alerts/active?area=CA` and saves each alert (a GeoJSON feature) once to:

```
archive/nws/<YYYY-MM-DD of properties.sent>/<first 16 hex chars of sha1(properties.id)>.json
```

It never overwrites existing files. Each saved alert gets a `_recorded_at` UTC timestamp.

## Why

The archive is replay data for the **Night Watch** hackathon project. The live alert feed only shows what's active right now. A history lets us replay real alert sequences while developing and demoing.

## Running locally

```sh
NWS_USER_AGENT="(your-app, you@example.com)" python3 record.py
```

The workflow reads `NWS_USER_AGENT` from a repository secret.

## Data source

The alert data comes from the [National Weather Service API](https://www.weather.gov/documentation/services-web-api). As a work of the U.S. federal government, it is in the public domain.
