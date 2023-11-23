import logging as log
import pandas as pd
import database as db
import static as st


class file_fin:
    #init
    def __init__(self, directory):
        self.directory = directory
        self.files = st.all_files(self.directory, [])

        #self.read_file(self.files[0])

    #Сохранить результат в базу
    def save_result(self, new_df, file_name, errors):
        # Инициализация базы
        base = db.Database()
        base.connect()
        sql = ('insert into file_result (transaction_amount, use_change, change_amount, payment_amount,'
               '  pament_fee, files, terminal_id, errors) values (%s, %s, %s, %s, %s, %s, %s, %s)')

        colums = new_df.index
        colums_err = errors.index
        i = 0
        j = 0

        # Пройдемся по результатам
        for el in list(new_df.values):
            params = el.tolist()
            params.append(file_name)
            params.append(colums[i])
            # Проверяем запись на ошибку
            if (j + 1) <= len(colums_err) and colums_err[j] == colums[i]:
                params.append("Error")
                j += 1
            else:
                params.append("OK")
            i += 1
            # Сохраняем результат
            base.query_not_result(sql, params)

        #Закрываем базу
        base.close()


    def read_file(self, file_name):
        try:
            # Распарсим файл
            data = pd.read_csv(file_name,  sep=';')
            # Простая проверка на правильній файл, можно потом дописать проверку на название полей
            if len(data.columns) == 30:
                cash = data.groupby('terminal_id')['transaction_amount'].sum()
                use_change = data.groupby('terminal_id')['use_change'].sum()
                change_amount = data.groupby('terminal_id')['change_amount'].sum()
                payment_amount = data.groupby('terminal_id')['payment_amount'].sum()
                pament_fee = data.groupby('terminal_id')['pament_fee'].sum()
                new_df = pd.merge(cash, use_change, how='inner', left_on='terminal_id', right_index=True)
                new_df = pd.merge(new_df, change_amount, how='inner', left_on='terminal_id', right_index=True)
                new_df = pd.merge(new_df, payment_amount, how='inner', left_on='terminal_id', right_index=True)
                new_df = pd.merge(new_df, pament_fee, how='inner', left_on='terminal_id', right_index=True)
                falls = new_df.query(" (transaction_amount + use_change) != (change_amount + payment_amount + pament_fee)")
                # Запишем в лог если есть ошибки
                if (len(falls)> 0):
                    log.error("Error data calculation")
                self.save_result(new_df, file_name, falls)
        except:
            log.error("Error read file")

    #find new file
    def find(self):
        log.info("Next round")
        # Поиск новіх файлов
        for el in st.all_files(self.directory, self.files):
            #Проверим данные в файле и запишем их в базу
            self.read_file(el)
            #Зпомним файл, что его уже обрабатывали
            self.files.append(el)
            log.info(str("New file = ") + str(el))
