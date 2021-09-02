import psycopg2
from psycopg2 import OperationalError
from flask import Flask, request
from datetime import date
from datetime import datetime
import pandas as pd
from flask import Response
import logging, sqlite3

app = Flask(__name__)

logger = logging.getLogger('werkzeug')
handler = logging.FileHandler('access.log')
logger.addHandler(handler)

conn= sqlite3.connect('kasprim.db',check_same_thread=False)
curs = conn.cursor()
curs.execute("""CREATE TABLE IF NOT EXISTS kasprim(
   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
   userip TEXT,
   text TEXT,
   num TEXT,
   date TEXT);
""")
conn.commit()


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


@app.route('/video', methods=['GET'])
def video():
    return Response('<table>'
                     '<tbody>'
                    '<tr><td><iframe src="https://camera.rt.ru/sl/ibsGS3n1j" width="700px" height="500px" frameborder="0" allowfullscreen scrolling="no">Этот сайт запрещает встраивать внешние видеоплееры. Обратитесь к технической поддержке сайта за подробной информацией.</iframe><p></p></td><td><iframe src="https://camera.rt.ru/sl/KmECYMK_g" width="700px" height="500px" frameborder="0" allowfullscreen scrolling="no">Этот сайт запрещает встраивать внешние видеоплееры. Обратитесь к технической поддержке сайта за подробной информацией.</iframe><p></p></td><td><iframe src="https://camera.rt.ru/sl/Wj3QBp9bL" width="700px" height="500px" frameborder="0" allowfullscreen scrolling="no">Этот сайт запрещает встраивать внешние видеоплееры. Обратитесь к технической поддержке сайта за подробной информацией.</iframe><p></p></td></tr>'
                    '<tr><td><iframe src="https://camera.rt.ru/sl/xs0Fk9a1v" width="700px" height="500px" frameborder="0" allowfullscreen scrolling="no">Этот сайт запрещает встраивать внешние видеоплееры. Обратитесь к технической поддержке сайта за подробной информацией.</iframe><p></p></td><td><iframe src="https://camera.rt.ru/sl/ZSqw-mflD" width="700px" height="500px" frameborder="0" allowfullscreen scrolling="no">Этот сайт запрещает встраивать внешние видеоплееры. Обратитесь к технической поддержке сайта за подробной информацией.</iframe><p></p></td><td><iframe src="https://camera.rt.ru/sl/tOKQQpihd" width="700px" height="500px" frameborder="0" allowfullscreen scrolling="no">Этот сайт запрещает встраивать внешние видеоплееры. Обратитесь к технической поддержке сайта за подробной информацией.</iframe><p></p></td></tr>'
                     '</tbody>'
                    '</table>')

@app.route('/', methods=['POST', 'GET'])
def index():
    tx = request.form.get('txt')
    delo = request.form.get('delo')
    try:
        if request.method == 'POST' and tx and delo != None:
            if delo[len(delo)-1:] == ',':
                delo = delo[:-1]
            connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
            cur = connection.cursor()
            cur.execute(f"UPDATE delo.delo set primech = CONCAT_WS(' ', primech, '|', '{tx}') WHERE num IN ({delo});")
            connection.commit()
            cur.close()
            connection.close()
            print(tx, delo)
            curs.execute("INSERT INTO kasprim(userip,text,num,date) VALUES(?, ?, ?, ?)", (request.remote_addr, tx, delo, datetime.now()))
            conn.commit()
            return f"Количество внесенных данных: {cur.rowcount}"
    except:
        return "Ошибка данных, проверьте введенные данные!"


    return ("\n"
            "<form method=\"post\">\n"
            "    Введите текст: <input type=\"text\" name=\"txt\" placeholder=\"Необходимый текст\">\n"
            "    Введите номера дел:<input type=\"text\" name=\"delo\" placeholder=\"123456, 500500\">\n"
            "    <input type=\"submit\" Value=\"Сформировать!\">\n"
            "</form>\n")


