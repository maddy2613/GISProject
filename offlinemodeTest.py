from arcgis.gis import GIS

# Connect to your ArcGIS Online organization
gis = GIS("https://www.arcgis.com", "username", "password")

# Get the item ID of your Field Map
field_map_item_id = "your_field_map_item_id"

# Access the Field Map item
field_map_item = gis.content.get(field_map_item_id)

# Access the Field Map
field_map = field_map_item.get_data()

# Iterate through layers in the Field Map
for layer in field_map['layers']:
    # Check if the layer supports offline mode
    supports_offline = layer.get('supportsOffline')
    if supports_offline:
        print(f"Layer '{layer['name']}' supports offline mode.")
    else:
        print(f"Layer '{layer['name']}' does not support offline mode.")


from arcgis.gis import GIS

# Connect to your ArcGIS Online organization
gis = GIS("https://www.arcgis.com", "username", "password")

# Get the item ID of your web map containing the layer
web_map_item_id = "your_web_map_item_id"

# Access the web map item
web_map_item = gis.content.get(web_map_item_id)

# Access the web map
web_map = web_map_item.get_data()

# Iterate through operational layers in the web map
for layer in web_map['operationalLayers']:
    # Check if the layer supports offline mode
    supports_offline = layer.get('supportsOffline')
    if supports_offline:
        print(f"Layer '{layer['title']}' supports offline mode.")
        
        # Check if any offline replicas exist for the layer
        replicas = gis.content.search(f"title:'{layer['title']}' AND type:'Feature Service' AND owner:{gis.users.me.username} AND access:org")
        if replicas:
            print(f"Offline replicas exist for Layer '{layer['title']}'.")
        else:
            print(f"No offline replicas found for Layer '{layer['title']}'.")
    else:
        print(f"Layer '{layer['title']}' does not support offline mode.")

from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection

# Connect to your ArcGIS Online organization
gis = GIS("https://www.arcgis.com", "username", "password")

# Get the URL of your feature service
feature_service_url = "URL_of_your_feature_service"

# Access the feature layer collection
feature_layer_collection = FeatureLayerCollection(feature_service_url)

# Check synchronization status
synchronization_status = feature_layer_collection.manager.synchronization_status()

# Print synchronization status
print("Synchronization Status:", synchronization_status)
