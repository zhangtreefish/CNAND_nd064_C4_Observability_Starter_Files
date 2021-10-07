
import os
import time
import requests

from flask import Flask, jsonify

import logging
from redis_opentracing import Config
# from flask_opentracing import FlaskTracing, FlaskTracer

import redis
import redis_opentracing

app = Flask(__name__)

rdb = redis.Redis(host='redis-primary.default.svc.cluster.local', port=6379, db=0)


def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
        },
        service_name=service,
        validate=True,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


#starter code
tracer = init_tracer('test-service')
# tracer = FlaskTracer('test-service', True, app)

# not entirely sure but I believe there's a flask_opentracing.init_tracing() missing here
redis_opentracing.init_tracing(tracer, trace_all_classes=False)

with tracer.start_span('first-span') as span:
    span.set_tag('first-tag', '100')


@app.route('/')
def hello_world():
    return 'Hello World!'



@app.route('/alpha')
def alpha():
    for i in range(100):
        # do_heavy_work()  # removed the colon here since it caused a syntax error - not sure about its purpose?
        with tracer.start_span(str(i), child_of=span) as num_span:
            print('Getting number %d' % i)
            try:
                num_span.set_tag('get-number', str(i))
            except:
                print('Unable to get number for %d' % i)
                site_span.set_tag('get-number', 'Failure')
        if i % 100 == 99:
            time.sleep(10)
    return 'This is the Alpha Endpoint!'

 
@app.route('/beta')
def beta():
    r = requests.get("https://www.google.com/search?q=python")
    dict = {}
    for key, value in r.headers.items():
        with tracer.start_span(result['company'], child_of=span) as site_span:
            try:
                print(key, ":", value)
                dict.update({key: value})
                site_span.set_tag('respond-header', key)
            except:
                print('Unable to get header for %s' % header)
                site_span.set_tag('respond-header', 'Failure')
    return jsonify(dict)      



@app.route('/writeredis') # needed to rename this view to avoid function name collision with redis import
def writeredis():
    # start tracing the redis client
    redis_opentracing.trace_client(rdb)    
    r = requests.get("https://www.google.com/search?q=python")
    dict = {}
    # put the first 50 results into dict
    for key, value in r.headers.items()[:50]:
        with tracer.start_span(result['company'], child_of=span) as site_span:
            try:
                print(key, ":", value)
                dict.update({key: value})
                site_span.set_tag('respond-header', key)
            except:
                print('Unable to get header for %s' % header)
                site_span.set_tag('respond-header', 'Failure')
    rdb.mset(dict)    
    return jsonify(dict)      

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8090)))