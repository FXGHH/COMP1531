import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200

# test dm create with correct situation and empty u_ids
def test_dm_create_correct():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    dm_1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": []
    })
    assert dm_1.status_code == OK_STATUS

# test dm create with correct situation and have u_ids
def test_dm_create_correct_have_u_ids():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    requests.post(config.url + "auth/register/v2", json = {
        "email": "abce@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
        
    dm_1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [2, 3]
    })
    assert dm_1.status_code == OK_STATUS

# test dm create with incorrect token
def test_token_error():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
        
    dm_1 = requests.post(config.url + "dm/create/v1", json = {
        "token": " ",
        "u_ids": []
    })
    assert dm_1.status_code == 403
# test dm creator in u_ids
def test_creator_id_in_uids_error():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
        
    dm_1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [1]
    })
    assert dm_1.status_code == 400

# test u_id repeat
def test_dm_create_u_ids_repeat():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()
    requests.post(config.url + "auth/register/v2", json = {
        "email": "abcd@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    dm_1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [2, 2]
    })
    assert dm_1.status_code == 400
# test uid not valid
def test_dm_u_ids_not_valid():
    requests.delete(config.url + "/clear/v1")
    user1 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    }).json()

    dm_1 = requests.post(config.url + "dm/create/v1", json = {
        "token": user1["token"],
        "u_ids": [2]
    })
    assert dm_1.status_code == 400