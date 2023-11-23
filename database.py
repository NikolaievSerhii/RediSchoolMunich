import psycopg2
import logging as log
import static as st

import numpy
from psycopg2.extensions import register_adapter, AsIs
def addapt_numpy_float64(numpy_float64):
    return AsIs(numpy_float64)
def addapt_numpy_int64(numpy_int64):
    return AsIs(numpy_int64)
register_adapter(numpy.float64, addapt_numpy_float64)
register_adapter(numpy.int64, addapt_numpy_int64)

class Database:
    _instance = None

    def __init__(self):
        self._fl_con = False

    # Инициализация класса, установка настроек
    def init(self, set_json):
        self.id     = st.json_param(set_json, 'ip', '')
        self.port   = st.json_param(set_json, 'port', '')
        self.dbname = st.json_param(set_json, 'dbname', '')
        self.user   = st.json_param(set_json, 'dbuser', '')
        self.dbpass = st.json_param(set_json, 'dbpass', '')

    # Инициализация. что бы создавался только 1 экземпляр
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            # If the instance doesn't exist, create it
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    # Соединится с базой данніх
    def connect(self):
        if (not self._fl_con):
            try:
                # пытаемся подключиться к базе данных
                self.conn = psycopg2.connect(dbname=self.dbname , user=self.user , password=self.dbpass, host=self.id, port = self.port)
                self._fl_con = True
                log.error("Database connect")
            except:
                # в случае сбоя подключения будет выведено сообщение в STDOUT
                log.error("Can`t establish connection to database")

    # Отключится от базы данных
    def close(self):
        if self._fl_con:
            self.conn.close()
            self._fl_con = False
            log.error("Database close")

    # Выполнить запрос и вернуть результат
    def query(self, sql):
        if (not self._fl_con):
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql)
        all_users = cursor.fetchall()
        cursor.close()  # закрываем курсор
        return all_users

    # Выполнить запрос без возвращение результата
    def query_not_result(self, sql, params):
        try:
            if (not self._fl_con):
                self.connect()
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()
        except Exception as inst:
            log.error("Sql execute = " + sql)
            log.error(inst)
        finally:
            cursor.close()  # закрываем курсор
