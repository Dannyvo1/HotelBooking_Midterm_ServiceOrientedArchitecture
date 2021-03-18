"""
Routes and views for the flask application.
"""

from HotelBooking_Midterm_ServiceOrientedArchitecture import app
from datetime import datetime
import os
from flask import Flask, render_template, redirect, url_for, request, session, g
from flask.helpers import flash, url_for
from werkzeug.wrappers import UserAgentMixin
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

#config Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'HOTELDB'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor' #this config line returns queries we execute as dictionaries, default is to return as a tuple; ex. User Login 

#
mysql = MySQL(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dashboard')
def dashboard():
    reviews=None
    upcoming=None
    current=None
    past=None
    user=None
    
    cur = mysql.connection.cursor()
    
    #Get Reviews
    result = cur.execute('select * from phong where cid=%ss',[session['cid']])
    if result>0:
        reviews = cur.fetchall()

    result = cur.execute("""SELECT DISTINCT reserves.invoiceNo, hotel.hotel_name, 
                                reserves.hotelID, reserves.inDate, reserves.outDate, 
                                COUNT(reserves.room_num) AS numRooms FROM reserves, reservation, hotel 
                             WHERE reserves.invoiceNo = reservation.invoiceNo 
                                AND reserves.hotelID = hotel.hotelID 
                                AND CID = %s 
                                AND reserves.outDate >= NOW() 
                                AND reserves.inDate <= NOW() 
                            GROUP BY reserves.invoiceNo, hotel.hotel_name, reserves.inDate, reserves.outDate 
                            ORDER BY reserves.inDate""", [session['cid']])
    if result>0:
        current=cur.fetchall()
        
    result = cur.execute("""SELECT DISTINCT reserves.invoiceNo, hotel.hotel_name, 
                                reserves.hotelID, reserves.inDate, reserves.outDate, 
                                COUNT(reserves.room_num) AS numRooms FROM reserves, reservation, hotel 
                             WHERE reserves.invoiceNo = reservation.invoiceNo 
                                AND reserves.hotelID = hotel.hotelID 
                                AND CID = %s 
                                AND reserves.outDate < NOW() 
                                AND reserves.inDate < NOW() 
                            GROUP BY reserves.invoiceNo, hotel.hotel_name, reserves.inDate, reserves.outDate 
                            ORDER BY reserves.inDate""", [session['cid']])
    if result>0:
        past=cur.fetchall()
    
    result = cur.execute("""SELECT DISTINCT reserves.invoiceNo, hotel.hotel_name, 
                                reserves.hotelID, reserves.inDate, reserves.outDate, 
                                COUNT(reserves.room_num) AS numRooms FROM reserves, reservation, hotel 
                             WHERE reserves.invoiceNo = reservation.invoiceNo 
                                AND reserves.hotelID = hotel.hotelID 
                                AND CID = %s 
                                AND reserves.outDate > NOW() 
                                AND reserves.inDate > NOW() 
                            GROUP BY reserves.invoiceNo, hotel.hotel_name, reserves.inDate, reserves.outDate 
                            ORDER BY reserves.inDate""", [session['cid']])
    if result>0:
        upcoming=cur.fetchall()
        
    result = cur.execute("""SELECT * FROM customer WHERE CID=%s""", [session['cid']])
    user=cur.fetchone()
    
    return render_template('dashboard.html', reviews=reviews, upcoming=upcoming, past=past, current=current, user=user)
    



