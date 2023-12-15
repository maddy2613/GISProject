from arcgis.gis import GIS
from arcgis.mapping import WebMap

# Connect to your ArcGIS Online organization
gis = GIS("home")

# Get the web map item
web_map_item = gis.content.get("<your_web_map_item_id>")

# Access the web map
web_map = WebMap(web_map_item)

# Access the first operational layer in the web map
operational_layer = web_map.layers[0]

# Update the popup attributes
# This example assumes that you have a field named 'field_to_update'
# Modify it according to your field names and values
popup_info = {
    "title": "New Title",
    "content": [
        {
            "type": "fields",
            "fieldInfos": [
                {
                    "fieldName": "field_to_update",
                    "label": "Field Label",
                    "visible": True
                },
                # Add more fields if needed
            ]
        }
    ]
}

operational_layer.popup_info = popup_info

# Save the changes back to the web map
web_map.update()

print("Popup attributes updated successfully.")