# Will be changed to channelmgmt.py prior to deployment

from sopel import module
import sqlite3

@module.require_admin("Permission Denied")
@module.commands('addop')
def insertUser(bot, trigger):
    args = trigger.group(2).split(" ")
    nick = args[0]
    channel = args[1]
    try:
        sqliteConnection = sqlite3.connect("/path/to/db")
        cursor = sqliteConnection.cursor()
        sqlite_select_query = "SELECT * from chanops where nick='" + nick + "' and channel='" + channel + "'"
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        if len(records) > 0:
            bot.say(target + ' Entry already exists.')
            cursor.close()
            return
    except sqlite3.Error as error:
        bot.say("An error occured")
        print("Failed to read data from sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
    try:
        sqliteConnection = sqlite3.connect('/path/to/db')
        cursor = sqliteConnection.cursor()
        sqlite_insert_query = "INSERT INTO chanops(nick, channel) VALUES ('" + nick + "','" + channel + "')"
        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        bot.say("User inserted successfully")
        cursor.close
    except sqlite3.Error as error:
        bot.say("An error occured")
        print("Failed to insert data into sqlite table", error)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()
