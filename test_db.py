from data.db_manager import DBManager

db = DBManager()

print(
    db.get_random_word()
)

db.close()