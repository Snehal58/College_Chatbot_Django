from django.apps import AppConfig

class ChatbotConfig(AppConfig):
    app = 'chatbot'


from email import message
import json
from flask import Flask, jsonify, render_template
from requests import request
from chat import get_response



@app.get("/")
def index_get():
    return render_template("index.html")

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)
    message= {"answer": response}
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)