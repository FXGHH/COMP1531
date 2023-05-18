import pytest
from src.auth import auth_register_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.other import clear_v1
# test if name entered is valid
def test_channels_create_v2_invalid_token():
    clear_v1() 
    with pytest.raises(AccessError):
        channels_create_v2('a', 'abc', True)
def test_channels_create_v2_invalid_name_less():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        channels_create_v2(user1['token'], '', True)
def test_channels_create_v2_invalid_name_more1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        channels_create_v2(user1['token'], 'Thenameismorethantwenty', True)
# test channels create is work
def test_channels_create_v2_is_work_1():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    assert channels_create_v2(user1['token'], 'abc', True) == {"channel_id": 1}
def test_channels_create_v2_is_work_2():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    assert channels_create_v2(user1['token'], 'a', True) == {"channel_id": 1}
def test_channels_create_v2_is_work_3():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    assert channels_create_v2(user1['token'], '12345678901234567890', True) == {"channel_id": 1}
def test_channels_create_v2_is_work_4():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'],'abc', True)
    assert channels_create_v2(user1['token'],'def',True) == {"channel_id": 2}
def test_channels_create_v2_is_work_5():
    clear_v1()
    user1 = auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    channels_create_v2(user1['token'], 'abc', True)
    channels_create_v2(user1['token'], 'def', False)
    assert channels_create_v2(user1['token'], 'def', True) == {"channel_id": 3}
    assert channels_create_v2(user1['token'], 'abc', True) == {"channel_id": 4}



