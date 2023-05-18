import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
def test_channels_create_invalid_token():
    requests.delete(config.url + '/clear/v1')   
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': 'abc',
        'name': 'abc',
        'is_public': True
    })
    assert resp.status_code == 403

def test_channels_create_invalid_name1():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': '',
        'is_public': True
    })
    assert resp.status_code == 400

def test_channels_create_invalid_name2():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'Thenameismorethantwenty',
        'is_public': True
    })
    assert resp.status_code == 400

def test_channels_create_v2_is_work_1():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    assert resp.status_code == OK_STATUS

def test_channels_create_v2_is_work_2():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'def',
        'is_public': True
    })
    assert resp.status_code == OK_STATUS

def test_channels_create_v2_is_work_3():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'def',
        'is_public': False
    })
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'def',
        'is_public': True
    })
    resp = requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': False
    })
    assert resp.status_code == OK_STATUS