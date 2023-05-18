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
    return {"user1": user1,
            "user2": user2}

def test_auth_login_invalid_email():
    requests.delete(config.url + '/clear/v1')
    response = requests.post(config.url + 'auth/login/v2', json = {'email': 'abc@outlook.com', 'password': '123456'})
    assert response.status_code == 400

def test_auth_login_incorrect_email(user):
    response = requests.post(config.url + 'auth/login/v2', json = {'email': 'abcde@outlook.com', 'password': '123456'})
    assert response.status_code == 400

def test_auth_login_incorrect_password(user):
    response = requests.post(config.url + 'auth/login/v2', json = {'email': 'abc@outlook.com', 'password': '1234567'})
    assert response.status_code == 400

def test_auth_login_is_work_1(user):
    response = requests.post(config.url + 'auth/login/v2', json = {'email': 'abc@outlook.com', 'password': '123456'})
    assert response.status_code == OK_STATUS

def test_auth_login_is_work_2(user):
    requests.post(config.url + 'auth/login/v2', json = {'email': 'abc@outlook.com', 'password': '123456'})
    response = requests.post(config.url + 'auth/login/v2', json = {'email': 'abcd@outlook.com', 'password': '123456'})
    assert response.status_code == OK_STATUS