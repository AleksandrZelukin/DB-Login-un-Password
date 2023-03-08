# https://timeweb.cloud/tutorials/python/sozdanie-veb-prilozheniya-s-ispolzovaniem-python-flask#bd-dlya-loginov-i-parolej
from flask import Flask, request, render_template, redirect,flash,url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

db_lp = sqlite3.connect('login_password.db')
cursor_db = db_lp.cursor()

sql_create = ('''CREATE TABLE IF NOT EXISTS passwords(
login TEXT PRIMARY KEY,
parole TEXT NOT NULL);''')

cursor_db.execute(sql_create)
db_lp.commit()

cursor_db.close()
db_lp.close()

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
      login = request.form.get('Login')
      parole = request.form.get('Password')
      db_lp = sqlite3.connect('login_password.db')
      cursor_db = db_lp.cursor()
      info = cursor_db.execute(('''SELECT login FROM passwords WHERE login = '{}';''').format(login)).fetchone()
      # if info.fetchone() is None: 
      if len(info) == 0 :
        return render_template ("index.html")
# https://ru.stackoverflow.com/questions/1240689/%D0%9A%D0%B0%D0%BA-%D0%BF%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%B8%D1%82%D1%8C-%D0%B5%D1%81%D1%82%D1%8C-%D0%BB%D0%B8-%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D1%8C-%D0%B2-%D1%82%D0%B0%D0%B1%D0%BB%D0%B8%D1%86%D0%B5-sqlite3
      cursor_db.execute(('''SELECT parole FROM passwords WHERE login = '{}';''').format(login))
      pwd = cursor_db.fetchone()
      print(pwd)
      cursor_db.close()
      pwd=pwd[0]  
      p = check_password_hash(pwd,parole)
      try:
          if not p:
               return render_template('auth_bad.html')
      except:
           return render_template('auth_bad.html')
      #  db_lp.close()
      return render_template('successfulauth.html')
    return render_template('authorization.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
   if request.method == 'POST':
       login = request.form.get('Login')
       parole = request.form.get('Password')
       # psw = generate_password_hash(parole)
       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       # sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, psw)
       sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(login,generate_password_hash(parole))
       cursor_db.execute(sql_insert)
       cursor_db.close()
       db_lp.commit()
       db_lp.close()
       return render_template('successfulregis.html')
   return render_template('registration.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)


