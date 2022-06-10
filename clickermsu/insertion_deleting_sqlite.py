"""Module of Telegram API interaction."""

import sqlite3
import telebot
from .restricted_area import token_crypto
import io
import json
import urllib
import ssl


API_TOKEN = token_crypto

bot = telebot.TeleBot(API_TOKEN)

global_data_chat = 721641425
global_data_message = 430
global_file_id = "BQACAgIAAxkDAAIBrmKbrXkKo_0d3Nbo-Cmr1Zpy0_fWAALzGwACYDDgSFN_tbcimLj3JAQ"


def get_data():
    """Get users' data from server."""
    # Very strange procedure, but it is necessary, in order to get new
    # file id from message (API doesn't support message return by its
    # id withount such manipulations)
    try:
        global_file_id = (bot.edit_message_caption(chat_id=global_data_chat,
                          message_id=global_data_message, caption=str("Current database"))).document.file_id
    except Exception:
        global_file_id = (bot.edit_message_caption(chat_id=global_data_chat,
                          message_id=global_data_message, caption=str("Current Database"))).document.file_id

    file_data = bot.get_file(global_file_id)
    print("ok")
    # Получаем файл по url
    file_data_path = file_data.file_path
    print(file_data_path)
    print("ok")
    file_url_data = bot.get_file_url(global_file_id)
    print("ok")
    print(file_url_data)
    # Считываем данные с файла
    context = ssl._create_unverified_context()
    with urllib.request.urlopen(file_url_data, context=context) as f:
        json_file = f.read().decode('utf-8')
    print("ok")

    # Переводим данные из json в словарь и возвращаем
    return json.loads(json_file)


@bot.message_handler(content_types=["document", "video", "audio"])
def handle_files(message):
    """Debugging function."""
    document_id = message.document.file_id
    file_info = bot.get_file(document_id)
    print(f'http://api.telegram.org/file/bot{token_crypto}/{file_info.file_path}')
    bot.send_message(message.chat.id, document_id)


@bot.message_handler(commands=["update"])
def update_data(messg):
    """Try to updtae users' data on server."""
    # server case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    # data = get_data()
    # cursor.executemany("INSERT INTO users VALUES (?,?,?)", data)
    # connect.commit()

    # local case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    sql = "SELECT * FROM login_id "
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(data)
    try:
        # Обновляем  наш файл с данными
        edit_file = bot.edit_message_media(chat_id=global_data_chat, message_id=global_data_message,
                                           media=telebot.types.InputMediaDocument(io.StringIO(str_data)))
        global global_file_id
        global_file_id = edit_file.document.file_id

    except Exception as ex:
        print(ex)


@bot.message_handler(commands=["save"])
def save_data(messg):
    """Use this function for initial message for bot-server."""
    # server case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    # data = get_data()
    # cursor.executemany("INSERT INTO users VALUES (?,?,?)", data)
    # connect.commit()

    # local case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    sql = "SELECT * FROM login_id "
    cursor.execute(sql)
    data = cursor.fetchall()
    str_data = json.dumps(data)
    send_document = bot.send_document(messg.chat.id, io.StringIO(str_data))
    bot.send_message(messg.chat.id, 'admin_id = {}'.format(messg.chat.id))
    bot.send_message(messg.chat.id, 'config_id = {}'.format(messg.message_id+1))
    admin_id = messg.chat.id
    config_id = messg.message_id+1
    global global_data_chat
    global global_data_message
    global global_file_id
    global_data_chat = messg.chat.id
    global_data_message = messg.message_id+1
    global_file_id = send_document.document.file_id
    bot.send_message(messg.chat.id, 'file_id = {}'.format(global_file_id))

    sql = "SELECT * FROM login_id "
    cursor.execute(sql)
    data = cursor.fetchall()
    try:
        str_data = json.dumps(data)
        bot.edit_message_media(chat_id=admin_id, message_id=config_id,
                               media=telebot.types.InputMediaDocument(io.StringIO(str_data)))

    except Exception as ex:
        print(ex)


