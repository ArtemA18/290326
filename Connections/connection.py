from peewee import *

def connect():
    try: # удачная попытка
        database = MySQLDatabase(
            'helpdeskpractice',
            user='Tema',
            password='111111',
            host='10.11.118',
            port= 3306
        )
        return database
    except : # Неудачная попытка
        return None

if __name__ ==  "__main__":
    print(connect().connect())