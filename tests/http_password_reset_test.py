import pytest
import requests
from src import config
from src.server import *
from flask import Flask, request, abort
OK_STATUS = 200
# test send reset email correct
def test_send_reset_email_correct():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        "email": "22t1.f133b.elephant@gmail.com",
        "password": "123456",
        "name_first": "Zuqi",
        "name_last": "Liu"
    })
    requests.post(config.url + "auth/register/v2", json = {
        "email": "22t1.f13b.elephant@gmail.com",
        "password": "123456",
        "name_first": "Zuqi",
        "name_last": "Liu"
    })
    res = requests.post(config.url + "auth/passwordreset/request/v1", json = {
        "email": "22t1.f13b.elephant@gmail.com"
    })
    assert res.status_code == OK_STATUS

# test reset password  length less than 6 
def test_reset_password_less_than_6():
    store = data_store.get()
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        "email": "22t1.f13b.elephant@gmail.com",
        "password": "123456",
        "name_first": "Zuqi",
        "name_last": "Liu"
    })
    reset_code = ""
    for dic in store["users"]:
        if dic["auth_user_id"] == 1:
            reset_code = dic["reset_code"]
    
    res = requests.post(config.url + "auth/passwordreset/reset/v1", json = {
        "reset_code" : reset_code,
        "new_password" : "12345"
    })
    assert res.status_code == 400

# test reset code not correct
def test_reset_password_reset_code_not_correct():
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        "email": "22t1.f13b.elephant@gmail.com",
        "password": "123456",
        "name_first": "Zuqi",
        "name_last": "Liu"
    })
    res = requests.post(config.url + "auth/passwordreset/reset/v1", json = {
        "reset_code" : "asdad",
        "new_password" : "12344242"
    })
    assert res.status_code == 400

# test reset passwor correct
def test_reset_password_correct():
    store = data_store.get()
    requests.delete(config.url + "/clear/v1")
    requests.post(config.url + "auth/register/v2", json = {
        "email": "22t1.f1sd3b.elephant@gmail.com",
        "password": "123456",
        "name_first": "Zuqi",
        "name_last": "Liu"
    })
    requests.post(config.url + "auth/register/v2", json = {
        "email": "22t1.f13b.elephant@gmail.com",
        "password": "123456",
        "name_first": "Zuqi",
        "name_last": "Liu"
    })
    requests.post(config.url + "auth/passwordreset/request/v1", json = {
        "email": "22t1.f13b.elephant@gmail.com"
    })
    reset_code = ""
    for dic in store["users"]:
        if dic["auth_user_id"] == 2:
            reset_code = dic["reset_code"]
    
    res = requests.post(config.url + "auth/passwordreset/reset/v1", json = {
        "reset_code" : reset_code,
        "new_password" : "12345123123"
    })
    assert res.status_code == OK_STATUS
