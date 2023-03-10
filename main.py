from flask import Flask, request, render_template, redirect,flash,url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import server
app = Flask(__name__)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port='8080',debug=True)

