from pydoc import Helper
from src.help import get_auth_user_id, check_channel_id_valid
import src.help as help
from src.error import AccessError
from src.error import InputError
from src.data_store import data_store
from datetime import datetime, timezone
import threading
import time


def message_send_v1(token, channel_id, message):
    '''
    Send a message from authorised_user to the channel specified by channel_id.
    Note: Each message should have it's own unique ID. I.E.
    No messages should share an ID with another message,
    even if that other message is in a different channel.

    Arguments:
        token (str) - authorised token(u_id and session_id)
        channel_id (int) - channel id
        message (str) - message content

    Exceptions:
        InputError - when message is more than 1000 characters
        AccessError - when the authorised user has not joined the channel they are trying to post to
        AccessError - when the token is invalid

    Return value:
        { message_id }
    '''

    # token is invalid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    # message len is invalid
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description="Message length error !!!")

    # channel id is invalid
    channel_exit = check_channel_id_valid(channel_id)
    if channel_exit == False:
        raise InputError(
            description="This Channel ID does not refer a valid channel!!!")

    # u_id is not in aim channel
    u_id = get_auth_user_id(token)
    store = data_store.get()
    channel_list = store['channels']

    channel_index = 0
    for channel in channel_list:
        if channel_id == channel["channel_id"]:
            if u_id not in channel["auth_user_id"] and u_id not in channel["channel_user_id"]:
                raise AccessError(
                    description="You're not a member of the channel !!!")
            break
        channel_index += 1

    # insert the message in aim channel
    message_created_time = int(time.time())
    # check all send later message
    is_later_message = False
    for later_mess in store['send_later_messages']:
        if later_mess["time_sent"] == message_created_time:
            is_later_message = True
            message_id = later_mess["message_id"]
            store["channels"][channel_index]["message"].insert(0, {
                "message_id": message_id,
                "u_id": u_id,
                "message": message,
                "time_created": message_created_time,
                "is_pinned": False,
                "reacts": [{"react_id": 1, "u_ids": [], "is_this_user_reacted": False}],
            })
            # remove the later message from send_later_message dic
            store['send_later_messages'].remove(later_mess)

    if is_later_message == False:
        store["recent_last_message_id"] = int(
            store["recent_last_message_id"]) + 1
        message_id = int(store["recent_last_message_id"])
        store["channels"][channel_index]["message"].insert(0, {
            "message_id": message_id,
            "u_id": u_id,
            "message": message,
            "time_created": message_created_time,
            "is_pinned": False,
            "reacts": [{"react_id": 1, "u_ids": [], "is_this_user_reacted": False}],
        })

    # notifications
    handle_list = help.get_message_tagged_list(message)
    user_handle = help.get_user_handle(u_id)
    ch_name = help.get_channel_name(channel_id)
    notification_detail = f"{user_handle} tagged you in {ch_name}: {message[0:20]}"
    for user in store["users"]:
        if user["handle"] in handle_list:
            user["notifications"].insert(0,{"dm_id": -1, "channel_id": channel_id, "notification_message": notification_detail})


    data_store.set(store)

    help.update_num_messages_sent(u_id)

    help.update_messages_exist(True)

    return {"message_id": message_id}


def message_remove_v1(token, message_id):
    '''
    Given a message_id for a message,
    this message is removed from the channel/DM

    Arguments:
        token (str) - authorised token(u_id and session_id)
        message_id (int) - message id of the original message

    Exceptions:
        InputError: message (based on ID) no longer exists
        AccessError: message with message_id was not sent by the authorised user making this request
        AccessError: the authorised user is an not owner of this channel (if it was sent to a channel) or the **Dreams**
    Return value: {}
    '''
    # token is invalid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    if help.message_id_is_valid_in_channel(message_id) == False and help.message_id_is_valid_in_dm(message_id) == False:
        raise InputError(description="Can't find related message")

    if help.message_id_is_valid_in_channel(message_id) == True:
        u_id = get_auth_user_id(token)
        found_channel = help.find_channel_by_message_id(message_id)
        found_message = help.find_message_in_channel(message_id)
        if u_id not in found_channel["auth_user_id"] and u_id != help.find_message_in_channel(message_id)["u_id"]:
            raise AccessError(
                description="You don't have permission to remove this channel message")
        found_channel["message"].remove(found_message)

    if help.message_id_is_valid_in_dm(message_id) == True:
        u_id = get_auth_user_id(token)
        found_dm = help.find_dm_by_message_id(message_id)
        found_message = help.find_message_in_dm(message_id)
        if u_id not in found_dm['dm_creator_id'] and u_id != help.find_message_in_dm(message_id)["u_id"]:
            raise AccessError(
                description="You don't have permission to remove this DM message")
        found_dm['dm_messages'].remove(found_message)
    data_store.set(data_store.get())

    help.update_messages_exist(False)
    return {}


