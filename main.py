# https://timeweb.cloud/tutorials/python/sozdanie-veb-prilozheniya-s-ispolzovaniem-python-flask#bd-dlya-loginov-i-parolej
from flask import Flask, request, render_template, redirect,flash,url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

db = sqlite3.connect('login_password.db')
sql = db.cursor()


sql.execute('''CREATE TABLE IF NOT EXISTS passwords(
login TEXT PRIMARY KEY,
parole TEXT NOT NULL);''')
db.commit()

sql.close()
db.close()



@app.route('/')
def index():
  return render_template("index.html")

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
      login = request.form.get('Login')
      parole = request.form.get('Password')
      db = sqlite3.connect('login_password.db')
      sql = db.cursor()
      info = sql.execute(('''SELECT login FROM passwords WHERE login = '{}';''').format(login)).fetchone()
      if info is None:
        return render_template ("auth_bad.html")
      sql.execute(('''SELECT parole FROM passwords WHERE login = '{}';''').format(login))
      pwd = sql.fetchone()
      sql.close()
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
    # return render_template('login_form.html')


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
   if request.method == 'POST':
       login = request.form.get('Login')
       parole = request.form.get('Password')
       parole2 = request.form.get('Password2')
       db = sqlite3.connect('login_password.db')
       sql = db.cursor()
       sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(login,generate_password_hash(parole))
       sql.execute(sql_insert)
       sql.close()
       db.commit()
       db.close()
       return render_template('successfulregis.html')
   return render_template('registration.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)


