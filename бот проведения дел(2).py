#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import telebot, time
from telebot import util
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import psycopg2
from psycopg2 import OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
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

TOKEN = '1852723832:AAHfi5nOfcDYp7mgj27yARb8zCwHyfe6dNI'
bot = telebot.TeleBot(TOKEN, threaded=True)

SUMMA =()
USER=()


def user_id(message):
    global USER
    USER = message.chat.id
    return USER
def dela(user1, pasw, file):
    # путь к драйверу chrome
    driver = webdriver.Firefox(executable_path=r'C:/134/geckodriver.exe')
    #driver.implicitly_wait(5) # seconds

    #Открываем сайт
    driver.get('http://172.20.111.3')
    #Вход
    user = driver.find_element_by_class_name('select2-selection')
    user.send_keys(Keys.ENTER)
    login = driver.find_element_by_class_name('select2-search__field')
    login.send_keys(user1)
    login.send_keys(Keys.ENTER)
    password = driver.find_element_by_id('Password')
    password.send_keys(pasw)
    vh = driver.find_element_by_id('login')
    vh.click()
    time.sleep(1)
    commit = driver.find_element_by_id('enter')
    commit.click()
    #переход на страницу КАС
    driver.get('http://172.20.111.3/backofice.php?act=list_open&isStop=1')

    #Получаем список дел
    select = driver.find_element_by_name("datpreset")
    for option in select.find_elements_by_tag_name('option'):
        if option.text == 'за текущие сутки':
            option.click()
    select = driver.find_element_by_id('select2-selEvent-container').click()
    select2 = driver.find_element_by_id('select2-selEvent-results').click()
    s=[]
    for row in driver.find_elements_by_xpath('/html/body/div[1]/center/table/tbody/tr[3]/td/table/tbody/tr/td/div/table/tbody/tr/td[1]/div[2]/div/div[2]/table/tbody/tr/td[1]'):
        s.append(row.text)

    s = set(s)
    global SUMMA
    global USER
    SUMMA = (len(s)-1)
    print(USER, SUMMA)
    try:
        bot.send_message(USER, f'Количество дел - {SUMMA}')
    except:
        pass
    #bot.reply_to(message, f'Количество дел - {SUMMA}')
    x = 0

    start_time = datetime.now()
    try:
        for i in s:
            if i != '':
                driver.get('http://172.20.111.3/backofice.php?act=delo')
                try:
                    commit = driver.find_element_by_id('idDela')
                    commit.send_keys(i)
                except:
                    continue
                commit.send_keys(Keys.ENTER)
                time.sleep(3)
                ActionChains(driver).send_keys(Keys.END).perform()
                time.sleep(1)
                try:
                    plan = driver.find_element_by_name('formEtap')
                    plan.click()
                except:
                    continue
                ActionChains(driver).send_keys(Keys.END).perform()
                #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                ActionChains(driver).send_keys(Keys.END).perform()
                data = driver.find_element_by_xpath('//*[@title="текущая дата"]')
                data.click()
                save = driver.find_element_by_name('savEtap')
                save.click()
                time.sleep(1.5)
                try:
                    save1 = driver.find_element_by_xpath('//button[text()="Да"]')
                    save1.click()
                except:
                    continue
                    #print(data.text)
                time.sleep(2)
                x +=1
        end_time = datetime.now()
        print('Проведено ' + str(x) + ' дел!' ' Потрачено: {}'.format(end_time - start_time))
        bot.send_message(USER, 'Проведено ' + str(x) + ' дел!' ' Потрачено: {}'.format(end_time - start_time))
        driver.quit()
    except Exception as e:
        print(e)
            #pass
        end_time = datetime.now()
        print('Проведено ' + str(x) + ' дел!' ' Потрачено: {}'.format(end_time - start_time))
        bot.send_message(USER, 'Проведено ' + str(x) + ' дел!' ' Потрачено: {}'.format(end_time - start_time))
        driver.quit()
        #break
    finally:
        driver.quit()
    with open(f'C:/Users/мфц/PycharmProjects/делакас/{file}.xls', 'a') as file:
            #stat = [b, v, res]
            dat = str(datetime.now())
            print('Проведено ' + str(x) + ' дел!' ' Потрачено: {}'.format(end_time - start_time), dat, '\n', file=file)
            #bot.send_message(USER, 'Проведено ' + str(x) + ' дел!' ' Потрачено: {}'.format(end_time - start_time))
            #print (q, '\n', file=file)
            