def message_senddm_v1(token, dm_id, message):
    '''
    Send a message from authorised_user to the DM specified by dm_id.
    Note: Each message should have it's own unique ID. I.E.
    No messages should share an ID with another message,
    even if that other message is in a different channel or DM.

    Arguments:
        token (str) - authorised token(u_id and session_id)
        dm_id (int) - the dm ID
        message (str) - the content of the message sent

    Exceptions:
        InputError: message is more than 1000 characters
        AccessError: the user is not a member of the DM

    Return value: {}

    '''  # token is invalid
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    # channel id is invalid
    channel_exit = help.check_dm_id_valid(dm_id)
    if channel_exit == False:
        raise InputError(
            description="This message ID does not refer a valid DM !!!")

    # u_id is not in aim DM
    u_id = get_auth_user_id(token)
    store = data_store.get()
    dm_list = store['dm']

    dm_index = 0
    for dm in dm_list:
        if dm_id == dm['dm_id']:
            if u_id not in dm['dm_creator_id'] and u_id not in dm['dm_members_id']:
                raise AccessError(
                    description="You're not a member of the DM !!!")
            break
        dm_index += 1

    # message len is invalid
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description="Message length error !!!")

    # insert the message in aim channel
    message_created_time = int(time.time())
    # check all send later message
    is_later_message = False
    for later_mess in store['send_later_dmmessages']:
        if later_mess["time_sent"] == message_created_time:
            is_later_message = True
            message_id = later_mess["message_id"]
            store['dm'][dm_index]["dm_messages"].insert(0, {
                "message_id": message_id,
                "u_id": u_id,
                "message": message,
                "time_created": message_created_time,
                "is_pinned": False,
                "reacts": [{"react_id": 1, "u_ids": [], "is_this_user_reacted": False}],
            })
            # remove the later message from send_later_dmmessage dic
            store['send_later_dmmessages'].remove(later_mess)
    if is_later_message == False:
        store['recent_last_message_id'] = int(
            store['recent_last_message_id']) + 1
        message_id = int(store['recent_last_message_id'])
        store['dm'][dm_index]['dm_messages'].insert(0, {
            "message_id": message_id,
            "u_id": u_id,
            "message": message,
            "time_created": message_created_time,
            "is_pinned": False,
            "reacts": [{"react_id": 1, "u_ids": [], "is_this_user_reacted": False}],
        })

    # notifications
    handle_list = help.get_message_tagged_list(message)
    user_handle = help.get_user_handle(u_id)
    dm_name = help.get_dm_name(dm_id)
    notification_detail = f"{user_handle} tagged you in {dm_name}: {message[0:20]}"
    for user in store["users"]:
        if user["handle"] in handle_list:
            user["notifications"].insert(0,{"dm_id": dm_id, "channel_id": -1, "notification_message": notification_detail})


    data_store.set(store)

    help.update_num_messages_sent(u_id)

    help.update_messages_exist(True)
    
    return {"message_id": message_id}


