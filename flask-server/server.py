from flask import Flask, request
from flask_cors import CORS
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/verification', methods=['POST'])
def process_sentence(): # takes in a sentence, and outputs if it's accurate
    # return [{'mary':'name'}, {'tom':'name'}] return an array of json items
    return request.data

if __name__ == '__main__':
    app.debug = True
    app.run()