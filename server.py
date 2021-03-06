import time
from flask import Flask, request, Response
from _datetime import datetime

app = Flask(__name__)

messages = [
    # {'name': 'Mary', 'time': time.time(), 'text': 'Hello ! '},
    # {'name': 'Jhon', 'time': time.time(), 'text': 'Hello , Mary! '}
]


@app.route("/send", methods=['POST'])
def send():
    name = request.json['name']
    text = request.json['text']
    if not (name and isinstance(name, str) and text and isinstance(text, str)):
        return Response(status=400)
    message = {'name': name, 'time': time.time(), 'text': text}
    messages.append(message)
    return Response(status=200)


def filter_by_key(elements, key, threshold):
    filtered_elements = []

    for element in elements:
        if element[key] > threshold:
            filtered_elements.append(element)

    return filtered_elements


@app.route("/messages")
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        return Response(status=400)
    return {
        'messages': filter_by_key(messages, key='time', threshold=after)
    }


@app.route("/")
def hello():
    return "Hello, World! <a href='/status'> Status </a>"


@app.route("/status")
def status():
    return {
        'status': True,
        'name': 'Easy messenger',
        'time': datetime.now(),
        'online': len(set(c['name'] for c in messages))
    }


app.run(debug=True)
