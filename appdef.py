from flask import Flask, render_template, request
import pymysql.cursors

app = Flask(__name__)


conn = pymysql.connect(host='localhost',
						user='root',
						# password='root',
						password='',
						db='pricosha',
						charset='utf8mb4',
						cursorclass=pymysql.cursors.DictCursor)