@bot.message_handler(commands=["register"])
def register(messg, username_in: str = None, password_in: str = None, coins: int = None) -> list:
    """Try to registrate new user in database.

        params:
            username_in - user name
            password_in - user password
            coins - user coins

        returns:
            top 10 table
            user's place
    """
    # server case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    try:
        cursor.execute("DROP TABLE login_id;")
    except Exception:
        pass
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    data = get_data()
    cursor.executemany("INSERT INTO login_id VALUES (?,?,?)", data)
    connect.commit()

    # local case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    # connect.commit()

    # регистрация
    print("Регистрация: ")
    if username_in is None or username_in == "":
        return 1, None

    # includes case when registration initiated with telegram app
    # try:
    #     user_id = [messg.chat.id]
    # except Exception:
    #     user_id = [random.randint(0, 9999)]

    cursor.execute("SELECT username FROM login_id WHERE username = ?", (username_in,))
    name_out = cursor.fetchone()
    if name_out is None:
        if password_in is None or password_in == "":
            return 2, None
        cursor.execute("INSERT INTO login_id (id, username, password) VALUES (?, ?, ?);", (0, username_in, password_in))
        connect.commit()
        print("Done")
        update_data(None)
        cursor.execute("SELECT id, username FROM login_id ORDER BY id DESC LIMIT 10;")
        results_10 = cursor.fetchall()
        cursor.execute("SELECT id, username, ROW_NUMBER() over(ORDER BY id DESC) AS Row FROM login_id;")

        user_place = cursor.fetchall()
        user_place = [i for i in user_place if i[1] == username_in]
        return results_10, user_place
    else:
        print("User with same also exists...")
        return 3, None


@bot.message_handler(commands=["update_signed"])
def update_signed(messg, username_in: str = None, coins: int = None) -> None:
    """Try to update data of sighned user.

        params:
            username_in - user name
            password_in - user password
            coins - user coins
    """
    # server case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    try:
        cursor.execute("DROP TABLE login_id;")
    except Exception:
        pass
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    data = get_data()
    cursor.executemany("INSERT INTO login_id VALUES (?,?,?)", data)
    connect.commit()

    # local case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    # connect.commit()

    cursor.execute("SELECT id, username, password FROM login_id WHERE username = (?)", (username_in,))
    score = cursor.fetchone()
    score_out = max(score[0], coins)
    print(score_out)

    # updating
    cursor.execute("DELETE FROM login_id WHERE username = (?)", (username_in,))
    cursor.executemany("INSERT INTO login_id VALUES (?,?,?)", [[int(score_out), str(score[1]), str(score[2])]])
    connect.commit()
    update_data(None)
    return


@bot.message_handler(commands=["sighin"])
def sighin(messg, username_in: str = None, password_in: str = None, coins: int = None) -> list:
    """Try to log in user in database.

        params:
            username_in - user name
            password_in - user password
            coins - user coins

        returns:
            top 10 table
            user's place
            score to implement
    """
    # server case
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    try:
        cursor.execute("DROP TABLE login_id;")
    except Exception:
        pass
    cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    data = get_data()
    cursor.executemany("INSERT INTO login_id VALUES (?,?,?)", data)
    connect.commit()

    # local case
    # connect = sqlite3.connect('users.db')
    # cursor = connect.cursor()
    # cursor.execute("CREATE TABLE IF NOT EXISTS login_id (id INTEGER, username TEXT, password TEXT);")
    # connect.commit()

    # вход с логином и паролем
    if username_in is None or username_in == "":
        # User didn't specify username
        return 4, None, coins
        username_in = str(input("username: "))
    cursor.execute("SELECT username, password FROM login_id WHERE username = ?", (username_in,))
    name_out = cursor.fetchone()
    if name_out is None:
        return 1, None, coins
    else:
        if password_in is None or password_in == "":
            # Пароль не введён
            return 2, None, coins

        if name_out[1] == password_in:
            # Вы успешно вошли
            cursor.execute("SELECT id FROM login_id WHERE username = (?)", (username_in,))
            score = cursor.fetchone()
            score_out = max(score[0], coins)
            print(score_out)

            # updating
            cursor.execute("DELETE FROM login_id WHERE username = (?)", (username_in,))
            cursor.executemany("INSERT INTO login_id VALUES (?,?,?)",
                               [[int(score_out), str(username_in), str(password_in)]])
            connect.commit()
            update_data(None)
            # table forming
            cursor.execute("SELECT id, username FROM login_id ORDER BY id DESC LIMIT 10;")
            results_10 = cursor.fetchall()
            cursor.execute("SELECT id, username, ROW_NUMBER() over(ORDER BY id DESC) AS Row FROM login_id;")

            user_place = cursor.fetchall()
            user_place = [i for i in user_place if i[1] == username_in]
            return results_10, user_place, score_out
        else:
            # Wrong password
            return 3, None, coins


@bot.message_handler(commands=["find"])
def start(messg):
    """Try to find message from user(DEBUG)."""
    bot.send_message(messg.chat.id, "Finding...")


def listener(messages):
    """Try to DEBUG."""
    print(type(messages[0].de_json))


@bot.message_handler(commands=["delete"])
def delete(messg):
    """Try to delete user in database."""
    bot.send_message(messg.chat.id, "Deleting")
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    people_id = messg.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    people_id_data = cursor.fetchone()

    if people_id_data is None:
        bot.send_message(messg.chat.id, "NO SUCH USER IN DATABASE")
    else:
        cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
        bot.send_message(messg.chat.id, f"Deleted user {people_id}")
        connect.commit()

    connect.commit()

# bot.set_update_listener(listener)
# bot.polling()
