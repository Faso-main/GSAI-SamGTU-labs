import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from BD.fun import Sql_functions
from BD.models import Base

# Убедитесь, что каталог для базы данных существует
db_directory = 'DataBase'
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Создание URL соединения с базой данных
db_path = os.path.join(db_directory, 'QuestAnswer.db')
engine = sa.create_engine(f"sqlite:///{db_path}")
print(engine)

# Создаем таблицу в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

q = 'asasaйцуйqwqw'
a = 'asasaуйцуйqwqwqwqweqwqwq'

# Добавление данных и получение всех данных
Sql_functions.add_if_not_exists(q, a, session)
all_data = Sql_functions.get_all_data(session)
z = {}
for record in all_data:
    z[record.question] = record.answer
    print(str(record))
print(z)