@bot.message_handler(commands=['start'])
def sms(message):
    user = message.chat.id
    bot.send_message(user,
        f'Привет {message.chat.first_name}! Помогу провести дела за тебя. Выбери команду /help.')
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)

@bot.message_handler(commands=['help'])
def help(message):
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
    bot.reply_to(message,'''Список команд\n /gudz - Дела Гудзь\n /hangina - Дела Ханжиной
/chudnova - Дела Чудновой\n Количество новых дел\n /gudz new\n /hangina new\n /chudnova new\n
/adres - Информация из Росреестра по адресу\n /cadnum - Расширенная информация по кадастровому номеру
                 ''')

@bot.message_handler(commands=['foma'])
def foma(message):
    user_id(message)
    print(user_id(message), message.chat.first_name, message.chat.last_name)
    dela('глав', 2010, 'админ')
    
@bot.message_handler(commands=['gudz'])
def gudz(message):
    user_id(message)
    us=(1284787275)
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
    if message.text == '/gudz new':
        connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
        cur = connection.cursor()
        cur.execute('select count(id) as kol from site.bo_new_dela(297) where colplan = 0')
        s= cur.fetchone()[0]
        connection.close()
        bot.reply_to(message, f'Новых дел {s}')
    #print(user_id(message))
#     dela('гудз', 1245, 'гудзь')
    elif message.chat.id == us:
        dela('гудз', 1245, 'гудзь')
    else:
        bot.reply_to(message, 'Не нужно лезть в чужую работу')
        
@bot.message_handler(commands=['hangina'])
def hangina(message):
    user_id(message)
    us=(240099489)
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
    if message.text == '/hangina new':
        connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
        cur = connection.cursor()
        cur.execute('select count(id) as kol from site.bo_new_dela(296) where colplan = 0')
        s= cur.fetchone()[0]
        connection.close()
        bot.reply_to(message, f'Новых дел {s}')
    #print(user_id(message))
    elif message.chat.id == us:
        dela('ханж', 1880, 'ханжина')
    else:
        bot.reply_to(message, 'Не нужно лезть в чужую работу')
    
    
@bot.message_handler(commands=['chudnova'])
def chudnova(message):
    user_id(message)
    us_ch=(411268462)
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
    if message.text == '/chudnova new':
        connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
        cur = connection.cursor()
        cur.execute('select count(id) as kol from site.bo_new_dela(170) where colplan = 0')
        s= cur.fetchone()[0]
        connection.close()
        bot.reply_to(message, f'Новых дел {s}')
    elif message.chat.id == us_ch:
        dela('chyd', 7896, 'чуднова')
    else:
        bot.reply_to(message, 'Не нужно лезть в чужую работу')
        #user_id(message)
        #print(user_id(message), message.chat.first_name, message.chat.last_name)
#         dela('chyd', 7896, 'чуднова')

@bot.message_handler(commands=['butcalenko'])
def chudnova(message):
    user_id(message)
    #us_ch=(411268462)
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
#     if message.text == '/chudnova new':
#         connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
#         cur = connection.cursor()
#         cur.execute('select count(id) as kol from site.bo_new_dela(170) where colplan = 0')
#         s= cur.fetchone()[0]
#         connection.close()
#         bot.reply_to(message, f'Новых дел {s}')
#     elif message.chat.id == us_ch:
    dela('but', 2302, 'буцаленко')
#     else:
#         bot.reply_to(message, 'Не нужно лезть в чужую работу')

@bot.message_handler(commands=['orishenko'])
def chudnova(message):
    user_id(message)
    #us_ch=(411268462)
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
#     if message.text == '/chudnova new':
#         connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
#         cur = connection.cursor()
#         cur.execute('select count(id) as kol from site.bo_new_dela(170) where colplan = 0')
#         s= cur.fetchone()[0]
#         connection.close()
#         bot.reply_to(message, f'Новых дел {s}')
#     elif message.chat.id == us_ch:
    dela('орищ', 1303, 'орищенко')


