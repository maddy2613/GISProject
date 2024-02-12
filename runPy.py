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
                        try:
                            obj_layer = map['layers'][layer_obj.url]
                        except Exception as err6:
                            print('given layer is not matching with web map layer => {0}'.format(layer_obj['title']))
                            logger.info('given layer is not matching with web map layer => {0}'.format(layer_obj['title']))
                            continue
                        oprn_lyr_fields = {}
                        layerObjRest = requests.get('{0}?token={1}&f=pjson'.format(layer_obj.url, token))
                        if layerObjRest.status_code == 200:
                            for fields_obj in layerObjRest.json()['fields']:
                                oprn_lyr_fields[fields_obj['alias']] = fields_obj['name']
                            fileds_info = []
                            # print('Test Layer')
                            popupInfo = {}
                            try:
                                popupInfo = layer_obj["popupInfo"]
                            except Exception as err:
                                logger.info('popupinfo not existed to the layer')
                            for l_fields in obj_layer['fields']:
                                try:
                                    fileds_info.append({
                                        "fieldName": oprn_lyr_fields[l_fields['aliyas']],
                                        "label": l_fields['aliyas'],
                                        "visible": True
                                    })
                                except Exception as err:
                                    logger.info(
                                        'aliyas not exist in the operation layer {0}'.format(l_fields['aliyas']))
                                    print('aliyas not exist in the operation layer {0}'.format(l_fields['aliyas']))
                                    continue
                            popupInfo['title'] = layer_obj['title']
                            popupInfo['fieldInfos'] = fileds_info
                            layer_obj.popupInfo = popupInfo
                            web_map.update()
                            logger.info(
                                'web map popup info updated successfully.. Item Id id {}'.format(layer_obj['title']))
                            print('web map popup info updated successfully.. Item Id id {}'.format(layer_obj['title']))
                        else:
                            logger.info('unbale to query fild aliyas..')
                            print('unbale to query fild aliyas..')
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
        webmaps = configReader.read_webmap_layer_fields()
        token = gis._con.token
        # logger.info(webmaps)
        for map in webmaps:
            try:
                web_map_item = gis.content.get(map['itemId'])
                web_map = WebMap(web_map_item)
                # print(web_map)
                for operation_layer in web_map.layers:
                    try:
                        #print(operation_layer)
                        logger.info(operation_layer)
                        #continue
                        if operation_layer.layerType == 'GroupLayer':
                            update_popup_Layer(operation_layer,map,token,web_map)
                            continue
                        layer_obj = map['layers'][operation_layer.url]
                        try:
                            #print(layer_obj['popupTitle'])
                            oprn_lyr_fields = {}
                            layerObjRest = requests.get('{0}?token={1}&f=pjson'.format(operation_layer.url, token))
                            if layerObjRest.status_code == 200:
                                # layer_fields = [obj['name'] for obj in layerObjRest.json()['fields']]
                                for fields_obj in layerObjRest.json()['fields']:
                                    oprn_lyr_fields[fields_obj['alias']] = fields_obj['name']
                                fileds_info = []
                                popupInfo = operation_layer.popupInfo
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
                                popupInfo['title'] = operation_layer['title']
                                popupInfo['fieldInfos'] = fileds_info
                                operation_layer.popupInfo =popupInfo
                                web_map.update()
                                logger.info('web map popup info updated successfully.. Item Id id {}'.format(map['itemId']))
                                print('web map popup info updated successfully.. Item Id id {}'.format(map['itemId']))
                        except Exception as err1:
                            logger.error(err1)
                            continue
                        print(layer_obj)
                    except Exception as err:
                        logger.error('Error Occured While Reading Operation Layer {0}'.format(err))
                        continue
            except Exception as err3:
                logger.error('error occurd while updating popup info {}'.format(err3))
                continue
    except Exception as err_m:
        logger.error(err_m)


update_webmaps_layer_popups()
