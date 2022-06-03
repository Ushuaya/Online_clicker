import sqlite3
import pandas
#from sqlalchemy import create_engine
import telebot


# engine = create_engine('sqlite://', echo=False)

# df = pandas.read_csv(csvfile)
# df.to_sql("MSK_test", con=engine, if_exists='append', index=False)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands = ["start"])
def start(messg): 
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS login_id(id INTEGER)") 

    connect.commit() 

    people_id = messg.chat.id 
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    people_id_data = cursor.fetchone() 

    if people_id_data is None: 
        user_id = [messg.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit() 
    else: 
        bot.send_message(messg.chat.id, "Уже есть такой")




@bot.message_handler(commands = ["delete"])
def delete(messg): 
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
 

bot.polling() 
