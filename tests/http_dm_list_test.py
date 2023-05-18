import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
# test all list correct
def test_dm_list_correct():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    }).json()
    requests.post(config.url + "dm/create/v1", json = {
        "token": user2["token"],
        "u_ids": [1]
    }).json()

    list_1 =  requests.get(config.url + '/dm/list/v1', params = {'token': user1['token']})
    list_2 =  requests.get(config.url + '/dm/list/v1', params = {'token': user2['token']})
    assert list_1.status_code == OK_STATUS
    assert list_2.status_code == OK_STATUS

# test token incorrect
def test_dm_list_token_incorrect():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    }).json()

    list_1 =  requests.get(config.url + '/dm/list/v1', params = {'token': ""})
    assert list_1.status_code == 403


