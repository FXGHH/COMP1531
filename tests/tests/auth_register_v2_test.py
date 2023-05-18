import pytest
from src.auth import auth_register_v2
from src.error import InputError
from src.other import clear_v1
from src.data_store import data_store
import src.help as help
##########################################################################################################################
# InputError test

# email not vaild1


def test_register_invalid_email_1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc', '1234567', 'Jake', 'Renzella')

# #email not vaild2


def test_register_invalid_email_2():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc.com', '1234567', 'Jake', 'Renzella')

# #email not vaild3


def test_register_invalid_email_3():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@com', '1234567', 'Jake', 'Renzella')

# #password less than 6


def test_register_password_less_6():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@outlook.com', '12345', 'Jake', 'Renzella')

# first name less than 1


def test_register_invalid_first_less_1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@outlook.com', '1234567', '', 'Renzella')

# first name more than 50


def test_register_invalid_first_more_50():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@outlook.com', '1234567',
                         'qwerqwerqwerqwerqwerqwerqwerqwerqwer12341234qwerqwer', 'Renzella')

# last name less than 1


def test_register_last_less_1():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@outlook.com', '1234567', 'Jake', '')

# last more than 50


def test_register_last_more_50():
    clear_v1()
    with pytest.raises(InputError):
        auth_register_v2('abc@qq.com', '1234567', 'Jake',
                         'qwerqwerqwerqwerqwerqwerqwerqwerqwer12341234qwerqwer')

##########################################################################################################################
# duplicate check

# duplicate check only 1 register


def test_register_no_duplicates_1():
    clear_v1()
    auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')

# duplicate check only 1 register, diff


def test_register_no_duplicates_2():
    clear_v1()
    auth_register_v2('abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_register_v2('abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')

# duplicate check 2 registers


def test_register_no_duplicates_2_register():
    clear_v1()
    auth_register_v2('abc@qq.com', '123123123123', 'Jake', 'Renzella')
    auth_register_v2('abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')
    with pytest.raises(InputError):
        auth_register_v2('abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')

##########################################################################################################################
# auth_user_id comfirm
# only 1


def test_user_id_work():
    clear_v1()
    register_id_returen = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    assert register_id_returen['auth_user_id'] == 1

# 2 users


def test_user_id_work_2_workers():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    register_id_returen_2 = auth_register_v2(
        'abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')
    assert register_id_returen_1['auth_user_id'] == 1
    assert register_id_returen_2['auth_user_id'] == 2
##########################################################################################################################
# handle check


def test_user_id_work_handle():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    id = register_id_returen_1['auth_user_id']
    store = data_store.get()
    handle = ''
    for user in store['users']:
        if user['auth_user_id'] == id:
            handle = user['handle']
    assert "jakerenzella" == handle

# when first + last more than 20


def test_user_id_work_more_20():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'JakeJakeJakeJake', 'Renzella')
    id = register_id_returen_1['auth_user_id']
    store = data_store.get()
    handle = ''
    for user in store['users']:
        if user['auth_user_id'] == id:
            handle = user['handle']
    assert "jakejakejakejakerenz" == handle


# when handle < 20 check handle+number0
def test_user_id_work_less_20_handle_number0():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    register_id_returen_2 = auth_register_v2(
        'abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')
    id1 = register_id_returen_1['auth_user_id']
    id2 = register_id_returen_2['auth_user_id']
    store = data_store.get()
    handle1 = ''
    for user in store['users']:
        if user['auth_user_id'] == id1:
            handle1 = user['handle']

    handle2 = ''
    for user in store['users']:
        if user['auth_user_id'] == id2:
            handle2 = user['handle']
    assert "jakerenzella" == handle1
    assert "jakerenzella0" == handle2

# when handle < 20 check handle+number1


def test_user_id_work_less_20_handle_number1():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    register_id_returen_2 = auth_register_v2(
        'abcdeee@qq.com', '123123123123', 'Jake', 'Renzella')
    register_id_returen_3 = auth_register_v2(
        'abcdeeed@qq.com', '123123123123', 'Jake', 'Renzella')
    id1 = register_id_returen_1['auth_user_id']
    id2 = register_id_returen_2['auth_user_id']
    id3 = register_id_returen_3['auth_user_id']
    store = data_store.get()
    handle1 = ''
    for user in store['users']:
        if user['auth_user_id'] == id1:
            handle1 = user['handle']

    handle2 = ''
    for user in store['users']:
        if user['auth_user_id'] == id2:
            handle2 = user['handle']

    handle3 = ''
    for user in store['users']:
        if user['auth_user_id'] == id3:
            handle3 = user['handle']
    assert "jakerenzella" == handle1
    assert "jakerenzella0" == handle2
    assert "jakerenzella1" == handle3


