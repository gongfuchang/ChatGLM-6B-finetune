from flask import Flask, Response, render_template, request
from flask_sse import sse
import time
from datetime import datetime

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')

@app.route('/chat_stream2', methods=["POST"])
def publish_hello():
    return Response(generate(), mimetype='text/event-stream')
def generate():
    for text in ['I', 'love', 'you']:
        # jsostr = "{\"id\":\"chatcmpl-743o2WK39oek7vfQNLg4bGnNTnxJ4\",\"object\":\"chat.completion.chunk\",\"created\":1681202298,\"model\":\"gpt-3.5-turbo-0301\",\"choices\":[{\"delta\":{\"content\":\"" + text + "\"},\"index\":0,\"finish_reason\":null}]}"
        sse.publish({"data": text}, type='event')
        time.sleep(1)
    sse.publish({"data": '[DONE]'}, type='event')


@app.route('/chat_stream', methods=["POST"])
def doyouhavethetime():
    return Response(generate2(), mimetype='text/plain')

def generate2():
    yield 'START'
    for i in range(1,5):
        yield "{}\n现在时间：".format(datetime.now().isoformat())
        time.sleep(1)
    yield 'DONE'

@app.route('/')
def test():
    return render_template("index2.html")

if __name__ == '__main__':
    app.run(debug=True)
