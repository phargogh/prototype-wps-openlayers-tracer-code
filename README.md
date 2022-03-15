# prototype-wps-openlayers-tracer-code

Objective: try out a simple WPS service, accessed via OpenLayers.

Setup:

    $ git submodule init
    $ git submodule update
    $ conda create -p ./env -c conda-forge python=3.9 pywps=4.5 flask requests shapely pygeoprocessing
    $ conda activate ./env
    $ python demo_wps_server.py

Approach taken:

* Using [OGC WPS 2.0 standard](http://docs.opengeospatial.org/is/14-065/14-065.html)
* [PyWPS](https://pywps.readthedocs.io/en/latest/api.html) implements WPS backend as a Flask Microservice
* [OWSLib](https://geopython.github.io/OWSLib/) implements a WPS client for python

Lessons Learned:
* We have to be really careful about how the WPS object is constructed.
  Exceptions that take place in within `Process._handler` are not reported as
  exceptions in the server log, but probably should be.
*

Future work:
* I struggled with the validation of inputs in the `Buffer` process, eventually
  disabling validation entirely because I couldn't get it to work and
  ultimately was not helpful for this demo.  When running a proper webservice,
  validation might matter then.
* Report exceptions within `Process._handler` to the server logs.

Conclusion:
