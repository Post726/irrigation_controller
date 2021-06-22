from flask import Flask, request, jsonify
import json
from irrigation import sql_helper

app = Flask(__name__)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/data", methods=["GET"])
def list_data():
    return jsonify({'water': sql_helper.Water().get_list()})


@app.route("/zones", methods=["GET"])
def list_zones():
    return jsonify(sql_helper.Zone().get_list())


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)