# handle more than 20 and add number from none = 1
def test_user_id_work_more_20_handle_number_none01():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'JakeJakeJakeJake', 'Renzella')
    register_id_returen_2 = auth_register_v2(
        'abcdeee@qq.com', '123123123123', 'JakeJakeJakeJake', 'Renzella')
    register_id_returen_3 = auth_register_v2(
        'abcdeeed@qq.com', '123123123123', 'JakeJakeJakeJake', 'Renzella')
    id1 = register_id_returen_1['auth_user_id']
    id2 = register_id_returen_2['auth_user_id']
    id3 = register_id_returen_3['auth_user_id']
    store = data_store.get()
    handle1 = ''
    for user in store['users']:
        if user['auth_user_id'] == id1:
            handle1 = user['handle']

    handle2 = ''
    for user in store['users']:
        if user['auth_user_id'] == id2:
            handle2 = user['handle']

    handle3 = ''
    for user in store['users']:
        if user['auth_user_id'] == id3:
            handle3 = user['handle']
    assert "jakejakejakejakerenz" == handle1
    assert "jakejakejakejakerenz0" == handle2
    assert "jakejakejakejakerenz1" == handle3
# ##########################################################################################################################
# detail register check


def test_detail_register_check_0():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')
    id = register_id_returen_1['auth_user_id']
    store = data_store.get()
    data_store_dit = {}
    for user in store['users']:
        if user['auth_user_id'] == id:
            data_store_dit = user
    #
    detail_dic = {
        'auth_user_id': 1,
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella',
        "handle": "jakerenzella",
        'is_global_owner': True
    }
    assert data_store_dit['auth_user_id'] == detail_dic['auth_user_id']
    assert data_store_dit['email'] == detail_dic['email']
    assert data_store_dit['password'] == help.hash(detail_dic['password'])
    assert data_store_dit['name_first'] == detail_dic['name_first']
    assert data_store_dit['name_last'] == detail_dic['name_last']
    assert data_store_dit['handle'] == detail_dic['handle']
    assert data_store_dit['is_global_owner'] == detail_dic['is_global_owner']
# ##########################################################################################################################


def test_test_handles_generated_correctly():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', 'klmnopqrst', '@bcdefgh!j', 'klmn opqrst')
    id = register_id_returen_1['auth_user_id']
    store = data_store.get()
    handle = ''
    for user in store['users']:
        if user['auth_user_id'] == id:
            handle = user['handle']
    assert "bcdefghjklmnopqrst" == handle
# ##########################################################################################################################
# ##########################################################################################################################
# # detail register check


def test_detail_register_check():
    clear_v1()
    register_id_returen_1 = auth_register_v2(
        'abc@qq.com', '123123123123', 'Jake', 'Renzella')

    id = register_id_returen_1['auth_user_id']
    store = data_store.get()
    data_store_dit = {}
    for user in store['users']:
        if user['auth_user_id'] == id:
            data_store_dit = user
    #
    detail_dic = {
        'auth_user_id': 1,
        'email': 'abc@qq.com',
        'password': '123123123123',
        'name_first': 'Jake',
        'name_last': 'Renzella',
        "handle": "jakerenzella",
        'is_global_owner': True
    }

    register_id_returen_2 = auth_register_v2(
        'abcde@qq.com', '123123123123', 'Jake', 'Renzella')
    id2 = register_id_returen_2['auth_user_id']
    # store = data_store.get()
    data_store_dit2 = {}
    for user in store['users']:
        if user['auth_user_id'] == id2:
            data_store_dit2 = user

    assert data_store_dit2['auth_user_id'] == 2
    assert data_store_dit2['is_global_owner'] == False

    assert data_store_dit['auth_user_id'] == detail_dic['auth_user_id']
    assert data_store_dit['email'] == detail_dic['email']
    assert data_store_dit['password'] == help.hash(detail_dic['password'])
    assert data_store_dit['name_first'] == detail_dic['name_first']
    assert data_store_dit['name_last'] == detail_dic['name_last']
    assert data_store_dit['handle'] == detail_dic['handle']
    assert data_store_dit['is_global_owner'] == detail_dic['is_global_owner']
