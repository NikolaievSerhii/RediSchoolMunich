# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import logging as log
import file_find as ff
import time
import json
import database as db
import static as st
import webserver as ws
from threading import Thread

# Запуск webservers, отдельная функция что бы можно было запустить в отдельном потоке
def ws_start(ip, port):
    webServer = ws.HTTPServer((ip, port), ws.MyServer)
    print("Server started http://%s:%s" % (ip, port))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass


def start():
    # Start alle classes
    log.info("Start.")
    data = ''

    #Читаем настройки с файла
    try:
        with open("settings.json", "r") as read_file:
            data = json.load(read_file)
    except:
        log.error("Config file not found")

    if data:
        # Created Webservers from interface
        t = Thread(target=ws_start, args=('127.0.0.1',8014))
        t.daemon = True
        t.start()

        # Start find files
        period = st.json_param(data, 'time_sek', 60)
        directory = st.json_param(data, 'directory', '')

        #Инициализация базы
        base = db.Database()
        base.init(data['db'])

        #Запускаем поиск и обработку файлов
        files = ff.file_fin(directory)
        timing = time.time()
        # Start вечного цикла
        while 1:
            # Выполнять каждые n sek
            if time.time() - timing > period:
                timing = time.time()
                files.find()
    else:
        log.error("Config file Error")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Устанавливаем параметрі логирования
    log.basicConfig(
        filename='login.log',
        level=log.INFO,
        format='%(asctime)s %(levelname)s | Line: %(lineno)d |  %(module)s | %(message)s'
    )
    start()

