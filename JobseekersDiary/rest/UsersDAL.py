import MongoConnection


def add_new_user(user_name):
    users = MongoConnection.get_users_database()
    inserted_id = users.insert_one({"user_name": user_name}).inserted_id
    return inserted_id


def retrieve_user_id(user_name):
    users = MongoConnection.get_users_database()
    user_id = users.find_one({"user_name": user_name})
    return user_id['_id']
