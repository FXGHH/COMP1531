import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
def test_channels_list_invalid_token():
    requests.delete(config.url + '/clear/v1')   
    resp = requests.get(config.url + '/channels/list/v2', params = {'token': 'abc'})
    assert resp.status_code == 403

def test_channels_list_v2_is_work_1():
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
    resp = requests.get(config.url + '/channels/list/v2', params = {'token': user['token']})
    assert resp.status_code == OK_STATUS

def test_channels_list_v2_is_work_2():
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
        'is_public': True
    })
    resp = requests.get(config.url + '/channels/list/v2', params = {'token': user['token']})
    assert resp.status_code == OK_STATUS

def test_channels_list_v2_is_work_3():
    requests.delete(config.url + '/clear/v1')
    user1 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    user2 = requests.post(config.url + 'auth/register/v2', json = {
        'email': 'abcd@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella'
    }).json()
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user1['token'],
        'name': 'abc',
        'is_public': True
    })
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user2['token'],
        'name': 'abc',
        'is_public': True
    })
    requests.post(config.url + '/channels/create/v2', json = {
        'token': user2['token'],
        'name': 'def',
        'is_public': True
    })
    resp = requests.get(config.url + '/channels/list/v2', params = {'token': user2['token']})
    assert resp.status_code == OK_STATUS

# def test_channels_list_v2_invite_1():
#     requests.delete(config.url + '/clear/v1')
#     user1 = requests.post(config.url + 'auth/register/v2', json = {
#         'email': 'sheriff.woody@andysroom.com',
#         'password': 'qazwsx!!',
#         'name_first': 'sheriff',
#         'name_last': 'woody'
#     }).json()
#     user2 = requests.post(config.url + 'auth/register/v2', json = {
#         'email': 'zerg.thedestroyer@zergworld.com',
#         'password': '!!qazwsx',
#         'name_first': 'lord',
#         'name_last': 'zerg'
#     }).json()
#     requests.post(config.url + '/channels/create/v2', json = {
#         'token': user1['token'],
#         'name': 'andy',
#         'is_public': True
#     })
#     requests.post(config.url + '/channel/invite/v2', json = {
#         'token': user1['token'],
#         'channel_id': 1,
#         'u_id': 2
#     })
#     resp = requests.get(config.url + '/channels/list/v2', params = {'token': user2['token']})
#     assert resp.status_code == 200

# def test_channels_list_v2_invite_2():
#     requests.delete(config.url + '/clear/v1')
#     user1 = requests.post(config.url + 'auth/register/v2', json = {
#         'email': 'sheriff.woody@andysroom.com',
#         'password': 'qazwsx!!',
#         'name_first': 'sheriff',
#         'name_last': 'woody'
#     }).json()
#     user2 = requests.post(config.url + 'auth/register/v2', json = {
#         'email': 'zerg.thedestroyer@zergworld.com',
#         'password': '!!qazwsx',
#         'name_first': 'lord',
#         'name_last': 'zerg'
#     }).json()
#     requests.post(config.url + '/channels/create/v2', json = {
#         'token': user1['token'],
#         'name': 'andy',
#         'is_public': False
#     })
#     requests.post(config.url + '/channel/invite/v2', json = {
#         'token': user1['token'],
#         'channel_id': 1,
#         'u_id': 2
#     })
#     resp = requests.get(config.url + '/channels/list/v2', params = {'token': user2['token']})
#     assert resp.status_code == 200