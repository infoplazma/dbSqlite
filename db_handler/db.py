import settings
from typing import Dict, List, Tuple
from loguru import logger

import sqlite3


conn = sqlite3.connect(settings.DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
logger.info(f"PRAGMA foreign_keys = ON")
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def insert_many(table: str, column_values_list: List[Dict]):
    columns = ', '.join(column_values_list[0].keys())
    values = [tuple(column_values.values()) for column_values in column_values_list]
    placeholders = ", ".join("?" * len(column_values_list[0].keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def fetchall(table: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result


def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    cursor.execute(f"delete from {table} where id={row_id}")
    conn.commit()


def get_cursor():
    return cursor


def _init_db():
    """Инициализирует БД"""
    with open(settings.DB_SCRIPT_PATH, "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
    logger.info(f"new db has been created '{settings.DB_PATH}'")


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='user'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