def message_edit_v1(token, message_id, message):
    '''
    Given a message, update its text with new text.
    If the new message is an empty string, the message is deleted.

    Arguments:
        token (str) - authorised token(u_id and session_id)
        message_id (int) - message unique ID

    Exceptions:
        InputError:  length of message is over 1000 characters
        InputError:  the user is not a member of the DM/channel
        AccessError: message with message_id was not sent by the authorised user making this request
        AccessError: The authorised user is an not owner/creator of this channel/DM
    Return value: {}

    '''
    store = data_store.get()
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    # message len is invalid
    if len(message) > 1000:
        raise InputError(description="Message length error !!!")

    # messaege ID is invalid
    if help.message_id_is_valid_in_channel(message_id) == False and help.message_id_is_valid_in_dm(message_id) == False:
        raise InputError(description="Can't find related message")

    # not owoner or message sender in channel
    if help.message_id_is_valid_in_channel(message_id) == True:
        u_id = get_auth_user_id(token)
        found_channel = help.find_channel_by_message_id(message_id)
        found_message = help.find_message_in_channel(message_id)
        if u_id not in found_channel["auth_user_id"] and u_id != help.find_message_in_channel(message_id)["u_id"]:
            raise AccessError(
                description="You don't have permission to remove this channel message")
        found_message["message"] = message

    # not a memeber or creator in DM
    if help.message_id_is_valid_in_dm(message_id) == True:
        u_id = get_auth_user_id(token)
        found_dm = help.find_dm_by_message_id(message_id)
        found_message = help.find_message_in_dm(message_id)

        if u_id not in found_dm['dm_creator_id'] and u_id != help.find_message_in_dm(message_id)["u_id"]:
            raise AccessError(
                description="You don't have permission to remove this DM message")
        found_message["message"] = message
    # mepty message (deleted)
    if message == '':
        message_remove_v1(token, message_id)

    # notifications
    #ch
    if help.message_id_is_valid_in_channel(message_id) == True:
        u_id = get_auth_user_id(token)
        channel_id = help.find_channel_by_message_id(message_id)["channel_id"]
        handle_list = help.get_message_tagged_list(message)
        user_handle = help.get_user_handle(u_id)
        ch_name = help.get_channel_name(channel_id)
        notification_detail = f"{user_handle} tagged you in {ch_name}: {message[0:20]}"
        for user in store["users"]:
            if user["handle"] in handle_list:
                user["notifications"].insert(0,{"dm_id": -1, "channel_id": channel_id, "notification_message": notification_detail})
    #dm
    if help.message_id_is_valid_in_dm(message_id) == True:
        u_id = get_auth_user_id(token)
        dm_id = help.find_dm_by_message_id(message_id)["dm_id"]
        handle_list = help.get_message_tagged_list(message)
        user_handle = help.get_user_handle(u_id)
        dm_name = help.get_dm_name(dm_id)
        notification_detail = f"{user_handle} tagged you in {dm_name}: {message[0:20]}"
        for user in store["users"]:
            if user["handle"] in handle_list:
                user["notifications"].insert(0,{"dm_id": dm_id, "channel_id": -1, "notification_message": notification_detail})


    data_store.set(store)

    if message == '':
        help.update_messages_exist(False)

    return {}


