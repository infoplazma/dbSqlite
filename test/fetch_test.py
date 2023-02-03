from db_handler import handler
from fill_data_to_db import FROM_USER_ID


res = handler.fetch_complaints(FROM_USER_ID)
print(res)

res = handler.fetch_symptoms(FROM_USER_ID)
print(res)

res = handler.fetch_conclusion(FROM_USER_ID)
print(res)
