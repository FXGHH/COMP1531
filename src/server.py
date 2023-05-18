import sys
import signal
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from src.error import InputError
from src import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import src.auth as auth
import src.channels as channels
import src.channel as channel
import src.message as message
import src.help as help
import src.other as other
import src.dm as dm
import src.admin as admin
import src.standup as standup
from src.data_store import data_store
import src.user_profile as user_profile
import src.user_stats as user_stats

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

#######################################

################################ A U T H ########################################


@APP.route("/auth/register/v2", methods=["POST"])
def auth_register_v2():
    input = request.get_json()
    resp = auth.auth_register_v2(
        input["email"], input["password"], input["name_first"], input["name_last"])
    help.save_data()
    return dumps(resp)


@APP.route("/auth/login/v2", methods=['POST'])
def auth_login_v2():
    input = request.get_json()
    resp = auth.auth_login_v2(input['email'], input['password'])
    help.save_data()
    return dumps(resp)


@APP.route("/auth/logout/v1", methods=['POST'])
def auth_logout_v1():
    input = request.get_json()
    auth.auth_logout_v1(input['token'])
    help.save_data()
    return dumps({})

@APP.route("/auth/passwordreset/request/v1", methods=['POST'])
def auth_passwordreset_request_v1():
    store = data_store.get()
    input = request.get_json()
    resp = auth.auth_passwordreset_request_v1(input["email"])
    reset_code = ""
    for dic in store["users"]:
        if dic["email"] == input["email"]:
            reset_code = dic["reset_code"]

    sender_address = "22t1.f13b.elephant@gmail.com"
    sender_pass = "qwerASDF4321"
    receiver_address = input["email"]

    mail_content = f"This is reset code for Seams:{reset_code}"
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "Password reset Seams"

    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com:587')
    session.ehlo()
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return dumps(resp)

@APP.route("/auth/passwordreset/reset/v1", methods=['POST'])
def auth_passwordreset_reset_v1():
    input = request.get_json()
    resp = auth.auth_passwordreset_reset_v1(input["reset_code"], input["new_password"])
    return dumps(resp)
################################ A U T H ########################################


################################ C H A N N E L S ################################
@APP.route("/channels/create/v2", methods=['POST'])
def channels_create_v2():
    input = request.get_json()
    channel_id = channels.channels_create_v2(
        input['token'], input['name'], input['is_public'])
    return dumps(channel_id)


@APP.route("/channels/list/v2", methods=['GET'])
def channels_list_v2():
    input = request.args.get('token')
    resp = channels.channels_list_v2(input)
    return dumps(resp)


@APP.route("/channels/listall/v2", methods=["GET"])
def channels_listall_v2():
    token = request.args.get("token")
    returned_list = channels.channels_listall_v2(token)
    return dumps(returned_list)
################################ C H A N N E L S ################################


################################ C H A N N E L ##################################
@APP.route("/channel/invite/v2", methods=['POST'])
def channel_invite_v2():
    input = request.get_json()
    resp = channel.channel_invite_v2(
        input["token"], input["channel_id"], input["u_id"])
    return dumps(resp)


@APP.route("/channel/join/v2", methods=["POST"])
def channel_join_v2():
    input = request.get_json()
    resp = channel.channel_join_v2(input['token'], input['channel_id'])
    return dumps(resp)


@APP.route("/channel/details/v2", methods=["GET"])
def channel_details_v2():
    token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    returned_dict = channel.channel_details_v2(token, int(channel_id))
    return dumps(returned_dict)


@APP.route("/channel/leave/v1", methods=["POST"])
def channel_leave_v1():
    input = request.get_json()
    resp = channel.channel_leave_v1(input['token'], input['channel_id'])
    return dumps(resp)


@APP.route("/channel/addowner/v1", methods=["POST"])
def channel_addowner_v1():
    input = request.get_json()
    resp = channel.channel_addowner_v1(
        input['token'], input['channel_id'], input['u_id'])
    return dumps(resp)


@APP.route("/channel/removeowner/v1", methods=["POST"])
def channel_removeowner_v1():
    input = request.get_json()
    resp = channel.channel_removeowner_v1(
        input['token'], input['channel_id'], input['u_id'])
    return dumps(resp)
################################ C H A N N E L ##################################


################################ M E S S A G E ##################################
@APP.route("/channel/messages/v2", methods=["GET"])
def channel_messages_v2():
    user_token = request.args.get("token")
    channel_id = request.args.get("channel_id")
    start = request.args.get("start")
    returned = channel.channel_messages_v2(
        user_token, int(channel_id), int(start))
    return dumps(returned)