def message_share_v1(token, og_message_id, message, channel_id, dm_id):
    '''
    og_message_id is the ID of the original message. channel_id is the channel
    that the message is being shared to, and is -1 if it is being sent to a DM.
    dm_id is the DM that the message is being shared to, and is -1 if it is being sent to a channel.
    message is the optional message in addition to the shared message,
    and will be an empty string '' if no message is given.
    A new message should be sent to the channel/DM identified by the channel_id/dm_id that
    contains the contents of both the original message and the optional message.
    The format does not matter as long as both the original and optional message exist as a substring within the new message.
    Once sent, this new message has no link to the original message, so if the original message is edited/deleted,
    no change will occur for the new message.

    Arguments:
        token (str) - authorised token(u_id and session_id)
        og_message_id (int) - the original message(id)
        message (str) - Shared message
        channel_id (int) - share the message to that channel
        dm_id (int) - share the message to that DM

    Exceptions:
        InputError: channel id or DM id is inavlid
        InputError: neither channel_id nor dm_id are -1
        InputError: og_message_id does not refer to a valid message within a channel/DM
                    that the authorised user has joined
        InputError: message is more than 1000 characters

        AccessError: The shared message is not a user that is not a member of the DM/channel
                     Invalid token
    Return value: {shared_message_id}
    '''
    store = data_store.get()
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    # check the input Channel id and DM id are invalid
    dm_exit = 0
    channel_exit = 0
    if help.check_dm_id_valid(dm_id) and channel_id == -1:
        dm_exit = 1
    if help.check_channel_id_valid(channel_id) and dm_id == -1:
        channel_exit = 1
    if dm_exit + channel_exit == 0 or dm_exit + channel_exit == 2:
        raise InputError(
            description="Input channel_ID or DM_ID not meet the specification")

    # original message id is invalid
    if help.message_id_is_valid_in_channel(og_message_id) == False and help.message_id_is_valid_in_dm(og_message_id) == False:
        raise InputError(description="Can't find related message")
    # message len is invalid
    if len(message) > 1000:
        raise InputError(description="Message length error !!!")

    u_id = get_auth_user_id(token)
    if help.message_id_is_valid_in_channel(og_message_id) == True:
        # og message channel
        og_channel = help.find_channel_by_message_id(og_message_id)
        if u_id not in og_channel["channel_user_id"]:
            raise InputError(
                description="You don't have permission to access the original message")
    else:
        # og message dm
        og_dm = help.find_dm_by_message_id(og_message_id)
        if u_id not in og_dm["dm_members_id"]:
            raise InputError(
                description="You don't have permission to access the original message")

    # aim channel is exit (judge the user in that channel or not)
    if channel_exit == 1:
        found_channel = help.searching_channel_with_channel_id(channel_id)

        if u_id not in found_channel["channel_user_id"]:
            raise AccessError(
                description="You can't share the message to this channel")
        # find the og_message
        if help.message_id_is_valid_in_channel(og_message_id) == True:
            # og message in channel
            found_message = help.find_message_in_channel(og_message_id)
        else:
            # og message in dm
            found_message = help.find_message_in_dm(og_message_id)
        new_message = found_message["message"] + '|' + str(message)
        mess_id = message_send_v1(token, channel_id, new_message)["message_id"]

     # aim dm is exit (judge the user in that dm or not)
    else:
        found_dm = help.searching_dm_with_dm_id(dm_id)
        found_message = help.find_message_in_dm(og_message_id)

        if u_id not in found_dm['dm_members_id']:
            raise AccessError(
                description="You can't share the message to this DM")
        if help.message_id_is_valid_in_channel(og_message_id) == True:
            # og message in channel
            found_message = help.find_message_in_channel(og_message_id)
        else:
            # og message in dm
            found_message = help.find_message_in_dm(og_message_id)
        new_message = found_message["message"] + '|' + str(message)
        mess_id = message_senddm_v1(token, dm_id, new_message)["message_id"]


    # notifications
    if dm_id == -1:
        handle_list = help.get_message_tagged_list(message)
        user_handle = help.get_user_handle(u_id)
        ch_name = help.get_channel_name(channel_id)
        notification_detail = f"{user_handle} tagged you in {ch_name}: {message[0:20]}"
        for user in store["users"]:
            if user["handle"] in handle_list:
                user["notifications"].insert(0,{"dm_id": -1, "channel_id": channel_id, "notification_message": notification_detail})


    if channel_id == -1:
        handle_list = help.get_message_tagged_list(message)
        user_handle = help.get_user_handle(u_id)
        dm_name = help.get_dm_name(dm_id)
        notification_detail = f"{user_handle} tagged you in {dm_name}: {message[0:20]}"
        for user in store["users"]:
            if user["handle"] in handle_list:
                user["notifications"].insert(0,{"dm_id": dm_id, "channel_id": -1, "notification_message": notification_detail})

    data_store.set(store)

    help.update_num_messages_sent(u_id)
    
    help.update_messages_exist(True)
    return {"shared_message_id": mess_id}


