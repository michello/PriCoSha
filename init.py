from flask import Flask, render_template, request, session, url_for, redirect
from appdef import app
import main, login, logout
import pymysql.cursors
import time


app.secret_key = 'D7X15LEycA'

if __name__ == "__main__":
  app.run('127.0.0.1', 5000, debug = True)
