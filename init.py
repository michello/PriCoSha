from flask import Flask, render_template, request, session, url_for, redirect
from appdef import app
import login

@app.route('/')
def main():
    return render_template("index.html")

if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
