# prototype-wps-openlayers-tracer-code

Objective: try out a simple WPS service, accessed via OpenLayers.

Setup:

    $ git submodule init
    $ git submodule update
    $ conda create -p ./env -c conda-forge python=3.9 pywps=4.5 flask requests shapely pygeoprocessing
    $ conda activate ./env

Starting the server, client:

    (env) $ python demo_wps_server.py
    (env) $ python demo_client.py

And also, open `index.html` in the browser to talk with the server.

Approach taken:

* Using [OGC WPS 2.0 standard](http://docs.opengeospatial.org/is/14-065/14-065.html)
* [PyWPS](https://pywps.readthedocs.io/en/latest/api.html) implements WPS backend as a Flask Microservice
* [OWSLib](https://geopython.github.io/OWSLib/) implements a WPS client for python
* [OpenLayers](https://openlayers.org/) used for rendering the basemap and
  vector geomtries.
* [jquery](https://api.jquery.com) used for communicating with the server.

Relevant files:
* `demo_wps_server.py` contains:
  * the JSON-only endpoint (akin to what we would write with a vanilla-flask
    solution)
  * Setup to avoid CORS errors
  * The defined WPS endpoint at `/wps`
* `demo_client.py` contains python examples of how to interact with the various
  endpoints.
* `buffer.py` contains the WPS implementation details for the WPS service.
* `index.html` contains a primitive webmap demonstrating interactivity with the
  server.

Lessons Learned:
* We have to be really careful about how the WPS object is constructed.
  Exceptions that take place in within `Process._handler` are not reported as
  exceptions in the server log, but probably should be.
* Most of the WPS functions (especially the ones with any reasonable complexity
  of their data inputs) are required to be XML documents submitted via HTTP
  `POST`.  We might find a decent javascript-based WPS client, but if that
  fails, we may have to fall back to writing an XML document ourselves in order
  to access WPS.
* For the simple case of buffering geometry, It is _far_ simpler and more
  direct to _just_ write a Flask endpoint and call it with JSON data and so
  offering a WPS interface is a lot of overhead for something so simple.

Future work:
* I struggled with the validation of inputs in the `Buffer` process, eventually
  disabling validation entirely because I couldn't get it to work and
  ultimately was not helpful for this demo.  When running a proper webservice,
  validation might matter then.
* Report exceptions within `Process._handler` to the server logs.

Conclusion:
* WPS is a lot of overhead just in defining parameters.  For getting something
  to work for the urban project, I think we might be better suited just writing
  a vanilla flask application and producing a conforming WPS interface later on
  if we need it.
* WPS requires defining outputs and their formats as well as inputs, so we
  would need to extend `ARGS_SPEC` for InVEST to include outputs if and when
  WPS becomes a useful interface for InVEST.
