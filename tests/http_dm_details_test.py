import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
# test token incorrect
def test_dm_details_token_incorrect():
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

    details_1 =  requests.get(config.url + '/dm/details/v1', params = {'token': "", 'dm_id': 1})
    assert details_1.status_code == 403
# test user not in dm
def test_dm_details_user_not_in_incorrect():
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

    details_1 =  requests.get(config.url + '/dm/details/v1', params = {'token': user2["token"], 'dm_id': 1})
    assert details_1.status_code == 403
# test no dm id
def test_dm_details_dmid_incorrect():
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

    details_1 =  requests.get(config.url + '/dm/details/v1', params = {'token': user1["token"], 'dm_id': 2})
    assert details_1.status_code == 400
# test all correct
def test_dm_details_correct():
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
        "u_ids": [1, 3]
    }).json()
    requests.post(config.url + "dm/create/v1", json = {
        "token": user3["token"],
        "u_ids": [1]
    }).json()

    details_1 =  requests.get(config.url + '/dm/details/v1', params = {'token': user1["token"], 'dm_id': 1})
    details_2 =  requests.get(config.url + '/dm/details/v1', params = {'token': user2["token"], 'dm_id': 2})
    details_3 =  requests.get(config.url + '/dm/details/v1', params = {'token': user3["token"], 'dm_id': 3})
    assert details_1.status_code == 200
    assert details_2.status_code == 200
    assert details_3.status_code == 200