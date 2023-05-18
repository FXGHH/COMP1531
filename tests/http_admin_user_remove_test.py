import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
@pytest.fixture
def user():
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
    user3 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abcde@outlook.com',
        'password': '123456',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    return {"user1": user1,
            "user2": user2,
            "user3": user3}

def test_admin_user_remove_v1_invalid_token(user):
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {'token': None, 'u_id': user['user1']['auth_user_id']})
    assert resp.status_code == 403

def test_admin_user_remove_v1_invalid_token2(user):
    requests.delete(config.url + 'admin/user/remove/v1', json = {'token': user['user1']['token'], 'u_id': user['user2']['auth_user_id']})
    resp = requests.post(config.url + 'auth/logout/v1', json = {'token': user['user2']['token']})
    assert resp.status_code == 403

def test_admin_user_remove_v1_token_is_not_owner(user):
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {'token': user['user2']['token'], 'u_id': user['user1']['auth_user_id']})
    assert resp.status_code == 403

def test_admin_user_remove_v1_invalid_uid(user):
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {'token': user['user1']['token'], 'u_id': None})
    assert resp.status_code == 400

def test_admin_user_remove_v1_token_is_the_only_owner(user):
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {'token': user['user1']['token'], 'u_id': user['user1']['auth_user_id']})
    assert resp.status_code == 400

def test_admin_user_remove_v1_is_work(user):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user1']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "channel/join/v2", json = {
        "token": user['user2']["token"],
        "channel_id": channel["channel_id"]
    })
    requests.post(config.url + "message/send/v1", json = {
        "token": user['user2']["token"],
        "channel_id": channel["channel_id"],
        "message": "abc"
    })
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': user['user1']['token'],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 200

def test_admin_user_remove_v1_is_work_2(user):
    channel = requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user2']['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + 'channels/create/v2', json = {
        'token': user['user2']['token'],
        'name': 'abcd',
        'is_public': True
    })
    requests.post(config.url + "channel/join/v2", json = {
        "token": user['user1']["token"],
        "channel_id": channel["channel_id"]
    })
    requests.post(config.url + "channel/join/v2", json = {
        "token": user['user3']["token"],
        "channel_id": channel["channel_id"]
    })

    requests.post(config.url + "message/send/v1", json={
        "token": user['user2']["token"],
        "channel_id": channel["channel_id"],
        "message": "We are the best"
    })

    requests.post(config.url + "message/send/v1", json={
        "token": user['user2']["token"],
        "channel_id": channel["channel_id"],
        "message": "Second message"
    })

    requests.post(config.url + "message/send/v1", json={
        "token": user['user3']["token"],
        "channel_id": channel["channel_id"],
        "message": "Third message"
    })

    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': user['user1']['token'],
        'u_id': user['user3']['auth_user_id']
    })
    assert resp.status_code == 200
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': user['user1']['token'],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 200

def test_admin_user_remove_v1_is_work_3(user):
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user['user2']["token"],
        "u_ids": [1, 3]
    }).json()
    dm2 = requests.post(config.url + "dm/create/v1", json = {
        "token": user['user2']["token"],
        "u_ids": [1]
    }).json()

    requests.post(config.url + "message/senddm/v1", json={
        "token": user['user1']["token"],
        "dm_id": dm1["dm_id"],
        "message": "Hello World"
    }).json()

    requests.post(config.url + "message/senddm/v1", json={
        "token": user['user2']["token"],
        "dm_id": dm2["dm_id"],
        "message": "Hi there!!"
    }).json()

    requests.post(config.url + "message/senddm/v1", json={
        "token": user['user2']["token"],
        "dm_id": dm2["dm_id"],
        "message": "Good day!!"
    }).json()

    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': user['user1']['token'],
        'u_id': user['user3']['auth_user_id']
    })
    assert resp.status_code == 200
    resp = requests.delete(config.url + 'admin/user/remove/v1', json = {
        'token': user['user1']['token'],
        'u_id': user['user2']['auth_user_id']
    })
    assert resp.status_code == 200