#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyCharm : 
Copyright (C) 2016-2017 EINDEX Li

@Author        : EINDEX Li
@File          : auto_pomotodo.py
@Created       : 2017/3/31
@Last Modified : 2017/3/31
"""
from flask import Flask, request, json
from requests import Session
import os

app = Flask(__name__)

pomotodo_key = os.getenv('POMOTODO_KEY')

session = Session()
session.headers.update({'Authorization': f'token {pomotodo_key}'})


@app.route('/')
def index():
    return 'auto pomotodo'


@app.route('/webhooks', methods=['POST'])
def webhooks():
    operation = request.json['operation']
    todo_id = request.json['after']['id']
    title = request.json['after']['title']
    params = {
        'description': f'{title} ${todo_id}$',
        'pin': request.json['after']['starred'],
        'completed': request.json['after']['completed'],
    }
    if operation == 'create':
        session.post('https://api.pomotodo.com/1/todos', params)
    elif operation == 'update':
        todos = json.loads(session.get('https://api.pomotodo.com/1/todos').content.decode())
        for todo in [todo for todo in todos if f'{todo_id}' in todo['description']]:
            r = session.patch(f'https://api.pomotodo.com/1/todos/{todo["uuid"]}', params)
    elif operation == 'delete':
        from pprint import pprint
        todos = json.loads(session.get('https://api.pomotodo.com/1/todos').content.decode())
        for todo in [todo for todo in todos if f'${todo_id}$' in todo['description']]:
            r = session.delete(f'https://api.pomotodo.com/1/todos/{todo["uuid"]}')
            pprint(r.text)
    return 'ok'


if __name__ == '__main__':
    app.run(port=8000, debug=True)
