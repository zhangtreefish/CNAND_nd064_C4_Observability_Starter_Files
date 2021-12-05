from flask import Flask, render_template, request, jsonify

import pymongo
from flask_pymongo import PyMongo

from jaeger_client import Config
from flask_opentracing import FlaskTracing
from prometheus_flask_exporter import PrometheusMetrics
from opentracing.ext import tags as ext_tags

import requests
import time
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)  # Set CORS for development
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MONGO_DBNAME'] = 'example-mongodb'
app.config['MONGO_URI'] = 'mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb'
mongo = PyMongo(app)

metrics = PrometheusMetrics(app, group_by='endpoint')
metrics.info("backend_app_info", "Backend App Info", version="1.0.3")

config = Config(
    config={
        'sampler':
        {'type': 'const',
         'param': 1},
        'logging': True,
        'reporter_batch_size': 1,
        },
        service_name="backend")
jaeger_tracer = config.initialize_tracer()
# Trace All Requests:
tracing = FlaskTracing(jaeger_tracer, True, app)

@app.route('/')
@cross_origin()
def homepage():
    with jaeger_tracer.start_span('TestSpan') as span:
        span.log_kv({'event': 'welcome to the backend!', 'life': 42})
        with jaeger_tracer.start_span('ChildSpan', child_of=span) as child_span:
            child_span.log_kv({'event': 'Welcome again!! in case you missed the first time.'})
    return "Hello World"

@app.route('/api')
@cross_origin()
def my_api():
    parent_span = tracing.get_span("api-span")
    with jaeger_tracer.start_span('TestSpan', child_of=parent_span) as span:
        span.set_tag("url: ", '/api"')
    answer = "something"
    return jsonify(repsonse=answer)

# should return 500:
@app.route('/pythonjobs')
def python_jobs():
    gh_jobs = 'https://jobs.github.com/positions.json?description=python'
    parent_span = tracing.get_span("python jobs")
    #return render_template("main.html")
    with jaeger_tracer.start_span('get-python-jobs', child_of=parent_span) as span:
        span.set_tag("http.url", gh_jobs)
        res = requests.get(gh_jobs)
        span.set_tag("http.status_code", res.status_code)  # 404


@app.route('/star', methods=['POST'])
@cross_origin()
def add_star():
    with jaeger_tracer.start_span('star') as span:
        star = mongo.db.stars
        name = request.json['name']
        distance = request.json['distance']
        star_id = star.insert({'name': name, 'distance': distance})
        new_star = star.find_one({'_id': star_id })
        output = {'name': new_star['name'], 'distance': new_star['distance']}
        span.set_tag('star', new_star['name'])

        return jsonify({'result': output})

if __name__ == "__main__":
    app.run()
