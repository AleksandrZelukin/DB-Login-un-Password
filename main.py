# https://timeweb.cloud/tutorials/python/sozdanie-veb-prilozheniya-s-ispolzovaniem-python-flask#bd-dlya-loginov-i-parolej
from flask import Flask, request, render_template
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

# cursor_db.close()
# db_lp.close()

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
      Login = request.form.get('Login')
      parole = request.form.get('parole')
      db_lp = sqlite3.connect('login_password.db')
      cursor_db = db_lp.cursor()
      cursor_db.execute(('''SELECT parole FROM passwords WHERE login = '{}';''').format(Login))
      pwd = cursor_db.fetchall()
      cursor_db.close()
      print(pwd)
      a = check_password_hash(pwd,parole)
      print(a)
      try:
        if check_password_hash(pwd,parole): 
        # if pwd[0][0] != parole:
          return render_template('successfulauth.html')
          # return render_template('auth_bad.html')
      except:
        return render_template('auth_bad.html')

      db_lp.close()
      return render_template('successfulauth.html')
    return render_template('authorization.html')

@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
   if request.method == 'POST':
       Login = request.form.get('Login')
       parole = request.form.get('Password')
       psw = generate_password_hash(parole)
       db_lp = sqlite3.connect('login_password.db')
       cursor_db = db_lp.cursor()
       sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, psw)
       cursor_db.execute(sql_insert)
       cursor_db.close()
       db_lp.commit()
       db_lp.close()
       return render_template('successfulregis.html')
   return render_template('registration.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1',debug=True)


# @app.route('/authorization', methods=['GET', 'POST'])
# def form_authorization():
#   if request.method == 'POST':
#        login = request.form.get('Login')
#        parole = request.form.get('Password')
#        db_lp = sqlite3.connect('login_password.db')
#        cursor_db = db_lp.cursor()
#        cursor_db.execute(('''SELECT parole FROM passwords WHERE login = '{}'; ''').format(login))
#        pas = list(cursor_db.fetchall())

#        try:
#         if request.form.get('Password') == check_password_hash(parole,pas):

#           return render_template("successfulauth.html")
#        except:
#           return render_template("auth_bad.html")
#   return render_template('authorization.html')
