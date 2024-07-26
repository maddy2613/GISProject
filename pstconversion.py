from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import pytz
from datetime import datetime, timezone, timedelta

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# Access the hosted feature layer
feature_layer_url = "https://services.arcgis.com/your_service/FeatureServer/0"
layer = FeatureLayer(feature_layer_url)

# Define the UTC and PST timezones
utc_tz = pytz.utc
pst_tz = pytz.timezone("US/Pacific")

# Query all features in the layer
features = layer.query(where="1=1").features

# Function to convert UTC date to PST
def convert_utc_to_pst(utc_date):
    utc_date = utc_date.replace(tzinfo=utc_tz)
    pst_date = utc_date.astimezone(pst_tz)
    return pst_date

# List to hold updated features
updated_features = []

for feature in features:
    # Convert the date fields
    if 'your_date_field' in feature.attributes:
        utc_date = feature.attributes['your_date_field']
        if utc_date:
            utc_date = datetime.fromtimestamp(utc_date / 1000, tz=utc_tz)
            pst_date = convert_utc_to_pst(utc_date)
            feature.attributes['your_date_field'] = int(pst_date.timestamp() * 1000)
    
    updated_features.append(feature)

# Update the feature layer with the new date values
if updated_features:
    result = layer.edit_features(updates=updated_features)
    print(f"Updated {len(updated_features)} features.")
else:
    print("No features to update.")
