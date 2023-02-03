import DATA
from pprint import pprint
from db_handler import handler


FROM_USER_ID = 5438181267#7777777777
SESSION_ID = "245d2d7f-5f90-49cd-94b7-c8e281b17fb3"


if __name__ == "__main__":
    sample = DATA.SAMPLE
    pprint(len(sample))
    # add user
    user = handler.add_user(from_user_id=FROM_USER_ID, session_id=SESSION_ID)
    # print(handler.get_user_by_from_user_id(FROM_USER_ID))

    handler.add_complaints(user.from_user_id, DATA.COMPLAINTS)
    handler.add_symptoms(user.from_user_id, DATA.SAMPLE)
    handler.add_conclusion(user.from_user_id, **DATA.CONCLUSION)

