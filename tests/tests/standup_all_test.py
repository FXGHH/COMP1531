import pytest
from src.error import InputError, AccessError
from src.other import clear_v1
from src.auth import auth_register_v2
from src.standup import standup_start_v1, standup_active_v1, standup_send_v1
from src.channel import channel_join_v2, channel_messages_v2
from src.channels import channels_create_v2
import time


@pytest.fixture
def users():
    clear_v1()
    user1 = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    user2 = auth_register_v2('abcd@outlook.com', '1234567', 'Jake', 'Renzella')
    return {"user1": user1, "user2": user2}


@pytest.fixture
def channel_id(users):
    channel = channels_create_v2(users['user1']["token"], "abc", True)
    channel_id = channel["channel_id"]
    return channel_id


def test_standup_start_invalid_token(channel_id):
    with pytest.raises(AccessError):
        assert standup_start_v1(None, channel_id, 1)


def test_standup_start_invalid_token2(users, channel_id):
    with pytest.raises(AccessError):
        assert standup_start_v1(users["user2"]["token"], channel_id, 1)


def test_standup_start_invalid_channel_id(users):
    with pytest.raises(InputError):
        assert standup_start_v1(users["user1"]["token"], 1, 1)


def test_standup_start_standup_already_running(users, channel_id):
    standup_start_v1(users["user1"]["token"], channel_id, 1)
    with pytest.raises(InputError):
        assert standup_start_v1(users["user1"]["token"], channel_id, 1)


def test_standup_start_standup_negative_length(users, channel_id):
    with pytest.raises(InputError):
        assert standup_start_v1(users["user1"]["token"], channel_id, -1)


def test_standup_active_invalid_token(channel_id):
    with pytest.raises(AccessError):
        assert standup_active_v1(None, channel_id)


def test_standup_active_invalid_channel_id(users):
    with pytest.raises(InputError):
        assert standup_active_v1(users["user1"]["token"], 2)


def test_standup_send_invalid_token(channel_id):
    with pytest.raises(AccessError):
        assert standup_send_v1(None, channel_id, 'abc')


def test_standup_send_invalid_token2(users, channel_id):
    standup_start_v1(users["user1"]["token"], channel_id, 1)
    with pytest.raises(AccessError):
        assert standup_send_v1(users["user2"]["token"], channel_id, 'abc')


def test_standup_send_invalid_channel_id(users):
    with pytest.raises(InputError):
        assert standup_send_v1(users["user1"]["token"], 1, 'abc')


def test_standup_send_no_standup_running(users, channel_id):
    with pytest.raises(InputError):
        assert standup_send_v1(users["user1"]["token"], channel_id, 'abc')


def test_standup_send_no_standup_running2(users, channel_id):
    standup_start_v1(users["user1"]["token"], channel_id, 1)
    time.sleep(2)
    with pytest.raises(InputError):
        assert standup_send_v1(users["user1"]["token"], channel_id, 'abc')


def test_standup_send_message_larger_than_1000(users, channel_id):
    standup_start_v1(users["user1"]["token"], channel_id, 1)
    with pytest.raises(InputError):
        assert standup_send_v1(users["user1"]["token"], channel_id, 'a'*1001)


def test_standup_work(users, channel_id):
    time_finish = standup_start_v1(users["user1"]["token"], channel_id, 1)[
        'time_finish']
    assert standup_active_v1(users["user1"]["token"], channel_id) == {
        "is_active": True, "time_finish": time_finish}
    standup_send_v1(users["user1"]["token"], channel_id, 'abc')

    time.sleep(3)

    assert standup_active_v1(users["user1"]["token"], channel_id) == {
        "is_active": False, "time_finish": None}
    messages = channel_messages_v2(
        users["user1"]["token"], channel_id, 0)["messages"]
    assert messages[0]["message"] == "jakerenzella: abc"
