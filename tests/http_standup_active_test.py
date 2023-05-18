import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
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

def test_standup_active_v1_invalid_token(users):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.get(config.url + 'standup/active/v1',
                        params={'token': None, 'channel_id': channel['channel_id']})
    assert resp.status_code == 403

def test_standup_active_v1_invalid_token2(users):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user2']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.get(config.url + 'standup/active/v1',
                        params={'token': users['user1']['token'], 'channel_id': channel1['channel_id']})
    assert resp.status_code == 403

def test_standup_send_invalid_channel_id(users):
    resp = requests.get(config.url + 'standup/active/v1',
                        params={'token': users['user1']['token'], 'channel_id': 1})
    assert resp.status_code == 400

def test_standup_active_is_work(users):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    channel2 = requests.post(config.url + 'channels/create/v2', json = {
        'token': users['user2']['token'],
        'name': 'abcd',
        'is_public': True
    }).json()
    requests.post(config.url + "channel/join/v2", json = {
        "token": users["user2"]["token"],
        "channel_id": channel1["channel_id"],
    })
    requests.post(config.url + 'standup/start/v1',
                        json={'token': users['user2']['token'], 'channel_id': channel1['channel_id'], 'length': 1})
    resp = requests.get(config.url + 'standup/active/v1',
                        params={'token': users['user2']['token'], 'channel_id': channel1['channel_id']})
    assert resp.status_code == OK_STATUS

    requests.post(config.url + 'standup/start/v1',
                        json={'token': users['user2']['token'], 'channel_id': channel2['channel_id'], 'length': 1})
    resp = requests.get(config.url + 'standup/active/v1',
                        params={'token': users['user2']['token'], 'channel_id': channel2['channel_id']})
    assert resp.status_code == OK_STATUS