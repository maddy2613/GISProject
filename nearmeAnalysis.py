from arcgis.gis import GIS
from arcgis.features import FeatureLayer
import logging
import arcpy
from arcgis.geometry import Geometry, project
import datetime

log_path = r"C:\Users\l7bw\OneDrive - PGE\Desktop\Near Analysis\Logs"
logger = logging.getLogger("LoggerName")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
filename = log_path + datetime.datetime.now().strftime('%Y_%m_%d.log')
logging.basicConfig(filename=filename, format=log_format,
                    level=log_level)
logger.info('process started')
in_fc =r"C:\Users\l7bw\OneDrive - PGE\Desktop\Prod Data Append 0617.gdb\FTI_SpanInspection_QC_Not_Ready_0617"
nearme_fc =r"C:\Users\l7bw\OneDrive - PGE\Desktop\Prod Data Append 0617.gdb\FTI_TreePrescription_QC_Not_Ready_0617"
nearest_dict = {}
with arcpy.da.SearchCursor(in_fc, ["OID", "SPAN_ID","AuditId"]) as rows:
    for row in rows:
        try:
            nearest_dict[row[0]] = {"field1":row[1],"field2":row[2]}
        except Exception as err:
            logger.error('error preparing obj {}'.format(err))
            print('error preparing obj {}'.format(err))
            continue
print(nearest_dict)
try:
    search_radius = "500 DecimalDegrees"
    arcpy.analysis.Near(nearme_fc,in_fc, search_radius, "NO_LOCATION", "NO_ANGLE","PLANAR","NEAR_FID NEAR_FID; NEAR_DIST NEAR_DIST")
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))
except Exception as err2:
    logger.error(err2)
print(print(arcpy.GetMessages()))

logger.info('calculating SPANID and Audit Id fields')
fields = ['NEAR_FID','SPAN_ID', 'AuditID']

# Create update cursor for feature class
with arcpy.da.UpdateCursor(nearme_fc, fields) as cursor:
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
