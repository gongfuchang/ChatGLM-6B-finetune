from flask import Flask, Response, request, render_template

from streamfy import generate, generate2
import time


app = Flask(__name__)


@app.route('/time')
def doyouhavethetime():
    return Response(generate2(), mimetype='text/plain')

@app.route('/')
def test():
    return render_template("index2.html")

@app.route('/chat_stream', methods=["POST"])
def generate_stream():
    return Response(generate(), mimetype='text/event-stream')
    # return Response('texthehe', mimetype='text/event-stream')

def generate():
    sentence = 'When I got canned, I took these keys as souvenirs'.split(' ')
    for text in sentence:
        time.sleep(1)
        yield text + ' '

if __name__ == "__main__":
    app.run(debug=True)