def message_pin_v1(token, message_id):
    '''
    Description:
        Given a message within a channel or DM, marks it as "pinned"

    Arguments:
        token (str) - authorised token(u_id and session_id)
        message_id (int) - the message(id) need pin

    InputError:
        1. The message is not a valid message within a channel or DM that the authorised user has joined
        2. The message is already pinned

    AccessError :
        1. The token is invalid.
        2. Message_id refers to a valid message in a joined channel/DM and the authorised user does not
        3. have owner permissions in the channel/DM

    Return Value:
        {}
    '''
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")
    # message id is invalid
    if help.message_id_is_valid_in_channel(message_id) == False and help.message_id_is_valid_in_dm(message_id) == False:
        raise InputError(description="Can't find related message")

    u_id = get_auth_user_id(token)
    # check the message id is in channle or dm
    if help.message_id_is_valid_in_channel(message_id) == True:
        channel_dic = help.find_channel_by_message_id(message_id)
        # if user don't have channle owner permission
        if u_id not in channel_dic["owner_permission"]:
            raise AccessError(
                description="You don't have permission to pin this channel message")
        message_dic = help.find_message_in_channel(message_id)
    else:
        dm_dic = help.find_dm_by_message_id(message_id)
        # if user is not dm creator
        if u_id not in dm_dic["dm_creator_id"]:
            raise AccessError(
                description="You don't have permission to pin this dm message")
        message_dic = help.find_message_in_dm(message_id)

    # message is already pinned
    if message_dic["is_pinned"] == True:
        raise InputError(description="This message is already pinned")
    else:
        message_dic["is_pinned"] = True

    data_store.set(data_store.get())
    return {}


def message_unpin_v1(token, message_id):
    '''
    Description:
        Given a message within a channel or DM, marks it as "unpinned"

    Arguments:
        token (str) - authorised token(u_id and session_id)
        message_id (int) - the message(id) need pin

    InputError:
        1. The message is not a valid message within a channel or DM that the authorised user has joined
        2. The message is not already pinned

    AccessError :
        1. The token is invalid.
        2. Message_id refers to a valid message in a joined channel/DM and the authorised user does not
        3. have owner permissions in the channel/DM

    Return Value:
        {}
    '''
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")
    # message id is invalid
    if help.message_id_is_valid_in_channel(message_id) == False and help.message_id_is_valid_in_dm(message_id) == False:
        raise InputError(description="Can't find related message")

    u_id = get_auth_user_id(token)
    # check the message id is in channle or dm
    if help.message_id_is_valid_in_channel(message_id) == True:
        channel_dic = help.find_channel_by_message_id(message_id)
        # if user don't have channle owner permission
        if u_id not in channel_dic["owner_permission"]:
            raise AccessError(
                description="You don't have permission to unpin this channel message")
        message_dic = help.find_message_in_channel(message_id)
    else:
        dm_dic = help.find_dm_by_message_id(message_id)
        # if user is not dm creator
        if u_id not in dm_dic["dm_creator_id"]:
            raise AccessError(
                description="You don't have permission to unpin this dm message")
        message_dic = help.find_message_in_dm(message_id)

    # message is already pinned
    if message_dic["is_pinned"] == False:
        raise InputError(description="This message is not already pinned")
    else:
        message_dic["is_pinned"] = False

    data_store.set(data_store.get())
    return {}