@app.route('/otchet', methods=['POST', 'GET'])
def egrn():
    #current_date = date.today()
    dat = request.form.get('dat')
    try:
        if request.method == 'POST' and dat != None:
            connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
            cur = connection.cursor()
            cur.execute(f'''SELECT *,
              '{dat}'::date-dat_ep_et as day_past,
              (SELECT array_to_string(array_agg(zayaviteli),',')
              FROM site.zayaviteli(ddd.id_delo)) AS zak
            FROM
              (SELECT DISTINCT ON (delo_stage.id_delo)delo_stage.id_delo,
                                  delo_stage.dat_ep_et,
                                  delo_stage.dat_e,
                                  CASE
                                      WHEN delo.prefix='' THEN delo.num::text
                                      ELSE concat(delo.prefix,'-',delo.num::text)
                                  END AS delonum,
                                  COALESCE(
                                             (SELECT string_agg(concat(btrim(zemh.kadn)||' ',btrim(zemh.adr)||' ',btrim(zemh.primech)),'; ')
                                              FROM delo.zemh
                                              WHERE id_delo = delo.id),delo.adr) AS adr,
                                  delo.dat,
                                  delo.cl,
                                  delo.tncl_o,
                                  delo.datcl_o,
                                  userst.ima,
                                  delo.id_usl_sp,
                                  usl_sp.nom||' '||usl_sp.naz_full AS naz,
                                  usl_sp.gr_id,
                                  grusl.idp,
                                  usl_sp.nom,
                                  grusl.naz AS naz_gr,
                                  delo_move.tn AS tn,
                                  string_agg(concat(
                                                      (SELECT nomer
                                                       FROM rosreestr.books
                                                       WHERE id = books_rd.id_book ) ||' :',books_rd.nomer),'</br> ') AS reg_book
               FROM delo.delo_stage
               JOIN delo.delo ON delo.id=id_delo
               LEFT JOIN uslugi.usl_sp ON delo.id_usl_sp=usl_sp.id
               LEFT JOIN uslugi.grusl ON uslugi.grusl.id=usl_sp.gr_id
               LEFT JOIN delo.delo_move ON(delo_move.id_delo=delo.id
                                           AND delo_move.dat_move IS NULL
                                           AND delo_move.tipr=3)
               JOIN public.userst ON userst.tn=delo_move.tn
               LEFT JOIN rosreestr.books_rd ON books_rd.id_delo=delo.id
               WHERE delo.cl=0
                 AND delo.datcl_o IS NOT NULL
                 AND delo.dat_stop IS NULL --and delo_stage.dat_e is not null     

             	 AND delo.id_usl_sp in (1804,1800)
              	 AND delo.ids_isp in (178,76,114,107,180,90,106,105,100,104,101,99,97,96,110,91,95,83,89,93,112,102,98,108,94,109,92,0)
             	 AND delo.ids_open in (178,76,114,107,180,90,106,105,100,104,101,99,97,96,110,91,95,83,89,93,112,102,98,108,94,109,92,0)
               GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17
               ORDER BY delo_stage.id_delo,
                        delo_stage.dat_ep_et DESC) ddd
            WHERE dat_ep_et< coalesce(dat_e, '{dat}'::date );''')
            connection.commit()
            spis = cur.fetchall()
            s4 = pd.DataFrame(spis)
            s4.index = s4.index + 1
            z = []
            for i in s4[0]:
                cur = connection.cursor()
                cur.execute(f"select kyvd FROM egrn.statement WHERE id_delo IN ({i});")
                kyvd = cur.fetchall()
                z.append(str(kyvd)[2:-3])
            connection.close()
            s4[20] = z
            s4[20] = s4[20].astype(str).str.replace(r"[\[\](),']", '')
            s41 = s4[[3, 11, 5, 19, 4, 18, 20]]
            s41.columns = ['№ дела', 'Услуга', 'Дата открытия дела', 'Заказчик', 'Адрес', 'Дней просрочки', 'КУВД']
            #s4.to_excel(f'{current_date}.xlsx', header=['№ дела', 'Услуга', 'Дата открытия дела', 'Заказчик', 'Адрес', 'Дней просрочки',                                'КУВД'], columns=[3, 11, 5, 19, 4, 18, 20])
            #s4 = get_dataframe_from_somewhere()
            return Response(s41.to_html(header="true", table_id="table", justify="center"))
            #return Response(s4.to_json(orient="records"), mimetype='application/json')
            #return send_from_directory('path_to_file', filename = '2021-03-24.xlsx')
    except:
        return "<h1>Ошибка данных!</h1>"

    return ("\n"
        "<form method=\"post\">\n"
        "   <input type=\"date\" name=\"dat\" required=\"required\" value=\"09.02.2015\">\n"
        "   <input type=\"submit\" Value=\"Сформировать!\">\n"
        "</form>\n")


@app.route('/passport', methods=['POST', 'GET'])
def inde():
    dela = request.form.get('delo')
    try:
        if request.method == 'POST' and dela != None:
            connection = create_connection('mfc_azov', 'webguest', 11, '172.20.111.31', 5432)
            cur = connection.cursor()
            cur.execute(f"select fam as fam, nam as nam, otch as ot, fadr as adr, telmob as tel, tel, num as num, naz as naz from delo.delo inner join clients.zakf on zakf.idf=delo.idf inner join isp.sp_struc on sp_struc.ids=delo.ids_open where num in ({dela});")
            connection.commit()
            s= cur.fetchall()
            cur.close()
            connection.close()
            s4=pd.DataFrame(s)
            s4.columns = ['Фамилия', 'Имя', 'Отчество', 'Адрес', 'Телефон моб', 'Телефон стац', 'Номер дела', 'Где принято']
            s4=s4.sort_values(by='Фамилия').reset_index(drop=True)
            s4.index = s4.index + 1
            return Response(s4.to_html(header="true", table_id="table", justify="center"))
            #print(tx, delo)
            #curs.execute("INSERT INTO kasprim(userip,text,num,date) VALUES(?, ?, ?, ?)", (request.remote_addr, tx, delo, datetime.now()))
            #conn.commit()
            #return f"Количество внесенных данных: {cur.rowcount}"
    except:
        return "Ошибка данных, проверьте введенные данные!"


    return ("\n"
            "<form method=\"post\">\n"
            "    Введите номера дел:<input type=\"text\" name=\"delo\" placeholder=\"123456, 500500\">\n"
            "    <input type=\"submit\" Value=\"Сформировать!\">\n"
            "</form>\n")


if __name__ == "__main__":
    app.run(host='172.20.111.55', port=5511)
