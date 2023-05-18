import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
import time
OK_STATUS = 200
@pytest.fixture

def users():
    requests.delete(config.url + '/clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abcd@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    return {"user1": user1,
            "user2": user2}

def test_standup_send_v1_invalid_token(users):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': None, 'channel_id': channel['channel_id'], 'message': 'abc'})
    assert resp.status_code == 403

def test_standup_send_v1_invalid_token2(users):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': users['user2']['token'], 'channel_id': channel['channel_id'], 'message': 'abc'})
    assert resp.status_code == 403

def test_standup_send_invalid_channel_id(users):
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': users['user1']['token'], 'channel_id': None, 'message': 'abc'})
    assert resp.status_code == 400

def test_standup_send_no_standup_running(users):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': users['user1']['token'], 'channel_id': channel['channel_id'], 'message': 'abc'})
    assert resp.status_code == 400

def test_standup_send_message_larger_than_1000(users):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + 'standup/start/v1',
                        json={'token': users['user1']['token'], 'channel_id': channel['channel_id'], 'length': 1})
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': users['user1']['token'], 'channel_id': channel['channel_id'], 'message': 'a'*1001})
    assert resp.status_code == 400

def test_standup_send_is_work1(users):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    channel2 = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user2']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "channel/join/v2", json = {
        "token": users["user2"]["token"],
        "channel_id": channel1["channel_id"],
    })
    requests.post(config.url + 'standup/start/v1',
                        json={'token': users['user1']['token'], 'channel_id': channel1['channel_id'], 'length': 1})
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': users['user2']['token'], 'channel_id': channel1['channel_id'], 'message': 'abc'})
    assert resp.status_code == OK_STATUS

    requests.post(config.url + 'standup/start/v1',
                        json={'token': users['user2']['token'], 'channel_id': channel2['channel_id'], 'length': 1})
    resp = requests.post(config.url + 'standup/send/v1',
                        json={'token': users['user2']['token'], 'channel_id': channel2['channel_id'], 'message': 'abc'})
    assert resp.status_code == OK_STATUS

def test_standup_send_is_work2(users):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user2']['token'],
        'name': 'abc',
        'is_public': True
    })
    
    request = requests.post(config.url + "channel/join/v2", json = {
        "token": users["user2"]["token"],
        "channel_id": channel1["channel_id"],
    })
    assert request.status_code == 200 

    request = requests.post(config.url + "standup/start/v1", json = {
        "token": users["user1"]["token"],
        "channel_id": channel1["channel_id"],
        "length": 2
    })
    assert request.status_code == 200
    
    request = requests.get(config.url + "standup/active/v1", params= {
        "token": users["user1"]["token"],
        "channel_id": channel1["channel_id"],
    })
    assert request.status_code == 200
    
    request = requests.post(config.url + "standup/send/v1", json = {
        "token": users["user1"]["token"],
        "channel_id": channel1["channel_id"],
        "message": "hello"
    })
    assert request.status_code == 200

    time.sleep(4)
    
    request = requests.post(config.url + "standup/send/v1", json = {
        "token": users["user1"]["token"],
        "channel_id": channel1["channel_id"],
        "message": "hello"
    })
    assert request.status_code == 400
