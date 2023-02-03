import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "data")
DB_FILE_NAME = "mke-bot.data"
DB_PATH = os.path.join(DB_DIR, DB_FILE_NAME)

DB_SCRIPT_FILE_NAME = "data/db_script.txt"
DB_SCRIPT_PATH = os.path.join(BASE_DIR, DB_SCRIPT_FILE_NAME)

DATA_DIR = r"D:\PycharmProjects\MedicalConsultant\data"
CONDITION_OF_SICK_CHILD_FILE_PATH = os.path.join(DATA_DIR, "condition of a sick child.joblib")
