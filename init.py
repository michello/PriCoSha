# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template
app = Flask(__name__)
import login


@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
