import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort


def test_user_stats_v1_invalid_token():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json={
        "email": "abc@gmail.com",
        "password": "1234567",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    resp = requests.get(config.url + 'user/stats/v1', params={'token': "wrong"})
    assert resp.status_code == 403

def test_user_stats_v1_with_channel_join_leave():    
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
    resp = requests.get(config.url + 'user/stats/v1', params={'token':user['token']})
    user_stats = resp.json()['user_stats']

    assert len(user_stats['channels_joined']) == 2
    assert len(user_stats['dms_joined']) == 1
    assert len(user_stats['messages_sent']) == 1
    assert user_stats['channels_joined'][-1]['num_channels_joined'] == 1
    assert user_stats['involvement_rate'] == 1


def test_user_stats_v1_with_dm_create_leave():    
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + "dm/create/v1", json = {
        "token": user["token"],
        "u_ids": []
    })
    resp = requests.get(config.url + 'user/stats/v1', params={'token':user['token']})
    user_stats = resp.json()['user_stats']

    assert len(user_stats['channels_joined']) == 1
    assert len(user_stats['dms_joined']) == 2
    assert len(user_stats['messages_sent']) == 1
    assert user_stats['dms_joined'][-1]['num_dms_joined'] == 1
    assert user_stats['involvement_rate'] == 1


def test_user_stats_v1_with_message_update():    
    requests.delete(config.url + '/clear/v1')
    user = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc2@qq.com',
        'password': '1231232123123',
        'name_first': 'Ja2k1e',
        'name_last': 'Renzel1la'
    }).json()
    channel_1 = requests.post(config.url + '/channels/create/v2', json = {
        'token': user['token'],
        'name': 'abc',
        'is_public': True
    }).json()
    requests.post(config.url + "message/send/v1", json={
        "token": user["token"],
        "channel_id": channel_1["channel_id"],
        "message": "We are the best"
    })
    resp = requests.get(config.url + 'user/stats/v1', params={'token':user['token']})
    user_stats = resp.json()['user_stats']

    assert len(user_stats['channels_joined']) == 2
    assert len(user_stats['dms_joined']) == 1
    assert len(user_stats['messages_sent']) == 2
    assert user_stats['messages_sent'][-1]['num_messages_sent'] == 1
    assert user_stats['involvement_rate'] == 1