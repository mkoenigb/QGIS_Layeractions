from qgis.core import QgsMessageLog
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import QUrl
from qgis.PyQt.QtNetwork import  QNetworkAccessManager, QNetworkRequest
import json

# Based on: https://gis-ops.com/qgis-actions-tutorial-reverse-geocoding-points-with-the-here-maps-api/

def do_request(manager, lat, lng):

    url = 'https://nominatim.openstreetmap.org/reverse?format=json&zoom=18&addressdetails=1&lat={}&lon={}'.format(lat, lng)
    QgsMessageLog.logMessage(f'Making a request to {url}')
    req = QNetworkRequest(QUrl(url))
    manager.get(req)

def handle_response(resp):

    QgsMessageLog.logMessage(f'Err ? {resp.error()}. Response message : {resp}')

    response_data = json.loads(bytes(resp.readAll()))
    QgsMessageLog.logMessage(f'Response {response_data}')
    
    try:
        road = response_data["address"]["road"]
    except:
        road = ''
    try:
        house_number = response_data["address"]["house_number"]
    except:
        house_number = ''
    try:
        plz = response_data["address"]["postcode"]
    except:
        plz = ''
    try:
        city = response_data["address"]["city"]
    except:
        city = ''
    try:
        suburb = response_data["address"]["suburb"]
    except:
        suburb = ''
    try:
        quarter = response_data["address"]["quarter"]
    except:
        quarter = ''
    try:
        neighbourhood = response_data["address"]["neighbourhood"]
    except:
        neighbourhood = ''
    try:
        state = response_data["address"]["state"]
    except:
        state = ''
    try:
        country = response_data["address"]["country"]
    except:
        country = ''
        
    if quarter != '' or neighbourhood != '': 
        sep1 = ' (' 
        sep3 = ')'
    else: 
        sep1 = ''
        sep3 = ''
    if quarter != '' and neighbourhood != '': 
        sep2 = ' / ' 
    else: 
        sep2 = ''
    if country != '': 
        sep4 = ', ' 
    else: 
        sep4 = ''

    address = (road + ' ' + house_number + '\n' +
        plz + ' ' + city + ' ' + suburb + sep1 + quarter + sep2 + neighbourhood + sep3 + '\n' +
        state + sep4 + country)

    QtWidgets.QMessageBox.information(None, "Success", "Location has been reverse geocoded: \n {}".format(address))

layer = qgis.utils.iface.activeLayer()
fid = [%$id%]

QgsMessageLog.logMessage("Selected layer ID is {}".format(str(layer)))
QgsMessageLog.logMessage("Selected feature ID is {}".format(str(fid)))

sourcecrs = qgis.core.QgsCoordinateReferenceSystem(layer.crs().authid())
destcrs = qgis.core.QgsCoordinateReferenceSystem("EPSG:4326")
crs_transfrom = qgis.core.QgsCoordinateTransform(sourcecrs, destcrs, QgsProject.instance())

feature = layer.getFeature(fid)
geom = feature.geometry()
geom.transform(crs_transfrom)
point = geom.asPoint()
lat = point.y()
lng = point.x()

QgsMessageLog.logMessage("Selected coordinates are {}, {}".format(lat, lng))

manager = QNetworkAccessManager()
manager.finished.connect(handle_response)

do_request(manager, lat, lng)