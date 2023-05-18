import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_details_v1
from src.channels import channels_create_v2
from src.other import clear_v1
import src.help as help

INVALID_TOKEN = "Thisisainvalidtoken"
INVALID_DM_ID = 50


@pytest.fixture
def users():
    clear_v1()
    user1 = auth_register_v2(
        'z5222222@ad.unsw.edu.au', '522222', 'Hongyi', 'Ai')
    user2 = auth_register_v2(
        'example@gmail.com', 'example', 'Hayden', 'Jacobs')
    user3 = auth_register_v2('helloworld@python.com',
                             'unswcomp1531', 'Hello', 'World')
    return {"user1": user1, "user2": user2, "user3": user3}



@pytest.fixture
def dm(users):
    # this fixture create a new dm
    # and then return the dm_id
    dm_1 = dm_create_v1(users["user1"]["token"],
                        [users["user2"]["auth_user_id"]])
    return dm_1

# test token invalid
def test_dm_details_with_invalid_token(dm):
    with pytest.raises(AccessError):
        dm_details_v1(INVALID_TOKEN, dm["dm_id"])

# test dm id invalid
def test_dm_details_with_invalid_dm_id(users):
    with pytest.raises(InputError):
        dm_details_v1(users["user1"]["token"], INVALID_DM_ID)

# test not auth user
def test_dm_details_with_not_auth_user(users, dm):
    with pytest.raises(AccessError):
        dm_details_v1(users["user3"]["token"], dm["dm_id"])

# test valid
def test_dm_details_valid(users, dm):
    r_dm = dm_details_v1(users["user1"]["token"], dm["dm_id"])
    assert r_dm["name"] == 'haydenjacobs, hongyiai'


