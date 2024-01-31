import logging
import  configReader
import datetime
from arcgis.gis import GIS
import  requests
import  arcpy
import json
from arcgis.features import FeatureLayer
from arcgis.mapping import WebMap

portal_url, portal_user, portal_password, log_path = configReader.get_portal_info()

logger = logging.getLogger("LoggerName")
log_format = "%(asctime)s - %(levelname)s - %(message)s"
log_level = logging.INFO
filename = log_path + datetime.datetime.now().strftime('%Y_%m_%d.log')
logging.basicConfig(filename=filename, format=log_format,
                    level=log_level)
def update_popup_Layer(operation_layer,map,token,web_map):
    try:
        if operation_layer.layerType == 'GroupLayer':
            if len(operation_layer.layers) > 0:
                for layer_obj in operation_layer.layers:
                    try:
                        obj_layer = map['layers'][layer_obj.url]
                        oprn_lyr_fields = {}
                        if hasattr(layer_obj,'popupInfo'):
                            layerObjRest = requests.get('{0}?token={1}&f=pjson'.format(layer_obj.url, token))
                            if layerObjRest.status_code == 200:
                                for fields_obj in layerObjRest.json()['fields']:
                                    oprn_lyr_fields[fields_obj['alias']] = fields_obj['name']
                                fileds_info = []
                                for l_fields in obj_layer['fields']:
                                    try:
                                        fileds_info.append({
                                            "fieldName": oprn_lyr_fields[l_fields['aliyas']],
                                            "label": l_fields['aliyas'],
                                            "visible": True
                                        })
                                    except Exception as err:
                                        logger.info('aliyas not exist in the operation layer {0}'.format(l_fields['aliyas']))
                                        print('aliyas not exist in the operation layer {0}'.format(l_fields['aliyas']))
                                        continue
                                popup_info = {
                                    "title": layer_obj['title'],
                                    "fieldInfos": fileds_info,
                                    "description":operation_layer.popupInfo["description"],
                                    "expressionInfos":operation_layer.popupInfo["expressionInfos"]
                                }
                                operation_layer.popupInfo = popup_info
                                web_map.update()
                                logger.info('web map popup info updated successfully.. Item Id id {}'.format(layer_obj['title']))
                                print('web map popup info updated successfully.. Item Id id {}'.format(layer_obj['title']))
                        else:
                            logger.info('popupInfo attribute not exist in the Layer {}'.format(layer_obj['title']))
                            print('popupInfo attribute not exist in the Layer {}'.format(layer_obj['title']))
                            continue
                    except Exception as err2:
                        logger.error('err2 in GroupLayerFun {0}'.format(err2))
                        print('err2 in GroupLayerFun {0}'.format(err2))
                        continue
            else:
                logger.info('no Layers found in  the Group Layer')
                print('no Layers found in  the Group Layer')
    except Exception as err:
        logger.error('error occued while updating popup {0}'.format(err))

def update_webmaps_layer_popups():
    try:
        logger.info('process started..!!!')
        gis = GIS("home")
        webmap_obj = configReader.read_webmap_layer_fields()
        logger.info(webmap_obj)
        # exit(0)

        webmaps = configReader.get_fields_mappings_by_webmap_layers()
        token = gis._con.token
        # logger.info(webmaps)
        for map in webmap_obj:
            try:
                web_map_item = gis.content.get(map['itemId'])
                web_map = WebMap(web_map_item)
                # print(web_map)
                for operation_layer in web_map.layers:
                    try:
                        if operation_layer.layerType == 'GroupLayer':
                            update_popup_Layer(operation_layer,map,token,web_map)
                            continue
                        layer_obj = map['layers'][operation_layer.url]
                        try:
                            oprn_lyr_fields = {}
                            layerObjRest = requests.get('{0}?token={1}&f=pjson'.format(operation_layer.url, token))
                            if layerObjRest.status_code == 200:
                                # layer_fields = [obj['name'] for obj in layerObjRest.json()['fields']]
                                for fields_obj in layerObjRest.json()['fields']:
                                    oprn_lyr_fields[fields_obj['alias']] = fields_obj['name']
                                fileds_info = []
                                for l_fields in layer_obj['fields']:
                                    try:
                                        fileds_info.append({
                                            "fieldName": oprn_lyr_fields[l_fields['aliyas']],
                                            "label": l_fields['aliyas'],
                                            "visible": True
                                        })
                                    except Exception as err:
                                        logger.info('aliyas not exist in the operation layer {0}'.format(l_fields['aliyas']))
                                        continue
                                popup_info = {
                                    "title": layer_obj['popupTitle'],
                                    "fieldInfos": fileds_info,
                                    "description": operation_layer.popupInfo["description"],
                                    "expressionInfos": operation_layer.popupInfo["expressionInfos"]
                                }
                                operation_layer.popupInfo = popup_info
                                web_map.update()
                        except Exception as err1:
                            continue
                        print(layer_obj)
                    except Exception as err:
                        continue
                logger.info('web map popup info updated successfully.. Item Id id {}'.format(map['itemId']))
            except Exception as err3:
                logger.error('error occurd while updating popup info {}'.format(err3))
                continue
    except Exception as err_m:
        logger.error(err_m)


update_webmaps_layer_popups()