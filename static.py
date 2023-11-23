import os

# Функции которые используються в разных модулях
def json_param(data, name, default):
    try:
        znach = data[name]
    except:
        znach = default
    return znach


def all_files(directory, sp_files):
    files = os.listdir(directory)
    new_spis = []
    for file in files:
        name = os.path.join(directory, file)
        if os.path.isdir(name):
            for el in all_files(name, sp_files):
                new_spis.append(el)
        elif os.path.isfile(name) and name not in sp_files:
            new_spis.append(name)
    return new_spis
