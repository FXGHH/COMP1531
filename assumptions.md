REPAIRED - If channels_create_v1 is given a invalid auth_user_id which is not in the data_store, it should return an InputError.(which means we have to write a check if the auth_user_id is in the ["users"] dic)-REPAIRED

All input types are equal to the information of table, and don't recerive a empty input.

REPAIRED - In 6.2 Interface channel_join_v1 and channel_invite_v1, we not sure The Return Type, it shows a "{}", so in these two functions we just return a empty {}. it is no influnce on the result of these two functions, because they change the informations of "initial_object" in data_store - REPAIRED

when after user remove, there are no same first and last name register, so it means no old handle beused, all handle only can be once.
