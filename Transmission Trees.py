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
feature_layer = gis.content.get("55c0e2640530490eb46c4b00cdfd7f50")
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
"PIProjectStatus",
"Trim_Status",
"HFTDType",
"TreesperLoc",
"Trees_Completed",
"TreeLocID",
"treerecsid",
"HFTDTier",
"ProjYr",
"AcctType",
"Division",
"Region",
"ProjectName",
"CIRCUIT_NAME",
"StreetNum",
"StreetName",
"City",
"CountyCode",
"SourceDev",
"SSDRoute",
"RouteNum",
"PoleNum",
"PoleNum2",
"LineID",
"Voltage",
"Latitude",
"Longitude",
"LOC_INSP_DATE",
"TREE_REC_INSP_DATE",
"Insp",
"InspComp",
"WorkBy",
"TreeCode",
"Descrip1",
"sTrimCode",
"ActTrimCode",
"Qty",
"nDBH",
"Notification",
"sPCode",

"workreq",
"Descrip2",
"SRA",
"CustomerName",
"CustomerPhone",
"TreeComments",

"LocationDirections",
"sComments",
"sDescrip",
"Prescription_Comments",
"Manager",
"Supervisor",
"Map_Delivery_Date",
"TreeCompanycode",
"Date_DataPulled",
"Orig_SpreadsheetFile",
"DataSource",
"T_or_D",
"QA_FieldMapStatus",
"QA_ChecklistStatus",
"QA_ChecklistDate",
"QC_FieldMapStatus",
"QC_ChecklistStatus",
"QC_ChecklistDate",
"Source_Device_Route",
"MWS",
"QA_Audit_ID",
"PI_Comp",
"project_number",
"PIActStartDate",
"PIActCompDate",
"TreeCompanyActStartDate",
"TreeCompanyActCompDate",
"MWSExemptDesc",
"MWSDocNum",
"AlertCodes",
"AlertDesc",
"Tree_Type",
"ProjNM_iSSDRoute",
"QC_Survey_ID",
"nHeight"
#"Clearance",
#"LocationComments",
#"WorkDate"
]

field_mapping = {}
field_mapping ["PIProjectStatus"]="PIProjectStatus"
field_mapping ["Trim_Status"]="Trim_Status"
field_mapping ["HFTDType"]="HFTDType"
field_mapping ["TreesperLoc"]="TreesperLoc"
field_mapping ["Trees_Completed"]="Trees_Completed"
field_mapping ["TreeLocID"]="TreeLocID"
field_mapping ["treerecsid"]="treerecsid"
field_mapping ["HFTDTier"]="HFTDTier"
field_mapping ["ProjYr"]="ProjYr"
field_mapping ["AcctType"]="AcctType"
field_mapping ["Division"]="Division"
field_mapping ["Region"]="Region"
field_mapping ["ProjectName"]="ProjectName"
field_mapping ["CIRCUIT_NAME"]="CIRCUIT_NAME"
field_mapping ["StreetNum"]="StreetNum"
field_mapping ["StreetName"]="StreetName"
field_mapping ["City"]="City"
field_mapping ["CountyCode"]="CountyCode"
field_mapping ["SourceDev"]="SourceDev"
field_mapping ["SSDRoute"]="SSDRoute"
field_mapping ["RouteNum"]="RouteNum"
field_mapping ["PoleNum"]="PoleNum"
field_mapping ["PoleNum2"]="PoleNum2"
field_mapping ["LineID"]="LineID"
field_mapping ["Voltage"]="Voltage"
field_mapping ["Latitude"]="Latitude"
field_mapping ["Longitude"]="Longitude"
field_mapping ["LOC_INSP_DATE"]="LOC_INSP_DATE"
field_mapping ["TREE_REC_INSP_DATE"]="TREE_REC_INSP_DATE"
field_mapping ["Insp"]="Insp"
field_mapping ["InspComp"]="InspComp"
field_mapping ["WorkBy"]="WorkBy"
field_mapping ["TreeCode"]="TreeCode"
field_mapping ["Descrip1"]="Descrip1"
field_mapping ["sTrimCode"]="sTrimCode"
field_mapping ["ActTrimCode"]="ActTrimCode"
field_mapping ["Qty"]="Qty"
field_mapping ["nDBH"]="nDBH"
field_mapping ["nHeight"]="nHeight"
field_mapping ["Clearance"]="Clearance"
field_mapping ["Notification"]="Notification"
field_mapping ["sPCode"]="sPCode"
field_mapping ["WorkDate"]="WorkDate"
field_mapping ["workreq"]="workreq"
field_mapping ["Descrip2"]="Descrip2"
field_mapping ["SRA"]="SRA"
field_mapping ["CustomerName"]="CustomerName"
field_mapping ["CustomerPhone"]="CustomerPhone"
field_mapping ["TreeComments"]="TreeComments"
field_mapping ["LocationComments"]="LocationComments"
field_mapping ["LocationDirections"]="LocationDirections"
field_mapping ["sComments"]="sComments"
field_mapping ["sDescrip"]="sDescrip"
field_mapping ["Prescription_Comments"]="Prescription_Comments"
field_mapping ["Manager"]="Manager"
field_mapping ["Supervisor"]="Supervisor"
field_mapping ["Map_Delivery_Date"]="Map_Delivery_Date"
field_mapping ["TreeCompanycode"]="TreeCompanycode"
field_mapping ["Date_DataPulled"]="Date_DataPulled"
field_mapping ["Orig_SpreadsheetFile"]="Orig_SpreadsheetFile"
field_mapping ["DataSource"]="DataSource"
field_mapping ["T_or_D"]="T_or_D"
field_mapping ["QA_FieldMapStatus"]="QA_FieldMapStatus"
field_mapping ["QA_ChecklistStatus"]="QA_ChecklistStatus"
field_mapping ["QA_ChecklistDate"]="QA_ChecklistDate"
field_mapping ["QC_FieldMapStatus"]="QC_FieldMapStatus"
field_mapping ["QC_ChecklistStatus"]="QC_ChecklistStatus"
field_mapping ["QC_ChecklistDate"]="QC_ChecklistDate"
field_mapping ["Source_Device_Route"]="Source_Device_Route"
field_mapping ["MWS"]="MWS"
field_mapping ["QA_Audit_ID"]="QA_Audit_ID"
field_mapping ["PI_Comp"]="PI_Comp"
field_mapping ["project_number"]="project_number"
field_mapping ["PIActStartDate"]="PIActStartDate"
field_mapping ["PIActCompDate"]="PIActCompDate"
field_mapping ["TreeCompanyActStartDate"]="TreeCompanyActStartDate"
field_mapping ["TreeCompanyActCompDate"]="TreeCompanyActCompDate"
field_mapping ["MWSExemptDesc"]="MWSExemptDesc"
field_mapping ["MWSDocNum"]="MWSDocNum"
field_mapping ["AlertCodes"]="AlertCodes"
field_mapping ["AlertDesc"]="AlertDesc"
field_mapping ["Tree_Type"]="Tree_Type"
field_mapping ["ProjNM_iSSDRoute"]="ProjNM_iSSDRoute"
field_mapping ["QC_Survey_ID"]="QC_Survey_ID"


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
        
        if col == 'Longitude':
            point_geometry["Y"] = row[col]
            continue
        if col == 'Latitude':
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

