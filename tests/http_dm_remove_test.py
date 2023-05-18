import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200

# test dm remove token incorrect
def test_dm_remove_token_incorrect():
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
    remove_1 =  requests.delete(config.url + 'dm/remove/v1', json = {
        'token': "",
        "dm_id": dm["dm_id"]
        })
    assert remove_1.status_code == 403

# test dm id incorrect
def test_dm_remove_dmid_incorrect():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    remove_1 =  requests.delete(config.url + 'dm/remove/v1', json = {
        'token': user1["token"],
        "dm_id": 1
        })
    assert remove_1.status_code == 400

# test not creator remove
def test_dm_remove_not_creator():
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
    dm = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [2]
    }).json()
    remove_1 =  requests.delete(config.url + 'dm/remove/v1', json = {
        'token': user2["token"],
        "dm_id": dm["dm_id"]
        })
    assert remove_1.status_code == 403

# test id not in dm
def test_dm_remove_auid_no_longer_in_dm():
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
    dm = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    }).json()
    remove_1 =  requests.delete(config.url + 'dm/remove/v1', json = {
        'token': user2["token"],
        "dm_id": dm["dm_id"]
        })
    assert remove_1.status_code == 403

# test all correct
def test_dm_remove_correct():
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
    dm1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [user2["auth_user_id"]]
    }).json()
    dm2 = requests.post(config.url + "dm/create/v1", json = {
        "token": user2["token"],
        "u_ids": [user1["auth_user_id"]]
    }).json()
    remove_1 = requests.delete(config.url + 'dm/remove/v1', json = {
        'token': user2["token"],
        "dm_id": dm2["dm_id"]
        })
    remove_2 = requests.delete(config.url + 'dm/remove/v1', json = {
        'token': user1["token"],
        "dm_id": dm1["dm_id"]
        })
    assert remove_1.status_code == OK_STATUS
    assert remove_2.status_code == OK_STATUS




