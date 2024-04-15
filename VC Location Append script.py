import pyodbc
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import logging
import datetime

import xml.etree.ElementTree as Et


tree = Et.parse(r'C:\Users\l7bw\Downloads\appenddata\appenddata\config.xml')
root = tree.getroot()
dbconnection = root.find('sqlconnection').text
viewcommand = root.find('sqlView').text
server = root.find('server').text
database = root.find('database').text
username = root.find('username').text
password = root.find('password').text
log_path = root.find('log_path').text

logger = logging.getLogger("LoggerName")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
filename = log_path + datetime.datetime.now().strftime('%Y_%m_%d.log')
logging.basicConfig(filename=filename, format=log_format,
                    level=log_level)

gis = GIS("home")
logger.info('connected to Portal')
feature_layer = gis.content.get("5fbb4fde46d643b896d36dbbc5069423")
feature_layer = feature_layer.layers[0]

Trusted_Connection= 'yes'
import pandas as pd
import pyodbc
import arcpy

# Define the connection parameters
# server = '10.93.209.78'
# database = 'gisdb'
# username = 'zhouser'
# password = 'Zho@Admin6789*'
insert_fields = [
"PM Assigned",
"Pole Number",
"Checklist_Status",
"City",
"PoleLat",
"PoleLong",
"ClearTypeDescription",
"ContactComments_1",
"ContactComments_2",
"created_date",
"Customer_Phone_Number_1",
"Customer_Phone_Number_2",
"CustomerName_1",
"CustomerName_2",             
"Directions",
"IsSubjectPole",
"Map_Delivery_Date",
"Notification_Type",
"PoleCounty",
"ProjPolePrc4292",
"ProjPoleScopeOfWork",
"ProjPoleUDS",
"ProjRegion",
"ProjStatus",
"ProjYear",
"QA Survey ID",
"QA_ChecklistDate",
"QA_ChecklistStatus",
"QA_FieldMapStatus",
"QC AWRR",
"QC Date",
"QC ResponsibleArea",
"QC Survey ID",
"SSD",
"Start_Pole_Barcode",
"Start_Pole_Number",
"Street",
"VCPoleNum",
"VM_Active_Alerts__c",
"VMI Inspector",
"WorkDate",
"QC ResponsibleArea",
"ProjDiv",
"ProjectPoleComments",     
"ProjectPolePrc4292Comments",
"ProjectPoleSubjectToUDS",              
"ProjName",
"ProjPole1254cStatus",
"ProjPole1255Exempt",
"ProjPoleCompletedCycle",
"ProjPoleConstraintType",
"ProjPoleEligibleCycle",
"ProjPoleID",
"ProjPoleInitialInspDate",
"ProjPoleInitialInspVendor",
"ProjPoleInspDate",
"ProjPoleName",
"PoleEquipmentList",            
"PoleFRA",        
"PoleHFTD",           
"PoleName",
"PoleRating",
"PoleSFID",
"PoleStatus",            
"ProjPoleInspector",    
"ProjPoleInspStatus"

]

