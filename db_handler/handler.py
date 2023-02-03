import numpy as np
from typing import Dict, NamedTuple, List
import datetime
import pytz
from db_handler import db


class User(NamedTuple):
    created: str
    from_user_id: int
    session_id: str


class Complaint(NamedTuple):
    name: str
    user_id: int


class Symptom(NamedTuple):
    name: str
    value: str
    user_id: int


class Conclusion(NamedTuple):
    diagnosis: str
    diagnosis_proba: float
    conclusion: str
    conclusion_proba: float
    is_true_predicted: bool
    user_id: int


def add_user(from_user_id: int, session_id: str) -> User:
    user = User(_get_now_formatted(), from_user_id, session_id)
    delete_user_by_from_user_id(user.from_user_id)
    db.insert("user", dict(user._asdict()))
    return user


def get_user_by_from_user_id(from_user_id: int) -> List:
    res = db.cursor.execute(f"SELECT * FROM user WHERE from_user_id='{from_user_id}'")
    return res.fetchone()


def get_user_id(from_user_id: int) -> int:
    result = get_user_by_from_user_id(from_user_id)
    return result[0] if result else None


def delete_user_by_from_user_id(from_user_id: int):
    db.cursor.execute(f"DELETE FROM user WHERE from_user_id='{from_user_id}'")
    db.conn.commit()


def add_complaints(from_user_id: int, complaint_names: List[str]):
    complaints_ = [dict(Complaint(name, get_user_id(from_user_id))._asdict()) for name in complaint_names]
    db.insert_many("complaint", complaints_)


def add_symptoms(from_user_id: int, symptoms: Dict[str, str | float]):
    symptoms_ = {k: str(v) for k, v in symptoms.items()}
    symptoms_ = [dict(Symptom(key, value, get_user_id(from_user_id))._asdict()) for key, value in symptoms_.items()]
    db.insert_many("symptom", symptoms_)


def add_conclusion(from_user_id: int,
                   diagnosis: str,
                   diagnosis_proba: float,
                   conclusion: str,
                   conclusion_proba: float,
                   is_true_predicted: bool):

    conclusion_ = dict(Conclusion(diagnosis,
                                  diagnosis_proba,
                                  conclusion,
                                  conclusion_proba,
                                  is_true_predicted,
                                  get_user_id(from_user_id)
                                  )._asdict())
    db.insert("conclusion", conclusion_)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime(timezone: str = None) -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом временной зоны, default Madrid."""
    if timezone is not None:
        tz = pytz.timezone(timezone)
    else:
        tz = pytz.timezone("Europe/Madrid")
    now = datetime.datetime.now(tz)
    return now
