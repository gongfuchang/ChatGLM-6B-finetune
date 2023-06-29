from transformers import AutoTokenizer, AutoModel
from flask import Flask, Response, request, render_template

from streamfy import generate, generate2
#
tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True, local_files_only = True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True, local_files_only = True).half().quantize(8).cuda()
model = model.eval()

app = Flask(__name__)


@app.route('/time')
def doyouhavethetime():
    return Response(generate2(), mimetype='text/plain')

@app.route('/')
def test():
    return render_template("index2.html")

@app.route('/chat_stream', methods=["POST"])
def generate_stream():
    # TODO 添加 stop
    # TODO 添加 session 控制
    # return 'po'
    answer = generate(request.json, model, tokenizer)
    return Response(answer, mimetype='text/event-stream')
    # return Response('texthehe', mimetype='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
