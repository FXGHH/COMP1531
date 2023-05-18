import pytest

from src.auth import auth_login_v2, auth_register_v2
from src.channel import channel_invite_v2, channel_details_v2
from src.channels import channels_create_v2
from src.error import AccessError, InputError
from src.other import clear_v1
from src.help import searching_channel_with_channel_id
invalid_channel_id = 20
invalid_token = "This is a invalid token"


@pytest.fixture
def users():
    # this fixture register 3 people in
    # return their token and u_id
    clear_v1()
    user_1 = auth_register_v2(
        'z5222222@ad.unsw.edu.au', '522222', 'Hongyi', 'Ai')
    user_2 = auth_register_v2(
        'example@gmail.com', 'example', 'Hayden', 'Jacobs')
    user_3 = auth_register_v2('helloworld@python.com',
                              'unswcomp1531', 'Hello', 'World')
    return {
        "user1": {
            "token": user_1["token"],
            "u_id": user_1["auth_user_id"]},
        "user2": {
            "token": user_2["token"],
            "u_id": user_2["auth_user_id"]},
        "user3": {
            "token": user_3["token"],
            "u_id": user_3["auth_user_id"]},
    }


@pytest.fixture
def valid_channel_id(users):
    # this fixture create a new channel with first member in the dictonary
    # and then return the channel_id
    channel_1 = channels_create_v2(
        users["user1"]["token"], "channel1", True)
    channel_id = channel_1["channel_id"]
    return channel_id


def test_channel_details_v2_invalid_auth_user(valid_channel_id):
    # AccessError should be raised since the input token was wrong
    with pytest.raises(AccessError):
        channel_details_v2(invalid_token, valid_channel_id)


def test_channel_details_v2_invalid_channel_id(users):
    # InputError should be raised since the input channel_id was wrong
    with pytest.raises(InputError):
        channel_details_v2(users["user1"]["token"], invalid_channel_id)


def test_channel_details_v2_not_auth_user(users, valid_channel_id):
    # AceessError should be raised since the user with token is not in the channel
    with pytest.raises(AccessError):
        channel_details_v2(users["user2"]["token"], valid_channel_id)


def test_channel_details_v2_valid(users, valid_channel_id):
    # AceessError should be raised since the user with token is not in the channel
    assert channel_details_v2(users["user1"]["token"], valid_channel_id) == {'name': 'channel1', 'is_public': True,
                                                                             'owner_members': [{'u_id': 1, 'email': 'z5222222@ad.unsw.edu.au', 'name_first': 'Hongyi', 'name_last': 'Ai', 'handle_str': 'hongyiai'}],
                                                                             'all_members': [{'u_id': 1, 'email': 'z5222222@ad.unsw.edu.au', 'name_first': 'Hongyi', 'name_last': 'Ai', 'handle_str': 'hongyiai'}]}


def test_channel_details_v2_valid_two_users(users, valid_channel_id):
    channel_invite_v2(users["user1"]["token"],
                      valid_channel_id, users["user2"]["u_id"])
    channel = channel_details_v2(users["user1"]["token"], valid_channel_id)
    # testing that owner user is in the list 'owner_members'
    assert users["user1"]["u_id"] in [owner_user["u_id"]
                                      for owner_user in channel['owner_members']]
    # testing that owner user is also in the list 'all_members'
    assert users["user1"]["u_id"] in [member["u_id"]
                                      for member in channel['all_members']]
    # testing that member is in the list 'all_members'
    assert users["user2"]["u_id"] in [member["u_id"]
                                      for member in channel['all_members']]
