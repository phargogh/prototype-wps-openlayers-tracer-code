import owslib.wps
import pygeoprocessing
import requests
import shapely.geometry
from osgeo import gdal
from osgeo import osr

SERVER = '127.0.0.1'
PORT = '5000'
URL = f'http://{SERVER}:{PORT}/wps'

_SRS = osr.SpatialReference()
_SRS.ImportFromEPSG(4326)  # WGS84
SRS_WKT = _SRS.ExportToWkt()


def get_info():
    response = requests.get(
        URL,
        params={
            'service': 'WPS',
            'request': 'getCapabilities',
        }
    )
    print(response.text)

    response = requests.get(
        URL, params={'service': 'WPS',
                     'request': 'DescribeProcess',
                     'identifier': 'ALL'})
    print(response.text)


def call_service_vector(point):
    """Example of how to call this service with a vector."""
    # write the point to a vector
    local_vector_path = 'target_vector.geojson'
    pygeoprocessing.shapely_geometry_to_vector(
        [shapely.geometry.Point(point)], local_vector_path, SRS_WKT, 'GeoJSON')

    # read the text
    with open(local_vector_path) as local_vector:
        vector_text = local_vector.read()

    # print the text
    print('VECTOR', vector_text)

    # print the buffered text in response.
    # This is a useful reference example of why POST is more useful for complex
    # inputs: https://docs.geoserver.org/stable/en/user/services/wps/operations.html#execute
    wps = owslib.wps.WebProcessingService(URL, verbose=False, skip_caps=True)
    response = wps.execute(
        identifier='buffer_vector',
        inputs=[
            ("point_geojson", str(vector_text)),
            ("buffer_dist", "10")  # literal inputs are provided as just a string value.
        ],
        output="OUTPUT",
        mode=owslib.wps.SYNC,
    )
    for output in response.processOutputs:
        # output.data has a string with the GeoJSON we're returning from WPS
        # output.retrieveData() presumably downloads the data for us if it's
        # stored remotely
        print(output.data)


def call_service_wkt(point):
    """Example of how to call this service with WKT."""
    point = shapely.geometry.Point(point)
    wps = owslib.wps.WebProcessingService(URL, verbose=False, skip_caps=True)
    response = wps.execute(
        identifier='buffer_wkt',
        inputs=[
            ('geometry_wkt', str(point.wkt)),
            ('buffer_dist', "10"),
        ],
        output='OUTPUT',
        mode=owslib.wps.SYNC,
    )
    for output in response.processOutputs:
        print(output.data)


if __name__ == '__main__':
    get_info()
    call_service_vector((90, -90))
    call_service_wkt((50, -50))
