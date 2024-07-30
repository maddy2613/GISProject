from arcgis.gis import GIS
from arcgis.features import FeatureLayer

# Connect to ArcGIS Online
gis = GIS("https://www.arcgis.com", "your_username", "your_password")

# Access the hosted feature layer
feature_layer_url = "https://services.arcgis.com/your_service/FeatureServer/0"
layer = FeatureLayer(feature_layer_url)

# Define the new layer definition
new_definition = {
    "drawingInfo": {
        "renderer": {
            "type": "simple",
            "symbol": {
                "type": "esriSMS",
                "style": "esriSMSCircle",
                "color": [255, 0, 0, 128],
                "size": 8,
                "outline": {
                    "color": [0, 0, 0, 255],
                    "width": 1
                }
            }
        }
    },
    "maxRecordCount": 2000,
    "timeInfo": {
        "startTimeField": "start_date",
        "endTimeField": "end_date",
        "timeReference": {
            "timeZone": "Pacific Standard Time",
            "respectsDaylightSaving": True
        }
    }
}

# Update the feature layer definition
response = layer.manager.update_definition(new_definition)

# Check the response
if 'success' in response and response['success']:
    print("Layer definition updated successfully.")
else:
    print("Failed to update layer definition.")
    print(response)
