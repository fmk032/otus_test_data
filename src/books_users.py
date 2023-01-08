import json
import itertools
from csv import DictReader
from data import USERS_FILE_PATH
from data import BOOKS_FILE_PATH
from data import REFERENCE_FILE_PATH
from data import RESULT_FILE_PATH

# Извлечение из шаблона reference.json ключей для user и book
with open(REFERENCE_FILE_PATH, "r") as f:
    reference = json.loads(f.read())[0]

ref_book_keys = reference['books'][0].keys()    # Ключи для book
reference.pop('books')
ref_user_keys = reference.keys()    # Ключи для user


with open(USERS_FILE_PATH, "r") as f:
    users = json.loads(f.read())

# Преобразование users.json в список словарей-юзеров по шаблону reference.json с пустым books
users_ = []
for user in users:
    user_ = {a: user[a] for a in ref_user_keys}
    user_['books'] = []
    users_.append(user_)

# Преобразование books.csv в список словарей-книг по шаблону reference.json
with open(BOOKS_FILE_PATH, "r") as f:
    books = DictReader(f)
    books_ = []
    for row in books:
        book_ = {a: row[a.title()] for a in ref_book_keys}
        books_.append(book_)

# Распределение книг по юзерам
users_cycle = itertools.cycle(users_)
i = 0
for user in users_cycle:
    user['books'].append(books_[i])
    i += 1
    if i == len(books_):
        break

# Преобразование итогового списка словарей в result.json
with open(RESULT_FILE_PATH, "w") as f:
    json.dump(users_, f, indent=4)
