from flask import Flask, render_template, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app, group_by='endpoint')
metrics.info("frontend_app_info", "Frontend App Info", version="1.0.3")

@app.route('/')
def homepage():
    return render_template("main.html")


if __name__ == "__main__":
    app.run()