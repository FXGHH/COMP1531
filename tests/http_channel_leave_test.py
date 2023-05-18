import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
@pytest.fixture
def user():
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + '/auth/register/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    })
    return user.json()

def test_channel_leave_invalid_channel_id(user):
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user['token'],
        'channel_id': 1
    })
    assert resp.status_code == 400

def test_channel_leave_invalid_token():
    requests.delete(config.url + "/clear/v1")
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': 'abc',
        'channel_id': 1
    })
    assert resp.status_code == 403

def test_channel_leave_incorrect_token(user):
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    requests.post(config.url + '/auth/logout/v1', json = {'token': user['token']})
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user['token'],
        'channel_id': 1
    })
    assert resp.status_code == 403

def test_channel_leave_incorrect_token2(user):
    user1 = requests.post(config.url + '/auth/register/v2', json = {
        'email': 'abcd@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user1['token'],
        'channel_id': 1
    })
    assert resp.status_code == 403

def test_channel_leave_is_work_1(user):
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user['token'],
        'channel_id': 1
    })
    assert resp.status_code == 200

def test_channel_leave_is_work_2(user):
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    })
    requests.post(config.url + "/channel/leave/v1", json = {
        'token': user['token'],
        'channel_id': 1
    })
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'def',
        'is_public': True
    })
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user['token'],
        'channel_id': 2
    })
    assert resp.status_code == 200

def test_channel_leave_is_work_3(user):
    user2 = requests.post(config.url + '/auth/register/v2', json = {
        'email': 'abcd@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    user3 = requests.post(config.url + '/auth/register/v2', json = {
        'email': 'abcde@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "/channel/join/v2", json = {
        "token": user2["token"],
        "channel_id": 1
    })
    requests.post(config.url + "/channel/join/v2", json = {
        "token": user3["token"],
        "channel_id": 1
    })
    resp = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user2['token'],
        'channel_id': 1
    })
    resp1 = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user3['token'],
        'channel_id': 1
    })
    resp2 = requests.post(config.url + "/channel/leave/v1", json = {
        'token': user['token'],
        'channel_id': 1
    })
    assert resp.status_code == 200
    assert resp1.status_code == 200
    assert resp2.status_code == 200