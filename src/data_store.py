'''
data_store.py

This contains a definition for a Datastore class which you should use to store your data.
You don't need to understand how it works at this point, just how to use it :)

The data_store variable is global, meaning that so long as you import it into any
python file in src, you can access its contents.

Example usage:

    from data_store import data_store

    store = data_store.get()
    print(store) # Prints { 'names': ['Nick', 'Emily', 'Hayden', 'Rob'] }

    names = store['names']

    names.remove('Rob')
    names.append('Jake')
    names.sort()

    print(store) # Prints { 'names': ['Emily', 'Hayden', 'Jake', 'Nick'] }
    data_store.set(store)
'''

# YOU SHOULD MODIFY THIS OBJECT BELOW
initial_object = {
    'users': [],
    'channels': [],
    'dm': [],
    'total_users': 0,
    'total_dm': 0,
    'standups': [],
    'workspace_stats':{'channels_exist':[],'dms_exist':[],'messages_exist':[]},
    'recent_last_message_id': 0,
    'send_later_messages': [],
    'send_later_dmmessages': [],
}

# 'users': [
#         {
#     'auth_user_id ': int,
#     'email': "string",
#     'password': "string",
#     'name_first': "string",
#     'name_last': "string",
#     "handle": "string",
#     "profile_img": "string",
#     'token': "string",
#     'session_id': int, #every time register or login, add a global session id into this lis
#     'is_global_owner': True/False,
#     'user_stats': {
#                 'channels_joined: [{num_channels_joined, time_stamp}],
#                 'dms_joined: [{num_dms_joined, time_stamp}], 
#                 'messages_sent: [{num_messages_sent, time_stamp}]}
#       }
#
#     ],
# 'channels': [
#         {
#     "channel_id": int,
#     "auth_user_id": [int],
#     "channel_name": "string",
#     "is_public": True or False,
#     "channel_user_id": [int],
#     "message": [dic],
#     "channel_creator": "string"
#         }
#     ],
# 'dm': [
# {
#   'dm_id': int,
#   'dm_creator_id': [int],
#   'dm_members_id': [int],
#   'dm_messages': [dic],
#   'dm_name': 'string'
#       }
#   ]
#
# 'workspace_stats':{'channels_exist':[{num_channels_exist, time_stamp}],
#                    'dms_exist':[{num_dms_exist, time_stamp}],
#                    'messages_exist':[{num_messages_exist, time_stamp}] }
#
#

# YOU SHOULD MODIFY THIS OBJECT ABOVE

# YOU ARE ALLOWED TO CHANGE THE BELOW IF YOU WISH
 

class Datastore:
    def __init__(self):
        self.__store = initial_object
 
    def get(self):
        return self.__store

    def reset(self):
        self.__store['users'] = []
        self.__store['channels'] = []
        self.__store['dm'] = []
        self.__store['total_users'] = 0
        self.__store['total_dm'] = 0
        self.__store['recent_last_message_id'] = 0
        self.__store['send_later_messages'] = []
        self.__store['send_later_dmmessages'] = []
        self.__store['standups'] = []
        self.__store['workspace_stats']['channels_exist'].clear()
        self.__store['workspace_stats']['dms_exist'].clear()
        self.__store['workspace_stats']['messages_exist'].clear() 
 
    def set(self, store):
        if not isinstance(store, dict):
            raise TypeError('store must be of type dictionary')
        self.__store = store


print('Loading Datastore...')

global data_store
data_store = Datastore()