def message_react_v1(token, message_id, react_id):
    '''
    Description:
        Given a message within a channel or DM the authorised user is part of,
        add a "react" to that particular message.

    Arguments:
        token (str) - authorised token(u_id and session_id)
        message_id (int) - the unique message id

    InputError:
        1. The message is not a valid message within a channel or DM that the authorised user has joined.
        2. react_id is not a valid react ID - currently, the only valid react ID the frontend has is 1.
        3. The message already contains a react with ID react_id from the authorised user
    AccessError :
        1. The token is invalid.

    Return Value:
        {}
    '''
    store = data_store.get()
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")
    # message id is invalid
    if help.message_id_is_valid_in_channel(message_id) == False and help.message_id_is_valid_in_dm(message_id) == False:
        raise InputError(description="Can't find related message")
    # (assume currently, the only valid react ID is 1)
    # invalid react ID
    if react_id != 1:
        raise InputError(description="Invalid react ID")

    if help.message_id_is_valid_in_channel(message_id) == True:
        # message in channel
        found_message = help.find_message_in_channel(message_id)
    else:
        # message in dm
        found_message = help.find_message_in_dm(message_id)

    u_id = get_auth_user_id(token)
    if u_id in found_message["reacts"][0]["u_ids"]:
        found_message["reacts"][0]["is_this_user_reacted"] = True
        raise InputError(description="This user already reacted this message")
    else:
        found_message["reacts"][0]["u_ids"].append(u_id)
        found_message["reacts"][0]["is_this_user_reacted"] = False


    # notifications
    if help.message_id_is_valid_in_channel(message_id) == True:
        # message in channel
        found_message = help.find_message_in_channel(message_id)
        sender_id = found_message['u_id']
        channel_id = help.find_channel_by_message_id(message_id)["channel_id"]
        ch_name = help.get_channel_name(channel_id)
        user_handle = help.get_user_handle(u_id)
        notification_detail = f"{user_handle} reacted to your message in {ch_name}"
        if sender_id != u_id:
            for user in store["users"]:
                if user["auth_user_id"] == sender_id:
                    user["notifications"].insert(0, {"channel_id": channel_id, "dm_id": -1, "notification_message": notification_detail})
                

    else:
        # message in dm

        found_message = help.find_message_in_dm(message_id)
        sender_id = found_message['u_id']
        dm_id = help.find_dm_by_message_id(message_id)['dm_id']
        dm_name = help.get_dm_name(dm_id)
        user_handle = help.get_user_handle(u_id)
        notification_detail = f"{user_handle} reacted to your message in {dm_name}"
        if sender_id != u_id:
            for user in store["users"]:
                if user["auth_user_id"] == sender_id:
                    user["notifications"].insert(0, {"channel_id": -1, "dm_id": dm_id, "notification_message": notification_detail})
    data_store.set(data_store.get())
    return{}


def message_unreact_v1(token, message_id, react_id):
    '''
    Description:
        Given a message within a channel or DM the authorised user is part of, 
        remove a "react" to that particular message.

    Arguments:
        token (str) - authorised token(u_id and session_id)
        message_id (int) - the unique message id

    InputError:
        1. The message is not a valid message within a channel or DM that the authorised user has joined.
        2. react_id is not a valid react ID.
        3. The message does not contain a react with ID react_id from the authorised user
        1. The token is invalid.

    Return Value:
        {}
    '''
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")
    # message id is invalid
    if help.message_id_is_valid_in_channel(message_id) == False and help.message_id_is_valid_in_dm(message_id) == False:
        raise InputError(description="Can't find related message")
    # invalid react ID(if there just have react_id = 1)
    if react_id != 1:
        raise InputError(description="Invalid react ID")
    if help.message_id_is_valid_in_channel(message_id) == True:
        # message in channel
        found_message = help.find_message_in_channel(message_id)
    else:
        # message in dm
        found_message = help.find_message_in_dm(message_id)

    u_id = get_auth_user_id(token)
    if u_id in found_message["reacts"][0]["u_ids"]:
        found_message["reacts"][0]["u_ids"].remove(u_id)
        found_message["reacts"][0]["is_this_user_reacted"] = False
    else:
        raise InputError(
            description=f"User not reacted this message whit react id {react_id}")
    data_store.set(data_store.get())
    return{}


