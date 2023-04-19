import sqlite3

GET_USER = """
    select user_id, username, chat_id from users where user_id = %s
"""

CREATE_USER = """
    insert into users (user_id, username, chat_id) values (?, ?, ?)
"""


# with sqlite3.connect("users.db") as db:
#     cursor = db.cursor()
#     create_query = """
#         create table if not exists users (
#             user_id int primary key,
#             username text,
#             chat_id int
#         )
#     """
#     cursor.execute(create_query)
#     cursor.execute("""insert into users (user_id, username, chat_id) values (1, 'clatta', 123);""")

# conn = sqlite3.connect("users.db")
#
# create_query = """
#         create table if not exists users (
#             user_id int primary key,
#             username text,
#             chat_id int
#         )
#     """
#
# conn.execute(create_query)
#
# conn.execute("""insert into users (user_id, username, chat_id) values (1, 'clatta', 123);""")
#
# conn.commit()

class SQLiteClient:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False)

    def execute_command(self, command: str, params: tuple):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("You need to create connection to database.")

    def execute_select_command(self, command: str):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError("You need to create connection to database.")


class UserActioner:
    GET_USER = """
        select user_id, username, chat_id from users where user_id = %s
    """

    CREATE_USER = """
        insert into users (user_id, username, chat_id) values (?, ?, ?)
    """

    def __init__(self, database_client: SQLiteClient):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER % user_id)
        return user[0] if user else user

    def create_user(self, user_id: int, username: str, chat_id: int):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id))


# sqlite_client = SQLiteClient("users.db")
# sqlite_client.create_conn()
# print(sqlite_client.execute_select_command(GET_USER % 1))
# user_actioner = UserActioner(SQLiteClient("users.db"))
# user_actioner.setup()
# user = user_actioner.get_user('2')
# print(user)
# user_2 = {"user_id": 3, "username": 'Aptyp', "chat_id": 213}
# user_actioner.create_user(**user_2)
