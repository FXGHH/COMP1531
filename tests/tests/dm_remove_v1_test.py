import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_list_v1, dm_remove_v1
from src.other import clear_v1
import src.help as help

# test remove correct
def test_remove_correct():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'bb', 'bb')
    token_3 = auth_register_v2(
        'abcdee@qq.com', '123123123123', 'cc', 'cc')
    token_4 = auth_register_v2(
        'abcdeef@qq.com', '123123123123', 'dd', 'dd')
    token_5 = auth_register_v2(
        'abcdeefg@qq.com', '123123123123', 'ee', 'ee')

    dm_create_v1(token_1['token'], [])
    dm_create_v1(token_2['token'], [1])
    dm_create_v1(token_3['token'], [1,2])
    dm_create_v1(token_4['token'], [1, 2, 3])
    dm_create_v1(token_5['token'], [1, 2, 3, 4])


    dm_remove_v1(token_5['token'], 5)
    re_list1_remove = dm_list_v1(token_1['token'])
    re_list2_remove = dm_list_v1(token_2['token'])
    re_list3_remove = dm_list_v1(token_3['token'])
    re_list4_remove = dm_list_v1(token_4['token'])
    re_list5_remove = dm_list_v1(token_5['token'])

    assert re_list1_remove == {'dms': [{'dm_id': 1, 'name': 'aaaa'}, {'dm_id': 2, 'name': 'aaaa, bbbb'}, {'dm_id': 3, 'name': 'aaaa, bbbb, cccc'}, {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'}]}
    assert re_list2_remove == {'dms': [{'dm_id': 2, 'name': 'aaaa, bbbb'}, {'dm_id': 3, 'name': 'aaaa, bbbb, cccc'}, {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'}]}
    assert re_list3_remove == {'dms': [{'dm_id': 3, 'name': 'aaaa, bbbb, cccc'}, {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'}]}
    assert re_list4_remove == {'dms': [{'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'}]}
    assert re_list5_remove == {'dms': []}


# test token error
def test_token_error():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    dm_create_v1(token_1['token'], [])
    with pytest.raises(AccessError):
        dm_remove_v1(' ', 1)

# test dm id error
def test_dmid_error():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    with pytest.raises(InputError):
        dm_remove_v1(token_1['token'], 1)

# test not creactor
def test_is_not_creater_error():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'bb', 'bb')

    dm_create_v1(token_2['token'], [1])
    with pytest.raises(AccessError):
        dm_remove_v1(token_1['token'], 1)

# test au id not in dm
def test_auid_not_in_dm_error():
    clear_v1()
    token_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'aa', 'aa')
    token_2 = auth_register_v2(
        'abcd@qq.com', '123123123123', 'bb', 'bb')

    dm_create_v1(token_1['token'], [])
    with pytest.raises(AccessError):
        dm_remove_v1(token_2['token'], 1)