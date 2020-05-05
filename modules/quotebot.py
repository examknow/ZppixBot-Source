from sopel import module
import sqlite3

module.commands('pickquote')
def pickQuote(bot, trigger):
  conn = sqlite3.connect('/data/project/zppixbot/.sopel/plugins/quotes.db')
  cursor = conn.execute("SELECT * from quotes ORDER BY RANDOM() LIMIT 1;")
     quote = row[0]
     author = row[1]
  for row in cursor:
     bot.say(quote + " - " + author)
     conn.close()
