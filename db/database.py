import json
import os

import MySQLdb as mysql
import pandas as pd
from datetime import datetime as datetime

from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def init():
    """Инициализирует базу данных со всеми необходимыми таблицами
    Если база данных с именем DB_NAME уже существует то будет ошибка"""

    def __load_init_sports():
        with open(os.path.join(DIRNAME, "sports_create.json")) as f:
            text = f.read()
            return json.loads(text)

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)

    cursor = conn.cursor()

    sql_code = "CREATE DATABASE IF NOT EXISTS {0}".format(DB_NAME)

    cursor.execute(sql_code)

    cursor.close()

    conn.close()

    print("База данных успешно создана")

    with open(os.path.join(DIRNAME, "mysql_create.sql"), "r") as f:
        sql_init_code = f.read()

        conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

        cursor = conn.cursor()

        cursor.execute(sql_init_code)

        cursor.close()

        conn.close()

        print("Таблицы успешно созданы")

    create_sports(__load_init_sports())


def create_bookmaker(bookmaker_name):
    """Создает нового букмекера"""
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = 'INSERT INTO bookmakers (Name) VALUES ("{0}")'.format(bookmaker_name)

    try:
        cursor.execute(sql_code)
        conn.commit()
        print("{0} контора успешно создана".format(bookmaker_name))
    except mysql.IntegrityError as err:
        print(err)

    cursor.close()

    conn.close()


def create_sports(sports):
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO sports (`Name`) VALUES (%s)"

    cursor.executemany(sql_code, [(sport,) for sport in sports])

    conn.commit()

    conn.close()

    print("Добавлены новые виды спорта")


def create_participants(names_df):

    names_df.columns = ["name"]
    names_list = names_df["name"].tolist()
    par = [(el,) for el in names_list]

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO participants (`Name`) VALUES (%s)"

    cursor.executemany(sql_code, par)

    conn.commit()

    df = pd.read_sql("SELECT * FROM participants WHERE name in %(names)s", con=conn, params={"names": names_list})

    conn.close()

    return df


def create_participant_names(names_df, bookmaker_id):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    names_df.columns = ["participant", "name"]
    names_df["bookmaker"] = bookmaker_id

    names_df.to_sql("participantnames", con=conn, if_exists="append", flavor="mysql", index=False)

    names_df = names_df.drop("bookmaker", 1)

    names_df.columns = ["id", "name"]

    return names_df

    conn.close()


def create_handicaps(handicaps_df):

    handicaps_df["oddsdate"] = datetime.now()

    if "score" in handicaps_df:
        handicaps_df = handicaps_df.drop(["score"], 1)

    if "league" in handicaps_df:
        handicaps_df = handicaps_df.drop(["league"], 1)

    if "sport" in handicaps_df:
        handicaps_df = handicaps_df.drop(["sport"], 1)

    if "livedate" in handicaps_df:
        handicaps_df = handicaps_df.drop(["livedate"], 1)

    if "gamedate" in handicaps_df:
        handicaps_df = handicaps_df.drop(["gamedate"], 1)

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)
    handicaps_df.to_sql("handicap", con=conn, if_exists="append", flavor="mysql", index=False)
    conn.close()


def get_bookmakers():
    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "SELECT * FROM bookmakers"

    cursor.execute(sql_code)

    res = cursor.fetchall()

    cursor.close()

    conn.close()

    return res