def message_sendlater_v1(token, channel_id, message, time_sent):
    '''
    Description:
         Sends a message from an authorised user to the channel specified by channel_id automatically at a specified time
    in the future

    Arguments:
        token (str) - authorised token(u_id and session_id)
        channel_id -  Send the message to that channel with this ID
        message -  Message should send
        time_sent - Set a time which in the future that the message should send

    Input Errror : 
        1. channel_id does not refer to a valid channel
        2. Length of message is less than 1 or over 1000 characters
        3. time_send is a time in the past

    AccessError : 
        1. The token of the authorised user is invalid.
        2. channel_id is valid and the authorised user is not a member of 
           the channel they are trying to post to

    Return Value:
    { message_id } - message ID of the message send
    '''
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    # message len is invalid
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description="Message length error !!!")

    # channel id is invalid
    if check_channel_id_valid(channel_id) == False:
        raise InputError(
            description="This Channel id does not refer a valid channel!!!")
    # Time sent is in the past
    now = int(time.time())
    time_diff = time_sent - now
    if time_diff < 0:
        raise InputError(description="Time sent is in the past")

    # User is not a member to this channle
    u_id = get_auth_user_id(token)
    found_channel = help.searching_channel_with_channel_id(channel_id)
    if u_id not in found_channel["channel_user_id"]:
        raise AccessError(
            description="You're not a member of this channel")
    timer = threading.Timer(time_diff, message_send_v1,
                            [token, channel_id, message])
    timer.start()
    store = data_store.get()
    store["recent_last_message_id"] = int(store["recent_last_message_id"]) + 1
    message_id = int(store["recent_last_message_id"])

    store['send_later_messages'].append(
        {"message_id": message_id, "time_sent": time_sent}
    )

    # notifications
    handle_list = help.get_message_tagged_list(message)
    user_handle = help.get_user_handle(u_id)
    ch_name = help.get_channel_name(channel_id)
    notification_detail = f"{user_handle} tagged you in {ch_name}: {message[0:20]}"
    for user in store["users"]:
        if user["handle"] in handle_list:
            user["notifications"].insert(0,{"dm_id": -1, "channel_id": channel_id, "notification_message": notification_detail})

    data_store.set(store)
    return {"message_id": message_id}


def message_sendlaterdm_v1(token, dm_id, message, time_sent):
    '''
    Description:
        Sends a message from an authorised user to the dm specified by dm_id automatically at a specified time
        in the future

    Arguments:
        token (str) - authorised token(u_id and session_id)
        dm_id -  Send the message to that dm with this ID
        message -  Message should send
        time_sent - Set a time which in the future that the message should send

    Input Errror : 
        1. channel_id does not refer to a valid channel
        2. Length of message is less than 1 or over 1000 characters
        3. time_send is a time in the past

    AccessError : 
        1. The token of the authorised user is invalid.
        2. dm_id is valid and the authorised user is not a member of 
           the DM they are trying to post to

    Return Value:
    { message_id } - message ID of the message send
    '''
    # invalid token
    if help.check_token(token) == False:
        raise AccessError(description="Invalid token !!!")

    # message len is invalid
    if len(message) > 1000 or len(message) < 1:
        raise InputError(description="Message length error !!!")

    # DM id is invalid
    if help.check_dm_id_valid(dm_id) == False:
        raise InputError(
            description="This dm id does not refer a valid DM!!!")
    # Time sent is in the past
    now = int(time.time())
    time_diff = time_sent - now
    if time_diff < 0:
        raise InputError(description="Time sent is in the past")

    # User is not a member to this channle
    u_id = get_auth_user_id(token)
    found_dm = help.searching_dm_with_dm_id(dm_id)
    if u_id not in found_dm["dm_members_id"]:
        raise AccessError(
            description="You're not a member of this DM")

    timer = threading.Timer(time_diff, message_senddm_v1,
                            [token, dm_id, message])
    timer.start()
    store = data_store.get()
    store["recent_last_message_id"] = int(store["recent_last_message_id"]) + 1
    message_id = int(store["recent_last_message_id"])

    store['send_later_dmmessages'].append(
        {"message_id": message_id, "time_sent": time_sent}
    )

    # notifications
    handle_list = help.get_message_tagged_list(message)
    user_handle = help.get_user_handle(u_id)
    dm_name = help.get_dm_name(dm_id)
    notification_detail = f"{user_handle} tagged you in {dm_name}: {message[0:20]}"
    for user in store["users"]:
        if user["handle"] in handle_list:
            user["notifications"].insert(0,{"dm_id": dm_id, "channel_id": -1, "notification_message": notification_detail})
    data_store.set(store)
    return {"message_id": message_id}