@APP.route("/message/send/v1", methods=["POST"])
def message_send_v2():
    user_input = request.get_json()
    returned = message.message_send_v1(user_input["token"], int(
        user_input["channel_id"]), user_input["message"])
    return dumps(returned)


@APP.route("/message/remove/v1", methods=["DELETE"])
def message_remove_v1():
    user_input = request.get_json()
    returned = message.message_remove_v1(
        user_input["token"], int(user_input["message_id"]))
    return dumps(returned)


@APP.route("/message/senddm/v1", methods=["POST"])
def message_senddm_v1():
    user_input = request.get_json()
    returned = message.message_senddm_v1(user_input["token"], int(
        user_input["dm_id"]), user_input["message"])
    return dumps(returned)


@APP.route("/message/edit/v1", methods=["PUT"])
def message_edit_v1():
    user_input = request.get_json()
    returned = message.message_edit_v1(user_input["token"], int(
        user_input["message_id"]), user_input["message"])
    return dumps(returned)


@APP.route("/message/share/v1", methods=["POST"])
def message_share_v1():
    user_input = request.get_json()
    returned = message.message_share_v1(user_input["token"], int(
        user_input["og_message_id"]), user_input["message"], int(user_input["channel_id"]), int(user_input["dm_id"]))
    return dumps(returned)


@APP.route("/message/pin/v1", methods=["POST"])
def message_pin_v1():
    user_input = request.get_json()
    returned = message.message_pin_v1(
        user_input["token"], int(user_input["message_id"]))
    return dumps(returned)


@APP.route("/message/unpin/v1", methods=["POST"])
def message_unpin_v1():
    user_input = request.get_json()
    returned = message.message_unpin_v1(
        user_input["token"], int(user_input["message_id"]))
    return dumps(returned)


@APP.route("/message/react/v1", methods=["POST"])
def message_react_v1():
    user_input = request.get_json()
    returned = message.message_react_v1(user_input["token"], int(
        user_input["message_id"]), int(user_input["react_id"]))
    return dumps(returned)


@APP.route("/message/unreact/v1", methods=["POST"])
def message_unreact_v1():
    user_input = request.get_json()
    returned = message.message_unreact_v1(user_input["token"], int(
        user_input["message_id"]), int(user_input["react_id"]))
    return dumps(returned)


@APP.route("/message/sendlater/v1", methods=["POST"])
def message_sendlater_v1():
    user_input = request.get_json()
    returned = message.message_sendlater_v1(user_input["token"], int(
        user_input["channel_id"]), user_input["message"], int(user_input["time_sent"]))
    return dumps(returned)


@APP.route("/message/sendlaterdm/v1", methods=["POST"])
def message_sendlaterdm_v1():
    user_input = request.get_json()
    returned = message.message_sendlaterdm_v1(user_input["token"], int(
        user_input["dm_id"]), user_input["message"], int(user_input["time_sent"]))
    return dumps(returned)
################################ M E S S A G E ##################################


################################ D M ############################################
@APP.route("/dm/create/v1", methods=['POST'])
def dm_create_v1():
    input = request.get_json()
    resp = dm.dm_create_v1(
        input["token"], input["u_ids"])
    return dumps(resp)


@APP.route("/dm/list/v1", methods=['GET'])
def dm_list_v1():
    token = request.args.get("token")
    resp = dm.dm_list_v1(token)
    return dumps(resp)


@APP.route("/dm/remove/v1", methods=['DELETE'])
def dm_remove_v1():
    input = request.get_json()
    resp = dm.dm_remove_v1(
        input["token"], input["dm_id"])
    return dumps(resp)


@APP.route("/dm/details/v1", methods=['GET'])
def dm_details_v1():
    token = request.args.get("token")
    dm_id = request.args.get("dm_id")
    resp = dm.dm_details_v1(token, int(dm_id))
    return dumps(resp)


@APP.route("/dm/leave/v1", methods=['POST'])
def dm_leave_v1():
    input = request.get_json()
    resp = dm.dm_leave_v1(
        input["token"], input["dm_id"])
    return dumps(resp)


@APP.route("/dm/messages/v1", methods=["GET"])
def dm_messages_v1():
    token = request.args.get("token")
    dm_id = request.args.get("dm_id")
    start = request.args.get("start")
    returned = dm.dm_messages_v1(token, int(dm_id), int(start))
    return dumps(returned)


