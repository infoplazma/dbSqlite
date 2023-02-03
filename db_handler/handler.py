import numpy as np
from typing import Dict, NamedTuple, List, Tuple
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


def add_complaints(from_user_id: int, complaint_names: List[str]):
    complaints_ = [dict(Complaint(name, _get_user_id(from_user_id))._asdict()) for name in complaint_names]
    db.insert_many("complaint", complaints_)


def add_symptoms(from_user_id: int, symptoms: Dict[str, str | float]):
    symptoms_ = {k: str(v) for k, v in symptoms.items()}
    symptoms_ = [dict(Symptom(key, value, _get_user_id(from_user_id))._asdict()) for key, value in symptoms_.items()]
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
                                  _get_user_id(from_user_id)
                                  )._asdict())
    db.insert("conclusion", conclusion_)


def fetch_complaints(from_user_id: int) -> Tuple[str]:
    user_id = _get_user_id(from_user_id)
    db.cursor.execute(f"SELECT name FROM complaint WHERE user_id='{user_id}'")
    rows = db.cursor.fetchall()
    if rows:
        return tuple([row[0] for row in rows])
    return None


def fetch_symptoms(from_user_id: int) -> Tuple[Dict[str, str]]:
    user_id = _get_user_id(from_user_id)
    db.cursor.execute(f"SELECT name, value FROM symptom WHERE user_id='{user_id}'")
    rows = db.cursor.fetchall()
    if rows:
        return dict(rows)
    return None


def fetch_conclusion(from_user_id: int) -> Conclusion:
    user_id = _get_user_id(from_user_id)
    db.cursor.execute(f"SELECT * FROM conclusion WHERE user_id='{user_id}'")
    rows = db.cursor.fetchall()
    if rows:
        return Conclusion(*(list(rows[0])[1:-1] + [from_user_id]))
    return None


def get_user_by_from_user_id(from_user_id: int) -> List:
    db.cursor.execute(f"SELECT * FROM user WHERE from_user_id='{from_user_id}'")
    return db.cursor.fetchone()


def delete_user_by_from_user_id(from_user_id: int):
    db.cursor.execute(f"DELETE FROM user WHERE from_user_id='{from_user_id}'")
    db.conn.commit()


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


def _get_user_id(from_user_id: int) -> int:
    result = get_user_by_from_user_id(from_user_id)
    return result[0] if result else None
