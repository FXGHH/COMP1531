import pytest
from src.data_store import data_store
from src.error import AccessError, InputError
from src.auth import auth_register_v2
from src.dm import dm_create_v1, dm_list_v1
from src.other import clear_v1
import src.help as help

# test list correct
def test_list_correct():
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
    token_6 = auth_register_v2(
        'abcdeefgg@qq.com', '123123123123', 'ff', 'ff')

    dm_create_v1(token_1['token'], [])
    dm_create_v1(token_2['token'], [1])
    dm_create_v1(token_3['token'], [1,2])
    dm_create_v1(token_4['token'], [1, 2, 3])
    dm_create_v1(token_5['token'], [1, 2, 3, 4])

    re_list1 = dm_list_v1(token_1['token'])
    re_list2 = dm_list_v1(token_2['token'])
    re_list3 = dm_list_v1(token_3['token'])
    re_list4 = dm_list_v1(token_4['token'])
    re_list5 = dm_list_v1(token_5['token'])
    re_list6 = dm_list_v1(token_6['token'])
    print(re_list1)
    print(re_list2)
    print(re_list3)
    print(re_list4)
    print(re_list5)
    print(re_list6)
    assert re_list1 == {
        'dms': [   
            {'dm_id': 1, 'name': 'aaaa'},
            {'dm_id': 2, 'name': 'aaaa, bbbb'},
            {'dm_id': 3, 'name': 'aaaa, bbbb, cccc'},
            {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'},
            {'dm_id': 5, 'name': 'aaaa, bbbb, cccc, dddd, eeee'}
            ]
        }

    assert re_list2 == {
        'dms': [
            {'dm_id': 2, 'name': 'aaaa, bbbb'},
            {'dm_id': 3, 'name': 'aaaa, bbbb, cccc'},
            {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'},
            {'dm_id': 5, 'name': 'aaaa, bbbb, cccc, dddd, eeee'}
            ]
        }

    assert re_list3 == {
        'dms': [
            {'dm_id': 3, 'name': 'aaaa, bbbb, cccc'},
            {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'},
            {'dm_id': 5, 'name': 'aaaa, bbbb, cccc, dddd, eeee'}
            ]
        }

    assert re_list4 == {
        'dms': [
            {'dm_id': 4, 'name': 'aaaa, bbbb, cccc, dddd'},
        {'dm_id': 5, 'name': 'aaaa, bbbb, cccc, dddd, eeee'}
        ]
    }

    assert re_list5 == {'dms': [{'dm_id': 5, 'name': 'aaaa, bbbb, cccc, dddd, eeee'}]}

    assert re_list6 == {'dms': []}

# test token error
def test_token_error():
    clear_v1()
    with pytest.raises(AccessError):
        dm_list_v1(' ')