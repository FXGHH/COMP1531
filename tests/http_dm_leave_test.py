import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
# test token incorrect
def test_dm_token_token_incorrect():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    dm = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    }).json()
    leave_1 =  requests.post(config.url + 'dm/leave/v1', json = {
        'token': "",
        "dm_id": dm["dm_id"]
    })
    assert leave_1.status_code == 403
# test dm id incorrect
def test_dm_dm_id_incorrect():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    leave_1 =  requests.post(config.url + 'dm/leave/v1', json = {
        'token': user1["token"],
        "dm_id": 1
    })
    assert leave_1.status_code == 400
# test auid not in dm
def test_auid_not_in_dm():
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
    leave_1 =  requests.post(config.url + 'dm/leave/v1', json = {
        'token': user2["token"],
        "dm_id": 1
    })
    assert leave_1.status_code == 403
# test dm leave correct
def test_dm_correct():
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
    user3 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abcde@outlook.com",
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
    requests.post(config.url + "dm/create/v1", json = {
        "token": user3["token"],
        "u_ids": [1,2]
    }).json()
    leave_1 =  requests.post(config.url + 'dm/leave/v1', json = {
        'token': user1["token"],
        "dm_id": 1
    })
    leave_2 =  requests.post(config.url + 'dm/leave/v1', json = {
        'token': user1["token"],
        "dm_id": 2
    })
    leave_3 =  requests.post(config.url + 'dm/leave/v1', json = {
        'token': user2["token"],
        "dm_id": 3
    })
    assert leave_1.status_code == OK_STATUS
    assert leave_2.status_code == OK_STATUS
    assert leave_3.status_code == OK_STATUS
