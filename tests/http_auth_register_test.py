import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
# register with correct situation
def test_register():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    })
    assert user.status_code == OK_STATUS

# register with incorrect email
def test_register_invalid_email():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    })
    assert user.status_code == 400

# register with incorrect password
def test_register_invalid_password():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123",
        "name_first": "Jake",
        "name_last": "Renzella"
    })
    assert user.status_code == 400

# register with incorrect firsname   
def test_register_invalid_firsname():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake" * 50,
        "name_last": "Renzella"
    })
    assert user.status_code == 400

    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "",
        "name_last": "Renzella"
    })
    assert user2.status_code == 400

# register with incorrect last_name
def test_register_invalid_last_name():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella" * 50
    })
    assert user.status_code == 400

    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": ""
    })
    assert user2.status_code == 400

# register with repeat_email
def test_register_repeat_email():
    requests.delete(config.url + "/clear/v1")
    user = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    })
    user2 = requests.post(config.url + "auth/register/v2", json = {
        "email": "abc@outlook.com",
        "password": "123456",
        "name_first": "Jake",
        "name_last": "Renzella"
    })
    assert user.status_code == OK_STATUS
    assert user2.status_code == 400
