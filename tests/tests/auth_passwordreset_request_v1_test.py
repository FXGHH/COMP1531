import pytest
from src.auth import auth_login_v2, auth_register_v2, auth_logout_v1, auth_passwordreset_request_v1, auth_passwordreset_reset_v1
from src.error import AccessError, InputError
from src.other import clear_v1
from src.data_store import data_store
import src.help as help
# all correct
def test_reset_password_code():
    clear_v1()
    store = data_store.get()
    user_register = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    res1 = auth_passwordreset_request_v1('abc@outlook.com')
    reset_code = ""
    for user in store["users"]:
        if user["auth_user_id"] == user_register["auth_user_id"]:
            reset_code = user["reset_code"]
    res2 = auth_passwordreset_reset_v1(reset_code, "asdzxcs")

    assert res1 == {}
    assert res2 == {}

# incorrect reset code
def test_reset_password_incorrect_code():
    clear_v1()
    auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_passwordreset_request_v1('abc@outlook.com')
    reset_code = "asdasd"
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(reset_code, "asdzxcs")

# password less than 6
def test_reset_password_incorrect_password():
    clear_v1()
    store = data_store.get()
    user_register = auth_register_v2('abc@outlook.com', '1234567', 'Jake', 'Renzella')
    auth_passwordreset_request_v1('abc@outlook.com')
    reset_code = ""
    for user in store["users"]:
        if user["auth_user_id"] == user_register["auth_user_id"]:
            reset_code = user["reset_code"]
    with pytest.raises(InputError):
        auth_passwordreset_reset_v1(reset_code, "12345")
