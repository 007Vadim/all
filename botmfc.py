#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import random
import nltk
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.svm import LinearSVC


# In[2]:


BOT_CONFIG = {'failure_phrases': ['Нужно писать только название населенного пункта или номер дела, иначе я не смогу Вам помочь!']}


# In[3]:


def filter_text(text):
    text = text.lower()
    text = [c for c in text if c in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя- ']
    text = ''.join(text)
    return text
 
with open('C:/134/mfcal2.txt', encoding='utf-8') as f:
    content = f.read()
dialogues = [dialogue_line.split('\n') for dialogue_line in content.split('\n\n')]
 
questions = set()
qa_dataset = []  # [[q, a], ...]
 
for replicas in dialogues:
    if len(replicas) < 2:
        continue
 
    question, answer = replicas[:2]
    question = filter_text(question[2:])
    answer = answer[2:]
 
    if question and question not in questions:
        questions.add(question)
        qa_dataset.append([question, answer])

qa_by_word_dataset = {}  # {'word': [[q, a], ...]}
for question, answer in qa_dataset:
    words = question.split(' ')
    for word in words:
        if word not in qa_by_word_dataset:
            qa_by_word_dataset[word] = []
        qa_by_word_dataset[word].append((question, answer))

qa_by_word_dataset_filtered = {word: qa_list
                               for word, qa_list in qa_by_word_dataset.items()
                               if len(qa_list) < 1000}


# In[4]:


def generate_answer_by_text(text):
    text = filter_text(text)
    words = text.split(' ')
    qa = []
    for word in words:
        if word in qa_by_word_dataset_filtered:
            qa += qa_by_word_dataset_filtered[word]
    qa = list(set(qa))[:1000]

    results = []
    for question, answer in qa:
        dist = nltk.edit_distance(question, text)
        dist_percentage = dist / len(question)
        results.append([dist_percentage, question, answer])
    
    if results:
        dist_percentage, question, answer = min(results, key=lambda pair: pair[0])
        if dist_percentage < 0.3:
            return answer


# In[5]:


def get_failure_phrase():
    phrases = BOT_CONFIG['failure_phrases']
    return random.choice(phrases)


# In[6]:


stats = [0, 0, 0]


# In[7]:


def delo(answer):
    if answer.isdigit() == True:
            connection = create_connection('data_name', 'USER', password, 'IP', *port, client_encoding="utf-8")
            cur = connection.cursor()
            #delo = input("Введите номер " )
            cur.execute(f"SELECT delo.id_usl_sp as id, delo.cl as cl, delo.prich as pr, usl_sp.naz as naz FROM delo.delo left join uslugi.usl_sp on usl_sp.id = delo.id_usl_sp where delo.num = {answer}")
            rows = cur.fetchall()
            if rows == []:
                return ("Не найдено. Проверьте правильность внесения номера.")
            for row in rows:
                if row[1] == 2:
                    return ("**Услуга:** {} \n **Статус:** Закрыто с отказом - {}".format(row[3], row[2]))
                elif row[1] == 1:
                    return ("**Услуга:** {} \n **Статус:** Дело исполнено(Для получения подробной информации Вы можете обратиться в офисы или ТОСП Азовского района https://azovskiy.mfc61.ru/ или на телефон горячей линии 8(86342)6-24-81".format(row[3]))
                elif row[1] == 0:
                    return ("**Услуга:** {} \n **Статус:** Исполняется".format(row[3]))
            connection.close()


# In[8]:


def bot(question):
    # NLU
    #intent = get_intent(question)
    
    # Получение ответа
    answer = delo(question)
    if answer:
        stats[0] += 1
        return answer
    # Ищем готовый ответ
    #if intent:
     #   answer = get_answer_by_intent(intent)
      #  if answer:
       #     stats[0] += 1
        #    return answer
    
    # Генеруем подходящий по контексту ответ
    answer = generate_answer_by_text(question)
    if answer:
        stats[1] += 1
        return answer

    # Используем заглушку
    stats[2] += 1
    answer = get_failure_phrase()
    return answer


# In[9]:


import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port, client_encoding="utf-8"):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


# In[10]:





# In[ ]:





# In[11]:


#question = None
 
#while question not in ['exit', 'выход']:
 #   question = input()
  #  if question.isdigit() == True:
   #     cur = connection.cursor()
          #  delo = input("Введите номер " )
    #    cur.execute("select cl, prich from delo.delo where num = " + question)
     #   rows = cur.fetchall()
      #  for row in rows:
       #         if row[0] == 2:
        #            print("Закрыто с отказом", row[1])
         #       elif row[0] == 1:
          #          print ("Закрыто")
           #     elif row[0] == 0:
            #        print("Исполняется")
             #   elif isinstance(question, str):
        #answer = bot(question)
        #print(answer, stats)


# In[12]:


#get_ipython().system(' pip install python-telegram-bot')


# In[13]:


from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
 

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Здравствуйте! Я подскажу Вам адреса и телефоны МФЦ Азовского района в Вашем Сельском поселении. Напишите название населенного пункта. Если Вы обрашались ранее введите номер дела и узнаете статус.')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

    
def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    answer = bot(update.message.text)
    update.message.reply_text(answer)
    print(stats, update.message.chat.id, update.message.chat.first_name, update.message.chat.last_name, update.message.chat.username)
    print('-', update.message.text)
    print('-', answer)
    print()
    with open('C:/134/mfcstat.txt', 'a') as file:
        stat = [stats, update.message.text, answer, update.message.chat.first_name, update.message.chat.last_name, update.message.chat.username, update.message.chat.id]
        print(stat, '\n', file=file)

def main():
    """Start the bot."""
    updater = Updater("TOKEN, use_context=True)
 
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
 
    # Start the Bot
    updater.start_polling()
    updater.idle()


# In[ ]:


main()


# In[ ]:





# In[ ]:




