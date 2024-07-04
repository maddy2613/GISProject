from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import logging
import arcpy
from arcgis.geometry import Geometry, project
import datetime
import xml.etree.ElementTree as Et
import os

tree = Et.parse(r'C:\Users\l7bw\OneDrive - PGE\Desktop\Near Analysis\config.xml')
root = tree.getroot()

log_path = r"C:\Users\l7bw\OneDrive - PGE\Desktop\Near Analysis\Logs"
logger = logging.getLogger("LoggerName")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
filename = log_path + datetime.datetime.now().strftime('%Y_%m_%d.log')
logging.basicConfig(filename=filename, format=log_format,
                    level=log_level)
logger.info('process started')
sde_connection = root.find('sdeconnection')
temp_gdbLoc = root.find('tempFcLocation')
span_fc = root.find('spanfc')
tree_fc = root.find('treefc')
arcpy.env.workspace = sde_connection
feature_classes = arcpy.ListFeatureClasses()
if not arcpy.Exists(temp_gdbLoc):
    arcpy.CreateFileGDB_management(temp_gdbLoc)
    print('temp gdb is created')

# Loop through the list of feature classes and copy each one
for feature_class_name in feature_classes:
    # Define the full path to the feature class in the SDE database
    if feature_class_name == span_fc:
        sde_feature_class = os.path.join(sde_connection , feature_class_name)
        output_feature_class = os.path.join(temp_gdbLoc, feature_class_name)
        arcpy.Copy_management(sde_feature_class, output_feature_class)
        print(f"Copied {feature_class_name} to {temp_gdbLoc}")
    if feature_class_name == tree_fc:
        sde_feature_class = os.path.join(sde_connection , feature_class_name)
        output_feature_class = os.path.join(temp_gdbLoc, feature_class_name)
        arcpy.Copy_management(sde_feature_class, output_feature_class)
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
print(nearest_dict)
try:
    search_radius = root.find('search_radius')
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