# @APP.route("/dm/messages/v1", methods=['GET'])

################################ D M ############################################


################################ U S E R ########################################
@APP.route("/users/all/v1", methods=["GET"])
def users_all_v1():
    token = request.args.get("token")
    result_user_list = user_profile.users_all_v1(token)
    return dumps(result_user_list)


@APP.route("/user/profile/v1", methods=["GET"])
def user_profile_v1():
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    returned_user = user_profile.user_profile_v1(token, int(u_id))
    return dumps(returned_user)


@APP.route("/user/profile/setname/v1", methods=["PUT"])
def user_profile_setname_v1():
    user_input = request.get_json()
    token = user_input['token']
    name_first = user_input['name_first']
    name_last = user_input['name_last']
    user_profile.user_profile_setname_v1(token, name_first, name_last)
    return dumps({})


@APP.route("/user/profile/setemail/v1", methods=["PUT"])
def user_profile_setemail_v1():
    user_input = request.get_json()
    token = user_input['token']
    email = user_input['email']
    user_profile.user_profile_setemail_v1(token, email)
    return dumps({})


@APP.route("/user/profile/sethandle/v1", methods=["PUT"])
def user_profile_sethandle_v1():
    user_input = request.get_json()
    token = user_input['token']
    handle_str = user_input['handle_str']
    user_profile.user_profile_sethandle_v1(token, handle_str)
    return dumps({})

@APP.route("/user/profile/v2", methods=["GET"])
def user_profile_v2():
    token = request.args.get("token")
    u_id = request.args.get("u_id")
    returned_user = user_profile.user_profile_v2(token, int(u_id))
    return dumps(returned_user)

@APP.route("/user/profile/uploadphoto/v1", methods=["POST"])
def user_profile_upload_photo_v1():
    user_input = request.get_json()
    token = user_input['token']
    img_url = user_input['img_url']
    x_start = user_input['x_start']
    y_start = user_input['y_start']
    x_end = user_input['x_end']
    y_end = user_input['y_end']
    user_profile.user_profile_upload_photo_v1(token, img_url, x_start, y_start, x_end, y_end)
    return dumps({})


@APP.route("/user/stats/v1", methods=["GET"])
def user_stat_v1():
    token = request.args.get("token")
    current_stats = user_stats.user_stats_v1(token)
    return dumps(current_stats)


@APP.route("/users/stats/v1", methods=["GET"])
def users_stat_v1():
    token = request.args.get("token")
    current_stats = user_stats.users_stats_v1(token)
    return dumps(current_stats)

################################ U S E R ########################################


################################ A D M I N ######################################
@APP.route("/admin/user/remove/v1", methods=['DELETE'])
def admin_user_remove_v1():
    input = request.get_json()
    resp = admin.admin_user_remove_v1(input["token"], input["u_id"])
    return dumps(resp)


@APP.route("/admin/userpermission/change/v1", methods=['POST'])
def admin_userpermission_change_v1():
    input = request.get_json()
    resp = admin.admin_userpermission_change_v1(
        input["token"], input["u_id"], input['permission_id'])
    return dumps(resp)
################################ A D M I N ######################################


################################ O T H E R ######################################
@APP.route("/clear/v1", methods=['DELETE'])
def clear_v1():
    other.clear_v1()
    return dumps({})

@APP.route("/search/v1", methods=['GET'])
def search_v1():
    token = request.args.get("token")
    query_str = request.args.get("query_str")
    resp = other.search_v1(token, query_str)
    return dumps(resp)

@APP.route("/notifications/get/v1", methods=['GET'])
def notifications_get_v1():
    token = request.args.get("token")
    resp = other.notifications_get_v1(token)
    return dumps(resp)
################################ O T H E R ######################################

################################ S T A N D U P ##################################
@APP.route("/standup/start/v1", methods=['POST'])
def standup_start_v1():
    input = request.get_json()
    resp = standup.standup_start_v1(
        input["token"], input["channel_id"], input['length'])
    return dumps(resp)

@APP.route("/standup/active/v1", methods=['GET'])
def standup_active_v1():
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    resp = standup.standup_active_v1(token, channel_id)
    return dumps(resp)

@APP.route("/standup/send/v1", methods=['POST'])
def standup_send_v1():
    input = request.get_json()
    resp = standup.standup_send_v1(
        input["token"], input["channel_id"], input['message'])
    return dumps(resp)
################################ S T A N D U P ##################################

#######################################
if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port)  # Do not edit this port
