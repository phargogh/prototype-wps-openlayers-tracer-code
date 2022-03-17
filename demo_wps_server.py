import buffer
import flask
import shapely.wkt
from flask import request
from flask_cors import CORS
from flask_cors import cross_origin
from pywps import Service

APP = flask.Flask(__name__)

# disable CORS errors.  FIXME
cors = CORS(APP)
APP.config['CORS_HEADERS'] = 'Content-Type'


PROCESSES = [
    buffer.BufferVector(),
    buffer.BufferWKT(),
]

SERVICE = Service(PROCESSES, ['pywps.cfg'])


@APP.route("/")
@cross_origin()
def helloWorld():
    return "Hello, cross-origin-world!"


@APP.route('/wps', methods=['GET', 'POST'])
def wps():
    return SERVICE


@APP.route('/json', methods=['GET'])
def json():
    """Keep it simple: buffer a geometry."""
    # Data might be passed in the data body as JSON or might be passed as
    # URL args.
    if request.json is not None:
        args = request.json
    else:
        args = request.args

    geom = shapely.wkt.loads(args['geometry_wkt'])
    buffered_geom = geom.buffer(float(args['buffer_dist']))

    return {'geometry_wkt': buffered_geom.wkt}


if __name__ == '__main__':
    APP.run(threaded=True, host='127.0.0.1')
