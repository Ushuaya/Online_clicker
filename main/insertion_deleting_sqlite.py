import sqlite3
from matplotlib.pyplot import text
import pandas
#from sqlalchemy import create_engine
import telebot
from restricted_area import token_crypto


# engine = create_engine('sqlite://', echo=False)

# df = pandas.read_csv(csvfile)
# df.to_sql("MSK_test", con=engine, if_exists='append', index=False)
API_TOKEN = token_crypto

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands = ["start"])
def start(messg): 

    #cursor.execute("CREATE TABLE IF NOT EXISTS login_id(id INTEGER)") 
    #connect.commit() 
    people_id = messg.chat.id 
    # cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    # people_id_data = cursor.fetchone() 
    bot.send_message(messg.chat.id, "Type \"/find\" to start search of porch lock-code")

    # if people_id_data is None: 
    #     user_id = [messg.chat.id]
    #     cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
    #     connect.commit() 
    # else: 
    #     bot.send_message(messg.chat.id, "Уже есть такой")

@bot.message_handler(commands = ["find"])
def start(messg): 
    connect = sqlite3.connect('./DB/test.db')
    cursor = connect.cursor()




def listener(messages):  
    print(type(messages[0].de_json))
    #print(dir(messages[0].de_json))
    #print(messages[0].de_json())


bot.set_update_listener(listener)
bot.polling() 



# @bot.message_handler(commands = ["delete"])
# def delete(messg): 
#     connect = sqlite3.connect('users.db')
#     cursor = connect.cursor()

#     people_id = messg.chat.id 
#     cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
#     people_id_data = cursor.fetchone()
    
    

#     if people_id_data is None: 
#         bot.send_message(messg.chat.id, "NO SUCH USER IN DATABASE") 
#     else: 
#         cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
#         bot.send_message(messg.chat.id, f"Deleted user {people_id}")
#         connect.commit() 
    
#     connect.commit() 
