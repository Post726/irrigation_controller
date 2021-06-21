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


@app.route("/date", methods=["GET"])
def list_data():
    return jsonify({'temperatures': sql_helper.get_list('temperature')
                    , 'water': sql_helper.get_list('water')})


@app.route("/zones", methods=["GET"])
def update_item(item_id):
    return jsonify(ToDoService().update(item_id, request.get_json()))


if __name__ == "__main__":
    Schema()
    app.run(debug=True, host='0.0.0.0', port=8888)