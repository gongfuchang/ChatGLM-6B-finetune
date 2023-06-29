# -*- coding: utf-8 -*-
# @Time    : 2022/6/8 19:01
# @Author  : dzg
from flask import Flask, render_template
from flask_sse import sse
from flask_cors import CORS

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix="/stream")
CORS(app, resources={r"/stream/*": {"origins": "*"}})




@app.route('/test/<username>')
def test(username):
    sse.publish({"message": {"name": username, "age": "18"}}, type="sseTest")
    return render_template("index.html")


if __name__ == '__main__':
    app.run()