# @bot.message_handler(commands=['adres'])
# def adres(message):
#     if message.text == '/adres':
#         msg = bot.reply_to(message,'Введите адрес')
#         bot.register_next_step_handler(msg, kadastr)
        
# def kadastr(message):
#     kadnumber = message.text
#     url= 'https://apiegrn.ru/api/cadaster/search'
#     headers= requests.options('https://apiegrn.ru/api/cadaster/search').headers
#     headers['Content-Type'] = 'application/json'
#     headers['Token'] = 'KKHD-NAOZ-LLA4-UTUJ'
#     #headersAuth = headers
#     #headers = {'Token': 'KKHD-NAOZ-LLA4-UTUJ','Content-Type': 'application/json', 'User-Agent': 'Mozilla'}  
#     payload = {f"query": kadnumber,
#         "mode": "normal",
#         "grouped": 0}
#     res = requests.post(url, json = payload, headers = headers)
#     #print (res.json())
#     if res.status_code == 200:
#         v=res.json()
#         b=[]
#         for i in v['objects']:
#             for key,value in i.items():
#                 b.append(str('u')+ value + str('\n'))
#         bot.send_message(message.chat.id, str(b))
#     else: 
#         bot.send_message(message.chat.id, 'Проверьте кадастровый номер')

@bot.message_handler(commands=['cadnum'])
def cadnum(message):
    if message.text == '/cadnum':
        msg = bot.reply_to(message,'Введите кадастровый номер')
        bot.register_next_step_handler(msg, cadnum1)
        
def cadnum1(message):
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
    kadnumber = message.text
    url= 'https://apiegrn.ru/api/cadaster/objectInfoFull'
    headers= requests.options('https://apiegrn.ru/api/cadaster/objectInfoFull').headers
    headers['Content-Type'] = 'application/json'
    headers['Token'] = 'KKHD-NAOZ-LLA4-UTUJ'
    #headersAuth = headers
    #headers = {'Token': 'KKHD-NAOZ-LLA4-UTUJ','Content-Type': 'application/json', 'User-Agent': 'Mozilla'}  
    payload = {f"query": kadnumber,
        "deep": 0}
    res = requests.post(url, json = payload, headers = headers)
    #print (res.json())
    if res.status_code == 200:
        n=f"{res.json()['EGRN']['details']}"
        f=n.split(',')
#         a=str()
#         for i in f:
#             #print(i + '\n')
#             i + '\n'
#             a+=i
#             #print(i)
        
        a="\n".join(f)
        splitted_text = util.split_string(a, 3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text)
        #bot.send_message(message.chat.id, a[1:-1])
    else: 
        bot.send_message(message.chat.id, 'Проверьте кадастровый номер')
        
@bot.message_handler(commands=['adres'])
def adres(message):
    if message.text == '/adres':
        msg = bot.reply_to(message,'Введите адрес')
        bot.register_next_step_handler(msg, kadastr)
        
def kadastr(message):
    print(message.chat.id, message.chat.first_name, message.chat.last_name, message.chat.username, message.text)
    adres = message.text
    url= 'https://apiegrn.ru/api/cadaster/search'
    headers= requests.options('https://apiegrn.ru/api/cadaster/search').headers
    headers['Content-Type'] = 'application/json'
    headers['Token'] = 'KKHD-NAOZ-LLA4-UTUJ'
    #headersAuth = headers
    #headers = {'Token': 'KKHD-NAOZ-LLA4-UTUJ','Content-Type': 'application/json', 'User-Agent': 'Mozilla'}  
    payload = {"query": adres,
    "mode": "normal",
    "grouped": 0}
    res = requests.post(url, json = payload, headers = headers)
    #print (res.json())
    if res.status_code == 200:
        n=f"{res.json()['objects']}"
        f=n.split(',')
#         a=str()
#         for i in f:
#             #print(i + '\n')
#             i + '\n'
#             a+=i
#             #print(i)
        
        a="\n".join(f)
        u=a.replace('{','')
        u1=u.replace('}','')
        splitted_text = util.split_string(u1, 3000)
        for text in splitted_text:
            bot.send_message(message.chat.id, text)
        #bot.send_message(message.chat.id, u1)
    else: 
        bot.send_message(message.chat.id, 'Проверьте адрес')
# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.polling(none_stop=True)


# In[ ]:





# In[ ]:




