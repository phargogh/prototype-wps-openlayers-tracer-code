import buffer
import flask
from pywps import Service

APP = flask.Flask(__name__)

PROCESSES = [
    buffer.Buffer(),
]

SERVICE = Service(PROCESSES, ['pywps.cfg'])


@APP.route('/wps', methods=['GET', 'POST'])
def wps():
    return SERVICE


if __name__ == '__main__':
    APP.run(threaded=True, host='127.0.0.1')
