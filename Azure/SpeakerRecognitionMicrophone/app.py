from flask import Flask, json, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
import time, boto3, requests, json, urllib.request, os
# Does not work on EC2
# from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
import random

app = Flask('__name__')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/azure')
def azure():
    return render_template('index.html')

@app.route('/demo.html')
def demo():
    return render_template('demo.html')

@app.route('/recorder.js')
def recorder():
    return render_template('recorder.js')

@app.route('/transcribe_azure.html', endpoint = "transcribe_azure.html")
def transcribe_azure():
    return render_template('transcribe_azure.html')

if __name__ == '__main__':
    app.run(debug=True)
