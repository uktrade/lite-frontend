
def save_user_info_to_session(session, data, user_profile):
    session["first_name"] = user_profile["first_name"]
    session["last_name"] = user_profile["last_name"]
    session["default_queue"] = data["default_queue"]
    session["user_token"] = data["token"]
    session["lite_api_user_id"] = data["lite_api_user_id"]
    session["email"] = user_profile["email"]
    session.save()
