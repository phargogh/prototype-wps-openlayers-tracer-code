import shapely.wkb
import shapely.wkt
from osgeo import ogr
from pywps import ComplexInput
from pywps import ComplexOutput
from pywps import Format
from pywps import FORMATS
from pywps import LiteralInput
from pywps import Process
from pywps.validator.mode import MODE


class BufferVector(Process):
    def __init__(self):
        inputs = [
            ComplexInput(
                'point_geojson',
                'Input point geometry',
                supported_formats=[Format('application/vnd.geo+json')],
                #mode=MODE.STRICT),  # GDAL is used to validate the vector
                #mode=MODE.SIMPLE),
                mode=MODE.NONE),
            LiteralInput(
                'buffer_dist',
                'Buffer distance',
                data_type='float'),  # do we need the allowed values?
        ]
        outputs = [
            ComplexOutput(
                'buffered_point_geojson',
                'Buffered point geometry',
                supported_formats=[Format('application/vnd.geo+json')]),
        ]

        super(BufferVector, self).__init__(
            self._handler,
            identifier='buffer_vector',
            version='0.1',
            title='GDAL buffer a point vector',
            abstract='Buffer the input vector',
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        source_vector = ogr.Open(request.inputs['point_geojson'][0].file)
        source_layer = source_vector.GetLayer()
        target_layer_name = f'{source_layer.GetName()}_buffered'

        driver = ogr.GetDriverByName('GeoJSON')
        target_vector = driver.CreateDataSource(target_layer_name)
        target_layer = target_vector.CreateLayer(target_layer_name,  None,
                                                 ogr.wkbUnknown)
        buffer_dist = float(request.inputs['buffer_dist'][0].data)
        n_features = source_layer.GetFeatureCount()
        for feat_index, source_feature in enumerate(source_layer):
            geometry = source_feature.GetGeometryRef()
            buffered_geom = geometry.Buffer(buffer_dist)
            target_feature = ogr.Feature(target_layer.GetLayerDefn())
            target_feature.SetGeometry(buffered_geom)
            target_layer.CreateFeature(target_feature)
            response.update_status('Buffering', 100 * (feat_index /
                                                       n_features))

        target_feature = None
        target_layer = None
        target_vector = None

        response.outputs['buffered_point_geojson'].output_format = FORMATS.GEOJSON
        response.outputs['buffered_point_geojson'].file = target_layer_name

        return response


class BufferWKT(Process):
    def __init__(self):
        inputs = [
            ComplexInput(
                "geometry_wkt", "geometry well-known text",
                supported_formats=[Format('text/plain')]),
            LiteralInput(
                "buffer_dist", "buffer distance", data_type='float'),
        ]
        outputs = [
            ComplexOutput(
                "buffered_geometry_wkt", "buffered geometry well-known text",
                supported_formats=[Format('text/plain')])
        ]
        super(BufferWKT, self).__init__(
            self._handler,
            identifier='buffer_wkt',
            version='0.1',
            title='buffer geometry WKT',
            abstract='buffer the input WKT geometry',
            profile='',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        geom = shapely.wkt.loads(request.inputs['geometry_wkt'][0].data)
        buffered_geom = geom.buffer(request.inputs['buffer_dist'][0].data)
        response.outputs['buffered_geometry_wkt'].output_format = FORMATS.TEXT
        response.outputs['buffered_geometry_wkt'].data = buffered_geom.wkt

        return response
