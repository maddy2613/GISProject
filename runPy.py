from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import logging
import arcpy
from arcgis.geometry import Geometry, project
import datetime
import xml.etree.ElementTree as Et
import os

tree = Et.parse(r'C:\Users\l7bw\OneDrive - PGE\Desktop\Near N Append\config.xml')
root = tree.getroot()

log_path = r"C:\Users\l7bw\OneDrive - PGE\Desktop\Near N Append\Logs"
logger = logging.getLogger("LoggerName")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
filename = log_path + datetime.datetime.now().strftime('%Y_%m_%d.log')
logging.basicConfig(filename=filename, format=log_format,
                    level=log_level)
logger.info('process started')
sde_connection = root.find('sdeconnection').text
temp_gdbLoc = root.find('tempFcLocation').text
span_fc = root.find('spanfc').text
tree_fc = root.find('treefc').text
hosted_fcItemId = root.find('hostedFeatureItemId').text
arcpy.env.workspace = sde_connection
feature_classes = arcpy.ListFeatureClasses()
if not arcpy.Exists(os.path.join(temp_gdbLoc,"temp.gdb")):
    arcpy.CreateFileGDB_management(temp_gdbLoc,"temp.gdb")
    print('temp gdb is created')


# Loop through the list of feature classes and copy each one
temp_gdbLoc = os.path.join(temp_gdbLoc,"temp.gdb")
arcpy.env.workspace = temp_gdbLoc
arcpy.env.overwriteOutput = True
for feature_class_name in feature_classes:
    # Define the full path to the feature class in the SDE database
    if feature_class_name == span_fc:
        arcpy.Copy_management(os.path.join(sde_connection,feature_class_name), os.path.join(temp_gdbLoc,feature_class_name))
        print(f"Copied {feature_class_name} to {temp_gdbLoc}")
    if feature_class_name == tree_fc:
        arcpy.Copy_management(os.path.join(sde_connection,feature_class_name), os.path.join(temp_gdbLoc,feature_class_name))
        print(f"Copied {feature_class_name} to {temp_gdbLoc}")
print("All feature classes have been copied.")

span_fc = os.path.join(temp_gdbLoc, span_fc)
tree_fc = os.path.join(temp_gdbLoc, tree_fc)
nearest_dict = {}
with arcpy.da.SearchCursor(span_fc, ["OID", "SPAN_ID","AuditId"]) as rows:
    for row in rows:
        try:
            nearest_dict[row[0]] = {"field1":row[1],"field2":row[2]}
        except Exception as err:
            logger.error('error preparing obj {}'.format(err))
            print('error preparing obj {}'.format(err))
            continue
#print(nearest_dict)
try:
    search_radius = root.find('search_radius').text
    arcpy.analysis.Near(tree_fc,span_fc, search_radius, "NO_LOCATION", "NO_ANGLE","PLANAR","NEAR_FID NEAR_FID; NEAR_DIST NEAR_DIST")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as err2:
    logger.error(err2)
print(print(arcpy.GetMessages()))

logger.info('calculating SPANID and Audit Id fields')
fields = ['NEAR_FID','SPAN_ID', 'AuditID']

# Create update cursor for feature class
with arcpy.da.UpdateCursor(tree_fc, fields) as cursor:
    for row in cursor:
        try:
            cal_fields =  nearest_dict[row[0]]
            row[1] = cal_fields['field1']
            row[2] = cal_fields['field2']
            cursor.updateRow(row)
        except Exception as err3:
            logger.info('failed while updating fileds')
            print('failed while updating fileds')
            continue

gis = GIS("Home")
feature_layer_item = gis.content.get(hosted_fcItemId)
feature_layer = feature_layer_item.layers[0]  # Assumes you are targeting the first layer

# Truncate (delete all features from) the FeatureLayer
feature_layer.delete_features(where="1=1")
##################################################################
# first approach
##################################################################
# Read the FeatureClass into a FeatureSet
# feature_set = arcpy.FeatureSet()
# feature_set.load(tree_fc)
# # Convert arcpy FeatureSet to ArcGIS FeatureCollection
# features = [f for f in feature_set]

# # Insert features into the hosted FeatureLayer
# feature_layer.edit_features(adds=features)

#############################################################################
# second approach
#############################################################################
fields = ['SHAPE@', 'PROJ_ID',
'PROJ_NAME',
'PROJ_BUNDLE',
'PROJ_REGION',
'PROJ_DIVISION',
'PROJ_SERVICE_TERRITORY',
'PROJ_PROGRAM',
'PROJ_PATROL_TYPE',
'PROJ_NUMBER',
'PROJ_TYPE',
'PROJ_RECORD_TYPE',
'PROJ_YEAR',
'PROJ_QUARTER',
'PROJ_VEG_WORK_STATUS',
'PRESCRIP_ID',
'SPECIES_COMMON',
'SPECIES_SCIENTIFIC',
'HEIGHT',
'DBH',
'STREET',
'CITY',
'COUNTY',
'COMMENTS',
'TREE_OWNERSHIP',
'CREATED_DATE',
'CREATED_BY',
'LAT',
'LONG',
'STATUS',
'f_VM_Work_Code__c',
'PRESCRIP_NAME',
'VM_Veg_Point__c',
'PRESCRIP_COMMENTS',
'PRESCRIP_PARCEL_ID',
'TAG_TYPE',
'TAG_NUMBER',
'Actual_Trim_Code',
'WO_NUM',
'VegPointName',
'HFTD',
'VP_ADDRESS',
'TW_WO_STATUS',
'TW_WO_VENDOR',
'WOLI_TW_PERFORMED_BY',
'WOLI_TW_VENDOR',
'WOLI_TW_STATUS',
'WOLI_COMMENT',
'PI_LANID',
'PI_COMPANY',
'SafetyAlerts',
'WORK_TYPE',
'APN',
'Directions',
'MWS_Exemption_Description',
'VM_Master_Parcel_ID__c',
'Load_date',
'SPAN_ID',
'Map_Delivery_Date',
'WOLI_TW_END',
'ContactComments_1',
'CustomerName_2',
'Customer_Phone_Number_2',
'ContactComments_2',
'VM_ACTION_TYPE_C',
'VegPointSource',
'MWS',
'DEAD_DYING',
'TREE_CREW_ADDED',
'RADIAL_CLEARANCE',
'VERTICAL_CLEARANCE',
'HORIZONTAL_CLEARANCE',
'OBSERVED_RADIAL_DISTANCE',
'BRUSH_QUANTITY',
'TRAFFIC_MITIGATION',
'TreeWorkPerformedBy',
'WO_LINE_ITEM_NUM',
'Constraint_Context',
'Constraint_Category']  # Replace with your specific fields

# Read the features with selected fields

with arcpy.da.SearchCursor(tree_fc, fields) as cursor:
    for row in cursor:
        try:
            attributes = dict(zip(fields, row))
            features = []
            features.append({
                "attributes": {k: v for k, v in attributes.items() if k != 'SHAPE@'},
                "geometry": attributes['SHAPE@'].__geo_interface__  # Convert geometry to GeoJSON format
            })
            feature_layer.edit_features(adds=features)
        except Exception as err:
            continue
        

# Insert selected features into the hosted FeatureLayer

print('Features added successfully.')
