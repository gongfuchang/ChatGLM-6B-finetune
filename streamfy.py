from transformers import AutoTokenizer, AutoModel
from flask import Flask, Response, request
import time
from datetime import datetime
from hashlib import md5


__MAX_TURNS = 20

def __decode(body):
    params = body
    msg = params['messages'] or []
    input = list(filter(lambda elm: elm['role'] == 'user', msg)).pop()
    input = (input or [])['content']

    parts = list(map(lambda elm: elm['content'] or '', msg))
    history = []
    for i, n in enumerate(parts):
        if i % 2 == 0 and i + 1 < len(parts):
            history.append([parts[i], parts[i + 1]])
    if len(history) > __MAX_TURNS:
        history = history[-__MAX_TURNS:]
    return input, history, params.get('max_tokens'), params.get('temperature'), params.get('top_p'), params.get('stream')


def __queue(base, response):
    if base is None or response is None or len(response) < len(base):
        return response
    return response[len(base):]


def generate(json_body, model, tokenizer):
    (input, history, max_length, temperature, top_p, stream) = __decode(json_body)
    print('[chat-request-query:]' + input)
    if not stream:
        response, history = model.chat(tokenizer, input, history,
                                   max_length=max_length if max_length else 2048,
                                   top_p=top_p if top_p else 0.7,
                                   temperature=temperature if temperature else 0.95)
        print('[chat-response-topic:]' + response)
        yield response
    else:
        # for streaming chat
        base = None
        for response, history in model.stream_chat(tokenizer, input, history,
                                       max_length=max_length if max_length else 2048,
                                       top_p=top_p if top_p else 0.7,
                                       temperature=temperature if temperature else 0.95):
            text = __queue(base, response)
            base = response
            yield text


def generate2():
    while True:
        yield "{}\n".format(datetime.now().isoformat())
        time.sleep(1)
