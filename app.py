import json
import os
import requests
from sys import stderr
from flask import Flask, request, jsonify

app = Flask(__name__)

api_key = os.environ.get("API_KEY", "")
if api_key == "":
    print("api key is required", file=stderr)

api_base_url = "https://api.stagingv3.microgen.id/query/api/v1/" + api_key

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask</h2>'

@app.get("/products")
def getProducts():
    try:
        url = "/".join([api_base_url, "products"])
        response = requests.get(url)
        respBody = response.json()

        if response.status_code != 200:
            if respBody.get('message') == 'project not found':
                respJson = jsonify(
                    {"message": "failed to connect to your project, please check if the api had been set properly."}, 
                )
                respJson.status_code = response.status_code

                return respJson

            respJson = jsonify(respBody)
            respJson.status_code = response.status_code

            return respJson

        return jsonify(respBody)
    except Exception as e:
        return jsonify({"message": "error occured: " + e.__str__()})

@app.post("/products")
def createProduct():
    try:
        url = "/".join([api_base_url, "products"])
        response = requests.post(url, json.dumps(request.json, indent=2))
        respBody = response.json()

        if response.status_code != 201:
            if respBody.get('message') == 'project not found':
                respJson = jsonify(
                    {"message": "failed to connect to your project, please check if the api had been set properly."}, 
                )
                respJson.status_code = response.status_code

                return respJson

            respJson = jsonify(respBody)
            respJson.status_code = response.status_code

            return respJson
        
        return jsonify(respBody)
    except Exception as e:
        return jsonify({"message": "error occured: " + e.__str__()})

@app.get("/products/<id>")
def getProductById(id):
    try:
        url = "/".join([api_base_url, "products", id])
        response = requests.get(url)
        respBody = response.json()

        if response.status_code != 200:
            if respBody.get('message') == 'project not found':
                respJson = jsonify(
                    {"message": "failed to connect to your project, please check if the api had been set properly."}, 
                )
                respJson.status_code = response.status_code

                return respJson

            respJson = jsonify(respBody)
            respJson.status_code = response.status_code

            return respJson

        return jsonify(respBody)
    except Exception as e:
        return jsonify({"message": "error occured: " + e.__str__()})

@app.patch("/products/<id>")
def updateProduct(id):
    try:
        url = "/".join([api_base_url, "products", id])
        response = requests.patch(url, json.dumps(request.json, indent=2))
        respBody = response.json()

        if response.status_code != 200:
            if respBody.get('message') == 'project not found':
                respJson = jsonify(
                    {"message": "failed to connect to your project, please check if the api had been set properly."}, 
                )
                respJson.status_code = response.status_code

                return respJson

            respJson = jsonify(respBody)
            respJson.status_code = response.status_code

            return respJson
        
        return jsonify(respBody)
    except Exception as e:
        return jsonify({"message": "error occured: " + e.__str__()})

@app.delete("/products/<id>")
def deleteProduct(id):
    try:
        url = "/".join([api_base_url, "products", id])
        response = requests.delete(url)
        respBody = response.json()

        if response.status_code != 200:
            if respBody.get('message') == 'project not found':
                respJson = jsonify(
                    {"message": "failed to connect to your project, please check if the api had been set properly."}, 
                )
                respJson.status_code = response.status_code

                return respJson

            respJson = jsonify(respBody)
            respJson.status_code = response.status_code

            return respJson

        return jsonify(respBody)
    except Exception as e:
        return jsonify({"message": "error occured: " + e.__str__()})

if __name__ == "__main__":
    app.run(debug=True)