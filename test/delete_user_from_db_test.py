from db_handler import handler
from fill_data_to_db import FROM_USER_ID


print(handler.get_user_by_from_user_id(FROM_USER_ID))
print(handler.get_user_id(FROM_USER_ID))
handler.delete_user_by_from_user_id(FROM_USER_ID)
print(handler.get_user_by_from_user_id(FROM_USER_ID))

