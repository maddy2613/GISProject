import pyodbc
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import logging
import datetime
import csv
import pandas as pd
import arcpy

csv_file_path = r'C:\Users\l7bw\OneDrive - PGE\Desktop\Append data\Distribution Span Location\Distribution Span Location.csv'
log_path = r'C:\Users\l7bw\OneDrive - PGE\Desktop\Append data\Distribution Span Location\Logs'
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
count = 0
feature_attributes=[];
for index, row in data.iterrows():
    feature_obj = {}
    point_geometry =arcpy.Point()
    end_point_geometry =arcpy.Point()
    spatial_reference = arcpy.SpatialReference(4326)
    array= arcpy.Array()
    #print(configObject['fieldsList'])   
    for col in configObject['fieldsList']:
        try:
            if col['sql_field'] == 'splong':
                try:
                    point_geometry.X = row[col['sql_field']]
                except Exception as Err2:
                    break
            if col['sql_field'] == 'splat':
                try:
                    point_geometry.Y = row[col['sql_field']]
                except Exception as Err3:
                    break
            
            if col['sql_field'] == 'eplong':
                try:
                    end_point_geometry.X = row[col['sql_field']]
                except Exception as Err2:
                    break
            if col['sql_field'] == 'eplat':
                try:
                    end_point_geometry.Y = row[col['sql_field']]
                except Exception as Err3:
                    break
            value = None
            if col['gis_datatype'] == 'boolean':
                if row[col['sql_field']] == 'Yes':
                    value = 1
                if row[col['sql_field']] == 'No':
                    value = 0
            elif col['gis_datatype'] == 'bit':
                value = None
                if row[col['sql_field']] == 'True':
                    value = 1
                if row[col['sql_field']] == 'False':
                    value = 0
            elif col['gis_datatype'] == 'varchar':
                if row[col['sql_field']] == 'XYZ':
                    value = 1
                if row[col['sql_field']] == 'No':
                    value = 0
            elif col['gis_datatype'] == 'nvarchar':
                value = row[col['sql_field']]
                if value is not None:
                    value = value.replace("<","&lt;")
                    value = value.replace(">","&gt;")
            elif col['gis_datatype'] == 'int':
                try:
                    value = (row[col['sql_field']])
                except Exception as err1:
                    value = 0
            elif col['gis_datatype'] == 'decimal':
                try:
                    value = (row[col['sql_field']])
                except Exception as err1:
                    value = 0.0
            elif col['gis_datatype'] == 'Date':
                try:
                    if str(row[col['sql_field']]) == 'NaT':
                        value = None
                    else:
                        value = row[col['sql_field']]
                except Exception as err1:
                    break
                #print(value)
            else:
                value = row[col['sql_field']]
            feature_obj[col['gis_field']] = value
        except Exception as err:
            logger.warning(err)
            print(err)
    try:
        pointG = arcpy.PointGeometry(point_geometry, spatial_reference).projectAs(arcpy.SpatialReference(102100))
        e_pointG = arcpy.PointGeometry(end_point_geometry, spatial_reference).projectAs(arcpy.SpatialReference(102100))
        array.add(point_geometry)
        array.add(end_point_geometry)
        polyline= arcpy.Polyline(array)
        #feature_obj["SHAPE"]= polyline
        feature = {"attributes": feature_obj,
                   "geometry": polyline.JSON
               }
        feature_attributes.append(feature)
        add_results = feature_layer.edit_features(adds = [feature])
        feature_attributes = []
        print(add_results)
        count = count + 1
    except Exception as err5:
        print(err5)
        continue
# print(feature_attributes)
# logger.info(feature_attributes)
# print(add_results)
# logger.info(add_results)
# count = 0
# for obj in add_results['addResults']:
#     if obj['success'] :
#         count = count+1
print('{} successfully inserted features'.format(count))
logger.info('{} successfully inserted features'.format(count))