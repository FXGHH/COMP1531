import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
@pytest.fixture
def user():
    requests.delete(config.url + 'clear/v1')
    user1 = requests.post(config.url + "auth/register/v2", json={
        "email": "abc@qq.com",
        "password": "123123123123",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    user2 = requests.post(config.url + "auth/register/v2", json={
        "email": "abcd@qq.com",
        "password": "123123123123",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    user3 = requests.post(config.url + "auth/register/v2", json={
        "email": "abcde@qq.com",
        "password": "123123123123",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    return {"user1": user1,
            "user2": user2,
            "user3": user3}

def test_channel_addowner_invalid_token_1():
    requests.delete(config.url + 'clear/v1')
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': 'abc',
        'channel_id': 1,
        'u_id': 1
    })
    assert resp.status_code == 403

def test_channel_addowner_invalid_token_2(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "channel/join/v2", json = {
        "token": user['user2']["token"],
        "channel_id": channel1["channel_id"]
    })
    requests.post(config.url + 'auth/logout/v1', json = {'token': user['user1']['token']})
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 403

def test_channel_addowner_incoreect_token_1(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "channel/join/v2", json = {
        "token": user['user2']["token"],
        "channel_id": channel1["channel_id"]
    })
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user2']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 403

def test_channel_addowner_incoreect_token_2(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "channel/join/v2", json = {
        "token": user['user2']["token"],
        "channel_id": channel1["channel_id"]
    })
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user2']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user3']['auth_user_id']
    })
    assert resp.status_code == 403

def test_channel_addowner_invalid_channel_id(user):
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': 1,
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 400

def test_channel_addowner_invalid_u_id(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': 4
    })
    assert resp.status_code == 400

def test_channel_addowner_incorrect_u_id(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 400

def test_channel_addowner_already_owner_1(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user1']['auth_user_id']
    })
    assert resp.status_code == 400

def test_channel_addowner_already_owner_2(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + 'channel/join/v2', json = {
        'token': user['user2']['token'],
        'channel_id': channel1['channel_id']
    })
    requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 400

def test_channel_addowner_public_channel(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user['user1']['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user['user2']['auth_user_id']
    })
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 200

def test_channel_addowner_private_channel(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': False
    }).json()
    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user['user1']['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user['user2']['auth_user_id']
    })
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user1']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 200

def test_channel_addowner_is_work(user):
    channel1 = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user2']['token'],
        'name': 'abc',
        'is_public': False
    }).json()
    requests.post(config.url + 'channel/invite/v2', json = {
        'token': user['user2']['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user['user1']['auth_user_id']
    })
    resp = requests.post(config.url + "channel/addowner/v1", json = {
        'token': user['user2']['token'],
        'channel_id': channel1["channel_id"],
        'u_id': user['user1']['auth_user_id']
    })
    assert resp.status_code == 200