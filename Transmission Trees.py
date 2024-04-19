import pyodbc
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import logging
import datetime
import csv
import pandas as pd
import arcpy

csv_file_path = r'C:\Users\l7bw\OneDrive - PGE\Desktop\Book1.csv'
log_path = r'C:\Users\l7bw\OneDrive - PGE\Desktop\Logs'
logger = logging.getLogger("LoggerName")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
filename = log_path + datetime.datetime.now().strftime('%Y_%m_%d.log')
logging.basicConfig(filename=filename, format=log_format,
                    level=log_level)
logger.info('process started')
# 'DRIVER={SQL Server};SERVER=DBServername;DATABASE=sqldatabase;Trusted_Connection=yes;'
configObject = {}
with open(csv_file_path, newline='') as csvfile:
    # Create a CSV reader object
    csv_reader = csv.reader(csvfile)
    # Iterate over each row in the CSV file

    configObject['fieldsList']= []
    rowIndex = 0
    for row in csv_reader:
        if rowIndex == 0:
            configObject['dbconnection'] = row[1]
        if rowIndex == 1:
            configObject['sqlcommand'] = row[1]
        if rowIndex == 2:
            configObject['itemId'] = row[1]
        if rowIndex == 3:
            rowIndex = rowIndex + 1
            continue
        if rowIndex > 3:
            configObject['fieldsList'].append({
                'sql_field': row[0],
                'gis_field': row[1],
                'gis_datatype': row[2]
            })
        rowIndex = rowIndex + 1
    print(configObject)

logger.info('csv read successfully')
gis = GIS("home")
logger.info('connected to Portal')
feature_layer = gis.content.get(configObject['itemId'])
feature_layer = feature_layer.layers[0]
conn = pyodbc.connect(configObject['dbconnection'])
data = pd.read_sql(configObject['sqlcommand'], conn)
conn.close()
logger.info('successfully read data from sql View')
print(data)
feature_attributes=[];
for index, row in data.iterrows():
    feature_obj = {}
    point_geometry =arcpy.Point()
    
    spatial_reference = arcpy.SpatialReference(4326)
    print(configObject['fieldsList'])   
    for col in configObject['fieldsList']:
        try:
            if col['sql_field'] == 'Longitude':
                #point_geometry["Y"] = row[col['sql_field']]
                point_geometry.Y = row[col['sql_field']]
                print(row[col['sql_field']])
            if col['sql_field'] == 'Latitude':
                #point_geometry["X"] = row[col['sql_field']]
                point_geometry.X = row[col['sql_field']]
                print(row[col['sql_field']])
            value = None
            if col['gis_datatype'] == 'boolean':
                if row[col['sql_field']] == 'Yes':
                    value = 1
                if row[col['sql_field']] == 'No':
                    value = 0
            elif col['gis_datatype'] == 'nvarchar':
                value = row[col['sql_field']]
            elif col['gis_datatype'] == 'int':
                value = int(row[col['sql_field']])
            elif col['gis_datatype'] == 'decimal':
                value = float(row[col['sql_field']])
                print(value)
            else:
                value = row[col['sql_field']]
            feature_obj[col['gis_field']] = value
        except Exception as err:
            logger.warning(err)
            print(err)
    pointG = arcpy.PointGeometry(point_geometry, spatial_reference).projectAs(arcpy.SpatialReference(102100))
    feature = {"attributes": feature_obj,
               "geometry": {"x": point_geometry.centroid.X, "y": point_geometry.centroid.Y}
               }
    feature_attributes.append(feature)
print(feature_attributes)
logger.info(feature_attributes)
add_results = feature_layer.edit_features(adds = feature_attributes)
print(add_results)
logger.info(add_results)
count = 0
for obj in add_results['addResults']:
    if obj['success'] :
        count = count+1
print('{} successfully inserted features'.format(count))
logger.info('{} successfully inserted features'.format(count))
