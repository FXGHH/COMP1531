import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.dm import dm_create_v1
from src.channels import channels_create_v2
from src.other import clear_v1
import src.help as help

# test token erroe
def test_dm_token_error():
    clear_v1()
    with pytest.raises(AccessError):
        dm_create_v1('', 1)

# test creator in uids
def test_dm_creater_in_uids():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        dm_create_v1(token_1['token'], [1])

# test uid repeat
def test_dm_uids_repeat():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    auth_register_v2(
        'abcd@qq.com', '123123123123', 'aa', 'aa')
    with pytest.raises(InputError):
        dm_create_v1(token_1['token'], [2, 2])

# test uid not vaild
def test_dm_uids_not_vaild():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    # auth_register_v2(
    #     'abcd@qq.com', '123123123123', 'aa', 'aa')
    with pytest.raises(InputError):
        dm_create_v1(token_1['token'], [2])

# test all correct
def test_dm_name_sort_and_id_correct():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'bb', 'bb')
    token_3 = auth_register_v2(
        'abcdee@qq.com', '123123123123', 'cc', 'cc')
    re1 = dm_create_v1(token_1['token'], [3, 2])
    re2 = dm_create_v1(token_2['token'], [1])
    re3 = dm_create_v1(token_3['token'], [2, 1])
    store = data_store.get()
    name_list = []
    for dmname in store['dm']:
        name_list.append(dmname["dm_name"])
    print(name_list)

    assert re1 == {'dm_id': 1}
    assert re2 == {'dm_id': 2}
    assert re3 == {'dm_id': 3}


    assert name_list == ['aaaa, bbbb, cccc', 'aaaa, bbbb', 'aaaa, bbbb, cccc']