field_mapping = {}
field_mapping["Checklist_Status"]="Checklist_Status"
field_mapping["City"]="City"
field_mapping["ClearTypeDescription"]="ClearTypeDescription"
field_mapping["ContactComments_1"]="ContactComments_1"
field_mapping["ContactComments_2"]="ContactComments_2"
field_mapping["created_date"]="created_date"
field_mapping["Customer_Phone_Number_1"]="Customer_Phone_Number_1"
field_mapping["Customer_Phone_Number_2"]="Customer_Phone_Number_2"
field_mapping["CustomerName_1"]="CustomerName_1"
field_mapping["CustomerName_2"]="CustomerName_2"
field_mapping["Directions"]="Directions"
field_mapping["IsSubjectPole"]="IsSubjectPole"
field_mapping["Map_Delivery_Date"]="Map_Delivery_Date"
field_mapping["Notification_Type"]="Notification_Type"
field_mapping["PM Assigned"]="PM_Assigned"
field_mapping["Pole Number"]="Pole_Number"
field_mapping["PoleCounty"]="PoleCounty"
field_mapping["PoleEquipmentList"]="PoleEquipmentList"
field_mapping["PoleFRA"]="PoleFRA"
field_mapping["PoleHFTD"]="PoleHFTD"
field_mapping["PoleLat"]="PoleLat"
field_mapping["PoleLong"]="PoleLong"
field_mapping["PoleName"]="PoleName"
field_mapping["PoleRating"]="PoleRating"
field_mapping["PoleSFID"]="PoleSFID"
field_mapping["PoleStatus"]="PoleStatus"
field_mapping["ProjDiv"]="ProjDiv"
field_mapping["ProjectPoleComments"]="ProjectPoleComments"
field_mapping["ProjectPolePrc4292Comments"]="ProjectPolePrc4292Comments"
field_mapping["ProjectPoleSubjectToUDS"]="ProjectPoleSubjectToUDS"
field_mapping["ProjName"]="ProjName"
field_mapping["ProjPole1254cStatus"]="ProjPole1254cStatus"
field_mapping["ProjPole1255Exempt"]="ProjPole1255Exempt"
field_mapping["ProjPoleCompletedCycle"]="ProjPoleCompletedCycle"
field_mapping["ProjPoleConstraintType"]="ProjPoleConstraintType"
field_mapping["ProjPoleEligibleCycle"]="ProjPoleEligibleCycle"
field_mapping["ProjPoleID"]="ProjPoleID"
field_mapping["ProjPoleInitialInspDate"]="ProjPoleInitialInspDate"
field_mapping["ProjPoleInitialInspVendor"]="ProjPoleInitialInspVendor"
field_mapping["ProjPoleInspDate"]="ProjPoleInspDate"
field_mapping["ProjPoleInspector"]="ProjPoleInspector"
field_mapping["ProjPoleInspStatus"]="ProjPoleInspStatus"
field_mapping["ProjPoleName"]="ProjPoleName"
field_mapping["ProjPolePrc4292"]="ProjPolePrc4292"
field_mapping["ProjPoleScopeOfWork"]="ProjPoleScopeOfWork"
field_mapping["ProjPoleUDS"]="ProjPoleUDS"
field_mapping["ProjRegion"]="ProjRegion"
field_mapping["ProjStatus"]="ProjStatus"
field_mapping["ProjYear"]="ProjYear"
field_mapping["QA Survey ID"]="QA_Survey_ID"
field_mapping["QA_ChecklistDate"]="QA_ChecklistDate"
field_mapping["QA_ChecklistStatus"]="QA_ChecklistStatus"
field_mapping["QA_FieldMapStatus"]="QA_FieldMapStatus"
field_mapping["QC AWRR"]="QC_AWRR"
field_mapping["QC Date"]="QC_Date"
field_mapping["QC Survey ID"]="QC_Survey_ID"
field_mapping["SSD"]="SSD"
field_mapping["Start_Pole_Barcode"]="Start_Pole_Barcode"
field_mapping["Start_Pole_Number"]="Start_Pole_Number"
field_mapping["Street"]="Street"
field_mapping["VCPoleNum"]="VCPoleNum"
field_mapping["VM_Active_Alerts__c"]="VM_Active_Alerts__c"
field_mapping["VMI Inspector"]="VMI_Inspector"
field_mapping["WorkDate"]="WorkDate"
field_mapping["QC ResponsibleArea"]="WVResponsibleArea"

# Establish the connection
# conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
conn = pyodbc.connect('DRIVER={SQL Server};SERVER='+server+';DATABASE='+database+';Trusted_Connection='+Trusted_Connection+';')
# Execute the query and fetch the results into a pandas DataFrame
data = pd.read_sql(viewcommand, conn)

# Close the connection
conn.close()
logger.info('successfully read data from sql View')
print(data)
#exit(0)
feature_attributes=[];
for index,row in data.iterrows():
    feature_obj = {}
    point_geometry = {}
    spatial_reference = arcpy.SpatialReference(4326)
    for col in insert_fields:
        try:
            fieldname=field_mapping[col]
            feature_obj[fieldname] = row[col] 
        except Exception as err:
            feature_obj[col] = row[col]   
        
        if col == 'PoleLong':
            point_geometry["Y"] = row[col]
            continue
        if col == 'PoleLat':
            point_geometry["X"] = row[col]
            continue
    feature = {"attributes": feature_obj,
              "geometry": {"x":point_geometry["X"],"y":point_geometry["Y"]}
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

