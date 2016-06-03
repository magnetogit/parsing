import MySQLdb as mysql
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWD
import json
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def init():
    """Инициализирует базу данных со всеми необходимыми таблицами
    Если база данных с именем DB_NAME уже существует то будет ошибка"""

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD)

    cursor = conn.cursor()

    sql_code = "CREATE DATABASE IF NOT EXISTS {0}; USE {0}".format(DB_NAME)

    cursor.execute(sql_code)

    with open(os.path.join(DIRNAME, "mysql_create.sql"), "r") as f:

        sql_init_code = f.read()

        cursor.execute(sql_init_code)

        cursor.close()

        conn.close()

        print("База данных успешно инициализирована")

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


def get_bookmakers():

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "SELECT * FROM bookmakers"

    cursor.execute(sql_code)

    res = cursor.fetchall()

    cursor.close()

    conn.close()

    return res


def create_sports(sports):

    conn = mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, db=DB_NAME)

    cursor = conn.cursor()

    sql_code = "INSERT INTO sports (`Name`) VALUES (%s)"

    cursor.executemany(sql_code, [(sport,) for sport in sports])

    conn.commit()

    conn.close()

    print("Добавлены новые виды спорта")


def create_sport_names(sport_names, bookmaker_id):
    return None


def __load_init_sports():
    with open(os.path.join(DIRNAME, "sports_create.json")) as f:
        text = f.read()
        return json.loads(text)
